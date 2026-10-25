import Std

/- Exact modular polynomial network semantics. No floating point, timing,
   optimizer implementation or hardware refinement is modeled. -/
namespace Residue

inductive Expr where
  | input (i : Nat)
  | lit (n : Nat)
  | add (a b : Expr)
  | mul (a b : Expr)

abbrev Env := Nat → Nat

def eval (q : Nat) (ρ : Env) : Expr → Nat
  | .input i => ρ i % q
  | .lit n => n % q
  | .add a b => (eval q ρ a + eval q ρ b) % q
  | .mul a b => (eval q ρ a * eval q ρ b) % q

/-- Projection commutes with every polynomial expression, for any depth. -/
theorem project (p k : Nat) (ρ : Env) :
    ∀ e : Expr, eval (p*k) ρ e % p = eval p ρ e := by
  intro e
  induction e with
  | input i => exact Nat.mod_mul_right_mod (ρ i) p k
  | lit n => exact Nat.mod_mul_right_mod n p k
  | add a b ha hb =>
    simp only [eval]
    rw [Nat.mod_mul_right_mod, Nat.add_mod, ha, hb]
  | mul a b ha hb =>
    simp only [eval]
    rw [Nat.mod_mul_right_mod, Nat.mul_mod, ha, hb]

theorem base_congr (p : Nat) (ρ σ : Env)
    (h : ∀ i, ρ i % p = σ i % p) :
    ∀ e : Expr, eval p ρ e = eval p σ e := by
  intro e
  induction e with
  | input i => exact h i
  | lit _ => rfl
  | add a b ha hb => simp only [eval, ha, hb]
  | mul a b ha hb => simp only [eval, ha, hb]

/-- All same-remainder inputs/weights have identical modeled content. -/
theorem noninterference (p k : Nat) (ρ σ : Env)
    (h : ∀ i, ρ i % p = σ i % p) (e : Expr) :
    eval (p*k) ρ e % p = eval (p*k) σ e % p := by
  rw [project, project]
  exact base_congr p ρ σ h e

def step (q : Nat) (program : Nat → Expr) (ρ : Env) : Env :=
  fun i => eval q ρ (program i)

def run (q : Nat) (program : Nat → Expr) (ρ : Env) : Nat → Env
  | 0 => ρ
  | n+1 => step q program (run q program ρ n)

/-- Fixed polynomial state updates preserve the property at every iteration.
    This covers algebraically expressed update programs, not arbitrary optimizers. -/
theorem training_noninterference (p k : Nat) (program : Nat → Expr) (ρ σ : Env)
    (h : ∀ i, ρ i % p = σ i % p) :
    ∀ n i, run (p*k) program ρ n i % p = run (p*k) program σ n i % p := by
  intro n
  induction n with
  | zero => exact h
  | succ n ih =>
    intro i
    exact noninterference p k _ _ ih (program i)

def features : List Expr :=
  [.lit 1, .input 0, .input 1, .input 2,
   .mul (.input 0) (.input 1), .mul (.input 0) (.input 2),
   .mul (.input 1) (.input 2), .mul (.mul (.input 0) (.input 1)) (.input 2)]

def weighted : Nat → List Expr → Expr
  | _, [] => .lit 0
  | i, f::fs => .add (.mul (.input i) f) (weighted (i+1) fs)

def network := weighted 3 features

def semanticEnv (coefficients : List Nat) (a b c : Bool) : Env
  | 0 => a.toNat
  | 1 => b.toNat
  | 2 => c.toNat
  | i+3 => coefficients[i]?.getD 0

def parityWeights := [0,1,1,1,1,1,1,1]
def majorityWeights := [0,0,0,0,1,1,1,1]
def andWeights := [0,0,0,0,0,0,0,1]
def orWeights := [0,1,1,1,2,2,2,1]

theorem parity_correct : ∀ a b c : Bool,
    eval 3 (semanticEnv parityWeights a b c) network = ((a.xor b).xor c).toNat := by decide

theorem majority_correct : ∀ a b c : Bool,
    eval 3 (semanticEnv majorityWeights a b c) network =
      (decide (a.toNat + b.toNat + c.toNat ≥ 2)).toNat := by decide

theorem and_correct : ∀ a b c : Bool,
    eval 3 (semanticEnv andWeights a b c) network = (a && b && c).toNat := by decide

theorem or_correct : ∀ a b c : Bool,
    eval 3 (semanticEnv orWeights a b c) network = (a || b || c).toNat := by decide

/-- Correctness transfers to every encoded world in the same input/weight fiber. -/
theorem lifted_correct (ρ σ : Env) (h : ∀ i, ρ i % 3 = σ i % 3)
    (target : Nat) (hc : eval 3 σ network = target) :
    eval 9 ρ network % 3 = target := by
  calc
    eval 9 ρ network % 3 = eval 3 ρ network := project 3 3 ρ network
    _ = eval 3 σ network := base_congr 3 ρ σ h network
    _ = target := hc

#print axioms noninterference
#print axioms training_noninterference
#print axioms lifted_correct

/-- Concrete network: two affine/square units and a learned affine readout.
    Inputs occupy slots 0,1; all nine learned weights occupy slots 2..10. -/
def hidden0 : Expr := .add (.add (.mul (.input 2) (.input 0))
  (.mul (.input 3) (.input 1))) (.input 4)
def hidden1 : Expr := .add (.add (.mul (.input 5) (.input 0))
  (.mul (.input 6) (.input 1))) (.input 7)
def network2 : Expr := .add (.add
  (.mul (.input 8) (.mul hidden0 hidden0))
  (.mul (.input 9) (.mul hidden1 hidden1))) (.input 10)
def network1 : Expr := .add (.mul (.input 5) (.mul hidden0 hidden0)) (.input 6)
def env2 (weights : List Nat) (a b : Bool) : Env
  | 0 => a.toNat
  | 1 => b.toNat
  | i+2 => weights[i]?.getD 0

theorem network2_lifted_correct (ρ σ : Env)
    (h : ∀ i, ρ i % 3 = σ i % 3) (target : Nat)
    (hc : eval 3 σ network2 = target) : eval 9 ρ network2 % 3 = target := by
  calc
    eval 9 ρ network2 % 3 = eval 3 ρ network2 := project 3 3 ρ network2
    _ = eval 3 σ network2 := base_congr 3 ρ σ h network2
    _ = target := hc

#print axioms network2_lifted_correct

theorem network1_lifted_correct (ρ σ : Env)
    (h : ∀ i, ρ i % 3 = σ i % 3) (target : Nat)
    (hc : eval 3 σ network1 = target) : eval 9 ρ network1 % 3 = target := by
  calc
    eval 9 ρ network1 % 3 = eval 3 ρ network1 := project 3 3 ρ network1
    _ = eval 3 σ network1 := base_congr 3 ρ σ h network1
    _ = target := hc

#print axioms network1_lifted_correct

/-- Any deterministic learner receiving only declared semantic observations
    returns the same model. Its implementation must satisfy this interface. -/
theorem observed_learner_noninterference (p : Nat) (learner : Env → Env)
    (ρ σ : Env) (h : ∀ i, ρ i % p = σ i % p) :
    learner (fun i => ρ i % p) = learner (fun i => σ i % p) := by
  have he : (fun i => ρ i % p) = (fun i => σ i % p) := funext h
  rw [he]

#print axioms observed_learner_noninterference
end Residue

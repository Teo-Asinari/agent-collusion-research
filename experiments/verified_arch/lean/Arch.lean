/-
Mechanized core of research/workstreams/architecture/formal-model.md (Theorem 1,
Lemma 2, payload corollary, witness-cell contract for all N). Core Lean 4 only.

Modeling choices relative to the Python IR (ir.py):
* Every function symbol is interpreted by an arbitrary `ι : Interp`, so the
  theorems quantify over all learned weights AND all "trusted" code at once.
  Weights are ordinary wires passed as arguments, as in the Python IR.
* `secondary` args are just args (the full rule joins over all of them).
* A release's implementation is an arbitrary function of the interpretation and
  the whole environment; its internal wires never enter the outer environment.
  The typing rule demands a Lean proof of the contract `impl = spec ∘ args`.
* Observations are values of `observe` nodes only (receiver model R0). Cost or
  timing is not modeled here.
-/
namespace Arch

abbrev Val := Int
abbrev Wire := Nat
abbrev Env := Wire → Val
abbrev Interp := String → List Val → Val

inductive Label where
  | pub
  | priv
  deriving DecidableEq

def Label.join : Label → Label → Label
  | .pub, .pub => .pub
  | _, _ => .priv

inductive Kind where
  | publicTask | publicRand | publicWeight
  | authorized | payload | privateWeight | privateRand | privateState
  deriving DecidableEq

def Kind.label : Kind → Label
  | .publicTask | .publicRand | .publicWeight => .pub
  | _ => .priv

/-- Rule (R1): a release spec may read only public task data and authorized data. -/
def Kind.specReadable : Kind → Bool
  | .publicTask | .authorized => true
  | _ => false

inductive Node where
  | op (out : Wire) (fn : String) (args : List Wire)
  | release (out : Wire) (spec : List Val → Val) (specArgs : List Wire)
      (impl : Interp → Env → Val)
  | observe (w : Wire)

abbrev Prog := List Node

def upd (ρ : Env) (w : Wire) (v : Val) : Env := fun x => if x = w then v else ρ x

/-- Big-step semantics: observations and final environment. -/
def run (ι : Interp) : Prog → Env → List Val × Env
  | [], ρ => ([], ρ)
  | .op out fn args :: p, ρ => run ι p (upd ρ out (ι fn (args.map ρ)))
  | .release out _ _ impl :: p, ρ => run ι p (upd ρ out (impl ι ρ))
  | .observe w :: p, ρ => ((ρ w) :: (run ι p ρ).1, (run ι p ρ).2)

def obs (ι : Interp) (p : Prog) (ρ : Env) : List Val := (run ι p ρ).1

abbrev Ctx := Wire → Option Label

def joinAll (Γ : Ctx) : List Wire → Label
  | [] => .pub
  | a :: as =>
    match Γ a with
    | some l => l.join (joinAll Γ as)
    | none => .priv

def setCtx (Γ : Ctx) (w : Wire) (l : Label) : Ctx :=
  fun x => if x = w then some l else Γ x

/-- Initial context: input wires carry the label of their kind. -/
def ctx0 (κ : Wire → Option Kind) : Ctx := fun a => (κ a).map Kind.label

/-- Typing judgment `WT κ Γ p Γ'`: p is well typed from context Γ, ending in Γ'.
Outputs must be fresh (SSA), op labels join over all reads, a release output is
public only with readable spec args and a proof of its contract, and only public
wires may be observed. -/
inductive WT (κ : Wire → Option Kind) : Ctx → Prog → Ctx → Prop where
  | nil (Γ : Ctx) : WT κ Γ [] Γ
  | op {Γ Γ' : Ctx} {out : Wire} {fn : String} {args : List Wire} {p : Prog} :
      Γ out = none →
      WT κ (setCtx Γ out (joinAll Γ args)) p Γ' →
      WT κ Γ (.op out fn args :: p) Γ'
  | release {Γ Γ' : Ctx} {out : Wire} {spec : List Val → Val} {specArgs : List Wire}
      {impl : Interp → Env → Val} {p : Prog} :
      Γ out = none →
      (∀ a ∈ specArgs, ∃ k, κ a = some k ∧ k.specReadable = true) →
      (∀ ι ρ, impl ι ρ = spec (specArgs.map ρ)) →
      WT κ (setCtx Γ out .pub) p Γ' →
      WT κ Γ (.release out spec specArgs impl :: p) Γ'
  | observe {Γ Γ' : Ctx} {w : Wire} {p : Prog} :
      Γ w = some .pub →
      WT κ Γ p Γ' →
      WT κ Γ (.observe w :: p) Γ'

/-- The declared releases of a program: (spec, spec args). -/
def releases : Prog → List ((List Val → Val) × List Wire)
  | [] => []
  | .release _ s sa _ :: p => (s, sa) :: releases p
  | _ :: p => releases p

/-! ### Helper lemmas -/

theorem map_congr' {f g : Wire → Val} :
    ∀ (l : List Wire), (∀ a ∈ l, f a = g a) → l.map f = l.map g
  | [], _ => rfl
  | a :: l, h => by
    simp only [List.map_cons]
    rw [h a (List.mem_cons_self ..), map_congr' l (fun b hb => h b (List.mem_cons_of_mem _ hb))]

theorem join_pub {l m : Label} (h : l.join m = .pub) : l = .pub ∧ m = .pub := by
  cases l <;> cases m <;> simp_all [Label.join]

theorem joinAll_pub (Γ : Ctx) :
    ∀ (args : List Wire), joinAll Γ args = .pub → ∀ a ∈ args, Γ a = some .pub
  | [], _, a, ha => by cases ha
  | b :: bs, h, a, ha => by
    unfold joinAll at h
    split at h
    · rename_i l hl
      have ⟨h1, h2⟩ := join_pub h
      cases ha with
      | head => rw [hl, h1]
      | tail _ hmem => exact joinAll_pub Γ bs h2 a hmem
    · cases h

/-! ### Theorem 1: noninterference modulo declared release, for every interpretation -/

theorem ni (κ : Wire → Option Kind) (ι : Interp) {Γ Γ' : Ctx} {p : Prog}
    (h : WT κ Γ p Γ') (ρ1₀ ρ2₀ : Env)
    (hrel : ∀ s sa, (s, sa) ∈ releases p → s (sa.map ρ1₀) = s (sa.map ρ2₀)) :
    ∀ (ρ1 ρ2 : Env),
      (∀ w, Γ w = some .pub → ρ1 w = ρ2 w) →
      (∀ a, κ a ≠ none → Γ a ≠ none) →
      (∀ a, κ a ≠ none → ρ1 a = ρ1₀ a ∧ ρ2 a = ρ2₀ a) →
      obs ι p ρ1 = obs ι p ρ2 := by
  induction h with
  | nil => intro ρ1 ρ2 _ _ _; rfl
  | @op Γ Γ' out fn args p hfresh _ ih =>
    intro ρ1 ρ2 hpub hdef hin
    simp only [obs, run]
    apply ih (fun s sa hm => hrel s sa (by simpa [releases] using hm))
    · intro w hw
      simp only [setCtx] at hw
      simp only [upd]
      by_cases hwo : w = out
      · simp only [hwo, ite_true] at hw ⊢
        have hargs := joinAll_pub Γ args (Option.some.inj hw)
        rw [map_congr' args (fun a ha => hpub a (hargs a ha))]
      · simp only [hwo, ite_false] at hw ⊢
        exact hpub w hw
    · intro a ha
      simp only [setCtx]
      by_cases hao : a = out
      · simp [hao]
      · simp only [hao, ite_false]; exact hdef a ha
    · intro a ha
      have hne : a ≠ out := fun he => hdef a ha (he ▸ hfresh)
      simp only [upd, hne, ite_false]
      exact hin a ha
  | @release Γ Γ' out spec specArgs impl p hfresh hread hcon _ ih =>
    intro ρ1 ρ2 hpub hdef hin
    simp only [obs, run]
    apply ih (fun s sa hm => hrel s sa (List.mem_cons_of_mem _ hm))
    · intro w hw
      simp only [setCtx] at hw
      simp only [upd]
      by_cases hwo : w = out
      · simp only [hwo, ite_true]
        rw [hcon ι ρ1, hcon ι ρ2]
        have e1 : specArgs.map ρ1 = specArgs.map ρ1₀ :=
          map_congr' specArgs (fun a ha => by
            obtain ⟨k, hk, _⟩ := hread a ha
            exact (hin a (by simp [hk])).1)
        have e2 : specArgs.map ρ2 = specArgs.map ρ2₀ :=
          map_congr' specArgs (fun a ha => by
            obtain ⟨k, hk, _⟩ := hread a ha
            exact (hin a (by simp [hk])).2)
        rw [e1, e2]
        exact hrel spec specArgs (List.mem_cons_self ..)
      · simp only [hwo, ite_false] at hw ⊢
        exact hpub w hw
    · intro a ha
      simp only [setCtx]
      by_cases hao : a = out
      · simp [hao]
      · simp only [hao, ite_false]; exact hdef a ha
    · intro a ha
      have hne : a ≠ out := fun he => hdef a ha (he ▸ hfresh)
      simp only [upd, hne, ite_false]
      exact hin a ha
  | @observe Γ Γ' w p hw _ ih =>
    intro ρ1 ρ2 hpub hdef hin
    simp only [obs, run]
    rw [hpub w hw]
    have := ih (fun s sa hm => hrel s sa (by simpa [releases] using hm)) ρ1 ρ2 hpub hdef hin
    simp only [obs] at this
    rw [this]

/-- Theorem 1 from the initial context: two worlds that agree on public inputs and
on every declared release value give identical observations, for every
interpretation of every function symbol (all weights). -/
theorem ni_init (κ : Wire → Option Kind) (ι : Interp) {p : Prog} {Γ' : Ctx}
    (h : WT κ (ctx0 κ) p Γ') (ρ1 ρ2 : Env)
    (hpubin : ∀ a k, κ a = some k → k.label = .pub → ρ1 a = ρ2 a)
    (hrel : ∀ s sa, (s, sa) ∈ releases p → s (sa.map ρ1) = s (sa.map ρ2)) :
    obs ι p ρ1 = obs ι p ρ2 := by
  apply ni κ ι h ρ1 ρ2 hrel ρ1 ρ2
  · intro w hw
    simp only [ctx0] at hw
    cases hk : κ w with
    | none => simp [hk] at hw
    | some k =>
      simp only [hk, Option.map_some] at hw
      exact hpubin w k hk (Option.some.inj hw)
  · intro a ha
    simp only [ctx0]
    cases hk : κ a with
    | none => exact absurd hk ha
    | some k => simp
  · intro a _; exact ⟨rfl, rfl⟩

/-! ### Rule (R1) makes the release condition a condition on authorized data only -/

theorem releases_readable (κ : Wire → Option Kind) {Γ Γ' : Ctx} {p : Prog}
    (h : WT κ Γ p Γ') :
    ∀ s sa, (s, sa) ∈ releases p → ∀ a ∈ sa, ∃ k, κ a = some k ∧ k.specReadable = true := by
  induction h with
  | nil => intro s sa hm; cases hm
  | op _ _ ih => intro s sa hm; exact ih s sa (by simpa [releases] using hm)
  | @release Γ Γ' out spec specArgs impl p _ hread _ _ ih =>
    intro s sa hm
    simp only [releases] at hm
    cases hm with
    | head => exact hread
    | tail _ hm' => exact ih s sa hm'
  | observe _ _ ih => intro s sa hm; exact ih s sa (by simpa [releases] using hm)

/-- **Payload corollary.** If two worlds agree on all public inputs and on all
authorized data, then for every interpretation (all weights, all predictors,
all readouts) observations are identical, whatever the payload, private
weights, private randomness and private state. -/
theorem payload_ni (κ : Wire → Option Kind) (ι : Interp) {p : Prog} {Γ' : Ctx}
    (h : WT κ (ctx0 κ) p Γ') (ρ1 ρ2 : Env)
    (hpubin : ∀ a k, κ a = some k → k.label = .pub → ρ1 a = ρ2 a)
    (hauth : ∀ a, κ a = some .authorized → ρ1 a = ρ2 a) :
    obs ι p ρ1 = obs ι p ρ2 := by
  apply ni_init κ ι h ρ1 ρ2 hpubin
  intro s sa hm
  congr 1
  apply map_congr' sa
  intro a ha
  obtain ⟨k, hk, hr⟩ := releases_readable κ h s sa hm a ha
  cases k with
  | publicTask => exact hpubin a .publicTask hk rfl
  | authorized => exact hauth a hk
  | _ => simp [Kind.specReadable] at hr

/-! ### Lemma 2: composition (sequential programs, multi-session unrolling) -/

theorem wt_append (κ : Wire → Option Kind) {Γ Γ' Γ'' : Ctx} {p q : Prog}
    (hp : WT κ Γ p Γ') (hq : WT κ Γ' q Γ'') : WT κ Γ (p ++ q) Γ'' := by
  induction hp with
  | nil => exact hq
  | op hf _ ih => exact WT.op hf (ih hq)
  | release hf hr hc _ ih => exact WT.release hf hr hc (ih hq)
  | observe hw _ ih => exact WT.observe hw (ih hq)

theorem releases_append : ∀ (p q : Prog), releases (p ++ q) = releases p ++ releases q
  | [], _ => rfl
  | .op .. :: p, q => by simp [releases, releases_append p q]
  | .release .. :: p, q => by simp [releases, releases_append p q]
  | .observe .. :: p, q => by simp [releases, releases_append p q]

/-- Composed (e.g. k unrolled sessions) programs are noninterferent modulo the
concatenated releases of all components. -/
theorem ni_compose (κ : Wire → Option Kind) (ι : Interp) {p q : Prog} {Γ' Γ'' : Ctx}
    (hp : WT κ (ctx0 κ) p Γ') (hq : WT κ Γ' q Γ'') (ρ1 ρ2 : Env)
    (hpubin : ∀ a k, κ a = some k → k.label = .pub → ρ1 a = ρ2 a)
    (hrel : ∀ s sa, (s, sa) ∈ releases p ++ releases q → s (sa.map ρ1) = s (sa.map ρ2)) :
    obs ι (p ++ q) ρ1 = obs ι (p ++ q) ρ2 :=
  ni_init κ ι (wt_append κ hp hq) ρ1 ρ2 hpubin (by rw [releases_append]; exact hrel)

/-! ### Lemma 3 (witness cell contract, all N, every predictor)

Predictor-first existential check: evaluate the candidate j chosen by any learned
predictor, then scan every other index. The value equals `ps.any id` for every
j and every predicate-value list. -/

def scanOthers (j : Nat) : List Bool → Nat → Bool
  | [], _ => false
  | p :: ps, i => ((i != j) && p) || scanOthers j ps (i + 1)

def witness (j : Nat) (ps : List Bool) : Bool := ps.getD j false || scanOthers j ps 0

theorem scan_any (j : Nat) :
    ∀ (ps : List Bool) (i : Nat),
      ((ps.getD (j - i) false && decide (i ≤ j)) || scanOthers j ps i) = ps.any id
  | [], i => by simp [scanOthers]
  | p :: ps, i => by
    have ih := scan_any j ps (i + 1)
    simp only [scanOthers, List.any_cons, id]
    by_cases hij : i = j
    · subst hij
      have h1 : decide (i + 1 ≤ i) = false := by simp
      rw [h1, Bool.and_false, Bool.false_or] at ih
      simp [ih]
    · have hne : (i != j) = true := by simp [hij]
      rw [hne, Bool.true_and]
      by_cases hle : i ≤ j
      · have hlt : i + 1 ≤ j := by omega
        have hsub : j - i = (j - (i + 1)) + 1 := by omega
        rw [hsub, List.getD_cons_succ]
        simp only [hle, hlt, decide_true, Bool.and_true] at ih ⊢
        rw [← ih]
        cases p <;> cases (ps.getD (j - (i + 1)) false) <;> simp
      · have hlt : ¬ (i + 1 ≤ j) := by omega
        simp only [hle, hlt, decide_false, Bool.and_false, Bool.false_or] at ih ⊢
        rw [ih]

theorem witness_contract (j : Nat) (ps : List Bool) : witness j ps = ps.any id := by
  have := scan_any j ps 0
  simp only [Nat.sub_zero, Nat.zero_le, decide_true, Bool.and_true] at this
  exact this

/-! ### Concrete instance: the witness architecture (programs.py `full(2)`)

Wires: 0 q (public task), 1 r (public tape), 2 phi (public readout weights),
3 c (private descriptor), 4 m (payload), 5 theta (private weights), 6 z1, 7 z2
(authorized records). The release reads the learned predictor `NetPred` through
`ι` (any weights), but checks the fixed trusted predicate `P`. The program also
contains a private training step for theta, and a public readout. -/

/-- A release implemented by any sub-program run in a local scope is an
`Interp → Env → Val`, so Theorem 1 covers sub-program releases too. -/
def localImpl (sub : Prog) (outW : Wire) : Interp → Env → Val :=
  fun ι ρ => (run ι sub ρ).2 outW

def κw : Wire → Option Kind
  | 0 => some .publicTask | 1 => some .publicRand | 2 => some .publicWeight
  | 3 => some .privateState | 4 => some .payload | 5 => some .privateWeight
  | 6 => some .authorized | 7 => some .authorized
  | _ => none

def existsSpec (P : Val → Val → Bool) : List Val → Val
  | q :: zs => if zs.any (P q) then 1 else 0
  | [] => 0

def witnessImpl (P : Val → Val → Bool) : Interp → Env → Val := fun ι ρ =>
  let j := (ι "NetPred" [ρ 5, ρ 0, ρ 3, ρ 4]).toNat
  if witness j ([ρ 6, ρ 7].map (P (ρ 0))) then 1 else 0

def witnessProg (P : Val → Val → Bool) : Prog :=
  [ .op 8 "NetGrad" [5, 3, 4, 6, 7],            -- private gradient (reads payload)
    .op 9 "Sgd" [5, 8],                         -- private training step
    .release 10 (existsSpec P) [0, 6, 7] (witnessImpl P),
    .op 11 "NetPub" [2, 0, 10, 1],              -- public readout of the release
    .observe 10, .observe 11 ]

theorem witnessImpl_contract (P : Val → Val → Bool) :
    ∀ ι ρ, witnessImpl P ι ρ = existsSpec P ([0, 6, 7].map ρ) := by
  intro ι ρ
  simp only [witnessImpl, witness_contract, List.map, existsSpec]
  rfl

theorem readable_067 : ∀ a ∈ [0, 6, 7], ∃ k, κw a = some k ∧ k.specReadable = true := by
  intro a ha
  simp at ha
  rcases ha with rfl | rfl | rfl <;> simp [κw, Kind.specReadable]

theorem witnessProg_wt (P : Val → Val → Bool) :
    ∃ Γ', WT κw (ctx0 κw) (witnessProg P) Γ' :=
  ⟨_, WT.op (by simp [ctx0, κw])
        (WT.op (by simp [setCtx, ctx0, κw])
          (WT.release (by simp [setCtx, ctx0, κw]) readable_067 (witnessImpl_contract P)
            (WT.op (by simp [setCtx, ctx0, κw])
              (WT.observe (by simp [setCtx])
                (WT.observe (by simp [setCtx, joinAll, ctx0, κw, Kind.label, Label.join])
                  (WT.nil _))))))⟩

/-- For every learned predictor, gradient, optimizer and readout (every `ι`), the
witness architecture's observations do not depend on payload, private weights or
the private descriptor. -/
theorem witnessProg_payload_ni (P : Val → Val → Bool) (ι : Interp) (ρ1 ρ2 : Env)
    (h : ∀ a, a ∈ [0, 1, 2, 6, 7] → ρ1 a = ρ2 a) :
    obs ι (witnessProg P) ρ1 = obs ι (witnessProg P) ρ2 := by
  obtain ⟨Γ', hwt⟩ := witnessProg_wt P
  apply payload_ni κw ι hwt ρ1 ρ2
  · intro a k hk hl
    match a, hk with
    | 0, _ => exact h 0 (by simp)
    | 1, _ => exact h 1 (by simp)
    | 2, _ => exact h 2 (by simp)
    | 3, hk => simp [κw] at hk; subst hk; simp [Kind.label] at hl
    | 4, hk => simp [κw] at hk; subst hk; simp [Kind.label] at hl
    | 5, hk => simp [κw] at hk; subst hk; simp [Kind.label] at hl
    | 6, hk => simp [κw] at hk; subst hk; simp [Kind.label] at hl
    | 7, hk => simp [κw] at hk; subst hk; simp [Kind.label] at hl
    | n + 8, hk => simp [κw] at hk
  · intro a hk
    match a, hk with
    | 6, _ => exact h 6 (by simp)
    | 7, _ => exact h 7 (by simp)
    | 0, hk | 1, hk | 2, hk | 3, hk | 4, hk | 5, hk => simp [κw] at hk
    | n + 8, hk => simp [κw] at hk

/-- Observing the privately trained parameters is rejected. -/
example (P : Val → Val → Bool) :
    ¬ ∃ Γ', WT κw (ctx0 κw) (witnessProg P ++ [.observe 9]) Γ' := by
  rintro ⟨Γ', h⟩
  cases h with | op _ h => cases h with | op _ h => cases h with | release _ _ _ h =>
  cases h with | op _ h => cases h with | observe _ h => cases h with | observe _ h =>
  cases h with | observe hw _ =>
  simp [setCtx, joinAll, ctx0, κw, Kind.label, Label.join] at hw

/-! ### Necessity examples (concrete counterexamples when a rule is dropped) -/

/-- Wire 0: public task, wire 1: payload. -/
def κex : Wire → Option Kind
  | 0 => some .publicTask
  | 1 => some .payload
  | _ => none

def ρm (m : Val) : Env := fun w => if w = 1 then m else 0

/-- (R1) dropped: a release whose spec reads the payload, with a valid contract. -/
def leakSpec : Prog :=
  [.release 2 (fun l => l.headD 0) [1] (fun _ ρ => ρ 1), .observe 2]

example (ι : Interp) : obs ι leakSpec (ρm 0) ≠ obs ι leakSpec (ρm 1) := by
  simp [obs, run, leakSpec, upd, ρm]

/-- Contract dropped: release claims spec "constant 0" but outputs the payload. -/
def leakImpl : Prog :=
  [.release 2 (fun _ => 0) [0] (fun _ ρ => ρ 1), .observe 2]

example (ι : Interp) : obs ι leakImpl (ρm 0) ≠ obs ι leakImpl (ρm 1) := by
  simp [obs, run, leakImpl, upd, ρm]

/-- Join rule dropped: an op reading the payload labeled public. Here, with
the identity interpretation of "id". -/
def leakOp : Prog := [.op 2 "id" [1], .observe 2]

example : obs (fun _ l => l.headD 0) leakOp (ρm 0) ≠
    obs (fun _ l => l.headD 0) leakOp (ρm 1) := by
  simp [obs, run, leakOp, upd, ρm]

/-- And the full checker rejects each of them: R1, the contract, and the join rule. -/
example : ¬ ∃ Γ', WT κex (ctx0 κex) leakSpec Γ' := by
  rintro ⟨Γ', h⟩
  cases h with
  | release _ hread _ _ =>
    obtain ⟨k, hk, hr⟩ := hread 1 (by simp)
    simp [κex] at hk; subst hk; simp [Kind.specReadable] at hr

example : ¬ ∃ Γ', WT κex (ctx0 κex) leakImpl Γ' := by
  rintro ⟨Γ', h⟩
  cases h with
  | release _ _ hcon _ =>
    have := hcon (fun _ _ => 0) (ρm 1)
    simp [ρm] at this

example : ¬ ∃ Γ', WT κex (ctx0 κex) leakOp Γ' := by
  rintro ⟨Γ', h⟩
  cases h with
  | op _ h2 =>
    cases h2 with
    | observe hw _ =>
      simp [setCtx, joinAll, ctx0, κex, Kind.label, Label.join] at hw

end Arch

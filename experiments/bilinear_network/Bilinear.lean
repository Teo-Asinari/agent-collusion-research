import Residue

namespace Bilinear
open Residue

def dotExpr (d start : Nat) : Expr :=
  (List.range d).foldl (fun e i =>
    .add e (.mul (.input (start+i)) (.input i))) (.lit 0)

def networkExpr (d r : Nat) : Expr :=
  (List.range r).foldl (fun e j =>
    .add e (.mul (dotExpr d (2*d+1+j*d))
                  (dotExpr d (2*d+1+r*d+j*d))))
    (.add (.input d) (dotExpr d (d+1)))

def env (xs parameters : List Nat) : Env :=
  fun i => if i < xs.length then xs[i]! else parameters[i-xs.length]!

def predict (d r q : Nat) (parameters xs : List Nat) : Nat :=
  eval q (env xs parameters) (networkExpr d r)

/-- All input and hidden/linear/bias weight words participate in the relation. -/
theorem content_noninterference (d r : Nat) (a b : Env)
    (h : ∀ i, a i % 3 = b i % 3) :
    eval 9 a (networkExpr d r) % 3 = eval 9 b (networkExpr d r) % 3 :=
  Residue.noninterference 3 3 a b h (networkExpr d r)

/-- The larger carrier gives no extra expressiveness for the released answer. -/
theorem direct_projection (d r : Nat) (a : Env) :
    eval 9 a (networkExpr d r) % 3 = eval 3 a (networkExpr d r) :=
  Residue.project 3 3 a (networkExpr d r)

def target (d q : Nat) (c : Nat) (linear matrix xs : List Nat) : Nat :=
  let affine := (List.range d).foldl
    (fun out i => out + linear[i]! * xs[i]!) c
  ((List.range (d*d)).foldl (fun out k =>
    out + matrix[k]! * xs[k/d]! * xs[k%d]!) affine) % q

#print axioms content_noninterference
#print axioms direct_projection
end Bilinear

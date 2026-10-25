/-
Leak-capped choice architecture: mechanized capacity bound. Core Lean 4, no mathlib.

Every receiver-visible value is produced either by public computation or by a
`choose` node: out := dec(public args, code), where code = (value of wire c) mod 2^k.
The wire c may be computed by ANY private network (every function symbol is
interpreted by an arbitrary ι, and private weights/payload/state are input wires).

Theorem `view_count`: for every interpretation ι and every fixed setting of the
public inputs, the receiver's whole view lies in an explicit list of at most
2^(k₁+…+kₙ) values, where k₁…kₙ are the code widths of the program's choose
nodes. So over all payloads, private inputs and private weights, the view takes
at most 2^(Σk) values: at most Σk bits (k per answer for one choose per answer).

Model scope: deterministic semantics given input wires (public randomness is a
public input wire, private sampling tapes are private input wires); only values
of `observe` nodes are observed (fixed-time / padded execution is assumed, not
modeled).
-/
namespace Choice

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

inductive CNode where
  | op (out : Wire) (fn : String) (args : List Wire)
  | choose (out : Wire) (c : Wire) (k : Nat) (dec : List Val → Nat → Val) (pubArgs : List Wire)
  | observe (w : Wire)

abbrev CProg := List CNode

def upd (ρ : Env) (w : Wire) (v : Val) : Env := fun x => if x = w then v else ρ x

/-- The k-bit code actually used: total and always < 2^k. -/
def code (k : Nat) (v : Val) : Nat := v.toNat % 2 ^ k

/-- Semantics: observations and the list of codes emitted. -/
def run (ι : Interp) : CProg → Env → List Val × List Nat
  | [], _ => ([], [])
  | .op out fn args :: p, ρ => run ι p (upd ρ out (ι fn (args.map ρ)))
  | .choose out c k dec args :: p, ρ =>
      let cd := code k (ρ c)
      let r := run ι p (upd ρ out (dec (args.map ρ) cd))
      (r.1, cd :: r.2)
  | .observe w :: p, ρ => let r := run ι p ρ; (ρ w :: r.1, r.2)

def obs (ι : Interp) (p : CProg) (ρ : Env) : List Val := (run ι p ρ).1

/-- Replay semantics: take codes from a supplied list instead of from wire c. -/
def replay (ι : Interp) : CProg → Env → List Nat → List Val
  | [], _, _ => []
  | .op out fn args :: p, ρ, cs => replay ι p (upd ρ out (ι fn (args.map ρ))) cs
  | .choose out _ _ dec args :: p, ρ, cs =>
      replay ι p (upd ρ out (dec (args.map ρ) (cs.headD 0))) cs.tail
  | .observe w :: p, ρ, cs => ρ w :: replay ι p ρ cs

theorem replay_own (ι : Interp) :
    ∀ (p : CProg) (ρ : Env), replay ι p ρ (run ι p ρ).2 = obs ι p ρ
  | [], _ => rfl
  | .op out fn args :: p, ρ => by
      simp only [replay, run, obs]; exact replay_own ι p _
  | .choose out c k dec args :: p, ρ => by
      simp only [replay, run, obs, List.headD, List.tail]; exact replay_own ι p _
  | .observe w :: p, ρ => by
      simp only [replay, run, obs]; rw [replay_own ι p ρ]; rfl

/-! ### Typing: the code is the only private-to-public path -/

abbrev Ctx := Wire → Option Label

def joinAll (Γ : Ctx) : List Wire → Label
  | [] => .pub
  | a :: as =>
    match Γ a with
    | some l => l.join (joinAll Γ as)
    | none => .priv

def setCtx (Γ : Ctx) (w : Wire) (l : Label) : Ctx :=
  fun x => if x = w then some l else Γ x

inductive WTc : Ctx → CProg → Prop where
  | nil (Γ : Ctx) : WTc Γ []
  | op {Γ : Ctx} {out : Wire} {fn : String} {args : List Wire} {p : CProg} :
      WTc (setCtx Γ out (joinAll Γ args)) p → WTc Γ (.op out fn args :: p)
  | choose {Γ : Ctx} {out c : Wire} {k : Nat} {dec : List Val → Nat → Val}
      {args : List Wire} {p : CProg} :
      (∀ a ∈ args, Γ a = some .pub) →
      WTc (setCtx Γ out .pub) p → WTc Γ (.choose out c k dec args :: p)
  | observe {Γ : Ctx} {w : Wire} {p : CProg} :
      Γ w = some .pub → WTc Γ p → WTc Γ (.observe w :: p)

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

theorem upd_pub {Γ : Ctx} {ρ1 ρ2 : Env} {out : Wire} {l : Label} {v1 v2 : Val}
    (hpub : ∀ w, Γ w = some .pub → ρ1 w = ρ2 w) (hv : l = .pub → v1 = v2) :
    ∀ w, setCtx Γ out l w = some .pub → upd ρ1 out v1 w = upd ρ2 out v2 w := by
  intro w hw
  simp only [setCtx] at hw
  simp only [upd]
  by_cases hwo : w = out
  · simp only [hwo, ite_true] at hw ⊢; exact hv (Option.some.inj hw)
  · simp only [hwo, ite_false] at hw ⊢; exact hpub w hw

/-- Given the same codes, the view depends only on public wires. -/
theorem replay_ni (ι : Interp) {Γ : Ctx} {p : CProg} (h : WTc Γ p) :
    ∀ (ρ1 ρ2 : Env) (cs : List Nat), (∀ w, Γ w = some .pub → ρ1 w = ρ2 w) →
      replay ι p ρ1 cs = replay ι p ρ2 cs := by
  induction h with
  | nil => intro _ _ _ _; rfl
  | @op Γ out fn args p _ ih =>
    intro ρ1 ρ2 cs hpub
    simp only [replay]
    apply ih _ _ cs
    apply upd_pub hpub
    intro hl
    rw [map_congr' args (fun a ha => hpub a (joinAll_pub Γ args hl a ha))]
  | @choose Γ out c k dec args p hargs _ ih =>
    intro ρ1 ρ2 cs hpub
    simp only [replay]
    apply ih _ _ cs.tail
    apply upd_pub hpub
    intro _
    rw [map_congr' args (fun a ha => hpub a (hargs a ha))]
  | @observe Γ w p hw _ ih =>
    intro ρ1 ρ2 cs hpub
    simp only [replay]
    rw [hpub w hw, ih ρ1 ρ2 cs hpub]

/-! ### Counting: all code lists, and the capacity bound -/

def widths : CProg → List Nat
  | [] => []
  | .choose _ _ k _ _ :: p => k :: widths p
  | _ :: p => widths p

def allCodes : List Nat → List (List Nat)
  | [] => [[]]
  | k :: ks => (List.range (2 ^ k)).flatMap (fun c => (allCodes ks).map (c :: ·))

theorem length_flatMap_cons (A : List (List Nat)) :
    ∀ (l : List Nat), (l.flatMap (fun c => A.map (c :: ·))).length = l.length * A.length
  | [] => by simp
  | c :: l => by
    simp only [List.flatMap_cons, List.length_append, List.length_map, List.length_cons,
      length_flatMap_cons A l]
    rw [Nat.succ_mul, Nat.add_comm]

theorem allCodes_length : ∀ (ks : List Nat), (allCodes ks).length = 2 ^ ks.sum
  | [] => rfl
  | k :: ks => by
    simp only [allCodes, length_flatMap_cons, List.length_range, allCodes_length ks,
      List.sum_cons, Nat.pow_add]

theorem codes_mem (ι : Interp) :
    ∀ (p : CProg) (ρ : Env), (run ι p ρ).2 ∈ allCodes (widths p)
  | [], _ => by simp [run, widths, allCodes]
  | .op out fn args :: p, ρ => by
      simp only [run, widths]; exact codes_mem ι p _
  | .choose out c k dec args :: p, ρ => by
      simp only [run, widths, allCodes, List.mem_flatMap, List.mem_range, List.mem_map]
      exact ⟨code k (ρ c), Nat.mod_lt _ (Nat.two_pow_pos k), _,
        codes_mem ι p _, rfl⟩
  | .observe w :: p, ρ => by
      simp only [run, widths]; exact codes_mem ι p ρ

/-- **Capacity bound.** Fix any interpretation ι (all weights, all policies) and any
reference environment ρ₀. For every environment ρ that agrees with ρ₀ on the
initially public wires — i.e. for every payload, private input, private sampling
tape and private weight setting — the receiver's view lies in the list
`(allCodes (widths p)).map (replay ι p ρ₀)`, which has exactly 2^(Σ widths)
entries. -/
theorem view_count (ι : Interp) {Γ0 : Ctx} {p : CProg} (h : WTc Γ0 p) (ρ0 ρ : Env)
    (hpub : ∀ w, Γ0 w = some .pub → ρ w = ρ0 w) :
    obs ι p ρ ∈ (allCodes (widths p)).map (replay ι p ρ0) ∧
    ((allCodes (widths p)).map (replay ι p ρ0)).length = 2 ^ (widths p).sum := by
  refine ⟨?_, by rw [List.length_map, allCodes_length]⟩
  rw [← replay_own ι p ρ, replay_ni ι h ρ ρ0 _ hpub]
  exact List.mem_map_of_mem (codes_mem ι p ρ)

/-! ### The seed instance: public proposer, private chooser, trusted decoder

Wires: 0 public input x, 1 public randomness r, 2 private payload m,
3 private weights θ, 4 private context. The public proposer is a public op;
the untrusted network's score is a private op; the decoder picks candidate
`code` out of 2^k produced from (x, r) only. One answer: view ≤ 2^k values. -/

def Γseed : Ctx
  | 0 => some .pub | 1 => some .pub
  | 2 => some .priv | 3 => some .priv | 4 => some .priv
  | _ => none

/-- dec gets the public args [x, r, proposer-state] and the code. -/
def seed (k : Nat) (dec : List Val → Nat → Val) : CProg :=
  [ .op 10 "PublicProposer" [0, 1],          -- public candidates' seed/state
    .op 11 "UntrustedNet" [0, 2, 3, 4, 10],  -- private: reads payload & weights
    .choose 12 11 k dec [0, 1, 10],          -- trusted decoder
    .observe 12 ]

theorem seed_wt (k : Nat) (dec : List Val → Nat → Val) : WTc Γseed (seed k dec) :=
  WTc.op (WTc.op (WTc.choose
    (by intro a ha; simp at ha
        rcases ha with rfl | rfl | rfl <;> simp [setCtx, Γseed, joinAll, Label.join])
    (WTc.observe (by simp [setCtx]) (WTc.nil _))))

theorem seed_capacity (k : Nat) (dec : List Val → Nat → Val) (ι : Interp) (ρ0 ρ : Env)
    (hpub : ρ 0 = ρ0 0 ∧ ρ 1 = ρ0 1) :
    obs ι (seed k dec) ρ ∈ (allCodes [k]).map (replay ι (seed k dec) ρ0) ∧
    ((allCodes [k]).map (replay ι (seed k dec) ρ0)).length = 2 ^ k := by
  have := view_count ι (seed_wt k dec) ρ0 ρ (by
    intro w hw
    match w, hw with
    | 0, _ => exact hpub.1
    | 1, _ => exact hpub.2
    | 2, hw | 3, hw | 4, hw => simp [Γseed] at hw
    | n + 5, hw => simp [Γseed] at hw)
  simpa [widths, seed] using this

/-- Necessity: if the decoder could read the private score directly (a private
arg), the view is no longer bounded by k: here k = 0 yet the payload leaks. -/
def leaky : CProg := [.op 11 "UntrustedNet" [2], .choose 12 11 0 (fun l _ => l.headD 0) [11], .observe 12]

example : ¬ WTc Γseed leaky := by
  intro h
  cases h with
  | op h => cases h with
    | choose hargs _ =>
      have := hargs 11 (by simp)
      simp [setCtx, joinAll, Γseed, Label.join] at this

end Choice

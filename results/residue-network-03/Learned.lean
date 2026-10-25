import Residue
namespace Learned
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000
def weights_0 : List Nat := [0, 0, 0, 0, 0]
def labels_0 : List Nat := [0, 0, 0, 0]
theorem task_0_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_0 a b) Residue.network1 =
  (labels_0[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_1 : List Nat := [1, 1, 1, 2, 1]
def labels_1 : List Nat := [0, 0, 0, 1]
theorem task_1_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_1 a b) Residue.network1 =
  (labels_1[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_2 : List Nat := [1, 2, 2, 2, 1]
def labels_2 : List Nat := [0, 0, 1, 0]
theorem task_2_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_2 a b) Residue.network1 =
  (labels_2[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_3 : List Nat := [1, 0, 0, 1, 0]
def labels_3 : List Nat := [0, 0, 1, 1]
theorem task_3_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_3 a b) Residue.network1 =
  (labels_3[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_4 : List Nat := [1, 2, 1, 2, 1]
def labels_4 : List Nat := [0, 1, 0, 0]
theorem task_4_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_4 a b) Residue.network1 =
  (labels_4[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_5 : List Nat := [0, 1, 0, 1, 0]
def labels_5 : List Nat := [0, 1, 0, 1]
theorem task_5_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_5 a b) Residue.network1 =
  (labels_5[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_6 : List Nat := [1, 1, 2, 2, 1]
def labels_6 : List Nat := [0, 1, 1, 0]
theorem task_6_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_6 a b) Residue.network1 =
  (labels_6[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_7 : List Nat := [1, 1, 0, 1, 0]
def labels_7 : List Nat := [0, 1, 1, 1]
theorem task_7_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_7 a b) Residue.network1 =
  (labels_7[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_8 : List Nat := [1, 1, 0, 2, 1]
def labels_8 : List Nat := [1, 0, 0, 0]
theorem task_8_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_8 a b) Residue.network1 =
  (labels_8[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_9 : List Nat := [1, 1, 2, 1, 0]
def labels_9 : List Nat := [1, 0, 0, 1]
theorem task_9_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_9 a b) Residue.network1 =
  (labels_9[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_10 : List Nat := [0, 1, 0, 2, 1]
def labels_10 : List Nat := [1, 0, 1, 0]
theorem task_10_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_10 a b) Residue.network1 =
  (labels_10[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_11 : List Nat := [1, 2, 1, 1, 0]
def labels_11 : List Nat := [1, 0, 1, 1]
theorem task_11_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_11 a b) Residue.network1 =
  (labels_11[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_12 : List Nat := [1, 0, 0, 2, 1]
def labels_12 : List Nat := [1, 1, 0, 0]
theorem task_12_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_12 a b) Residue.network1 =
  (labels_12[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_13 : List Nat := [1, 2, 2, 1, 0]
def labels_13 : List Nat := [1, 1, 0, 1]
theorem task_13_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_13 a b) Residue.network1 =
  (labels_13[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_14 : List Nat := [1, 1, 1, 1, 0]
def labels_14 : List Nat := [1, 1, 1, 0]
theorem task_14_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_14 a b) Residue.network1 =
  (labels_14[a.toNat * 2 + b.toNat]?).getD 0 := by decide
def weights_15 : List Nat := [0, 0, 0, 0, 1]
def labels_15 : List Nat := [1, 1, 1, 1]
theorem task_15_correct : ∀ a b : Bool,
  Residue.eval 3 (Residue.env2 weights_15 a b) Residue.network1 =
  (labels_15[a.toNat * 2 + b.toNat]?).getD 0 := by decide
#print axioms task_6_correct
end Learned

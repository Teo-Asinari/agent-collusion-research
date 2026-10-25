import Bilinear
set_option maxRecDepth 200000
set_option maxHeartbeats 0
namespace LearnedBilinear
def parameters_0 : List Nat := [2, 2, 2, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0]
theorem correct_0 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 1 3 parameters_0 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 2 [2, 2, 1, 0] [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_0
def parameters_1 : List Nat := [1, 1, 2, 0, 0, 1, 0, 0, 2, 1, 0, 0, 2]
theorem correct_1 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 1 3 parameters_1 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 1 [1, 2, 0, 0] [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_1
def parameters_2 : List Nat := [2, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
theorem correct_2 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 1 3 parameters_2 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 2 [0, 1, 0, 0] [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_2
def parameters_3 : List Nat := [2, 2, 0, 0, 1, 1, 2, 2, 2, 1, 2, 2, 2]
theorem correct_3 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 1 3 parameters_3 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 2 [2, 0, 0, 1] [1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_3
def parameters_4 : List Nat := [1, 1, 0, 2, 0, 2, 0, 2, 2, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0]
theorem correct_4 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 2 3 parameters_4 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 1 [1, 0, 2, 0] [2, 0, 2, 2, 0, 1, 0, 0, 2, 0, 2, 2, 2, 0, 2, 2] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_4
def parameters_5 : List Nat := [2, 0, 0, 1, 2, 2, 0, 0, 0, 0, 2, 1, 0, 1, 0, 0, 0, 0, 1, 2, 0]
theorem correct_5 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 2 3 parameters_5 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 2 [0, 0, 1, 2] [2, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_5
def parameters_6 : List Nat := [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
theorem correct_6 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 2 3 parameters_6 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 0 [0, 0, 0, 1] [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_6
def parameters_7 : List Nat := [0, 1, 2, 0, 1, 1, 0, 2, 2, 0, 1, 2, 2, 1, 0, 2, 2, 0, 1, 2, 2]
theorem correct_7 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 2 3 parameters_7 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 0 [1, 2, 0, 1] [1, 0, 2, 2, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_7
def parameters_8 : List Nat := [2, 2, 2, 1, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
theorem correct_8 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 4 3 parameters_8 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 2 [2, 2, 1, 0] [2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_8
def parameters_9 : List Nat := [1, 2, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
theorem correct_9 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 4 3 parameters_9 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 1 [2, 0, 0, 1] [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_9
def parameters_10 : List Nat := [2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
theorem correct_10 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 4 3 parameters_10 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 2 [0, 1, 0, 0] [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_10
def parameters_11 : List Nat := [2, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
theorem correct_11 : ∀ a b c d : Fin 3,
  Bilinear.predict 4 4 3 parameters_11 [a.val,b.val,c.val,d.val] =
  Bilinear.target 4 3 2 [0, 1, 0, 1] [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2] [a.val,b.val,c.val,d.val] := by decide
#print axioms correct_11
end LearnedBilinear

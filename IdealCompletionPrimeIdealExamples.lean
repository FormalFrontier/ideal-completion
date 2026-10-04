/-
SPDX-License-Identifier: Apache-2.0
Authors: Formal Frontier Agents
-/
module

public import IdealCompletion.PrimeIdeal
public import Mathlib.Order.Hom.BoundedLattice
import Mathlib.Order.CompleteLattice.Lemmas

/-!
# Boolean-valued maps and prime ideals: examples

The identity map on `Bool` and the first-coordinate map on `Bool × Bool` exhibit
nonempty false fibers. The one-element bounded lattice `PUnit` has neither a
Boolean-valued bounded lattice homomorphism nor a prime ideal.
-/

@[expose] public section

namespace IdealCompletionPrimeIdealExamples

private theorem bool_principal_false_prime :
    (Order.Ideal.principal (false : Bool)).IsPrime := by
  have hproper : (Order.Ideal.principal (false : Bool)).IsProper := by
    apply Order.Ideal.isProper_iff_top_notMem.mpr
    simp
  refine @Order.Ideal.IsPrime.of_mem_or_mem Bool _ (Order.Ideal.principal false) hproper ?_
  intro x y hxy
  cases x <;> cases y <;> simp_all [Order.Ideal.mem_principal]

private theorem bool_prime_characteristic :
    bool_principal_false_prime.toBoolHom false = false ∧
      bool_principal_false_prime.toBoolHom true = true := by
  constructor
  · apply (bool_principal_false_prime.toBoolHom_apply_eq_false_iff false).2
    simp
  · apply (bool_principal_false_prime.toBoolHom_apply_eq_true_iff true).2
    simp

/-- The identity map on `Bool` has exactly `false` in its false fiber. -/
theorem bool_identity_false_fiber :
    false ∈ (BoundedLatticeHom.id Bool).falseIdeal ∧
      true ∉ (BoundedLatticeHom.id Bool).falseIdeal := by
  simp

private def firstCoordinate : BoundedLatticeHom (Bool × Bool) Bool where
  toFun := Prod.fst
  map_sup' := by intros; rfl
  map_inf' := by intros; rfl
  map_top' := rfl
  map_bot' := rfl

private theorem first_coordinate_false_fiber :
    (false, true) ∈ firstCoordinate.falseIdeal ∧
      (true, false) ∉ firstCoordinate.falseIdeal := by
  simp [firstCoordinate]

private theorem first_coordinate_characteristic :
    ((Order.Ideal.primeEquivBoolHom.symm firstCoordinate).property.toBoolHom)
      (true, false) = true := by
  simp [firstCoordinate]

private theorem no_boolHom_punit : IsEmpty (BoundedLatticeHom PUnit Bool) := by
  refine ⟨fun f => ?_⟩
  have h : (false : Bool) = true := by
    calc
      false = f (⊥ : PUnit) := (map_bot f).symm
      _ = f (⊤ : PUnit) := congrArg f (Subsingleton.elim _ _)
      _ = true := map_top f
  exact Bool.false_ne_true h

private theorem no_prime_punit : ¬ ∃ I : Order.Ideal PUnit, I.IsPrime := by
  rintro ⟨I, hI⟩
  have htop : (⊤ : PUnit) ∈ I := (Subsingleton.elim (⊥ : PUnit) ⊤) ▸ I.bot_mem
  exact hI.toIsProper.top_notMem htop

end IdealCompletionPrimeIdealExamples

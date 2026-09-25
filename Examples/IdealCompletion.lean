/-

SPDX-License-Identifier: Apache-2.0
Authors: Formal Frontier Agents
-/
module

import IdealCompletion

/-!
# Using ideal completions

These named private clients use only the public aggregate import, without opening
private declarations or reproducing the implementation of the library's results.
They are a separate default build target, not part of the library's public API.
-/

open Order

universe u

namespace IdealCompletionExamples

variable {A : Type u} [DistribLattice A] [BoundedOrder A]

-- The embedding is a bundled map, so its operation laws are available directly.
private noncomputable def principalHom : BoundedLatticeHom A (Ideal A) := Ideal.principalHom

private theorem principalHom_map_sup (a b : A) :
    Ideal.principalHom (a ⊔ b) = Ideal.principalHom a ⊔ Ideal.principalHom b :=
  map_sup (Ideal.principalHom : BoundedLatticeHom A (Ideal A)) a b

private theorem principalHom_injective {a b : A}
    (h : Ideal.principalHom a = Ideal.principalHom b) : a = b :=
  Ideal.principalHom_injective h

-- Infinite joins, frame operations and compact generation use native classes.
@[instance_reducible] private noncomputable def completeLattice : CompleteLattice (Ideal A) :=
  inferInstance

@[instance_reducible] private noncomputable def frame : Order.Frame (Ideal A) := inferInstance

private theorem compactlyGenerated : IsCompactlyGenerated (Ideal A) := inferInstance

private theorem mem_sSup_iff (S : Set (Ideal A)) (x : A) :
    x ∈ sSup S ↔
      ∃ t : Finset A, (∀ a ∈ t, ∃ I ∈ S, a ∈ I) ∧ x ≤ t.sup id :=
  Ideal.mem_sSup_iff

-- Compact means compact in the complete lattice, not a finite underlying set.
private theorem isCompactElement_principal (a : A) : IsCompactElement (Ideal.principal a) :=
  Ideal.isCompactElement_principal a

private theorem isCompactElement_iff_eq_principal (I : Ideal A) :
    IsCompactElement I ↔ ∃ a : A, I = Ideal.principal a :=
  Ideal.isCompactElement_iff_eq_principal I

-- Combining the public results characterizes the image of the embedding.
private theorem principalHom_range_iff_compact (I : Ideal A) :
    I ∈ Set.range (Ideal.principalHom : A → Ideal A) ↔ IsCompactElement I := by
  constructor
  · rintro ⟨a, rfl⟩
    exact Ideal.isCompactElement_principal a
  · intro hI
    obtain ⟨a, rfl⟩ := (Ideal.isCompactElement_iff_eq_principal I).mp hI
    exact ⟨a, rfl⟩

-- The interface also covers bottom and the empty family of ideals.
private theorem bottom_compact : IsCompactElement (Ideal.principal (⊥ : A)) :=
  Ideal.isCompactElement_principal ⊥

private theorem empty_sSup : sSup (∅ : Set (Ideal A)) = ⊥ := sSup_empty

end IdealCompletionExamples

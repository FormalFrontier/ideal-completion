> **Historical scope (human-maintained notice):** The generated reference below
> covers the seven public declarations of the ideal-completion library at its
> [recorded source revision](api-manifest.json), when `IdealCompletion` imported
> only `IdealCompletion.OrderIdeal`. The current aggregate also publicly imports
> `IdealCompletion.PrimeIdeal`; see the [prime-ideal API guide](PrimeIdeals.md).
> References below to "every public declaration" and "its leaf" describe that
> historical revision, not the current library. The manifest's `api_sha256`
> hashes the unchanged generated payload beginning at `# Generated API reference`,
> excluding this notice.

# Generated API reference

This reference covers every public declaration defined by ideal-completion.
Import `IdealCompletion`; its leaf is `IdealCompletion.OrderIdeal`.
`Examples.IdealCompletion` contains private checked clients, not additional public API.

Headers below are native doc-gen4 display signatures, not complete declarations
with proof bodies. Short mathematical names use the source's `Order.Ideal`
namespace and imports. All implicit lattice parameters are displayed; `u` is
an arbitrary universe. Source links are relative to this same checkout.

The source/pin hashes and generation provenance are in [api-manifest.json](api-manifest.json).
See [generation instructions](README.md) and the [mathematical overview](../README.md).

## Order.Ideal.principalHom

```lean
def Order.Ideal.principalHom {A : Type u} [DistribLattice A] [BoundedOrder A] : BoundedLatticeHom A (Ideal A)
```

The principal-ideal embedding as a bounded lattice homomorphism.

[Source](../IdealCompletion/OrderIdeal.lean#L29) (line 29).

## Order.Ideal.principalHom_injective

```lean
theorem Order.Ideal.principalHom_injective {A : Type u} [DistribLattice A] [BoundedOrder A] : Function.Injective ⇑principalHom
```

The principal-ideal bounded lattice homomorphism is injective.

[Source](../IdealCompletion/OrderIdeal.lean#L47) (line 47).

## Order.Ideal.mem_sSup_iff

```lean
theorem Order.Ideal.mem_sSup_iff {A : Type u} [DistribLattice A] [BoundedOrder A] {S : Set (Ideal A)} {x : A} : x ∈ sSup S ↔ ∃ (t : Finset A), (∀ a ∈ t, ∃ I ∈ S, a ∈ I) ∧ x ≤ t.sup id
```

Membership in a supremum of order ideals is witnessed by a finite join of
elements drawn from those ideals.

[Source](../IdealCompletion/OrderIdeal.lean#L77) (line 77).

## Order.Ideal.instFrame_idealCompletion

```lean
instance Order.Ideal.instFrame_idealCompletion {A : Type u} [DistribLattice A] [BoundedOrder A] : Frame (Ideal A)
```

The ideal completion of a bounded distributive lattice is a frame, also
known as a complete Heyting algebra.

[Source](../IdealCompletion/OrderIdeal.lean#L96) (line 96).

## Order.Ideal.isCompactElement_principal

```lean
theorem Order.Ideal.isCompactElement_principal {A : Type u} [DistribLattice A] [BoundedOrder A] (a : A) : IsCompactElement (principal a)
```

Every principal ideal is a compact element of the ideal completion.

[Source](../IdealCompletion/OrderIdeal.lean#L116) (line 116).

## Order.Ideal.isCompactElement_iff_eq_principal

```lean
theorem Order.Ideal.isCompactElement_iff_eq_principal {A : Type u} [DistribLattice A] [BoundedOrder A] (I : Ideal A) : IsCompactElement I ↔ ∃ (a : A), I = principal a
```

The compact elements of an ideal completion are exactly the principal ideals.

[Source](../IdealCompletion/OrderIdeal.lean#L141) (line 141).

## Order.Ideal.instIsCompactlyGenerated_idealCompletion

```lean
instance Order.Ideal.instIsCompactlyGenerated_idealCompletion {A : Type u} [DistribLattice A] [BoundedOrder A] : IsCompactlyGenerated (Ideal A)
```

Every ideal completion is compactly generated.

[Source](../IdealCompletion/OrderIdeal.lean#L168) (line 168).

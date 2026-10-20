# ideal-completion

Reusable Lean theory of ideal completions and prime order ideals.

For `A` with `[DistribLattice A]` and `[BoundedOrder A]`, this library works
with mathlib's order ideals: nonempty, directed lower sets. It constructs a
principal-ideal embedding, equips `Order.Ideal A` with a frame (complete Heyting
algebra) structure, and characterizes its order-theoretically compact elements.
No finiteness or nontriviality assumption on `A` is needed.

For any bounded lattice, prime order ideals also correspond to bounded lattice
homomorphisms into `Bool`, without assuming distributivity or decidable ideal
membership.

## Headline results

- **Principal embedding.** [`Order.Ideal.principalHom`](IdealCompletion/OrderIdeal.lean#L29)
  sends `a` to its principal ideal as a bounded lattice homomorphism;
  [`principalHom_injective`](IdealCompletion/OrderIdeal.lean#L47) shows it is
  injective. Its operation laws are available through the bundled homomorphism.
- **Frame and arbitrary suprema.** The
  [`Order.Frame` instance](IdealCompletion/OrderIdeal.lean#L96) makes the ideal
  completion a complete Heyting algebra. The
  [`mem_sSup_iff` theorem](IdealCompletion/OrderIdeal.lean#L77) characterizes
  `x ∈ sSup S` by a finite set of elements, each in some ideal of the *arbitrary*
  family `S`, whose join is **at least** `x`. This includes the empty-family and
  bottom cases; it is not restricted to directed families.
- **Compact generation.** Every principal ideal is
  [compact](IdealCompletion/OrderIdeal.lean#L116), and
  [`isCompactElement_iff_eq_principal`](IdealCompletion/OrderIdeal.lean#L141)
  identifies **all** compact ideals as principal. The
  [`IsCompactlyGenerated` instance](IdealCompletion/OrderIdeal.lean#L168)
  expresses every ideal as a supremum of compact ideals. Compactness here is
  order-theoretic, not finiteness of the ideal's underlying set.
- **Prime ideals and Boolean-valued maps.** For `[Lattice A]` and
  `[BoundedOrder A]`,
  [`Order.Ideal.primeEquivBoolHom`](IdealCompletion/PrimeIdeal.lean)
  identifies prime order ideals with bounded lattice homomorphisms `A → Bool`.
  The characteristic map sends precisely the ideal to `false`; conversely
  [`BoundedLatticeHom.falseIdeal`](IdealCompletion/PrimeIdeal.lean)
  is its prime false fiber. Every such map is surjective. This includes the
  one-element lattice, for which both sides of the equivalence are empty.

These constructions and proofs build on mathlib's existing ideal, lattice and
compactness infrastructure. They do not establish prime-ideal existence,
spectra, Stone duality, a universal extension property, generic partial-order
completion, or completion of any source text.

This repository is organized around reusable order theory. Source-specific
interpretation, provenance, correspondence, and coverage remain in the relevant
source-metadata repositories; the Formal Frontier source-maintainer team
maintains this library.

The [generated API reference](docs/API.md) is bound to an earlier seven-declaration
ideal-completion revision and does **not** cover the new prime-ideal module or
the current aggregate import. See the [prime-ideal API guide](docs/PrimeIdeals.md)
for the new declarations, and [reference scope and generation](docs/README.md)
for the historical native signatures and exact source binding.

## Public interface

Use `import IdealCompletion` in a client, or `public import IdealCompletion` in a
module that deliberately re-exports this API. The following example also appears
in [the examples module](Examples/IdealCompletion.lean):

```lean
module
import IdealCompletion

open Order

example {A : Type*} [DistribLattice A] [BoundedOrder A] (I : Ideal A) :
    IsCompactElement I ↔ ∃ a : A, I = Ideal.principal a :=
  Ideal.isCompactElement_iff_eq_principal I
```

The main interface, in namespace `Order.Ideal`, is:

| Interface | Purpose |
| --- | --- |
| `principalHom` | Principal ideals as a bounded lattice homomorphism |
| `principalHom_injective` | Recover equality in the original lattice |
| `mem_sSup_iff` | Finite-join witnesses for membership in an arbitrary supremum |
| `Order.Frame (Order.Ideal A)` | Complete Heyting algebra structure, inferred by typeclass search |
| `isCompactElement_principal` | Every principal ideal is compact |
| `isCompactElement_iff_eq_principal` | Every compact ideal is principal, and conversely |
| `IsCompactlyGenerated (Order.Ideal A)` | Compact generation, inferred by typeclass search |

The separate [prime-ideal guide](docs/PrimeIdeals.md) covers the equivalence,
both inverse constructions, characteristic evaluation, and false-fiber laws
for arbitrary bounded lattices.

The examples also exercise operation laws, the image of the embedding, and the
bottom/empty-family cases. They import only the public aggregate module and store
twelve named private clients for inspection without extending the public API.
[Prime-ideal examples](IdealCompletionPrimeIdealExamples.lean) additionally
instantiate the correspondence on `Bool` and `Bool × Bool` and check its empty
boundary on `PUnit`.

## Build and checks

The exact Lean toolchain is in `lean-toolchain`, and `lake-manifest.json` pins
the complete dependency graph. Install the pinned toolchain with `elan`; it must
support Lean's module system. From the repository root, run:

```sh
lake exe cache get
lake --wfail build
```

The default build includes `IdealCompletion` and the separate
`IdealCompletionExamples` and `IdealCompletionPrimeIdealExamples` targets.
Examples are not imported by the public library. Fetch the matching mathlib
cache again after replacing `.lake`
or changing the pinned toolchain/dependencies; do not silently rebuild mathlib
from source when cache retrieval fails.

The root [formalization.yaml](formalization.yaml) uses format v0.4. With the
upstream `check-jsonschema` command available, validate it against the pinned
v0.4 schema:

```sh
check-jsonschema --schemafile https://raw.githubusercontent.com/mathlib-initiative/formalization.yaml/99c678e569c7c4c0772db297c5ddd5e4c9b6322e/schema/v0.4.schema.json formalization.yaml
```

### Initial resource baseline

On 2026-09-25, in a Linux x86-64 container with a 23 GiB memory limit, Lean
4.34.0-rc2 and the committed dependency pins, a clean compilation of the three
then-shipped ideal-completion modules took 5.01 seconds after the dependencies
were available from the matching mathlib cache. The subsequent no-target default
check took 1.50 seconds; an external public-import client took 2.01 seconds.
These are single local
measurements with warm dependency and filesystem caches, not cold-download or
whole-mathlib-build estimates. Timing includes the recorder's roughly 0.5-second
sampling granularity. No speedup or cross-machine guarantee is claimed.

## Mathematical references and credit

The construction is classical order theory. A motivating account is Kazuhiro
Fujiwara and Fumiharu Kato, *Foundations of Rigid Geometry I*,
[arXiv:1308.4734v5](https://arxiv.org/abs/1308.4734v5), Chapter 0, §2.2(b),
the paragraph after Definition 2.2.6 (printed page 38). Its "finite elements"
are the order-theoretic compact elements used here. Definition 2.2.7 of the same
account motivates the prime-ideal/Boolean-map construction in the distributive
setting; this library's two-sided bounded-lattice correspondence does not require
distributivity. This library gives reusable Lean proofs using mathlib's existing
order ideals, prime ideals and compactness notions;
detailed source correspondence and coverage remain outside this repository.

Authors: Formal Frontier Agents. The mathematical core was developed by the
Formal Frontier Anchor AI agent; another AI contributor prepared the modules
and examples. Anchor also prepared the generated-reference adapter and packaging.
Independent AI agents reviewed the formalization. No human peer review or
source-author endorsement is claimed.

Lean and mathlib provide the proof infrastructure and underlying mathematical
definitions. Their authors retain their respective credit and licenses. Unless
otherwise stated in a file, original code here is licensed under the
[Apache License 2.0](LICENSE).

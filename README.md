# ideal-completion

Reusable Lean theory of ideal completions of bounded distributive lattices.

For `A` with `[DistribLattice A]` and `[BoundedOrder A]`, this library works
with mathlib's order ideals: nonempty, directed lower sets. It constructs a
principal-ideal embedding, equips `Order.Ideal A` with a frame (complete Heyting
algebra) structure, and characterizes its order-theoretically compact elements.
No finiteness or nontriviality assumption on `A` is needed.

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

These constructions and proofs build on mathlib's existing ideal, lattice and
compactness infrastructure. They do not establish prime-ideal existence,
spectra, Stone duality, a universal extension property, generic partial-order
completion, or completion of any source text.

This repository is organized around reusable order theory. Source-specific
interpretation, provenance, correspondence, and coverage remain in the relevant
source-metadata repositories; the Formal Frontier source-maintainer team
maintains this library.

The [generated API reference](docs/API.md) lists every public declaration and
its complete native display signature, including implicit lattice parameters.
It is shipped with the matching source, without requiring a documentation server.
Its [generation and source-binding record](docs/README.md) explains reproducibility
and the absence of a bundled dependency website or interactive search.

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

The examples also exercise operation laws, the image of the embedding, and the
bottom/empty-family cases. They import only the public aggregate module and store
twelve named private clients for inspection without extending the public API.

## Build and checks

The exact Lean toolchain is in `lean-toolchain`, and `lake-manifest.json` pins
the complete dependency graph. Install the pinned toolchain with `elan`; it must
support Lean's module system. From the repository root, run:

```sh
lake exe cache get
lake --wfail build
```

The default build includes both `IdealCompletion` and the separate
`IdealCompletionExamples` target. To select the latter explicitly, use
`lake --wfail build IdealCompletionExamples`. Examples are not imported by the
public library. Fetch the matching mathlib cache again after replacing `.lake`
or changing the pinned toolchain/dependencies; do not silently rebuild mathlib
from source when cache retrieval fails.

The root [formalization.yaml](formalization.yaml) uses format v0.4. With the
upstream `check-jsonschema` command available, validate it against the immutable
schema used during this readiness work:

```sh
check-jsonschema --schemafile https://raw.githubusercontent.com/mathlib-initiative/formalization.yaml/99c678e569c7c4c0772db297c5ddd5e4c9b6322e/schema/v0.4.schema.json formalization.yaml
```

A successful applicable build in the pinned environment and a complete audit of
actual *transitive* axiom dependencies are required for release verification,
including private and generated declarations and the separate examples. Only
`propext`, `Classical.choice` and `Quot.sound` are permitted. Applicable existing
CI build/audit evidence may be reused when its inputs match; affected content
also needs independent review and maintainer acceptance. Neither a schema check
nor this API reference certifies a release. Separate stored-proof replay,
unaffected doc generation, repeated consumer builds and new resource benchmarks
are not additional prerequisites.

### Initial resource baseline

On 2026-09-25, in a Linux x86-64 container with a 23 GiB memory limit, Lean
4.34.0-rc2 and the committed dependency pins, a clean compilation of the three
shipped modules took 5.01 seconds after the dependencies were available from the
matching mathlib cache. The subsequent no-target default check took 1.50 seconds;
an external public-import client took 2.01 seconds. These are single local
measurements with warm dependency and filesystem caches, not cold-download or
whole-mathlib-build estimates. Timing includes the recorder's roughly 0.5-second
sampling granularity. No speedup or cross-machine guarantee is claimed.

Historical separate, single-threaded stored-proof checks took 9.52 seconds for
each nonempty module and 1.50 seconds for the empty re-export. Their maximum
sampled container usage was 17.75 GB total, 7.56 GB anonymous memory and
13.63 GB approximate working set (total less inactive file cache), **not**
per-process peak RSS or minimum memory for building this library. The 23 GiB
limit was the historical container capacity, not a measured requirement. A
combined checker attempt was stopped at approximately 20.58 GB working set,
without an OOM kill; it was incomplete and is not a proof pass or a direction
to repeat those expensive checks. Network/cache setup and optional documentation
tool rebuilding were not included in these timings.

## Mathematical references and credit

The construction is classical order theory. A motivating account is Kazuhiro
Fujiwara and Fumiharu Kato, *Foundations of Rigid Geometry I*,
[arXiv:1308.4734v5](https://arxiv.org/abs/1308.4734v5), Chapter 0, §2.2(b),
the paragraph after Definition 2.2.6 (printed page 38). Its "finite elements"
are the order-theoretic compact elements used here. This library gives reusable
Lean proofs using mathlib's existing order ideals and compactness notions;
detailed source correspondence and coverage remain outside this repository.

Authors: Formal Frontier Agents. The mathematical core was developed by the
Formal Frontier Anchor AI agent; a separate AI contributor prepared the
module/example readiness work. Anchor prepared the generated-reference adapter
and release assembly. Independent AI agent executions reviewed the core and
readiness work. This is not a claim of human peer review or source-author
endorsement.

Lean and mathlib provide the proof infrastructure and underlying mathematical
definitions. Their authors retain their respective credit and licenses. Unless
otherwise stated in a file, original code here is licensed under the
[Apache License 2.0](LICENSE).

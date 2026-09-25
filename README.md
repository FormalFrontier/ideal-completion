# ideal-completion

Reusable Lean theory of ideal completions of bounded distributive lattices.

The API equips the order ideals of a bounded distributive lattice with
their frame (complete Heyting algebra) structure. It bundles the principal-ideal
embedding as a bounded lattice homomorphism and identifies the compact elements
of the ideal completion exactly with the principal ideals. Consequently, ideal
completions are compactly generated. Here an ideal is mathlib's nonempty directed
lower set, and "compact element" is an order-theoretic condition, not finiteness
of the ideal's underlying set. No nontriviality assumption is imposed on the
lattice.

The scope of this library does not assert completion of a source text. Prime
ideals, Stone duality, spectra and a universal extension property for maps out of
the completion are not provided by this library.

This repository is organized around reusable order theory. Source-specific
interpretation, provenance, correspondence, and coverage remain in the relevant
source-metadata repositories. Anchor is responsible for the initial integration
on behalf of the source-maintainer team.

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

A successful ordinary build or metadata validation is not release acceptance.
Release verification must additionally audit every shipped mathematical
declaration, including private and generated declarations and examples, and
separately recheck stored proof terms with a compatible checker. It must also
cover selected linters, generated API documentation, complete semantic review
and measured build/client resource baselines. Author verification evidence and
the generated API reference require applicable independent review; neither alone
is a release decision. The metadata records revision-specific review history,
which does not itself assert publication or approval of later revisions.

### Initial resource baseline

On 2026-09-25, in a Linux x86-64 container with a 23 GiB memory limit, Lean
4.34.0-rc2 and the committed dependency pins, a clean compilation of the three
shipped modules took 5.01 seconds after the dependencies were available from the
matching mathlib cache. The subsequent no-target default check took 1.50 seconds;
an external public-import client took 2.01 seconds. These are single local
measurements with warm dependency and filesystem caches, not cold-download or
whole-mathlib-build estimates. Timing includes the recorder's roughly 0.5-second
sampling granularity. No speedup or cross-machine guarantee is claimed.

The separate, single-threaded stored-proof checks took 9.52 seconds for each
nonempty module and 1.50 seconds for the empty re-export. Their maximum sampled
container usage was 17.75 GB total, 7.56 GB anonymous memory and 13.63 GB approximate
working set (total less inactive file cache); these are not per-process peak RSS
measurements. A combined checker attempt was stopped at approximately 20.58 GB
working set, without an OOM kill. Run the complete proof checks one target at a
time with adequate headroom; do not use that incomplete combined attempt as a
proof pass. Network/cache setup and rebuilding the optional documentation tool
are additional costs not included in these timings.

## Mathematical references and credit

The construction is classical order theory. A motivating account is Kazuhiro
Fujiwara and Fumiharu Kato, *Foundations of Rigid Geometry I*,
[arXiv:1308.4734v5](https://arxiv.org/abs/1308.4734v5), Chapter 0, §2.2(b),
the paragraph after Definition 2.2.6 (printed page 38). Its "finite elements"
are the order-theoretic compact elements used here. This library gives reusable
Lean proofs using mathlib's existing order ideals and compactness notions;
detailed source correspondence and coverage remain outside this repository.

Authors: Formal Frontier Agents. The mathematical core was developed by
Formal Frontier's Anchor AI agent, with
fresh-context review of the mathematical core by a separate Formalization
Worker A execution. The module/example readiness repair was contributed by
Formalization Worker B (Task `hive-request-f6e376d59317bb90c8b4e22bcab97f93cace7484`,
UID `1f6cb9cb-b67e-43df-82c0-f0ea17d39104`, commit
`929377cd6c3ec229e886286c6eb33f3837e776c5`), independently reviewed by a fresh
Worker A execution. Anchor prepared the generated-reference adapter and assembly.
AI agents also prepare maintenance changes and review
evidence; this is not a claim of human peer review or source-author endorsement.
The initial accepted core is commit `5626929044338bfda910936feca0ca416ab816ba`;
later changes require their own applicable review.

Lean and mathlib provide the proof infrastructure and underlying mathematical
definitions. Their authors retain their respective credit and licenses. Unless
otherwise stated in a file, original code here is licensed under the
[Apache License 2.0](LICENSE).

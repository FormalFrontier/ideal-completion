# API reference generation

[API.md](API.md) is a generated, self-contained Markdown reference for all seven
public declarations defined by this library, including both typeclass instances.
It supplies the native displayed signatures, all implicit lattice parameters,
docstrings and relative source links. The mathematical explanation and public-import
example are in the root README. Private helpers and examples still require the
complete actual transitive standard-axiom audit alongside the ordinary build;
they are not additional public API documentation. Separate stored-proof replay
is not a release prerequisite.

The reference deliberately does not ship a dependency website, JavaScript, fonts
or remotely loaded styles. It does not provide interactive search or claim to
document all of Lean/mathlib. Native pretty-printing can abbreviate names in the
source namespace. The library and its declared mathematical dependencies remain
the authoritative definitions.

## Reproduction

Use Python 3 and unchanged native doc-gen4 at
`97d4ecdfc8e09e7f511724c25e303d448de6a3db`, with its committed manifest and
Lean `v4.34.0-rc2`, in a separate checkout. Build that core-only tool with
`lake build doc-gen4`. Fetch this library's matching mathlib cache before building
the three modules, following the root README.

In this library's pinned Lake environment, run the native executable's `single`
command for each of `IdealCompletion.OrderIdeal`, `IdealCompletion` and
`Examples.IdealCompletion`. Use one fresh database and an explicit immutable
source URI ending in `/<full-source-commit>/<module-path>.lean` for each module.
For example, from this library's root, set the native executable's absolute path
and create fresh build directories **before** calling `single` (its SQLite opener
does not create the parent directory). Read the recorded source selection from
the committed manifest when reproducing this reference:

```sh
docgen_executable=/absolute/path/to/doc-gen4
docs_work=$(mktemp -d)
mkdir "$docs_work/analysis" "$docs_work/rendered"
source_revision=$(python3 -c 'import json; print(json.load(open("docs/api-manifest.json"))["analyzed_source_revision"])')
for module in IdealCompletion.OrderIdeal IdealCompletion Examples.IdealCompletion; do
  module_path=${module//.//}
  lake env "$docgen_executable" single --build "$docs_work/analysis" "$module" api.db "https://github.com/FormalFrontier/ideal-completion/blob/$source_revision/$module_path.lean"
done
```

The loop uses Bash. Then render the three analyzed records:

```sh
lake env "$docgen_executable" bibPrepass --build "$docs_work/rendered" --none
lake env "$docgen_executable" fromDb --build "$docs_work/rendered" --manifest "$docs_work/rendered/manifest.json" "$docs_work/analysis/api.db"
python3 scripts/generate_api.py --native-data "$docs_work/rendered/doc-data" --source-revision "$source_revision" --check
```

For a new generation, use the actual full source commit and omit `--check` after
the native commands; never use a mutable branch name. The pinned native GitHub
linker adds `#Lstart-Lend`. The adapter requires the exact repository/commit/path,
a canonical positive line range, a start equal to native `info.line`, and an end
within the matching source file. It does not accept an arbitrary suffix match.
Do not treat an unpublished URL as verified remote availability.
Source hyperlinks in the distributed Markdown instead resolve to the source
shipped alongside it. Run these commands in this project's `lake env`; the tested
native executable carries its own implementation while resolving the documented
library's imports in that environment. Preserve both projects' resolved pins and
record the effective search path. Do not change the mathematical pins to install
the documentation tool. Native generator warnings are findings, not silent passes.

The adapter reads all three native module records and rejects missing/duplicate/
unexpected public names, source-revision or source/pin drift, missing docstrings,
missing implicit lattice parameters and malformed headers. It retains every
header text token, normalizing whitespace only. Native records and command
receipts must be checked independently: this adapter is not an attestation that
input JSON was genuinely produced by doc-gen4, nor a kernel or release checker.

`api-manifest.json` records the exact analyzed revision, all three source hashes,
toolchain/Lake configuration/manifest hashes, native-record hashes and generated
reference hash. If a later candidate changes only documentation, identical
source/pin hashes make that exact-input correspondence inspectable, subject to
affected prose and link review. If sources or pins change, reassess affected
signatures and navigation: the adapter's `--check` cannot certify changed inputs
against the old manifest. An honestly labeled historical reference may remain
bound to its exact analyzed inputs, with reviewed current navigation where
appropriate; regenerate natively when needed to represent a changed current
API accurately. Unrelated source changes alone do not mandate expensive native
regeneration. Never relabel old native output as new, silently retarget source
line links, or use the absent-Git-object fallback on a source/hash mismatch.

Public releases have independent Git ancestry, so the recorded development
commit may be absent. When it is present, the adapter checks the sources against
that exact Git object and never falls back on a source mismatch. Only an explicit
Git `missing` result, or a source-only library tree with no `.git` marker, permits
the manifest path; repository/command failures and non-commit objects refuse.
The manifest path requires the committed manifest's exact
recorded revision, module/tool selection and all six source/pin hashes. This
permits reproduction in a public-lineage or source-only checkout without access
to internal Git history; it does not authenticate untrusted JSON or prove that
the referenced GitHub URL exists. Changing source/pins while the Git object is
absent fails closed and requires new reviewed generation evidence.

The generated reference copies this project's Apache-2.0 docstrings and native
displayed mathematical signatures. No third-party implementation, docstring,
stylesheet or JavaScript asset is bundled by this adapter. Lean/mathlib and
doc-gen4 retain their respective authorship; using their tools is not independent
release approval. The precise artifact and provenance remain subject to review.

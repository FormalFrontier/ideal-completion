# API reference generation

[API.md](API.md) begins with a human-maintained scope notice; the unchanged
generated payload below it is a historical, self-contained Markdown reference
for the seven public ideal-completion declarations at its recorded source
revision, including both typeclass instances. The manifest's `api_sha256`
hashes the bytes beginning at `# Generated API reference`, excluding the notice.
The payload does not document `IdealCompletion.PrimeIdeal` or the current
aggregate module. The
[prime-ideal guide](PrimeIdeals.md) covers that newer interface without claiming
native generated signatures.

The reference supplies native displayed signatures, implicit lattice parameters,
docstrings and relative source links for its analyzed revision. Its links to
`IdealCompletion.OrderIdeal` refer to unchanged source, whereas its aggregate-module
link and recorded Lake configuration predate the additional prime-ideal import and
target. The mathematical explanation and public-import example are in the root
README. Private helpers and examples still require the
complete actual transitive standard-axiom audit alongside the ordinary build;
they are not additional public API documentation. Separate stored-proof replay
is not a release prerequisite.

The reference deliberately does not ship a dependency website, JavaScript, fonts
or remotely loaded styles. It does not provide interactive search or claim to
document all of Lean/mathlib. Native pretty-printing can abbreviate names in the
source namespace. The library and its declared mathematical dependencies remain
the authoritative definitions.

## Reproduction

To reproduce the **shipped historical payload**, use a clean, disposable checkout
of this library at `3359d255c9831e0806ca6fe8c86ce6a327783f64`, not this
checkout's current sources or Lake inputs. The six source/pin files in that
checkout must match [the shipped manifest](api-manifest.json). Use Python 3 and
unchanged native doc-gen4 at `97d4ecdfc8e09e7f511724c25e303d448de6a3db`,
with its committed manifest and Lean `v4.34.0-rc2`, in a separate checkout;
build that core-only tool with `lake build doc-gen4`. Verify both checkouts'
exact revisions. If the historical source commit is unavailable, the native
reproduction cannot be claimed from the current checkout alone.

Before native generation, verify the historical library checkout against the
shipped manifest (replace the absolute-path placeholders). Run the following
blocks in the same Bash session:

```sh
set -e
reference_checkout=/absolute/path/to/checkout/with/shipped/reference
historical_checkout=/absolute/path/to/disposable/checkout/at/3359d255c9831e0806ca6fe8c86ce6a327783f64
docgen_checkout=/absolute/path/to/doc-gen4/at/97d4ecdfc8e09e7f511724c25e303d448de6a3db
source_revision=3359d255c9831e0806ca6fe8c86ce6a327783f64
test "$(git -C "$historical_checkout" rev-parse HEAD)" = "$source_revision"
test -z "$(git -C "$historical_checkout" status --porcelain)"
test "$(git -C "$docgen_checkout" rev-parse HEAD)" = 97d4ecdfc8e09e7f511724c25e303d448de6a3db
python3 - "$reference_checkout" "$historical_checkout" <<'PY'
import hashlib, json, sys
from pathlib import Path

reference, historical = (Path(path) for path in sys.argv[1:])
manifest = json.loads((reference / 'docs/api-manifest.json').read_bytes())
if manifest['analyzed_source_revision'] != '3359d255c9831e0806ca6fe8c86ce6a327783f64':
    raise SystemExit('wrong historical source revision')
for path, expected in manifest['inputs'].items():
    if hashlib.sha256((historical / path).read_bytes()).hexdigest() != expected:
        raise SystemExit('source or pin drift: ' + path)
PY
```

In the historical library checkout, fetch the matching mathlib cache before
building the three modules; do not rebuild mathlib from source if the cache
fails. Run doc-gen4's `single` on those exact historical imports using one
fresh database and source URIs at the analyzed revision. Create the directories
**before** calling `single` (its SQLite opener does not create the parent):

```sh
(cd "$docgen_checkout" && lake build doc-gen4)
docgen_executable="$docgen_checkout/.lake/build/bin/doc-gen4"
docs_work=$(mktemp -d)
mkdir "$docs_work/analysis" "$docs_work/rendered"
cd "$historical_checkout"
lake exe cache get
lake build +IdealCompletion.OrderIdeal +IdealCompletion +Examples.IdealCompletion
for module in IdealCompletion.OrderIdeal IdealCompletion Examples.IdealCompletion; do
  module_path=${module//.//}
  lake env "$docgen_executable" single --build "$docs_work/analysis" "$module" api.db "https://github.com/FormalFrontier/ideal-completion/blob/$source_revision/$module_path.lean"
done
```

The loop uses Bash. Render the three analyzed records with the **historical**
checkout's adapter, without `--check`:

```sh
lake env "$docgen_executable" bibPrepass --build "$docs_work/rendered" --none
lake env "$docgen_executable" fromDb --build "$docs_work/rendered" --manifest "$docs_work/rendered/manifest.json" "$docs_work/analysis/api.db"
python3 scripts/generate_api.py --native-data "$docs_work/rendered/doc-data" --source-revision "$source_revision"
```

That historical checkout originally committed documentation for a *different*
source revision; its unmodified `docs/api-manifest.json` is not the shipped
reference, so running `--check` there against those old files is not a valid
comparison. Instead, compare the newly generated historical output to the
shipped generated payload and the shipped manifest byte-for-byte:

```sh
python3 - "$reference_checkout" "$historical_checkout" <<'PY'
import hashlib, json, sys
from pathlib import Path

reference, historical = (Path(path) for path in sys.argv[1:])
page = (reference / 'docs/API.md').read_bytes()
marker = b'# Generated API reference\n\n'
if page.count(marker) != 1:
    raise SystemExit('historical payload marker missing or duplicated')
payload = marker + page.split(marker, 1)[1]
manifest = (reference / 'docs/api-manifest.json').read_bytes()
if hashlib.sha256(payload).hexdigest() != json.loads(manifest)['api_sha256']:
    raise SystemExit('shipped historical payload hash differs')
if (historical / 'docs/API.md').read_bytes() != payload:
    raise SystemExit('regenerated payload differs from shipped payload')
if (historical / 'docs/api-manifest.json').read_bytes() != manifest:
    raise SystemExit('regenerated manifest differs from shipped manifest')
PY
```

The historical adapter is used to reproduce the unchanged hashed payload; the adapter
in this checkout corrects the opening for any *new* generation, so it is not a
byte-for-byte reproducer of the old payload. For new generation, select the
actual full source commit and verify its complete input set first; the
seven-declaration adapter cannot document new public declarations in the
current aggregate. Never use a mutable branch name. The pinned native GitHub
linker adds `#Lstart-Lend`. The adapter requires the exact repository/commit/path,
a canonical positive line range, a start equal to native `info.line`, and an end
within the matching source file. It does not accept an arbitrary suffix match.
Do not treat an unpublished URL as verified remote availability.
Source hyperlinks in the distributed Markdown instead resolve to the source
shipped alongside it. Run these commands in the **historical checkout's**
`lake env`; the native executable carries its own implementation while resolving
that historical library's imports. Preserve both projects' resolved pins and
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
payload hash (not the human-maintained notice). If a later candidate changes
only documentation, identical source/pin hashes make that exact-input
correspondence inspectable, subject to
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

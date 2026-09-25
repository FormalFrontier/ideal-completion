# SPDX-License-Identifier: Apache-2.0
# Authors: Formal Frontier Agents
"""Bounded data-only controls; actual native records are checked separately."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import generate_api as api

REV = "a" * 40


def fixture():
    records = {m: dict(name=m, declarations=[]) for m in api.MODULES}
    for i, (name, kind) in enumerate(api.EXPECTED.items(), 1):
        header = (f'<div class="decl_header"><span class="decl_kind">{kind}</span> '
                  f'<span class="decl_name">{name}</span> '
                  '<span>{A : Type u} [DistribLattice A] [BoundedOrder A]</span> :'
                  '<div class="decl_type">A → A</div></div>')
        records[api.MODULES[0]]["declarations"].append(dict(header=header, info=dict(
            name=name, kind=kind, doc="Fixture only; not a claimed Lean declaration.",
            line=i, sourceLink=api.GITHUB_SOURCE + REV + f"/IdealCompletion/OrderIdeal.lean#L{i}-L{i+1}",
            docLink="./IdealCompletion/OrderIdeal.html#" + name)))
    sources = {p: b"fixture\n" * 20 for p in api.INPUTS}
    return records, sources


class Controls(unittest.TestCase):
    def test_all_seven_and_binding(self):
        records, sources = fixture()
        raw, manifest = api.render(records, REV, sources)
        facts = json.loads(manifest)
        self.assertEqual(raw.count(b"\n## Order.Ideal."), 7)
        self.assertEqual(facts["api_sha256"], api.digest(raw))
        self.assertEqual(set(facts["inputs"]), set(api.INPUTS))
        self.assertNotIn(b"example.invalid", raw + manifest)
        self.assertFalse(facts["proof_certification"])

    def test_implicit_arguments_and_entities_retained(self):
        header = api.Header('<div><span>{A : Type u} [DistribLattice A] '
                            '[BoundedOrder A]</span> :<div class="decl_type">'
                            'x &lt; y ∧ x ≤ y</div></div>')
        self.assertEqual(header.rendered(),
                         '{A : Type u} [DistribLattice A] [BoundedOrder A] : x < y ∧ x ≤ y')

    def test_no_whitespace_inside_name_added(self):
        self.assertEqual(api.Header('<span><span>Order</span>.<span>Ideal</span></span>').rendered(),
                         'Order.Ideal')

    def test_refuse_corruptions(self):
        mutations = [
            lambda r: r.pop(api.MODULES[1]),
            lambda r: r[api.MODULES[0]]["declarations"].pop(),
            lambda r: r[api.MODULES[0]]["declarations"].append(copy.deepcopy(r[api.MODULES[0]]["declarations"][0])),
            lambda r: r[api.MODULES[1]]["declarations"].append(copy.deepcopy(r[api.MODULES[0]]["declarations"][0])),
            lambda r: r[api.MODULES[0]].update(name="Wrong"),
        ]
        for key, value in [("name", "Wrong"), ("kind", "axiom"), ("doc", ""),
                           ("line", 0), ("line", 999), ("line", True),
                           ("sourceLink", "https://example.invalid/main/x.lean"),
                           ("docLink", "wrong"), ("doc", "```inject")]:
            mutations.append(lambda r, k=key, v=value: r[api.MODULES[0]]["declarations"][0]["info"].update({k: v}))
        mutations += [
            lambda r: r[api.MODULES[0]]["declarations"][0].update(header="<script>bad</script>"),
            lambda r: r[api.MODULES[0]]["declarations"][0].update(header="<div><span></div>"),
            lambda r: r[api.MODULES[0]]["declarations"][0].update(header="<span onclick='bad'>x</span>"),
            lambda r: r[api.MODULES[0]]["declarations"][0].update(header=r[api.MODULES[0]]["declarations"][0]["header"].replace("[BoundedOrder A]", "")),
        ]
        for i, mutate in enumerate(mutations):
            with self.subTest(control=i):
                records, sources = fixture()
                mutate(records)
                with self.assertRaises(ValueError):
                    api.render(records, REV, sources)

    def test_revision_and_inventory(self):
        records, sources = fixture()
        for rev in ["main", "a" * 39, "-" * 40]:
            with self.assertRaises(ValueError):
                api.render(records, rev, sources)
        sources.pop("lean-toolchain")
        with self.assertRaises(ValueError):
            api.render(records, REV, sources)

    def test_source_url_and_range_refusals(self):
        records, sources = fixture()
        valid = records[api.MODULES[0]]["declarations"][0]["info"]["sourceLink"]
        changes = [valid.replace("github.com", "github.com.evil.invalid"),
                   valid.replace("https://", "http://"),
                   valid.replace("/ideal-completion/", "/other/"),
                   valid.replace(REV, "b" * 40),
                   valid.replace("/OrderIdeal.lean", "/Other.lean"),
                   valid.split("#")[0], valid + "?query=1", valid + "\n",
                   valid.replace("#L1-L2", "#L2-L3"),
                   valid.replace("#L1-L2", "#L1-L0"),
                   valid.replace("#L1-L2", "#L1-L999"),
                   valid.replace("#L1-L2", "#L01-L2"),
                   valid.replace("#L1-L2", "#L1"),
                   valid.replace("#L1-L2", "#L1-L2#extra")]
        for value in changes:
            with self.subTest(value=value):
                altered = copy.deepcopy(records)
                altered[api.MODULES[0]]["declarations"][0]["info"]["sourceLink"] = value
                with self.assertRaises(ValueError): api.render(altered, REV, sources)

    def test_manifest_source_binding(self):
        records, sources = fixture()
        _, raw = api.render(records, REV, sources)
        manifest = json.loads(raw)
        api.manifest_source_binding(manifest, REV, sources)
        for key, value in [("format", 2), ("format", True), ("docgen_revision", "b" * 40),
                           ("analyzed_source_revision", "b" * 40),
                           ("modules", list(api.MODULES[:-1])), ("inputs", {})]:
            altered = dict(manifest, **{key: value})
            with self.subTest(key=key), self.assertRaises(ValueError):
                api.manifest_source_binding(altered, REV, sources)
        for path in api.INPUTS:
            with self.subTest(path=path), self.assertRaises(ValueError):
                api.manifest_source_binding(manifest, REV, dict(sources, **{path: b"changed"}))

    def test_git_absence_is_not_git_failure(self):
        with tempfile.TemporaryDirectory(prefix="ideal-api-git-") as temp:
            root = Path(temp)
            self.assertFalse(api.git_source_available(root, REV))
            (root / ".git").write_text("invalid worktree marker\n")
            with self.assertRaisesRegex(ValueError, "refusing fallback"):
                api.git_source_available(root, REV)
            (root / ".git").unlink()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            self.assertFalse(api.git_source_available(root, REV))


if __name__ == "__main__":
    unittest.main()

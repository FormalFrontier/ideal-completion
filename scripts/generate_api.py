#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Authors: Formal Frontier Agents
"""Generate this library's Markdown API from pinned native doc-gen4 records.

This is a deliberately seven-declaration adapter, not a general documentation
certifier, a Lean parser, or a proof check. Native generation receipts remain
separate review evidence. See docs/README.md for the reproduction contract.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess

TOOL = "97d4ecdfc8e09e7f511724c25e303d448de6a3db"
MODULES = ("IdealCompletion.OrderIdeal", "IdealCompletion", "Examples.IdealCompletion")
INPUTS = tuple(m.replace(".", "/") + ".lean" for m in MODULES) + (
    "lean-toolchain", "lakefile.toml", "lake-manifest.json")
EXPECTED = {
    "Order.Ideal.principalHom": "def",
    "Order.Ideal.principalHom_injective": "theorem",
    "Order.Ideal.mem_sSup_iff": "theorem",
    "Order.Ideal.instFrame_idealCompletion": "instance",
    "Order.Ideal.isCompactElement_principal": "theorem",
    "Order.Ideal.isCompactElement_iff_eq_principal": "theorem",
    "Order.Ideal.instIsCompactlyGenerated_idealCompletion": "instance",
}
GITHUB_SOURCE = "https://github.com/FormalFrontier/ideal-completion/blob/"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def source_range(info, revision, path, sources):
    """Validate the pinned native GitHub linker, not remote URL availability."""
    line_count = len(sources[path].splitlines())
    require(type(info["line"]) is int and 0 < info["line"] <= line_count,
            "invalid native source line")
    expected = GITHUB_SOURCE + revision + "/" + path
    match = re.fullmatch(re.escape(expected) + r"#L([1-9][0-9]*)-L([1-9][0-9]*)",
                         info["sourceLink"])
    require(match is not None, "native GitHub source URI or range differs")
    start, end = map(int, match.groups())
    require(start == info["line"] and start <= end <= line_count,
            "native GitHub range disagrees with source line/bounds")


def manifest_source_binding(manifest, revision, sources):
    """Reproduction without development ancestry; metadata is not an attestation."""
    require(type(manifest.get("format")) is int and manifest["format"] == 1
            and manifest.get("docgen_revision") == TOOL,
            "unsupported provenance manifest")
    require(manifest.get("analyzed_source_revision") == revision and
            manifest.get("modules") == list(MODULES), "manifest source selection differs")
    require(manifest.get("inputs") == {p: digest(sources[p]) for p in sorted(INPUTS)},
            "source/pin drift from recorded manifest")


def git_source_available(root, revision):
    """Only a source-only tree or Git's explicit missing result permits fallback."""
    marker = root / ".git"
    if not marker.exists() and not marker.is_symlink():
        return False
    probe = subprocess.run(["git", "--no-replace-objects", "cat-file", "--batch-check"],
                           input=(revision + "\n").encode(), cwd=root,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(probe.returncode == 0, "cannot inspect selected Git object; refusing fallback")
    line = probe.stdout.decode().strip()
    if line == revision + " missing":
        return False
    require(re.fullmatch(re.escape(revision) + r" commit [0-9]+", line) is not None,
            "selected Git object is not a commit")
    return True


class Header(HTMLParser):
    """Keep all visible text, including every implicit argument; discard markup."""

    def __init__(self, value):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.text = []
        self.kinds = []
        self.names = []
        self.feed(value)
        self.close()
        require(not self.stack, "unclosed native header")

    def handle_starttag(self, tag, attrs):
        require(tag in {"div", "span", "a"}, "unexpected native header tag")
        attrs = dict(attrs)
        require(not any(k.startswith("on") for k in attrs), "active header attribute")
        if tag == "div" and "decl_type" in attrs.get("class", "").split():
            self.text.append(" ")
        self.stack.append((tag, set(attrs.get("class", "").split())))

    def handle_endtag(self, tag):
        require(bool(self.stack) and self.stack[-1][0] == tag, "unbalanced native header")
        self.stack.pop()

    def handle_data(self, value):
        require(bool(self.stack) or not value.strip(), "text outside native header")
        self.text.append(value)
        if any("decl_kind" in classes for _, classes in self.stack):
            self.kinds.append(value)
        if any("decl_name" in classes for _, classes in self.stack):
            self.names.append(value)

    def handle_comment(self, _):
        raise ValueError("unexpected header comment")

    def handle_decl(self, _):
        raise ValueError("unexpected header declaration")

    def rendered(self):
        # Whitespace alone is normalized; all tokens and implicit binders remain.
        return " ".join("".join(self.text).split())


def render(records, revision, sources):
    require(re.fullmatch(r"[0-9a-f]{40}", revision) is not None, "full source revision required")
    require(set(records) == set(MODULES), "shipped module records differ")
    require(set(sources) == set(INPUTS), "source/pin inventory differs")
    rows = []
    found = {}
    for module in MODULES:
        record = records[module]
        require(record["name"] == module, "native module name differs")
        for row in record["declarations"]:
            info = row["info"]
            name, kind = info["name"], info["kind"]
            require(module == MODULES[0], "unexpected public declaration in re-export/examples")
            require(name in EXPECTED and EXPECTED[name] == kind, "unexpected public name/kind")
            require(name not in found, "duplicate public declaration")
            path = module.replace(".", "/") + ".lean"
            source_range(info, revision, path, sources)
            require(info["docLink"] == "./" + module.replace(".", "/") + ".html#" + name,
                    "native self link differs")
            header = Header(row["header"])
            require("".join(header.names) == name and "".join(header.kinds) == kind,
                    "native header identity differs")
            text = header.rendered()
            require("{A : Type u}" in text and "[DistribLattice A]" in text
                    and "[BoundedOrder A]" in text, "implicit assumptions absent")
            require("```" not in text and "```" not in info["doc"], "unsupported Markdown fence")
            require(bool(info["doc"].strip()), "public docstring absent")
            found[name] = kind
            rows.append(dict(name=name, kind=kind, header=text,
                             doc=info["doc"].strip(), path=path, line=info["line"]))
    require(found == EXPECTED, "missing public declaration")
    rows.sort(key=lambda row: row["line"])
    lines = ["# Generated API reference", "",
             "This reference covers every public declaration defined by ideal-completion.",
             "Import `IdealCompletion`; its leaf is `IdealCompletion.OrderIdeal`.",
             "`Examples.IdealCompletion` contains private checked clients, not additional public API.", "",
             "Headers below are native doc-gen4 display signatures, not complete declarations",
             "with proof bodies. Short mathematical names use the source's `Order.Ideal`",
             "namespace and imports. All implicit lattice parameters are displayed; `u` is",
             "an arbitrary universe. Source links are relative to this same checkout.", "",
             "The source/pin hashes and generation provenance are in [api-manifest.json](api-manifest.json).",
             "See [generation instructions](README.md) and the [mathematical overview](../README.md).", ""]
    for row in rows:
        lines += ["## " + row["name"], "", "```lean", row["header"], "```", "",
                  row["doc"], "", f"[Source](../{row['path']}#L{row['line']}) (line {row['line']}).", ""]
    markdown = "\n".join(lines).encode()
    manifest = dict(format=1, generator="scripts/generate_api.py", docgen_revision=TOOL,
                    analyzed_source_revision=revision, modules=list(MODULES),
                    inputs={p: digest(sources[p]) for p in sorted(sources)},
                    public_declarations=[r["name"] for r in rows],
                    native_record_sha256={m: digest(json.dumps(records[m], sort_keys=True).encode())
                                          for m in MODULES},
                    api_sha256=digest(markdown), proof_certification=False)
    return markdown, (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--native-data", type=Path, required=True,
                   help="native fromDb output doc-data directory")
    p.add_argument("--source-revision", required=True)
    p.add_argument("--check", action="store_true", help="compare, never write")
    args = p.parse_args()
    require(re.fullmatch(r"[0-9a-f]{40}", args.source_revision) is not None,
            "full source revision required")
    root = Path(__file__).resolve().parent.parent
    sources = {path: (root / path).read_bytes() for path in INPUTS}
    # A public release has independent ancestry: its analyzed development commit
    # need not be present. Prefer the exact Git object when available, otherwise
    # require the already committed complete source/pin manifest. Neither branch
    # attests that supplied JSON was genuinely produced by the native tool.
    if git_source_available(root, args.source_revision):
        for path, raw in sources.items():
            old = subprocess.check_output(["git", "--no-replace-objects", "show",
                                           args.source_revision + ":" + path], cwd=root)
            require(old == raw, "source/pin drift from analyzed revision: " + path)
        binding = "git-object"
    else:
        manifest = json.loads((root / "docs/api-manifest.json").read_bytes())
        manifest_source_binding(manifest, args.source_revision, sources)
        binding = "committed-source-hashes"
    records = {m: json.loads((args.native_data / ("declaration-data-" + m + ".bmp")).read_bytes())
               for m in MODULES}
    api, manifest = render(records, args.source_revision, sources)
    for name, raw in [("API.md", api), ("api-manifest.json", manifest)]:
        target = root / "docs" / name
        if args.check:
            require(target.read_bytes() == raw, "generated file differs: " + name)
        else:
            target.write_bytes(raw)
    print(json.dumps(dict(status="matched" if args.check else "generated",
                          declarations=len(EXPECTED), api_sha256=digest(api),
                          source_binding=binding, release_acceptance=False)))


if __name__ == "__main__":
    main()

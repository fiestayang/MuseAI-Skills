#!/usr/bin/env python3
"""Validate report coverage, local links, source syntax, and offline conversion."""
from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import io
import json
from pathlib import Path
import re
import runpy
import subprocess
import tempfile
from types import SimpleNamespace
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[3]
REPORTS = ROOT / "docs/analysis"
BASELINE = "61121abf5c4da12fe32ef970a861108b16a0731b"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def tracked_files() -> list[str]:
    return subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASELINE],
        cwd=ROOT, text=True,
    ).splitlines()


def validate_coverage(files: list[str]) -> dict[str, int]:
    inventory = json.loads((REPORTS / "appendices/source-inventory.json").read_text())
    check(inventory["baseline"] == BASELINE, "Inventory baseline mismatch")
    rows = inventory["files"]
    paths = [row["path"] for row in rows]
    check(len(paths) == len(set(paths)), "Duplicate inventory path")
    check(set(paths) == set(files), "Inventory does not match baseline")
    for row in rows:
        check((ROOT / row["path"]).exists(), f"Missing source: {row['path']}")
        check((ROOT / row["report"]).is_file(), f"Missing report: {row['report']}")
    coverage = (REPORTS / "appendices/file-coverage.md").read_text()
    for path in paths:
        check(coverage.count(f"| [{path}](") == 1, f"Coverage row mismatch: {path}")
    skills = [ROOT / f for f in files if f.endswith("/SKILL.md")]
    independent = [p for p in skills if not p.is_symlink()]
    for p in independent:
        key = p.parent.relative_to(ROOT / "opt/hatch/skills")
        report = REPORTS / "skills" / f"{key}.md"
        check(report.is_file(), f"Missing skill report: {key}")
        text = report.read_text()
        for section in ("scope", "flow", "design", "files", "permissions", "eval", "migration", "source"):
            check(f'id="{section}"' in text, f"Missing {section}: {key}")
    manifests = [ROOT / f for f in files if f.endswith("/manifest.yaml")]
    evals = [f for f in files if "/eval/" in f and f.endswith(".yaml")]
    stats = {"baseline_paths": len(paths), "independent_skills": len(independent),
             "skill_aliases": len(skills) - len(independent),
             "independent_manifests": sum(not p.is_symlink() for p in manifests),
             "manifest_aliases": sum(p.is_symlink() for p in manifests),
             "eval_files": len(evals)}
    check(stats == {"baseline_paths": 2658, "independent_skills": 68, "skill_aliases": 4,
                    "independent_manifests": 38, "manifest_aliases": 2, "eval_files": 12},
          f"Baseline counts changed: {stats}")
    return stats


def validate_links() -> dict[str, int]:
    count = 0
    documents = sorted(REPORTS.rglob("*.md"))
    for p in documents:
        body = p.read_text()
        check(body.endswith("\n"), f"Missing final newline: {p}")
        check(all(line == line.rstrip() for line in body.splitlines()), f"Trailing whitespace: {p}")
        link_body = re.sub(r"```.*?```|`[^`]*`", "", body, flags=re.S)
        for match in re.finditer(r"\]\(([^\s)]+)\)", link_body):
            url = match.group(1)
            if url.startswith(("http:", "https:", "mailto:", "#")):
                continue
            parsed = urlsplit(url)
            target = (p.parent / unquote(parsed.path)).resolve()
            check(target.exists(), f"Broken link: {p.relative_to(ROOT)} -> {url}")
            count += 1
            if re.fullmatch(r"L\d+", parsed.fragment):
                line = int(parsed.fragment[1:])
                check(line <= len(target.read_text().splitlines()), f"Invalid line: {url}")
    return {"markdown_documents": len(documents), "local_links": count}


def validate_syntax(files: list[str]) -> dict[str, int]:
    count = 0
    for f in files:
        if not f.startswith(("opt/hatch/runtime-cell/", "opt/hatch-image/bin/")):
            continue
        if "/npm-package/" in f or "/rtc-sidecar-lib/" in f:
            continue
        p = ROOT / f
        if p.is_symlink():
            continue
        with p.open("rb") as fh:
            head = fh.readline(160)
        if head.startswith(b"#!") and (b"/sh" in head or b"bash" in head):
            shell = "bash" if b"bash" in head else "sh"
            subprocess.run([shell, "-n", str(p)], check=True, capture_output=True)
            count += 1
    ast.parse((ROOT / "opt/hatch-image/bin/convert-cell-intent").read_text())
    ast.parse(Path(__file__).read_text())
    return {"shell_syntax_files": count, "python_syntax_files": 2}


def validate_converter() -> dict[str, int]:
    source = ROOT / "opt/hatch-image/bin/convert-cell-intent"
    api = runpy.run_path(str(source), run_name="report_offline_fixture")
    with tempfile.TemporaryDirectory(prefix="muse-analysis-") as tmp:
        root = Path(tmp)
        old = root / "old"
        status = old / api["DPKG_STATUS_REL"]
        status.parent.mkdir(parents=True)
        status.write_text(
            "Package: base\nVersion: 2\nStatus: install ok installed\n\n"
            "Package: extra\nVersion: 3\nStatus: hold ok installed\n\n"
            "Package: removed\nVersion: 1\nStatus: deinstall ok config-files\n\n"
            "Version: 99\nStatus: install ok installed\n\n"
            "Package: minimal\n"
        )
        entries = api["parse_dpkg_status"](status)
        check(len(entries) == 4, "Parser must skip unnamed stanzas")
        check(entries[-1] == ("minimal", "", ""), "Missing fields contract changed")
        base = root / "base.txt"
        base.write_text("# baseline\nbase 1\n")
        out = root / "out"
        args = SimpleNamespace(old_rootfs=old, base_manifest=base, out=out)
        with contextlib.redirect_stderr(io.StringIO()):
            api["cmd_convert"](args)
            ledger = out / api["LEDGER"]
            content = ledger.read_text()
            check(json.loads(content)["pkgs"] == ["extra"], "Package-name difference mismatch")
            check((out / api["DONE_MARKER"]).is_file(), "Missing done marker")
            check("removed 1 deinstall ok config-files\n" in (out / api["DPKG_STATE"]).read_text(),
                  "Snapshot must retain noninstalled rows")
            status.unlink()
            api["cmd_convert"](args)
            check(ledger.read_text() == content, "Done rerun changed ledger")
            status.write_text("Package: extra\nVersion: 3\nStatus: install ok installed\n")
            preserved = root / "preserved"
            preserved.mkdir()
            (preserved / api["DPKG_STATE"]).write_text("keep original\n")
            api["cmd_convert"](SimpleNamespace(old_rootfs=old, base_manifest=base, out=preserved))
            check((preserved / api["DPKG_STATE"]).read_text() == "keep original\n",
                  "Existing snapshot overwritten")
            emitted = root / "manifest.txt"
            api["cmd_emit_base_manifest"](SimpleNamespace(rootfs=old, output=emitted))
            check(emitted.read_text() == "extra 3\n", "Base manifest mismatch")
            try:
                api["load_status_or_die"](root / "missing")
            except SystemExit:
                pass
            else:
                raise AssertionError("Missing dpkg status accepted")
    return {"offline_converter_checks": 9}


def validate_checksums() -> dict[str, int]:
    count = 0
    failures = []
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        digest, filename = line.split("  ", 1)
        h = hashlib.sha256()
        with (ROOT / filename).open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(chunk)
        if h.hexdigest() != digest:
            failures.append(filename)
        count += 1
    check(not failures, f"Checksum mismatches: {failures}")
    return {"checksum_entries": count}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checksums", action="store_true", help="Read and verify SHA256SUMS")
    args = parser.parse_args()
    files = tracked_files()
    results = {}
    results.update(validate_coverage(files))
    results.update(validate_links())
    results.update(validate_syntax(files))
    results.update(validate_converter())
    if args.checksums:
        results.update(validate_checksums())
    print(json.dumps({"status": "passed", "checks": results}, indent=2))


if __name__ == "__main__":
    main()

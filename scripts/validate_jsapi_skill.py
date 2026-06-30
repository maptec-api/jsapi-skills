#!/usr/bin/env python3
"""Validate jsapi-skills structure and public-facing guardrails."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_SKILL_SECTIONS = [
    "安装接入",
    "鉴权",
    "功能列表",
    "能力路由",
    "强约束",
    "输出要求",
]

REQUIRED_README_SECTIONS = [
    "简介",
    "功能列表",
    "安装 Skill",
    "如何被 Agent 使用",
]

REAL_KEY_PATTERNS = [
    re.compile(r"Maptec\.apiKey\s*=\s*[\"'](?!YOUR_|<你的|YOUR_MAPTEC_KEY)[A-Za-z0-9_-]{16,}[\"']"),
    re.compile(r"Authorization:\s*Bearer\s+(?!\$MAPTEC_JSAPI_KEY)[A-Za-z0-9._-]{16,}"),
]


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def check_frontmatter(skill_md: Path, text: str) -> list[str]:
    findings: list[str] = []
    if not text.startswith("---\n"):
        return [f"{skill_md}:1: missing YAML frontmatter"]

    end = text.find("\n---", 4)
    if end == -1:
        return [f"{skill_md}:1: malformed YAML frontmatter"]

    frontmatter = text[4:end]
    if not re.search(r"^name:\s*jsapi-skills$", frontmatter, re.M):
        findings.append(f"{skill_md}:1: missing or invalid name")
    if not re.search(r"^description:\s*.{40,}$", frontmatter, re.M):
        findings.append(f"{skill_md}:1: missing or too-short description")
    return findings


def find_reference_links(text: str) -> set[str]:
    return set(re.findall(r"references/[A-Za-z0-9_.-]+\.md", text))


def check_skill_md(skill_dir: Path) -> list[str]:
    findings: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_md}: missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    findings.extend(check_frontmatter(skill_md, text))

    for section in REQUIRED_SKILL_SECTIONS:
        if f"## {section}" not in text:
            findings.append(f"{skill_md}:1: missing section '## {section}'")

    for required in ["不要发明", "需确认", "[lng, lat]", "MAPTEC_JSAPI_KEY"]:
        if required not in text:
            findings.append(f"{skill_md}:1: missing required guardrail '{required}'")

    for ref in find_reference_links(text):
        if not (skill_dir / ref).exists():
            findings.append(f"{skill_md}:1: missing referenced file {ref}")

    return findings


def check_readme(skill_dir: Path) -> list[str]:
    findings: list[str] = []
    readme = skill_dir / "README.md"
    if not readme.exists():
        return [f"{readme}: missing README.md"]

    text = readme.read_text(encoding="utf-8", errors="ignore")
    for section in REQUIRED_README_SECTIONS:
        if f"## {section}" not in text:
            findings.append(f"{readme}:1: missing section '## {section}'")

    for ref in find_reference_links(text):
        if not (skill_dir / ref).exists():
            findings.append(f"{readme}:1: missing referenced file {ref}")

    return findings


def check_references(skill_dir: Path) -> list[str]:
    findings: list[str] = []
    refs_dir = skill_dir / "references"
    if not refs_dir.exists():
        return [f"{refs_dir}: missing references directory"]

    refs = sorted(refs_dir.glob("*.md"))
    if not refs:
        return [f"{refs_dir}: no reference files"]

    for ref in refs:
        text = ref.read_text(encoding="utf-8", errors="ignore")
        if "## Agent 规则" not in text and "## Agent Rules" not in text:
            findings.append(f"{ref}:1: missing Agent 规则 section")
        if "TODO" in text:
            findings.append(f"{ref}:1: unresolved TODO")
        for linked_ref in find_reference_links(text):
            if not (skill_dir / linked_ref).exists():
                findings.append(f"{ref}:1: missing referenced file {linked_ref}")

    return findings


def check_key_leaks(skill_dir: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(skill_dir.rglob("*")):
        if ".git" in path.parts or "node_modules" in path.parts or not path.is_file():
            continue
        if path.suffix not in {".md", ".yaml", ".yml", ".py", ".js", ".ts", ".html"}:
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in REAL_KEY_PATTERNS:
            for match in pattern.finditer(text):
                findings.append(f"{path}:{line_of(text, match.start())}: possible real key or bearer token")
    return findings


def main(argv: list[str]) -> int:
    skill_dir = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    if not skill_dir.exists():
        print(f"ERROR: {skill_dir} does not exist")
        return 2

    findings: list[str] = []
    findings.extend(check_skill_md(skill_dir))
    findings.extend(check_readme(skill_dir))
    findings.extend(check_references(skill_dir))
    findings.extend(check_key_leaks(skill_dir))

    if findings:
        for finding in findings:
            print(finding)
        return 1

    print("OK: jsapi-skills passes validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

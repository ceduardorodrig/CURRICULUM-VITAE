from __future__ import annotations

import re
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "gov_toc",
    "description": "Verifica se o sumario/ToC do README esta completo, na ordem e com anchors corretos",
}

CVROOT = Path(__file__).resolve().parents[2]
README_PATH = CVROOT / "README.md"


def _github_anchor(text: str) -> str:
    text = text.lower()
    result = []
    for ch in text:
        if ch.isalnum() or ch == " ":
            result.append(ch)
        else:
            result.append("-")
    text = "".join(result)
    text = text.replace(" ", "-")
    while "---" in text:
        text = text.replace("---", "--")
    return text


def _strip_emoji(text: str) -> str:
    return "".join(ch for ch in text if ch.isalnum() or ch in " /—–-&" or ch.isspace()).strip()


def check() -> CheckResult:
    content = README_PATH.read_text(encoding="utf-8")
    lines = content.split("\n")
    details = []

    headings = []
    for i, line in enumerate(lines):
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            h = m.group(1).strip()
            headings.append((i + 1, h))

    # Find ToC boundaries
    toc_start = None
    for i, (line_no, h) in enumerate(headings):
        if "Sumário" in h or "Table of Contents" in h:
            toc_start = line_no - 1
            break

    if toc_start is None:
        return CheckResult.fail("gov_toc", "Secao de Sumario nao encontrada no README")

    toc_entries = []
    toc_start_line = toc_start
    for line in lines[toc_start_line + 1:]:
        if line.startswith("---"):
            break
        if line.startswith("##"):
            break
        m = re.search(r"\[([^\]]+)\]\(#([^)]+)\)", line)
        if m:
            toc_entries.append((m.group(1).strip(), m.group(2).strip()))

    # Build expected ToC from ## headings
    expected = []
    for line_no, h in headings:
        if "Sumário" in h or "Table of Contents" in h:
            continue
        if h.startswith("🇧🇷") or h.startswith("🇺🇸"):
            continue
        h_clean = _strip_emoji(h)
        expected.append((h_clean, _github_anchor(h)))

    for i, (exp_h, exp_anchor) in enumerate(expected):
        if i >= len(toc_entries):
            details.append(
                f"Sumario: faltando entrada para '{exp_h}'"
            )
            continue
        toc_label, toc_anchor = toc_entries[i]
        toc_clean = _strip_emoji(toc_label)
        if toc_clean != exp_h:
            details.append(
                f"Sumario: esperado '{exp_h}' na posicao {i+1}, encontrado '{toc_clean}'"
            )
        if toc_anchor != exp_anchor:
            details.append(
                f"Sumario: anchor incorreto para '{exp_h}' — esperado '{exp_anchor}', atual '{toc_anchor}'"
            )

    if len(toc_entries) > len(expected):
        extras = toc_entries[len(expected):]
        for label, anchor in extras:
            details.append(f"Sumario: entrada extra '{_strip_emoji(label)}'")

    for label, anchor in toc_entries:
        found = False
        for line_no, h in headings:
            expected_a = _github_anchor(h)
            if expected_a == anchor:
                found = True
                break
        if not found:
            toc_clean = _strip_emoji(label)
            details.append(
                f"Sumario: anchor '{anchor}' ('{toc_clean}') nao corresponde a nenhum cabecalho"
            )

    if details:
        return CheckResult.fail(
            "gov_toc",
            f"{len(details)} problema(s) no sumario do README",
            details,
        )

    return CheckResult.pass_(
        "gov_toc",
        f"Sumario com {len(toc_entries)} entradas, ordem e anchors corretos"
    )

from __future__ import annotations

import re
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "parity",
    "description": "Compara sections entre versoes PT-BR e EN-US",
}

CVROOT = Path(__file__).resolve().parents[2]

PAIRS = [
    ("pt-br/01-tech-produto-dados.md", "en-us/01-tech-product-data.md"),
    ("pt-br/02-socioambiental-tech.md", "en-us/02-socioenvironmental-tech.md"),
    ("pt-br/03-sumaenima.md", "en-us/03-sumaenima.md"),
]

HEADING_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)


def _strip_emoji(name: str) -> str:
    return re.sub(r"[^\w\s/]", "", name).strip()


def check() -> CheckResult:
    details = []

    for pt_path, en_path in PAIRS:
        pt_file = CVROOT / pt_path
        en_file = CVROOT / en_path

        if not pt_file.exists() or not en_file.exists():
            details.append(f"Par ausente: {pt_path} ou {en_path}")
            continue

        pt_heads = {_strip_emoji(m.group(1)) for m in HEADING_RE.finditer(pt_file.read_text(encoding="utf-8"))}
        en_heads = {_strip_emoji(m.group(1)) for m in HEADING_RE.finditer(en_file.read_text(encoding="utf-8"))}

        pt_ignored = {"Sobre", "About", "Contato", "Contact", "Narrativa", "Narrative", "O Fio da Meada", "The Thread", "Overview"}
        pt_filtered = {h for h in pt_heads if h not in pt_ignored and not h.startswith("Vers")}
        en_filtered = {h for h in en_heads if h not in pt_ignored and not h.startswith("Vers")}

        pt_only = pt_filtered - en_filtered
        en_only = en_filtered - pt_filtered

        if pt_only:
            details.append(f"{pt_path} -> sections sem equivalente EN: {', '.join(sorted(pt_only))}")
        if en_only:
            details.append(f"{en_path} -> sections sem equivalente PT: {', '.join(sorted(en_only))}")

    if details:
        return CheckResult.fail("parity", f"{len(details)} divergencia(s) entre PT e EN", details)

    return CheckResult.pass_("parity", f"{len(PAIRS)} pares conferidos, sections equivalentes")

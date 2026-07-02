from __future__ import annotations

import re
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "gov_orphan_lines",
    "description": "Detecta linhas soltas — texto orfao apos URL ou fechamento de parentese",
}

CVROOT = Path(__file__).resolve().parents[2]

FILES = [
    "pt-br/01-tech-produto-dados.md",
    "pt-br/02-socioambiental-tech.md",
    "pt-br/02-socioambiental-nichado.md",
    "pt-br/03-sumaenima.md",
    "en-us/01-tech-product-data.md",
    "en-us/02-socioenvironmental-tech.md",
    "en-us/03-sumaenima.md",
    "README.md",
]

ORPHAN_PATTERNS = [
    # URL seguida de nova frase SEM pontuacao entre elas
    # Ex: `](url) Estreia no INPA` (orfao) vs `](url). The` (normal)
    re.compile(r'\]\(https?://[^)]+\)\s+([A-ZÀ-Ÿ][a-zà-ÿ]{2,})'),
]

CONTINUATIONS = {
    "For", "The", "In", "On", "At", "By", "To", "With", "And", "But", "Or",
    "For", "From", "This", "That", "These", "Those", "It", "Its", "A", "An",
    "O", "A", "As", "Os", "As", "Na", "No", "Nas", "Nos", "Da", "Do",
    "Das", "Dos", "Em", "Com", "Por", "Para", "De", "Um", "Uma",
}


def check() -> CheckResult:
    details = []

    for rel in FILES:
        path = CVROOT / rel
        if not path.exists():
            continue

        lines = path.read_text(encoding="utf-8").split("\n")

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("|") or stripped.startswith(">"):
                continue

            for pattern in ORPHAN_PATTERNS:
                m = pattern.search(stripped)
                if m:
                    word = m.group(1)
                    if word in CONTINUATIONS:
                        continue
                    snippet = stripped[:90]
                    details.append(
                        f"{rel}:{i}: possivel texto orfao — «{snippet}»"
                    )
                    break

    if details:
        return CheckResult.warn(
            "gov_orphan_lines",
            f"{len(details)} possivel(eis) linha(s) solta(s)",
            details,
        )

    return CheckResult.pass_("gov_orphan_lines", "Nenhuma linha solta detectada")


def check() -> CheckResult:
    details = []

    for rel in FILES:
        path = CVROOT / rel
        if not path.exists():
            continue

        lines = path.read_text(encoding="utf-8").split("\n")

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("|") or stripped.startswith(">"):
                continue

            for pattern in ORPHAN_PATTERNS:
                m = pattern.search(stripped)
                if m:
                    snippet = stripped[:90]
                    details.append(
                        f"{rel}:{i}: possivel texto orfao — «{snippet}»"
                    )
                    break

    if details:
        return CheckResult.warn(
            "gov_orphan_lines",
            f"{len(details)} possivel(eis) linha(s) solta(s)",
            details,
        )

    return CheckResult.pass_("gov_orphan_lines", "Nenhuma linha solta detectada")

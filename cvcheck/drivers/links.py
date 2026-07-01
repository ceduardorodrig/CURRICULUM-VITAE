from __future__ import annotations

import re
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "links",
    "description": "Verifica se links relativos em .md resolvem para arquivos existentes",
}

CVROOT = Path(__file__).resolve().parents[2]

MD_LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")

FILES = [
    "pt-br/01-tech-produto-dados.md",
    "pt-br/02-socioambiental-tech.md",
    "pt-br/03-sumaenima.md",
    "en-us/01-tech-product-data.md",
    "en-us/02-socioenvironmental-tech.md",
    "en-us/03-sumaenima.md",
    "README.md",
]

EXTERNAL_LINK_PATTERNS = [
    (r"linkedin\.com", "LinkedIn"),
    (r"github\.com/ceduardorodrig", "GitHub"),
    (r"sumaenima\.chimaera-heptatonic\.ts\.net", "Sumaenima"),
    (r"mailto:", "Email"),
]


def check() -> CheckResult:
    details = []

    for f in FILES:
        path = CVROOT / f
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")

        for m in MD_LINK.finditer(content):
            dest = m.group(2).strip()

            if dest.startswith(("#", "http://", "https://", "mailto:")):
                continue

            if dest.startswith("/"):
                resolved = CVROOT / dest.lstrip("/")
            else:
                resolved = (path.parent / dest).resolve()

            if not resolved.exists():
                details.append(f"{f}: link relativo quebrado '{dest}' -> esperado em {resolved}")

    for f in FILES:
        path = CVROOT / f
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")

        for pattern, name in EXTERNAL_LINK_PATTERNS:
            found = re.search(pattern, content)
            if not found:
                details.append(f"{f}: link externo para {name} ausente")

    if details:
        return CheckResult.fail("links", f"{len(details)} problema(s) de link", details)

    return CheckResult.pass_("links", f"{len(FILES)} arquivos conferidos, links OK")

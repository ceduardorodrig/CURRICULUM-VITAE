from __future__ import annotations

import re
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "gov_acronyms",
    "description": "Verifica se siglas sao definidas na primeira ocorrencia (Nome da Sigla (NdS))",
}

CVROOT = Path(__file__).resolve().parents[2]

FILES = [
    "pt-br/01-tech-produto-dados.md",
    "pt-br/02-socioambiental-tech.md",
    "pt-br/03-sumaenima.md",
    "en-us/01-tech-product-data.md",
    "en-us/02-socioenvironmental-tech.md",
    "en-us/03-sumaenima.md",
    "README.md",
]

ACRONYM_RE = re.compile(r"\b[A-ZÀ-Ÿ]{2,}\b")

SKIP_CONTEXTS = [
    r"http[s]?://",
    r"github\.com",
    r"tailscale",
    r"chimaera",
    r"mailto:",
    r"/assets/",
    r"\.svg",
    r"\.png",
    r"\.ts\.net",
    r"[Ss]umaenima",
    r"[Ss]umænimá",
    r"[Ll]arge[-\s][vV]\d",
    r"/03[.-]",
    r"\.md",
]

NOT_ACRONYMS: set[str] = {
    "DF", "GO", "TO", "MG", "SP", "RJ", "BA", "PA", "AM", "MT", "MS",
    "PR", "SC", "RS", "PE", "CE", "MA", "PI", "AL", "RN", "PB",
    "RO", "AC", "AP", "RR",
}


def _in_skip_context(line: str, pos: int) -> bool:
    ctx = line[max(0, pos - 30) : pos + 30]
    for pat in SKIP_CONTEXTS:
        if re.search(pat, ctx):
            return True
    return False


def _is_proper_name_acronym(line: str, pos: int) -> bool:
    ctx_before = line[max(0, pos - 15) : pos]
    if ctx_before.rstrip().endswith("-"):
        return True
    return False


def _is_followed_by_digit(line: str, pos: int, acr: str) -> bool:
    after = line[pos + len(acr) : pos + len(acr) + 5].strip()
    if after and after[0].isdigit():
        return True
    return False


def _is_roman_numeral(acr: str) -> bool:
    return acr in {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"}


def _has_definition(lines: list[str], line_idx: int, acr: str) -> bool:
    for check_idx in range(max(0, line_idx - 3), min(len(lines), line_idx + 3)):
        line = lines[check_idx]
        if re.search(rf"[A-ZÀ-Ÿ][a-zà-ÿ].*\({re.escape(acr)}\)", line):
            return True
        if re.search(rf"\({re.escape(acr)}\)", line):
            return True
    return False


def check() -> CheckResult:
    errors = []

    for rel in FILES:
        path = CVROOT / rel
        if not path.exists():
            continue

        content = path.read_text(encoding="utf-8")
        lines = content.split("\n")

        all_matches = list(ACRONYM_RE.finditer(content))
        from collections import Counter
        freq = Counter(m.group(0) for m in all_matches)

        first_occ: dict[str, tuple[int, int]] = {}

        for i, line in enumerate(lines):
            for m in ACRONYM_RE.finditer(line):
                acr = m.group(0)
                if acr in first_occ:
                    continue
                if _in_skip_context(line, m.start()):
                    continue
                if acr in NOT_ACRONYMS:
                    continue
                if _is_roman_numeral(acr):
                    continue
                if _is_proper_name_acronym(line, m.start()):
                    continue
                if _is_followed_by_digit(line, m.start(), acr):
                    continue
                first_occ[acr] = (i, m.start())

        for acr, (line_idx, _col) in first_occ.items():
            if freq.get(acr, 0) < 2:
                continue
            if _has_definition(lines, line_idx, acr):
                continue
            line_snippet = lines[line_idx].strip()[:70]
            errors.append(
                f"{rel}:{line_idx + 1}: Sigla '{acr}' sem definicao "
                f"«{line_snippet}»"
            )

    if errors:
        return CheckResult.warn(
            "gov_acronyms",
            f"{len(errors)} sigla(s) sem definicao na primeira ocorrencia",
            errors[:50],
        )

    return CheckResult.pass_(
        "gov_acronyms", f"{len(FILES)} arquivos conferidos, siglas definidas corretamente"
    )

from __future__ import annotations

import re
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "gov_glossary",
    "description": "Verifica se nomes proprios, siglas e termos estao escritos corretamente nos CVs",
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

# (regex pattern, correct form, case_insensitive)
BANNED_TERMS = [
    # ── Sumænimá / StênioBOT ─────────────────────────────────────────
    (r"\bSumaenima\b", "Sumænimá", True),
    (r"\bStenio[Bb]ot\b", "StênioBOT", False),
    (r"\bStênio[Bb]ot\b", "StênioBOT", False),
    (r"\bStenioBOT\b", "StênioBOT", False),
    (r"\bSteniokernel\b", "StênioKernel", True),
    (r"\bStenioKernel\b", "StênioKernel", False),

    # ── Grafia PT-BR ─────────────────────────────────────────────────
    (r"\bautomapecimento\b", "automapeamento", False),
    (r"\bauto-corrige\b", "autocorrige", False),
    (r"\bre-assinatura\b", "reassinatura", False),
    (r"\bre-assinando\b", "reassinando", False),
    (r"\bflakyness\b", "flakiness", False),
    (r"\bJunho\b", "junho", False),

    # ── Maiúscula no meio da frase ───────────────────────────────────
    (r"\bÉ a infraestrutura", "é a infraestrutura", False),
    (r"\bIS the", "is the", False),

    # ── Orgs e siglas ─────────────────────────────────────────────────
    (r"\bIPAM\b", "IPAM", False),

    # ── Lugares ───────────────────────────────────────────────────────
    (r"\bBrasilia\b", "Brasília", False),

    # ── Refs academicas ───────────────────────────────────────────────
    (r"\bUnB\b", "UnB", False),

    # ── Nodes ─────────────────────────────────────────────────────────
    (r"\bpsicopompo\b", "psicopompo", False),
    (r"\bybyra\b", "ybyra", False),
    (r"\bybytu\b", "ybytu", False),
    (r"\bkuaray\b", "kuaray", False),

    # ── Tech ──────────────────────────────────────────────────────────
    (r"\bMnemocine\b", "Mnemocine", False),

    # ── PT-PT evitado ─────────────────────────────────────────────────
    (r"\bautomauditoria\b", "auto-auditoria (remover em ingles)", False),
]


def check() -> CheckResult:
    errors = []

    for rel in FILES:
        path = CVROOT / rel
        if not path.exists():
            continue

        content = path.read_text(encoding="utf-8")

        for pattern, correct, ignore_case in BANNED_TERMS:
            flags = re.IGNORECASE if ignore_case else 0

            for match in re.finditer(pattern, content, flags):
                matched = match.group(0)

                start = max(0, match.start() - 10)
                end = min(len(content), match.end() + 10)
                context = content[start:end]

                if "http" in context or "github.com" in context or "tailscale" in context or "mailto" in context or "chimaera" in context or "/03-" in context or "/03." in context or ".md" in context or ".svg" in context or "/assets/" in context:
                    continue

                if matched == correct:
                    continue

                errors.append(f"{rel}: Encontrado '{matched}', deveria ser '{correct}'")

    errors = list(dict.fromkeys(errors))

    if errors:
        return CheckResult.fail("gov_glossary", f"{len(errors)} violacao(oes) de glossario", errors)

    return CheckResult.pass_("gov_glossary", "Glossario consistente em todos os arquivos")

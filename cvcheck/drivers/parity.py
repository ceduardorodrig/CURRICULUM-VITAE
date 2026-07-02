from __future__ import annotations

import re
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "parity",
    "description": "Verifica se todos arquivos PT tem versao EN e vice-versa (exceto sub-versoes)",
}

CVROOT = Path(__file__).resolve().parents[2]

SOLO_PATTERNS = ("nichado",)

HEADING_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)

KNOWN_MAPPINGS = {
    "Perfil": "Profile",
    "Experiência": "Experience",
    "Formação": "Education",
    "Habilidades": "Skills",
    "Publicações": "Publications",
    "Idiomas": "Languages",
    "Prêmios": "Awards",
    "Infraestrutura — Sumænimá & Mnemocine": "Infrastructure — Sumænimá & Mnemocine",
    "Infraestrutura — Homelab Mnemocine": "Infrastructure — Mnemocine Homelab",
    "Visão Geral": "Overview",
    "O Problema": "The Problem",
    "A Solução — StênioBOT": "The Solution — StênioBOT",
    "Design & Experiência": "Design & Experience",
    "Escala do Ecossistema": "Ecosystem Scale",
    "Fundador": "Founder",
    "Próximos Passos": "Next Steps",
    "Stack Tecnológica": "Tech Stack",
    "StênioKernel — Kernel de Governança para Agentes de IA": "StênioKernel — AI Agent Governance Kernel",
}


def _strip_emoji(name: str) -> str:
    return re.sub(r"[^\w\s/–—\-&\u00C0-\u024F]", "", name).strip()


def _find_pairs(pt_dir: Path, en_dir: Path) -> tuple[list, list, list]:
    pt_files = sorted(pt_dir.glob("*.md"))
    en_files = sorted(en_dir.glob("*.md"))

    en_by_prefix: dict[str, Path] = {}
    for f in en_files:
        m = re.match(r"(\d{2})-", f.name)
        if m:
            en_by_prefix[m.group(1)] = f

    pairs = []
    pt_orphans = []

    for pt_f in pt_files:
        if any(p in pt_f.name for p in SOLO_PATTERNS):
            continue
        m = re.match(r"(\d{2})-", pt_f.name)
        if m:
            prefix = m.group(1)
            if prefix in en_by_prefix:
                pairs.append((pt_f, en_by_prefix[prefix]))
            else:
                pt_orphans.append(pt_f)

    en_orphans = []
    for en_f in en_files:
        m = re.match(r"(\d{2})-", en_f.name)
        if m:
            prefix = m.group(1)
            pt_matches = [p for p in pt_files if p.name.startswith(prefix)]
            if not pt_matches and not any(p in en_f.name for p in SOLO_PATTERNS):
                en_orphans.append(en_f)

    return pairs, pt_orphans, en_orphans


def check() -> CheckResult:
    details = []
    pt_dir = CVROOT / "pt-br"
    en_dir = CVROOT / "en-us"

    pairs, pt_orphans, en_orphans = _find_pairs(pt_dir, en_dir)

    for pt_f in pt_orphans:
        details.append(f"{pt_f.relative_to(CVROOT)}: existe em PT mas sem versao EN correspondente")
    for en_f in en_orphans:
        details.append(f"{en_f.relative_to(CVROOT)}: existe em EN mas sem versao PT correspondente")

    for pt_file, en_file in pairs:
        pt_rel = pt_file.relative_to(CVROOT)
        en_rel = en_file.relative_to(CVROOT)

        pt_heads = {_strip_emoji(m.group(1)) for m in HEADING_RE.finditer(pt_file.read_text(encoding="utf-8"))}
        en_heads = {_strip_emoji(m.group(1)) for m in HEADING_RE.finditer(en_file.read_text(encoding="utf-8"))}

        pt_ignored = {"Sobre", "About", "Contato", "Contact", "Narrativa", "Narrative",
                       "O Fio da Meada", "The Thread", "Sumaenima  Mnemocine"}
        pt_filtered = {h for h in pt_heads if h not in pt_ignored and not h.startswith("Vers")}
        en_filtered = {h for h in en_heads if h not in pt_ignored and not h.startswith("Vers")}

        pt_mapped = {KNOWN_MAPPINGS.get(h, h) for h in pt_filtered}
        en_mapped = {KNOWN_MAPPINGS.get(h, h) for h in en_filtered}

        pt_only = pt_mapped - en_mapped
        en_only = en_mapped - pt_mapped

        if pt_only:
            details.append(f"{pt_rel}: sections sem equivalente EN: {', '.join(sorted(pt_only)[:5])}")
        if en_only:
            details.append(f"{en_rel}: sections sem equivalente PT: {', '.join(sorted(en_only)[:5])}")

    if details:
        return CheckResult.fail("parity", f"{len(details)} divergencia(s) entre PT e EN", details)

    return CheckResult.pass_("parity", f"{len(pairs)} pares conferidos, sections equivalentes")

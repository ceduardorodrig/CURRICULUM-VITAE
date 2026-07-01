from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "gov_bilingual",
    "description": "Verifica se conteudo adicionado em PT foi traduzido para EN — compara chars, bullets e paragrafos por secao",
}

CVROOT = Path(__file__).resolve().parents[2]

PAIRS = [
    ("pt-br/01-tech-produto-dados.md", "en-us/01-tech-product-data.md"),
    ("pt-br/02-socioambiental-tech.md", "en-us/02-socioenvironmental-tech.md"),
    ("pt-br/03-sumaenima.md", "en-us/03-sumaenima.md"),
]

KNOWN_MAPPINGS = {
    "Perfil": "Profile",
    "Experiência": "Experience",
    "Formação": "Education",
    "Habilidades": "Skills",
    "Publicações": "Publications",
    "Idiomas": "Languages",
    "Prêmios": "Awards",
    "Infraestrutura — Sumænimá & Mnemocine": "Infrastructure — Sumænimá & Mnemocine",
    "Visão Geral": "Overview",
    "O Problema": "The Problem",
    "A Solução — StênioBOT": "The Solution — StênioBOT",
    "Design & Experiência": "Design & Experience",
    "Stack Tecnológica": "Tech Stack",
    "Escala do Ecossistema": "Ecosystem Scale",
    "Fundador": "Founder",
    "Próximos Passos": "Next Steps",
    "StênioKernel — Kernel de Governança para Agentes de IA": "StênioKernel — AI Agent Governance Kernel",
    "Infraestrutura — Homelab Mnemocine": "Infrastructure — Mnemocine Homelab",
}

REVERSE_MAPPINGS = {v: k for k, v in KNOWN_MAPPINGS.items()}

IGNORE_HEADINGS = {
    "Sobre", "About",
    "Contato", "Contact",
    "Narrativa", "Narrative",
    "O Fio da Meada", "The Thread",
    "cvcheck — Miniatura do StênioKernel",
    "Sumænimá — StênioBOT",
}


@dataclass
class Section:
    heading: str
    body: str


def _strip_emoji(text: str) -> str:
    return re.sub(r"[^\w\s/–—\-&\u00C0-\u024F]", "", text).strip()


def _parse_sections(text: str) -> list[Section]:
    blocks = re.split(r"\n(?=^##\s)", text.strip(), flags=re.MULTILINE)
    sections = []
    for block in blocks:
        lines = block.strip().split("\n")
        m = re.match(r"^##\s+(.+)$", lines[0])
        if m:
            body = "\n".join(lines[1:]).strip()
            sections.append(Section(heading=m.group(1).strip(), body=body))
    return sections


def _meaningful_chars(text: str) -> int:
    text = re.sub(r"\*\*|__|~~", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[>#|`_*]", "", text)
    text = re.sub(r"[^\w\s\u00C0-\u024F]", "", text)
    text = re.sub(r"\s+", "", text)
    return len(text)


def _count_bullets(text: str) -> int:
    return len(re.findall(r"^- ", text, re.MULTILINE))


def _match(heading: str, sections: list[Section]) -> Section | None:
    cleaned = _strip_emoji(heading)
    for sec in sections:
        sec_cleaned = _strip_emoji(sec.heading)
        if sec_cleaned == cleaned:
            return sec
        if KNOWN_MAPPINGS.get(cleaned) == sec_cleaned:
            return sec
        if REVERSE_MAPPINGS.get(cleaned) == sec_cleaned:
            return sec
    return None


def check() -> CheckResult:
    details = []
    CHAR_RATIO_WARN = 1.5
    BULLET_RATIO_WARN = 2.0
    BULLET_DIFF_MIN = 3

    for pt_path, en_path in PAIRS:
        pt_file = CVROOT / pt_path
        en_file = CVROOT / en_path

        if not pt_file.exists() or not en_file.exists():
            details.append(f"Par ausente: {pt_path} ou {en_path}")
            continue

        pt_secs = _parse_sections(pt_file.read_text(encoding="utf-8"))
        en_secs = _parse_sections(en_file.read_text(encoding="utf-8"))

        for pt_sec in pt_secs:
            pt_heading_clean = _strip_emoji(pt_sec.heading)
            if pt_heading_clean in {_strip_emoji(h) for h in IGNORE_HEADINGS}:
                continue

            en_sec = _match(pt_sec.heading, en_secs)
            if en_sec is None:
                details.append(f"{pt_path}: Secao '{pt_sec.heading}' existe em PT mas nao em EN")
                continue

            pt_chars = _meaningful_chars(pt_sec.body)
            en_chars = _meaningful_chars(en_sec.body)
            ratio = pt_chars / max(en_chars, 1)

            if ratio > CHAR_RATIO_WARN:
                details.append(
                    f"{pt_path} | '{pt_heading_clean}': PT {pt_chars}c vs EN {en_chars}c ({ratio:.1f}x)"
                )
            elif ratio < 1 / CHAR_RATIO_WARN:
                details.append(
                    f"{en_path} | '{pt_heading_clean}': EN {en_chars}c vs PT {pt_chars}c ({1/ratio:.1f}x)"
                )

            pt_bullets = _count_bullets(pt_sec.body)
            en_bullets = _count_bullets(en_sec.body)

            if pt_bullets > en_bullets * BULLET_RATIO_WARN and (pt_bullets - en_bullets) >= BULLET_DIFF_MIN:
                details.append(
                    f"{pt_path} | '{pt_heading_clean}': PT {pt_bullets} bullets vs EN {en_bullets}"
                )

        for en_sec in en_secs:
            en_heading_clean = _strip_emoji(en_sec.heading)
            if en_heading_clean in {_strip_emoji(h) for h in IGNORE_HEADINGS}:
                continue
            pt_match = _match(en_sec.heading, pt_secs)
            if pt_match is None:
                details.append(f"{en_path}: Secao '{en_sec.heading}' existe em EN mas nao em PT")

    if details:
        return CheckResult.warn("gov_bilingual", f"{len(details)} divergencia(s) bilingue", details)

    return CheckResult.pass_("gov_bilingual", f"{len(PAIRS)} pares conferidos, densidade de conteudo ok")

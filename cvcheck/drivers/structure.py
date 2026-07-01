from __future__ import annotations

from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "structure",
    "description": "Verifica se todos os 6 arquivos .md existem com sections obrigatorias",
}

CVROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    "pt-br/01-tech-produto-dados.md",
    "pt-br/02-socioambiental-tech.md",
    "pt-br/03-sumaenima.md",
    "en-us/01-tech-product-data.md",
    "en-us/02-socioenvironmental-tech.md",
    "en-us/03-sumaenima.md",
]

REQUIRED_SECTIONS_BY_LANG = {
    "pt-br": ["Experiência", "Formação", "Habilidades"],
    "en-us": ["Experience", "Education", "Skills"],
}


def _cvs() -> list[Path]:
    return [CVROOT / f for f in REQUIRED_FILES]


def _lang_of(path: Path) -> str:
    return "pt-br" if "pt-br" in path.parts else "en-us"


def _required_sections(content: str, lang: str) -> list[str]:
    needed = REQUIRED_SECTIONS_BY_LANG.get(lang, [])
    missing = []
    for sec in needed:
        if f"## {sec}" not in content and f"## 💼 {sec}" not in content and f"## 🎓 {sec}" not in content and f"## 🛠️ {sec}" not in content:
            missing.append(sec)
    return missing


def check() -> CheckResult:
    details = []

    for f in _cvs():
        if not f.exists():
            details.append(f"Arquivo ausente: {f.relative_to(CVROOT)}")

    if details:
        return CheckResult.fail("structure", f"{len(details)} arquivo(s) ausente(s)", details)

    for f in _cvs():
        content = f.read_text(encoding="utf-8")
        lang = _lang_of(f)
        missing = _required_sections(content, lang)
        if missing:
            details.append(f"{f.relative_to(CVROOT)}: sections ausentes: {', '.join(missing)}")

    if details:
        return CheckResult.fail("structure", f"{len(details)} problema(s) de estrutura", details)

    return CheckResult.pass_("structure", f"{len(REQUIRED_FILES)} arquivos OK, sections obrigatorias presentes")

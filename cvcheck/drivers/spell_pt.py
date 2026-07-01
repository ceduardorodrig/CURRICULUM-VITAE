from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "spell_pt",
    "description": "Verifica ortografia PT-BR nos arquivos pt-br/ (aspell ou hunspell)",
}

CVROOT = Path(__file__).resolve().parents[2]

PT_FILES = [
    "pt-br/01-tech-produto-dados.md",
    "pt-br/02-socioambiental-tech.md",
    "pt-br/03-sumaenima.md",
]

LOCAL_DICT = {
    "Mnemocine", "psicopompo", "ybyra", "ybytu", "kuaray",
    "Sumaenima", "StênioBOT", "StênioREC", "StênioPANEL", "StênioDIVE",
    "DataVis", "Gemma", "Valkey", "Kalunga", "Caché", "Tailscale",
    "Loki", "Promtail", "Grafana", "UnB", "IPAM", "ISPN",
    "ICMBio", "MMA", "CIPA", "LGPD",
    "IPEA", "IEB", "CNS", "MCM", "CONFREM", "APAFE", "FLONA",
    "PROTEJA", "Tefé", "INPA", "FastAPI", "Docker",
    "PaddleOCR", "QGIS", "AdGuard", "Alembic",
    "Mercado", "Pago", "PIX", "SaaS", "OKRs",
    "big", "tech", "dashboard", "benchmarking",
    "Veredas", "Buritis", "Catingueiro", "Canadá",
    "Scrum", "Mestrado", "Antropologia",
    "GroundingDINO", "Homepage", "CachyOS",
    "Land", "Use", "Policy", "Elsevier",
    "MPF", "API", "ERP", "CMS", "VAD", "WAL",
    "AES", "GCM", "CGNAT", "NGINX", "DNS", "SSH", "VRAM",
    "Mutex", "TTL", "CI", "CD", "FMEA", "ADR", "ADRs",
    "QAdrivers", "CheckResult", "auto", "descoberta",
    "PCI", "NVME", "RTX", "NVIDIA",
    "Swarm", "nginx", "AdWords", "Ads",
    "Brasilia", "Brasília", "Cavalcante",
    "Amazônia", "Amazônia", "Cerrado", "Pantanal",
    "Desenvolvimento", "Sustentabilidade",
    "Antropoceno", "Antropoceno",
    "Comunicação", "Comunicação",
    "president", "presidente",
    "TCC", "PROUNI", "Enem",
    "Vite", "TipTap", "Syncthing",
    "Mercosul", "Mercosur",
    "Storytelling", "storytelling",
    "Arquitetura", "Arquitetura",
    "Governança", "Governança",
    "socioambiental", "socioambiental",
    "supraconectividade",
    "Arquivo", "Nacional",
    "chapada", "Chapada", "Veadeiros",
    "relatoria", "sistematização", "sistematizacao",
    "planejamento", "estratégico",
    "etnografia", "automatica", "autoajustável",
    "logs", "métricas", "dashboard",
    "reaproveitado", "indistinguíveis",
    "Data", "Bureau",
    "Caring", "Economy",
}


def check() -> CheckResult:
    spellchecker = _detect_spellchecker()
    if spellchecker is None:
        return CheckResult.skip("spell_pt", "Nenhum corretor ortográfico disponível (instale aspell-pt-br ou hunspell-pt-br)")

    details = []

    for rel in PT_FILES:
        path = CVROOT / rel
        if not path.exists():
            continue

        text = path.read_text(encoding="utf-8")

        words = _extract_words(text)
        if not words:
            continue

        if spellchecker == "aspell":
            bad = _check_aspell_pt(words)
        else:
            bad = _check_hunspell_pt(words)

        known_bad = _known_errors(bad, LOCAL_DICT)
        if known_bad:
            details.append(f"{rel}: {', '.join(sorted(known_bad))}")

    if details:
        return CheckResult.warn("spell_pt", f"{len(details)} arquivo(s) com possiveis erros", details)

    return CheckResult.pass_("spell_pt", f"{len(PT_FILES)} arquivos PT-BR conferidos")


def _detect_spellchecker() -> str | None:
    try:
        r = subprocess.run(["aspell", "version"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            r2 = subprocess.run(["aspell", "dicts"], capture_output=True, text=True, timeout=5)
            if "pt_BR" in r2.stdout or "portuguese" in r2.stdout:
                return "aspell"
    except FileNotFoundError:
        pass

    try:
        r = subprocess.run(["hunspell", "-D"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and ("pt_BR" in r.stdout or "pt_BR" in r.stderr):
            return "hunspell"
    except FileNotFoundError:
        pass

    return None


def _extract_words(text: str) -> list[str]:
    words = re.findall(r"[a-zA-ZáéíóúâêîôûãõàèìòùäëïöüçñÁÉÍÓÚÂÊÎÔÛÃÕÀÈÌÒÙÄËÏÖÜÇÑ]+(?:'[a-zA-Z]+)?", text)
    return sorted(set(w for w in words if len(w) > 1 and not w.isupper() and not w.isdigit()))


def _check_aspell_pt(words: list[str]) -> set[str]:
    input_text = "\n".join(words)
    try:
        r = subprocess.run(
            ["aspell", "pipe", "-l", "pt_BR", "-d", "pt_BR"],
            input=input_text,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception:
        return set()

    bad: set[str] = set()
    for line in r.stdout.splitlines():
        if not line:
            continue
        parts = line.split(":")
        if len(parts) >= 2 and parts[0].strip() == "*":
            continue
        if "&" in line:
            bad_word = line.split(" ")[1] if len(line.split(" ")) > 1 else ""
        elif "#" in line:
            bad_word = line.split(" ")[1] if len(line.split(" ")) > 1 else ""
        else:
            continue
        if bad_word:
            bad.add(bad_word)
    return bad


def _check_hunspell_pt(words: list[str]) -> set[str]:
    input_text = "\n".join(words)
    try:
        r = subprocess.run(
            ["hunspell", "-d", "pt_BR", "-l"],
            input=input_text,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception:
        return set()
    return set(w for w in r.stdout.strip().split("\n") if w.strip())


def _known_errors(bad: set[str], local_dict: set[str]) -> set[str]:
    return {w for w in bad if w.lower() not in {x.lower() for x in local_dict}}

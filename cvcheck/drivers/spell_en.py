from __future__ import annotations

import re
import subprocess
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "spell_en",
    "description": "Verifica ortografia EN-US nos arquivos en-us/ (aspell ou hunspell)",
}

CVROOT = Path(__file__).resolve().parents[2]

EN_FILES = [
    "en-us/01-tech-product-data.md",
    "en-us/02-socioenvironmental-tech.md",
    "en-us/03-sumaenima.md",
]

LOCAL_DICT = {
    "Mnemocine", "psicopompo", "ybyra", "ybytu", "kuaray",
    "Sumaenima", "StênioBOT", "StênioREC", "StênioPANEL", "StênioDIVE",
    "DataVis", "Gemma", "Valkey", "Kalunga", "Tailscale",
    "Loki", "Promtail", "Grafana", "UnB", "IPAM", "ISPN",
    "ICMBio", "MMA", "CIPA", "LGPD", "IPEA", "IEB", "CNS",
    "MCM", "CONFREM", "APAFE", "FLONA", "PROTEJA", "Tefé", "INPA",
    "FastAPI", "Docker", "PaddleOCR", "QGIS", "AdGuard", "Alembic",
    "Mercado", "Pago", "PIX", "SaaS", "OKRs",
    "Veredas", "Buritis", "Catingueiro", "Canadá",
    "GroundingDINO", "Homepage", "CachyOS",
    "Land", "Use", "Policy", "Elsevier", "MPF",
    "CGNAT", "NGINX", "VRAM", "Mutex", "TTL",
    "FMEA", "ADR", "ADRs", "RTX", "NVIDIA",
    "Swarm", "Brasília", "Cavalcante",
    "Vite", "TipTap", "Syncthing",
    "Mercosul", "Mercosur", "Cerrado",
    "socioenvironmental", "socioenvironmental",
    "homelab", "Homelab", "Homelab",
    "backlog", "Backlog", "backlog",
    "scalable", "Scalable",
    "observability", "Observability",
    "ITAM", "ITAM",
    "PATCH", "Swagger",
    "et al", "et al",
    "TCC", "PROUNI", "Enem",
    "Analytics", "analytics",
    "pipeline", "Pipeline",
    "dashboard", "Dashboard",
    "ecosystem", "Ecosystem",
    "realtime", "Real", "time",
    "automated", "Automated",
    "methodology", "Methodology",
    "transformative", "Transformative",
    "biome", "Biome",
    "subdivision", "Subdivision",
    "sovereign", "Sovereign",
    "Governance", "governance",
    "Architecture", "architecture",
    "Infrastructure", "infrastructure",
    "Resilience", "resilience",
    "funnel", "Funnel",
    "mesh", "Mesh",
    "handoff", "Handoff",
    "Socioenvironmental", "socioenvironmental",
    "ethnography", "Ethnography",
    "ethnographic", "Ethnographic",
    "participant", "Participant",
    "observation", "Observation",
    "NGOs", "NGOs",
    "reached", "Reached",
    "segmentation", "Segmentation",
    "award", "Award",
    "institute", "Institute",
    "institutes", "Institutes",
    "organization", "Organization",
    "organizations", "Organizations",
    "articulation", "Articulation",
    "biome", "Biome",
    "biomes", "Biomes",
    "endangered", "Endangered",
    "deforestation", "Deforestation",
    "savanna", "Savanna",
    "grassland", "Grassland",
    "submitted", "Submitted",
    "premiered", "Premiered",
    "co", "directed",
    "codirected", "codirected",
    "engaged", "Engaged",
    "engagement", "Engagement",
    "insight", "Insights",
    "Interrupted", "interrupted",
    "interrupted", "interrupted",
    "Bureau", "Bureau",
    "Caring", "Economy",
    "Arquivo", "Nacional",
}


def check() -> CheckResult:
    spellchecker = _detect_spellchecker_en()
    if spellchecker is None:
        return CheckResult.skip("spell_en", "Nenhum corretor ortográfico disponível (instale aspell-en ou hunspell-en-us)")

    details = []

    for rel in EN_FILES:
        path = CVROOT / rel
        if not path.exists():
            continue

        text = path.read_text(encoding="utf-8")

        words = _extract_words(text)
        if not words:
            continue

        if spellchecker == "aspell":
            bad = _check_aspell_en(words)
        else:
            bad = _check_hunspell_en(words)

        known_bad = _known_errors(bad, LOCAL_DICT)
        if known_bad:
            details.append(f"{rel}: {', '.join(sorted(known_bad))}")

    if details:
        return CheckResult.warn("spell_en", f"{len(details)} arquivo(s) com possiveis erros", details)

    return CheckResult.pass_("spell_en", f"{len(EN_FILES)} arquivos EN-US conferidos")


def _detect_spellchecker_en() -> str | None:
    try:
        r = subprocess.run(["aspell", "version"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            r2 = subprocess.run(["aspell", "dicts"], capture_output=True, text=True, timeout=5)
            if "en_US" in r2.stdout or "english" in r2.stdout:
                return "aspell"
    except FileNotFoundError:
        pass

    try:
        r = subprocess.run(["hunspell", "-D"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and ("en_US" in r.stdout or "en_US" in r.stderr):
            return "hunspell"
    except FileNotFoundError:
        pass

    return None


def _extract_words(text: str) -> list[str]:
    words = re.findall(r"[a-zA-ZáéíóúâêîôûãõàèìòùäëïöüçñÁÉÍÓÚÂÊÎÔÛÃÕÀÈÌÒÙÄËÏÖÜÇÑ]+(?:'[a-zA-Z]+)?", text)
    return sorted(set(w for w in words if len(w) > 1 and not w.isupper() and not w.isdigit()))


def _check_aspell_en(words: list[str]) -> set[str]:
    input_text = "\n".join(words)
    try:
        r = subprocess.run(
            ["aspell", "pipe", "-l", "en_US", "-d", "en_US"],
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
        if "&" in line:
            bad_word = line.split(" ")[1] if len(line.split(" ")) > 1 else ""
        elif "#" in line:
            bad_word = line.split(" ")[1] if len(line.split(" ")) > 1 else ""
        else:
            continue
        if bad_word:
            bad.add(bad_word)
    return bad


def _check_hunspell_en(words: list[str]) -> set[str]:
    input_text = "\n".join(words)
    try:
        r = subprocess.run(
            ["hunspell", "-d", "en_US", "-l"],
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

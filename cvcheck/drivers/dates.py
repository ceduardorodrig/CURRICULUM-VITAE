from __future__ import annotations

import re
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "dates",
    "description": "Valida datas criticas em todos os arquivos",
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

DATE_PATTERNS: list[tuple[str, str]] = [
    (r"IPAM[^)]*?(\d{4})\s*[–-]\s*(\d{4})", "IPAM deve ser 2022–2025"),
    (r"Sumaenima[^)]*?(\d{4})\s*[–-]\s*(presente|present)", "Sumaenima deve comecar em 2016"),
    (r"StênioBOT[^)]*?(\d{4})\s*[–-]\s*(presente|present)", "StenioBOT deve comecar em 2024"),
    (r"(?:Rede de Monitoria|Monitoring Network)[^)]*?(\d{4})\s*[–-]\s*(\d{4})", "Rede de Monitoria deve ser 2020–2022"),
    (r"ISPN[^)]*?(\d{4})\s*[–-]\s*(\d{4})", "ISPN deve ser 2017–2021"),
    (r"UnB[^)]*?(\d{4})\s*[–-]\s*(\d{4})", "UnB graduacao deve ser 2016–2023"),
    (r"Mestrado[^)]*?(\d{4})\s*[–-]\s*(\d{4})", "Mestrado deve ser 2024–2025"),
]


def check() -> CheckResult:
    details = []

    for f in FILES:
        path = CVROOT / f
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")

        for pattern, desc in DATE_PATTERNS:
            for m in re.finditer(pattern, content, re.IGNORECASE):
                captured = m.groups()
                if f == "README.md" and "Sumaenima" in desc:
                    if captured[0] != "2016":
                        details.append(f"{f}: {desc} (encontrado {captured[0]})")
                elif "Sumaenima" in desc and "2016" in desc:
                    if captured[0] != "2016":
                        details.append(f"{f}: {desc} (encontrado {captured[0]})")
                elif "IPAM" in desc:
                    if captured[0] != "2022" or captured[1] != "2025":
                        details.append(f"{f}: {desc} (encontrado {captured[0]}–{captured[1]})")
                elif "Stenio" in desc:
                    if captured[0] != "2024":
                        details.append(f"{f}: {desc} (encontrado {captured[0]})")
                elif "Monitoria" in desc:
                    if captured[0] != "2020" or captured[1] != "2022":
                        details.append(f"{f}: {desc} (encontrado {captured[0]}–{captured[1]})")
                elif "ISPN" in desc:
                    if captured[0] != "2017" or captured[1] != "2021":
                        details.append(f"{f}: {desc} (encontrado {captured[0]}–{captured[1]})")
                elif "UnB" in desc and "graduacao" in desc:
                    if captured[0] != "2016" or captured[1] != "2023":
                        details.append(f"{f}: {desc} (encontrado {captured[0]}–{captured[1]})")
                elif "Mestrado" in desc:
                    if captured[0] != "2024" or captured[1] != "2025":
                        details.append(f"{f}: {desc} (encontrado {captured[0]}–{captured[1]})")

    if details:
        return CheckResult.fail("dates", f"{len(details)} data(s) incorreta(s)", details)

    return CheckResult.pass_("dates", f"{len(FILES)} arquivos conferidos, datas corretas")

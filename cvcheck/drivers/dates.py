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


def check() -> CheckResult:
    details = []

    for f in FILES:
        path = CVROOT / f
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        lines = content.split("\n")

        for i, line in enumerate(lines):
            stripped = line.strip()

            # IPAM
            if "IPAM" in stripped and stripped.startswith("##"):
                if i + 1 < len(lines):
                    m = re.search(r"\*(\d{4})\s*[–-]\s*(\d{4})", lines[i + 1])
                    if m and (m.group(1) != "2022" or m.group(2) != "2025"):
                        details.append(f"{f}: IPAM deve ser 2022–2025 (encontrado {m.group(1)}–{m.group(2)})")

            # ISPN
            if "ISPN" in stripped and stripped.startswith("##"):
                if i + 1 < len(lines):
                    m = re.search(r"\*(\d{4})\s*[–-]\s*(\d{4})", lines[i + 1])
                    if m and (m.group(1) != "2017" or m.group(2) != "2021"):
                        details.append(f"{f}: ISPN deve ser 2017–2021 (encontrado {m.group(1)}–{m.group(2)})")

            # UnB graduation: section header
            if stripped.startswith("##") and ("🎓" in stripped or "Formação" in stripped or "Education" in stripped or "Forma" in stripped):
                # Look for UnB in the next lines
                for j in range(i + 1, min(i + 6, len(lines))):
                    if "UnB" in lines[j] and ("Bacharelado" in lines[j] or "Bachelor" in lines[j] or "Sociai" in lines[j] or "Ciências" in lines[j]):
                        yr = re.search(r"(\d{4})\s*[–-]\s*(\d{4})", lines[j])
                        if yr and (yr.group(1) != "2016" or yr.group(2) != "2023"):
                            details.append(f"{f}: UnB graduacao deve ser 2016–2023 (encontrado {yr.group(1)}–{yr.group(2)})")
                        break

            # Rede de Monitoria
            if ("Rede de Monitoria" in stripped or "Monitoring Network" in stripped) and stripped.startswith("##"):
                date_next = re.search(r"(\d{4})\s*[–-]\s*(\d{4})", lines[i + 1] if i + 1 < len(lines) else "")
                if date_next and (date_next.group(1) != "2020" or date_next.group(2) != "2022"):
                    details.append(f"{f}: Rede de Monitoria deve ser 2020–2022 (encontrado {date_next.group(1)}–{date_next.group(2)})")

        # Sumaenima start 2016
        for line in content.split("\n"):
            if "Sumaenima" in line:
                m = re.search(r"\b(201[0-9]|202[0-9])\s*[–-]\s*", line)
                if m and m.group(1) != "2016":
                    details.append(f"{f}: Sumaenima deve comecar em 2016 (encontrado {m.group(1)})")

        # StênioBOT start 2024
        for line in content.split("\n"):
            if "StênioBOT" in line or "StenioBOT" in line:
                m = re.search(r"\b(201[0-9]|202[0-9])\s*[–-]\s*", line)
                if m and m.group(1) != "2024":
                    details.append(f"{f}: StenioBOT deve comecar em 2024 (encontrado {m.group(1)})")

        # Mestrado 2024-2025 (but NOT phone numbers)
        for line in content.split("\n"):
            if "Mestrado" in line or "Master's" in line:
                m = re.search(r"\((\d{4})\s*[–-]\s*(\d{4})\)", line)
                if m and (m.group(1) != "2024" or m.group(2) != "2025"):
                    details.append(f"{f}: Mestrado deve ser 2024–2025 (encontrado {m.group(1)}–{m.group(2)})")

    if details:
        return CheckResult.fail("dates", f"{len(details)} data(s) incorreta(s)", details)

    return CheckResult.pass_("dates", f"{len(FILES)} arquivos conferidos, datas corretas")

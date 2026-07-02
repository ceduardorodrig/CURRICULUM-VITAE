from __future__ import annotations

import subprocess
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "gov_consistency",
    "description": "Verifica se alteracoes em CVs foram refletidas no README e nas versoes correspondentes PT/EN",
}

CVROOT = Path(__file__).resolve().parents[2]

CV_PAIRS = [
    ("pt-br/01-tech-produto-dados.md", "en-us/01-tech-product-data.md"),
    ("pt-br/02-socioambiental-tech.md", "en-us/02-socioenvironmental-tech.md"),
    ("pt-br/03-sumaenima.md", "en-us/03-sumaenima.md"),
]

README_PATH = CVROOT / "README.md"
README_EN_PATH = CVROOT / "README.md"


def check() -> CheckResult:
    details = []
    modified = _get_modified_files()

    if not modified:
        return CheckResult.pass_("gov_consistency", "Nenhum arquivo modificado no working tree")

    modified_set = {str(m) for m in modified}

    for pt_rel, en_rel in CV_PAIRS:
        pt_path = str(CVROOT / pt_rel)
        en_path = str(CVROOT / en_rel)

        if pt_path in modified_set and en_path not in modified_set:
            details.append(
                f"{pt_rel}: modificado, mas {en_rel} nao foi. Se adicionou conteudo em PT, "
                "traduza para EN."
            )
        elif en_path in modified_set and pt_path not in modified_set:
            details.append(
                f"{en_rel}: modificado, mas {pt_rel} nao foi. Se adicionou conteudo em EN, "
                "atualize tambem o PT."
            )

    all_cv_modified = any(
        p in modified_set or e in modified_set for p, e in CV_PAIRS
    )

    if all_cv_modified:
        readme_modified = str(README_PATH) in modified_set
        if not readme_modified:
            modified_cvs = [
                p for p, e in CV_PAIRS
                if (str(CVROOT / p) in modified_set) or (str(CVROOT / e) in modified_set)
            ]
            details.append(
                f"README.md nao foi modificado, mas CV(s) {'/'.join(modified_cvs)} "
                "foram. Considere atualizar a secao Narrativa do README."
            )

    icmbio_path = str(CVROOT / "pt-br" / "02-socioambiental-nichado.md")
    socio_path = str(CVROOT / "pt-br" / "02-socioambiental-tech.md")

    if socio_path in modified_set and icmbio_path not in modified_set:
        details.append(
            "02-socioambiental-tech.md foi modificado, mas 02-socioambiental-nichado.md "
            "(sub-versao) nao. Se a mudanca for relevante, atualize a sub-versao."
        )

    if details:
        return CheckResult.warn(
            "gov_consistency",
            f"{len(details)} inconsistencia(s) entre arquivos",
            details,
        )

    return CheckResult.pass_(
        "gov_consistency", "Arquivos consistentes entre si"
    )


def _get_modified_files() -> list[Path]:
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=10,
        )
        if not r.stdout.strip():
            return []

        modified = []
        for line in r.stdout.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            status = line[:2].strip()
            filepath = line[3:]
            if status in ("M", "A", "??"):
                full_path = CVROOT / filepath
                if full_path.exists():
                    modified.append(full_path)
        return modified
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

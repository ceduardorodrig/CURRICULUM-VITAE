from __future__ import annotations

import hashlib
import json
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "gov_immutability",
    "description": "Verifica integridade dos scripts cvcheck via hashes SHA256",
}

CVROOT = Path(__file__).resolve().parents[2]
CVCHECK_DIR = CVROOT / "cvcheck"
HASH_FILE = CVROOT / "cvcheck" / ".cvcheck-hashes.json"

CRITICAL_FILES = [
    "__main__.py",
    "kernel/module.py",
    "include/types.py",
    "drivers/structure.py",
    "drivers/parity.py",
    "drivers/dates.py",
    "drivers/links.py",
    "drivers/spell_pt.py",
    "drivers/spell_en.py",
    "drivers/sec_bypass_guard.py",
    "drivers/sec_scope_guard.py",
    "drivers/gov_immutability.py",
    "drivers/gov_glossary.py",
    "drivers/gov_acronyms.py",
    "drivers/gov_bilingual.py",
    "drivers/gov_self_audit.py",
    "drivers/gov_consistency.py",
    "drivers/gov_image_assets.py",
    "drivers/gov_orphan_lines.py",
    "drivers/gov_toc.py",
]


def check() -> CheckResult:
    details = []

    if not HASH_FILE.exists():
        _save_baseline()
        return CheckResult.warn(
            "gov_immutability",
            "Baseline de hashes nao existia. Criado agora. Execute novamente para verificar.",
        )

    baseline = json.loads(HASH_FILE.read_text(encoding="utf-8"))
    current_hashes: dict[str, str] = {}

    for rel in CRITICAL_FILES:
        path = CVCHECK_DIR / rel
        if not path.exists():
            details.append(f"Arquivo critico ausente: cvcheck/{rel}")
            continue
        h = _file_hash(path)
        current_hashes[rel] = h

        if rel in baseline:
            if baseline[rel] != h:
                details.append(f"cvcheck/{rel}: HASH ALTERADO (possivel modificacao nao autorizada)")
        else:
            details.append(f"cvcheck/{rel}: novo arquivo nao registrado no baseline")

    if details:
        result = CheckResult.fail("gov_immutability", f"{len(details)} alteracao(oes) nos scripts cvcheck", details)
        result._fix_fn = _rebuild_baseline
        return result

    return CheckResult.pass_("gov_immutability", f"{len(CRITICAL_FILES)} arquivos cvcheck intactos, hashes conferidos")


def _rebuild_baseline() -> None:
    _save_baseline()


def _save_baseline() -> None:
    hashes: dict[str, str] = {}
    for rel in CRITICAL_FILES:
        path = CVCHECK_DIR / rel
        if path.exists():
            hashes[rel] = _file_hash(path)
    HASH_FILE.write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

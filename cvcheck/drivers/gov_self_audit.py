from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path

from cvcheck.include.types import CheckResult, CheckStatus

CHECK_METADATA = {
    "name": "gov_self_audit",
    "description": "Auto-auditoria do kernel cvcheck — importabilidade, metadata, drivers nao registrados, dead code",
}

CVROOT = Path(__file__).resolve().parents[2]
DRIVERS_DIR = CVROOT / "cvcheck" / "drivers"


def check() -> CheckResult:
    details = []

    import_errors = _check_importability()
    details.extend(import_errors)

    meta_errors = _check_metadata()
    details.extend(meta_errors)

    dead_code = _check_dead_code()
    details.extend(dead_code)

    baseline_gaps = _check_baseline_gaps()
    details.extend(baseline_gaps)

    if details:
        return CheckResult.fail("gov_self_audit", f"{len(details)} anomalia(s) interna(s)", details)

    return CheckResult.pass_("gov_self_audit", "Kernel cvcheck integro — 0 anomalias")


def _discover_py_files() -> dict[str, Path]:
    result: dict[str, Path] = {}
    for p in sorted(DRIVERS_DIR.rglob("*.py")):
        if p.name == "__init__.py":
            continue
        result[p.stem] = p
    return result


def _check_importability() -> list[str]:
    details = []
    for name, path in _discover_py_files().items():
        module_name = f"cvcheck.drivers.{name}"
        if module_name in sys.modules:
            continue
        spec = importlib.util.spec_from_file_location(module_name, path)
        if not spec or not spec.loader:
            details.append(f"{name}.py: spec nao carregavel")
            continue
        try:
            mod = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = mod
            spec.loader.exec_module(mod)
        except Exception as e:
            details.append(f"{name}.py: erro ao importar — {e}")
    return details


def _check_metadata() -> list[str]:
    details = []
    for name, path in _discover_py_files().items():
        module_name = f"cvcheck.drivers.{name}"
        mod = sys.modules.get(module_name)
        if mod is None:
            continue
        metadata = getattr(mod, "CHECK_METADATA", None)
        if metadata is None:
            details.append(f"{name}.py: sem CHECK_METADATA")
            continue
        if not isinstance(metadata, dict):
            details.append(f"{name}.py: CHECK_METADATA nao e dict")
            continue
        if "name" not in metadata:
            details.append(f"{name}.py: CHECK_METADATA sem 'name'")
        if "description" not in metadata:
            details.append(f"{name}.py: CHECK_METADATA sem 'description'")
        check_fn = getattr(mod, "check", None)
        if check_fn is None:
            details.append(f"{name}.py: sem funcao check()")
        elif not callable(check_fn):
            details.append(f"{name}.py: check() nao e callable")
    return details


def _check_dead_code() -> list[str]:
    details = []
    for name, path in _discover_py_files().items():
        module_name = f"cvcheck.drivers.{name}"
        mod = sys.modules.get(module_name)
        if mod is None:
            continue
        source = inspect.getsource(mod)
        all_funcs = [n for n, _ in inspect.getmembers(mod, inspect.isfunction)]
        for fn_name in all_funcs:
            if fn_name.startswith("_"):
                continue
            if fn_name in ("check",):
                continue
            refs = source.count(fn_name)
            if refs <= 1 and fn_name != "main":
                details.append(f"{name}.py: funcao '{fn_name}' definida mas nunca chamada (dentro do proprio modulo)")
    return details


def _check_baseline_gaps() -> list[str]:
    gaps = []
    try:
        hash_file = CVROOT / "cvcheck" / ".cvcheck-hashes.json"
        if not hash_file.exists():
            return []
        import json, hashlib
        baseline = json.loads(hash_file.read_text(encoding="utf-8"))

        for name, path in _discover_py_files().items():
            rel = f"drivers/{path.name}"
            if rel not in baseline:
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                gaps.append(f"{rel}: presente no disco, ausente no baseline (hash={actual[:12]}...)")

        for rel in baseline:
            if rel.startswith("drivers/"):
                path = DRIVERS_DIR / Path(rel).name
                if not path.exists():
                    gaps.append(f"{rel}: no baseline mas ausente no disco")
    except Exception:
        pass
    return gaps

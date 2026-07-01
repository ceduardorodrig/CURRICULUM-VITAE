from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

from cvcheck.include.types import CheckResult

CVROOT = Path(__file__).resolve().parents[2]
DRIVERS_DIR = CVROOT / "cvcheck" / "drivers"

CHECK_METADATA_KEY = "CHECK_METADATA"
CHECK_FN_NAME = "check"


def discover_drivers() -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}

    for driver_path in sorted(DRIVERS_DIR.rglob("*.py")):
        if driver_path.name == "__init__.py":
            continue

        rel = driver_path.relative_to(DRIVERS_DIR)
        module_name = "cvcheck.drivers." + str(rel.with_suffix("")).replace("/", ".")

        spec = importlib.util.spec_from_file_location(module_name, driver_path)
        if not spec or not spec.loader:
            continue

        try:
            mod = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = mod
            spec.loader.exec_module(mod)
        except Exception as e:
            registry[str(rel)] = {"error": str(e), "check": None, "metadata": {}}
            continue

        metadata = getattr(mod, CHECK_METADATA_KEY, {})
        check_fn = getattr(mod, CHECK_FN_NAME, None)

        if check_fn is None or not callable(check_fn):
            continue

        name = metadata.get("name", rel.with_suffix("").name)
        registry[name] = {
            "name": name,
            "metadata": metadata,
            "check": check_fn,
            "path": driver_path,
        }

    return registry


def run_single(driver: dict[str, Any]) -> CheckResult:
    import time
    check_fn = driver.get("check")
    name = driver.get("name", "unknown")
    if check_fn is None:
        return CheckResult.error(name, "check function not loaded")

    start = time.perf_counter()
    try:
        result = check_fn()
    except Exception as e:
        result = CheckResult.error(name, f"{type(e).__name__}: {e}")

    elapsed = (time.perf_counter() - start) * 1000
    result.duration_ms = round(elapsed, 1)
    return result

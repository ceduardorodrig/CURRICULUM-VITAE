from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

CVROOT = Path(__file__).resolve().parents[2]
HISTORY_FILE = CVROOT / "cvcheck" / ".cvcheck-history.json"
MAX_HISTORY = 20


def save_run(history: dict[str, list[dict]]) -> None:
    HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_history() -> dict[str, list[dict]]:
    if not HISTORY_FILE.exists():
        return {}
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def record_result(name: str, result: str, duration_ms: float) -> None:
    history = load_history()
    entry = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "result": result,
        "duration_ms": duration_ms,
    }
    history.setdefault(name, []).append(entry)
    history[name] = history[name][-MAX_HISTORY:]
    save_run(history)


def trend(name: str, history: dict[str, list[dict]] | None = None) -> tuple[str, str]:
    if history is None:
        history = load_history()
    entries = history.get(name, [])
    if len(entries) < 2:
        return ("➖", "poucos dados")

    last_5 = [e["result"] for e in entries[-5:]]
    last_3 = last_5[-3:]

    all_pass = all(r == "PASS" for r in last_3)
    all_fail = all(r in ("FAIL", "ERROR") for r in last_3)

    if all_pass:
        if len(last_5) >= 3 and all(r == "PASS" for r in last_5[-3:]):
            return ("✅", "estavel (3+ PASS)")
        return ("✅", "estavel")

    if all_fail:
        return ("❌", "falhas consecutivas")

    if len(last_5) >= 4:
        osc = Counter(last_5)
        if osc.get("PASS", 0) >= 2 and osc.get("FAIL", 0) >= 1:
            return ("⚠️", "oscilante (flaky)")

    last_2 = last_5[-2:]
    if last_2 == ["FAIL", "PASS"] or last_2 == ["ERROR", "PASS"]:
        return ("📈", "recuperou")
    if last_2 == ["PASS", "FAIL"] or last_2 == ["PASS", "ERROR"]:
        return ("📉", "piorou")

    return ("➖", "dados insuficientes")

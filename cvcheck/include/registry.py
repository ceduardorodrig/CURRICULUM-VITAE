from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

CVROOT = Path(__file__).resolve().parents[2]
REGISTRY_FILE = CVROOT / "cvcheck" / ".cvcheck-registry.json"


class Registry:
    def __init__(self) -> None:
        self.permanent: dict[str, list[str]] = {}
        self.negative: dict[str, list[str]] = {}
        self._load()

    def _load(self) -> None:
        if not REGISTRY_FILE.exists():
            return
        try:
            data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
            self.permanent = data.get("permanent", {})
            self.negative = data.get("negative", {})
        except (json.JSONDecodeError, OSError):
            self.permanent = {}
            self.negative = {}

    def _save(self) -> None:
        data = {
            "permanent": self.permanent,
            "negative": self.negative,
        }
        REGISTRY_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def record_permanent(self, driver: str, note: str) -> None:
        self.permanent.setdefault(driver, []).append(f"[{_now()}] {note}")
        self._save()

    def record_negative(self, driver: str, note: str) -> None:
        self.negative.setdefault(driver, []).append(f"[{_now()}] {note}")
        self._save()

    def is_negative(self, driver: str, note_fragment: str) -> bool:
        for entry in self.negative.get(driver, []):
            if note_fragment in entry:
                return True
        return False

    def summary(self) -> list[str]:
        lines = []
        for driver, notes in sorted(self.permanent.items()):
            lines.append(f"{driver}: {len(notes)} fix(es) permanentes")
        for driver, notes in sorted(self.negative.items()):
            lines.append(f"{driver}: {len(notes)} fix(es) com falha")
        return lines


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

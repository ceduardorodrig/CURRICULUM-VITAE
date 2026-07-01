from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CheckStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"
    ERROR = "ERROR"
    SKIP = "SKIP"


@dataclass
class CheckResult:
    name: str
    status: CheckStatus
    summary: str
    details: list[str] = field(default_factory=list)
    duration_ms: float = 0

    @classmethod
    def pass_(cls, name: str, summary: str, details: list[str] | None = None) -> CheckResult:
        return cls(name=name, status=CheckStatus.PASS, summary=summary, details=details or [])

    @classmethod
    def fail(cls, name: str, summary: str, details: list[str] | None = None) -> CheckResult:
        return cls(name=name, status=CheckStatus.FAIL, summary=summary, details=details or [])

    @classmethod
    def warn(cls, name: str, summary: str, details: list[str] | None = None) -> CheckResult:
        return cls(name=name, status=CheckStatus.WARN, summary=summary, details=details or [])

    @classmethod
    def error(cls, name: str, exception: str) -> CheckResult:
        return cls(name=name, status=CheckStatus.ERROR, summary=f"Exception: {exception}", details=[exception])

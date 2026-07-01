from __future__ import annotations

import re
import subprocess
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "sec_bypass_guard",
    "description": "Detecta tentativas de bypass da verificacao (--no-verify, || true, etc.)",
}

CVROOT = Path(__file__).resolve().parents[2]
HOOKS_DIR = CVROOT / ".git" / "hooks"


def check() -> CheckResult:
    details = []

    if not (CVROOT / ".git").is_dir():
        return CheckResult.skip("sec_bypass_guard", "Nao e um repositorio git")

    bypass_patterns = _scan_git_log()
    if bypass_patterns:
        details.extend(bypass_patterns)

    if not _is_ci():
        hook_status = _check_hooks()
        if hook_status:
            details.extend(hook_status)

        env_bypass = _check_env_bypass()
        if env_bypass:
            details.extend(env_bypass)

    ci_bypass = _check_ci_bypass()
    if ci_bypass:
        details.extend(ci_bypass)

    if details:
        return CheckResult.fail("sec_bypass_guard", f"{len(details)} indicio(s) de bypass", details)

    return CheckResult.pass_("sec_bypass_guard", "Nenhum indicio de bypass detectado")


def _is_ci() -> bool:
    return "CI" in __import__("os").environ or "GITHUB_ACTIONS" in __import__("os").environ


def _scan_git_log() -> list[str]:
    details = []
    try:
        r = subprocess.run(
            ["git", "log", "--oneline", "--since=7.days", "--format=%H %s"],
            capture_output=True, text=True, timeout=10,
        )
        for line in r.stdout.strip().split("\n"):
            if not line.strip():
                continue
            commit_hash = line.split()[0]
            msg = line[len(commit_hash):].strip().lower()
            bypass_markers = ["no-verify", "skip-ci", "check skipped", "bypass cvcheck", "temp: skip"]
            for marker in bypass_markers:
                if marker in msg:
                    details.append(f"Commit suspeito {commit_hash[:8]}: '{msg[:60]}' contem '{marker}'")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return details


def _check_hooks() -> list[str]:
    details = []
    pre_push = HOOKS_DIR / "pre-push"
    if not pre_push.exists():
        details.append("Hook pre-push nao encontrado em .git/hooks/pre-push")
        return details

    try:
        content = pre_push.read_text(encoding="utf-8")
        if "cvcheck" not in content:
            details.append("Hook pre-push existe mas nao executa cvcheck")
    except Exception:
        details.append("Nao foi possivel ler .git/hooks/pre-push")

    for hook_name in ["pre-commit", "commit-msg", "pre-push"]:
        hook_path = HOOKS_DIR / hook_name
        if not hook_path.exists():
            continue
        try:
            stat = hook_path.stat()
            if not (stat.st_mode & 0o100):
                details.append(f"Hook {hook_name} existe mas nao tem permissao de execucao")
        except Exception:
            pass

    for suspicious in ["pre-commit.bak", "pre-commit.old", "pre-commit.disabled"]:
        if (HOOKS_DIR / suspicious).exists():
            details.append(f"Arquivo suspeito encontrado: .git/hooks/{suspicious}")

    return details


def _check_env_bypass() -> list[str]:
    details = []
    try:
        r = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            capture_output=True, text=True, timeout=5,
        )
        if r.stdout.strip():
            alt_path = r.stdout.strip()
            if str(CVROOT / ".git" / "hooks") not in alt_path:
                details.append(f"hooksPath redirecionado para {alt_path}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return details


def _check_ci_bypass() -> list[str]:
    details = []
    ci_path = CVROOT / ".github" / "workflows"
    if not ci_path.is_dir():
        return details

    for yml in sorted(ci_path.rglob("*.yml")):
        content = yml.read_text(encoding="utf-8", errors="replace")
        if "continue-on-error: true" in content:
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                if "continue-on-error: true" in line:
                    context_before = lines[max(0, i - 3):i]
                    context_str = " ".join(c.strip() for c in context_before)
                    if "cvcheck" in context_str.lower():
                        details.append(f"{yml.relative_to(CVROOT)}:L{i} continue-on-error: true em step cvcheck")
    return details

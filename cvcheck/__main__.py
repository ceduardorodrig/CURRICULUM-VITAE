"""
cvcheck — Verificação de currículos CVR (Curriculum Vitae Repository).

Uso:
  python -m cvcheck                        # todas as verificações
  python -m cvcheck --list                 # listar drivers
  python -m cvcheck --only structure       # apenas um driver
  python -m cvcheck --quiet                # menos verbosidade
  python -m cvcheck --health               # dashboard de saude
  python -m cvcheck --blame                # git blame nas falhas
  python -m cvcheck --self-test            # auto-teste do kernel
  python -m cvcheck --fix                  # tenta corrigir automaticamente
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from cvcheck.kernel.module import discover_drivers, run_single, CVROOT
from cvcheck.include.history import load_history, record_result, trend
from cvcheck.include.registry import Registry

STATUS_ICONS = {
    "PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "ERROR": "💥", "SKIP": "⏭️",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="cvcheck — Curriculum Vitae Checker")
    parser.add_argument("--list", action="store_true", help="Listar drivers disponiveis")
    parser.add_argument("--only", help="Executar apenas um driver especifico")
    parser.add_argument("--quiet", action="store_true", help="Menos verbosidade")
    parser.add_argument("--health", action="store_true", help="Dashboard de saude do repositorio")
    parser.add_argument("--blame", action="store_true", help="Git blame nas violacoes")
    parser.add_argument("--self-test", action="store_true", help="Auto-teste do kernel cvcheck")
    parser.add_argument("--fix", action="store_true", help="Tenta corrigir violacoes automaticamente")
    args = parser.parse_args()

    if args.list:
        return _list_drivers()

    if args.self_test:
        return _self_test()

    if args.health:
        return _health_check()

    drivers = discover_drivers()

    if args.only:
        if args.only not in drivers:
            print(f"❌ Driver '{args.only}' nao encontrado. Use --list para ver os disponiveis.")
            return 1
        drivers = {args.only: drivers[args.only]}

    results = _run_all(drivers, args.quiet)

    if args.blame:
        _run_blame(results)

    if args.fix:
        _run_fix(results)

    passed = sum(1 for r in results if r.status.value == "PASS")
    failed = sum(1 for r in results if r.status.value in ("FAIL", "ERROR"))
    warned = sum(1 for r in results if r.status.value == "WARN")
    skipped = sum(1 for r in results if r.status.value == "SKIP")

    if not args.quiet:
        print(f"\n{'='*50}")
        print(f"  ✅ {passed} pass | ❌ {failed} fail | ⚠️  {warned} warn | ⏭️  {skipped} skip")

    return 1 if failed > 0 else 0


def _list_drivers() -> int:
    drivers = discover_drivers()
    print(f"\n📋 {len(drivers)} drivers disponiveis:\n")
    for name, d in sorted(drivers.items()):
        meta = d.get("metadata", {})
        desc = meta.get("description", "")
        print(f"  {name:30s}  {desc}")
    print()
    return 0


def _run_all(drivers: dict, quiet: bool) -> list:
    total = len(drivers)
    results = []
    start = time.perf_counter()

    if not quiet:
        print(f"\n🔍 Executando {total} driver(s)...\n")

    with ThreadPoolExecutor(max_workers=total or 1) as executor:
        future_map = {executor.submit(run_single, d): name for name, d in drivers.items()}
        for future in as_completed(future_map):
            name = future_map[future]
            result = future.result()
            results.append(result)
            icon = STATUS_ICONS.get(result.status.value, "❓")
            dur = f"({result.duration_ms:.0f}ms)" if result.duration_ms else ""
            if not quiet:
                print(f"  {icon} {result.name:25s} {result.summary[:90]} {dur}")
                for d in result.details[:3]:
                    print(f"    · {d}")

    for r in results:
        record_result(r.name, r.status.value, r.duration_ms)

    elapsed = time.perf_counter() - start
    if not quiet:
        print(f"\n  ⏱️  {elapsed:.2f}s")
    return results


def _run_blame(results: list) -> None:
    print("\n🔍 SELF-DIAGNOSIS (git blame):")
    blame_found = False
    for r in results:
        if r.status.value not in ("FAIL", "ERROR"):
            continue
        for detail in r.details:
            for token in detail.split():
                if "/" in token and token.endswith(".md"):
                    parts = token.split(":")
                    filepath = parts[0]
                    try:
                        bp = subprocess.run(
                            ["git", "blame", "--since=30.days", filepath],
                            capture_output=True, text=True, timeout=10,
                        )
                        if bp.stdout.strip():
                            lines = bp.stdout.strip().split("\n")
                            print(f"  {filepath}:")
                            for l in lines[:3]:
                                print(f"    {l[:100]}")
                            blame_found = True
                    except Exception:
                        pass
    if not blame_found:
        print("  Nenhum arquivo modificado recentemente encontrado nas falhas.")
    print()


def _run_fix(results: list) -> None:
    print("\n🔧 AUTO-FIX:")
    registry = Registry()
    fixed = 0
    for r in results:
        if r.status.value in ("FAIL", "ERROR", "WARN") and hasattr(r, "_fix_fn"):
            try:
                r._fix_fn()
                registry.record_permanent(r.name, "auto-fix applied")
                print(f"  ✅ {r.name}: corrigido")
                fixed += 1
            except Exception as e:
                registry.record_negative(r.name, f"auto-fix failed: {e}")
                print(f"  ❌ {r.name}: erro na correcao: {e}")

    reg_summary = registry.summary()
    if reg_summary:
        print(f"\n  📊 Registry:")
        for line in reg_summary:
            print(f"    {line}")

    if fixed == 0:
        print("  Nenhuma correcao automatica disponivel para as falhas encontradas.")
    print()


def _self_test() -> int:
    print("\n🧪 AUTO-TESTE DO KERNEL cvcheck:\n")
    failures = 0

    tests = [
        ("Descoberta de drivers", _test_discovery),
        ("Import dos modulos", _test_imports),
        ("CheckResult interface", _test_checkresult),
        ("Hashes do kernel", _test_hashes),
        ("Registry integridade", _test_registry),
        ("History integridade", _test_history),
    ]

    for name, fn in tests:
        try:
            fn()
            print(f"  ✅ {name}")
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failures += 1

    print(f"\n  {'✅ Todos os testes passaram' if failures == 0 else f'❌ {failures} falha(s)'}\n")
    return 1 if failures > 0 else 0


def _test_discovery() -> None:
    drivers = discover_drivers()
    assert len(drivers) >= 3, f"Esperado >=3 drivers, encontrado {len(drivers)}"


def _test_imports() -> None:
    from cvcheck.include.types import CheckResult, CheckStatus
    from cvcheck.kernel.module import discover_drivers, run_single
    assert CheckResult is not None
    assert CheckStatus is not None
    assert callable(discover_drivers)
    assert callable(run_single)


def _test_checkresult() -> None:
    from cvcheck.include.types import CheckResult, CheckStatus
    r = CheckResult.pass_("test", "ok")
    assert r.status == CheckStatus.PASS
    assert r.name == "test"
    r = CheckResult.fail("test", "fail")
    assert r.status == CheckStatus.FAIL
    assert len(r.details) == 0


def _test_hashes() -> None:
    hash_file = CVROOT / "cvcheck" / ".cvcheck-hashes.json"
    if not hash_file.exists():
        return
    import json
    hashes = json.loads(hash_file.read_text(encoding="utf-8"))
    assert len(hashes) > 0, "Nenhum hash registrado"


def _test_registry() -> None:
    from cvcheck.include.registry import Registry
    r = Registry()
    assert r is not None
    assert hasattr(r, "permanent")
    assert hasattr(r, "negative")


def _test_history() -> None:
    from cvcheck.include.history import load_history, record_result, trend
    h = load_history()
    assert isinstance(h, dict)
    prev = len(h.get("gov_self_audit", []))
    record_result("gov_self_audit", "PASS", 1.0)
    h2 = load_history()
    assert len(h2.get("gov_self_audit", [])) == prev + 1
    t_icon, t_desc = trend("gov_self_audit", h2)
    assert t_icon in ("✅", "📈", "📉", "⚠️", "➖", "❌")


def _health_check() -> int:
    print("\n🏥 DASHBOARD DE SAUDE DO REPOSITORIO:\n")

    md_files = list(CVROOT.rglob("*.md"))
    print(f"  📄 Arquivos .md: {len(md_files)}")

    git_status = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, timeout=10,
    )
    modified = len([l for l in git_status.stdout.strip().split("\n") if l.strip()])
    print(f"  📝 Arquivos modificados: {modified}")

    try:
        r = subprocess.run(["git", "log", "--oneline", "-1"], capture_output=True, text=True, timeout=5)
        last_commit = r.stdout.strip()[:60]
        print(f"  🔖 Ultimo commit: {last_commit}")
    except Exception:
        pass

    cvcheck_size = sum(p.stat().st_size for p in CVROOT.rglob("*.py") if "cvcheck" in str(p))
    print(f"  ⚙️  Tamanho total cvcheck: {cvcheck_size / 1024:.1f} KB")

    registry = Registry()
    reg_summary = registry.summary()
    if reg_summary:
        print(f"\n  📊 Registry de Fixes:")
        for line in reg_summary:
            print(f"    {line}")

    history = load_history()
    if history:
        print(f"\n  📈 Tendencias por driver:")
        drivers = discover_drivers()
        for name in sorted(history):
            if name not in drivers:
                continue
            t_icon, t_desc = trend(name, history)
            entries = history[name]
            last_result = entries[-1]["result"] if entries else "?"
            icon = STATUS_ICONS.get(last_result, "❓")
            print(f"    {icon} {name:25s} {t_icon} {t_desc}")

    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

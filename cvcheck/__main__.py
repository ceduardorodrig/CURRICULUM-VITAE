"""
cvcheck — Verificação de currículos CVR (Curriculum Vitae Repository).

Uso:
  python -m cvcheck                        # todas as verificações
  python -m cvcheck --list                 # listar drivers
  python -m cvcheck --only structure       # apenas um driver
  python -m cvcheck --quiet                # menos verbosidade
"""
from __future__ import annotations

import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from cvcheck.kernel.module import discover_drivers, run_single


def main() -> int:
    parser = argparse.ArgumentParser(description="cvcheck — Curriculum Vitae Checker")
    parser.add_argument("--list", action="store_true", help="Listar drivers disponiveis")
    parser.add_argument("--only", help="Executar apenas um driver especifico")
    parser.add_argument("--quiet", action="store_true", help="Menos verbosidade")
    args = parser.parse_args()

    drivers = discover_drivers()

    if args.list:
        print(f"\n📋 {len(drivers)} drivers disponiveis:\n")
        for name, d in sorted(drivers.items()):
            meta = d.get("metadata", {})
            desc = meta.get("description", "")
            print(f"  {name:25s}  {desc}")
        print()
        return 0

    if args.only:
        if args.only not in drivers:
            print(f"❌ Driver '{args.only}' nao encontrado. Use --list para ver os disponiveis.")
            return 1
        drivers = {args.only: drivers[args.only]}

    total = len(drivers)
    if not args.quiet:
        print(f"\n🔍 Executando {total} driver(s)...\n")

    results = []
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=total) as executor:
        future_map = {executor.submit(run_single, d): name for name, d in drivers.items()}
        for future in as_completed(future_map):
            name = future_map[future]
            result = future.result()
            results.append(result)

            status_icon = {
                "PASS": "✅",
                "FAIL": "❌",
                "WARN": "⚠️",
                "ERROR": "💥",
                "SKIP": "⏭️",
            }.get(result.status.value, "❓")

            dur = f"({result.duration_ms:.0f}ms)" if result.duration_ms else ""
            if not args.quiet:
                print(f"  {status_icon} {result.name:25s} {result.summary[:100]} {dur}")
                for d in result.details[:5]:
                    print(f"    · {d}")

    elapsed = time.perf_counter() - start
    passed = sum(1 for r in results if r.status.value == "PASS")
    failed = sum(1 for r in results if r.status.value in ("FAIL", "ERROR"))
    warned = sum(1 for r in results if r.status.value == "WARN")
    skipped = sum(1 for r in results if r.status.value == "SKIP")

    if not args.quiet:
        print(f"\n{'='*50}")
        print(f"  ✅ {passed} pass | ❌ {failed} fail | ⚠️  {warned} warn | ⏭️  {skipped} skip")
        print(f"  ⏱️  {elapsed:.2f}s\n")

    return 1 if failed > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())

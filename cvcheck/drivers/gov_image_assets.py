from __future__ import annotations

import subprocess
from pathlib import Path

from cvcheck.include.types import CheckResult

CHECK_METADATA = {
    "name": "gov_image_assets",
    "description": "Verifica se imagens em assets/ sao JPEG Q90 com borda maxima 2K (2560px)",
}

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"
MAX_EDGE = 2560
ALLOWED_EXTENSIONS = {".jpg", ".jpeg"}
SKIP_PREFIXES = {"hub-", "logo-"}
SKIP_EXTENSIONS = {".svg", ".ico"}


def check() -> CheckResult:
    details = []
    images = sorted(ASSETS_DIR.rglob("*"))

    if not images:
        return CheckResult.skip("gov_image_assets", "Nenhum arquivo em assets/")

    for img_path in images:
        if not img_path.is_file():
            continue

        if img_path.suffix.lower() in SKIP_EXTENSIONS:
            continue

        if any(img_path.name.startswith(p) for p in SKIP_PREFIXES):
            continue

        ext = img_path.suffix.lower()
        if ext in ALLOWED_EXTENSIONS:
            dims = _get_dimensions(img_path)
            if dims:
                w, h = dims
                longest = max(w, h)
                if longest > MAX_EDGE:
                    details.append(
                        f"{img_path.name}: {w}x{h} — borda maior {longest}px > {MAX_EDGE}px"
                    )
        else:
            if ext in (".png", ".tif", ".tiff", ".bmp", ".gif", ".webp"):
                details.append(
                    f"{img_path.name}: formato {ext.upper()} nao permitido — use JPEG (.jpg)"
                )
            elif ext in (".svg", ".ico"):
                continue
            else:
                continue

    # Heuristic: JPEG > 5MB at 2K is probably not Q90
    for img_path in images:
        if not img_path.is_file():
            continue
        if img_path.suffix.lower() in SKIP_EXTENSIONS:
            continue
        if any(img_path.name.startswith(p) for p in SKIP_PREFIXES):
            continue
        if img_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        size_mb = img_path.stat().st_size / (1024 * 1024)
        dims = _get_dimensions(img_path)
        if dims:
            mega_pixels = (dims[0] * dims[1]) / 1_000_000
            if mega_pixels <= 5 and size_mb > 5:
                details.append(
                    f"{img_path.name}: {size_mb:.1f}MB para {dims[0]}x{dims[1]} — "
                    "provalvemente nao e Q90"
                )

    if details:
        return CheckResult.fail(
            "gov_image_assets",
            f"{len(details)} imagem(ns) fora do padrao",
            details,
        )

    return CheckResult.pass_(
        "gov_image_assets",
        f"{_count_jpegs(images)} imagens JPEG dentro do padrao 2K",
    )


def _count_jpegs(images: list[Path]) -> int:
    return sum(1 for p in images if p.suffix.lower() in ALLOWED_EXTENSIONS)


def _get_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        r = subprocess.run(
            ["identify", "-format", "%w %h", str(path)],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode == 0 and r.stdout.strip():
            parts = r.stdout.strip().split()
            return int(parts[0]), int(parts[1])
    except Exception:
        pass
    return None

#!/usr/bin/env bash
# Локальный предпросмотр всего сайта (основной + раздел Gonka).
#
# ВАЖНО: `mkdocs serve` здесь НЕ подходит — он обслуживает только основной
# mkdocs.yml, в котором раздел Gonka исключён (exclude_docs) и собирается
# отдельно. Поэтому для полного предпросмотра собираем сайт через build.sh
# и отдаём статику под тем же префиксом, что и на GitHub Pages (/gonkadocs/).
#
# Открой: http://127.0.0.1:8000/gonkadocs/
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_DIR="$ROOT/_site"
PORT="${1:-8000}"

# 1. Полная сборка.
bash "$ROOT/buildtools/build.sh"

# 2. Эмулируем префикс /gonkadocs/ через временный каталог с симлинком.
SERVE_ROOT="$(mktemp -d)"
chmod 755 "$SERVE_ROOT"
ln -s "$SITE_DIR" "$SERVE_ROOT/gonkadocs"
trap 'rm -rf "$SERVE_ROOT"' EXIT

echo
echo "==> Открой: http://127.0.0.1:${PORT}/gonkadocs/"
echo "==> Ctrl+C для остановки"
cd "$SERVE_ROOT"
python3 -m http.server "$PORT"

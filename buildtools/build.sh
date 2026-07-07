#!/usr/bin/env bash
# Сборка сайта gonkadocs.
#
# Сайт состоит из двух независимых сборок MkDocs, объединённых в одном
# каталоге публикации (_site):
#
#   1. Основной сайт  (Главная + Обсуждения + Сообщество + Proposals)
#      -> собирается корневым mkdocs.yml в _site/
#
#   2. Раздел "Gonka" -> ТОЧНАЯ копия документации gonka-ai/gonka-docs.
#      Собирается её РОДНЫМ mkdocs.yml (с плагином i18n: en + zh), который
#      синхронизируется экшеном sync-gonka-ai-docs.yml. Благодаря этому раздел
#      выглядит 1-в-1 как оригинал и автоматически подхватывает любые изменения
#      структуры/навигации/материалов оригинала -> _site/gonka/
#
# Порядок важен: основной сайт собирается ПЕРВЫМ (mkdocs build --clean стирает
# весь site_dir). Сборка Gonka идёт во вложенный каталог _site/gonka и чистит
# только его, не трогая остальной сайт.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_DIR="$ROOT/_site"

echo "==> [0/7] Генерация llms.txt и llms-full.txt для AI-агентов"
python3 "$ROOT/buildtools/generate-llms.py"
python3 "$ROOT/buildtools/generate-llms-full.py"

echo "==> [1/7] Сборка основного сайта -> $SITE_DIR"
cd "$ROOT"
python3 -m mkdocs build --clean --site-dir "$SITE_DIR"

echo "==> [2/7] Сборка раздела Gonka (родной конфиг оригинала, i18n en+zh) -> $SITE_DIR/gonka/docs"
cd "$ROOT/docs/gonka/docs"

# В оригинале docs/index.md — это ЛЕНДИНГ gonka.ai (template home.html), а не
# документация. Сам оригинал при сборке /docs/ подменяет index.md на
# introduction.md (см. его buildtools/prepare-stages.sh). Повторяем это: на
# время сборки промотируем introduction.md -> index.md, после сборки
# восстанавливаем исходные файлы, чтобы не портить синканутый репозиторий.
DOCS="docs"
declare -a _restore=()
_swap_intro() {
  local dir="$1"            # "" для en, "zh/" для zh
  local idx="$DOCS/${dir}index.md"
  local intro="$DOCS/${dir}introduction.md"
  if [ -f "$intro" ]; then
    if [ -f "$idx" ]; then
      cp "$idx" "$idx.landing.bak"
      _restore+=("$idx")
    fi
    cp "$intro" "$idx"
  fi
}
_restore_intro() {
  for idx in "${_restore[@]}"; do
    if [ -f "$idx.landing.bak" ]; then
      mv "$idx.landing.bak" "$idx"
    fi
  done
}
trap _restore_intro EXIT

_swap_intro ""
_swap_intro "zh/"

# Переопределяем site_url для корректной работы i18n переключателя.
# Оригинальный site_url указывает на gonka.ai — это ломает ссылки на zh/lang
# при развёртывании под путём /gonkadocs/gonka/docs/. Создаём временную копию
# конфига с исправленным site_url и собираем по ней.
SITE_URL="https://gonkadocs.com/gonka/docs/"
BUILD_CFG=".mkdocs.yml.build"

# Мержим overrides: upstream originals + наши shared-шаблоны.
# mkdocs-material подхватывает custom_dir как overlay поверх стандартной темы.
# Наш overrides идёт вторым → перезаписывает header upstream'а на наш shared.
OVR_DIR=".overrides.merged"
rm -rf "$OVR_DIR"
cp -r overrides "$OVR_DIR"
cp -r "$ROOT/buildtools/gonka-overrides/"* "$OVR_DIR/"

sed -e "s|site_url: .*|site_url: ${SITE_URL}|" \
    -e "s|custom_dir: overrides|custom_dir: ${OVR_DIR}|" \
    mkdocs.yml > "$BUILD_CFG"
python3 -m mkdocs build --config-file "$BUILD_CFG" --site-dir "$SITE_DIR/gonka/docs"
rm -rf "$BUILD_CFG" "$OVR_DIR"

_restore_intro
trap - EXIT

# CNAME принадлежит только корню сайта (домен GitHub Pages задаётся один раз).
# Оригинал кладёт свой CNAME (gonka.ai) в docs/ — удаляем его из подкаталога.
rm -f "$SITE_DIR/gonka/docs/CNAME"

# -----------------------------------------------------------------------
# Пост-обработка: исправление абсолютных путей к изображениям.
#
# В исходниках gonka-ai/gonka-docs изображения указаны абсолютными путями
# вида "/images/foo.png", которые корректно работают на gonka.ai (корень
# сайта = корень документации). В подкаталоге /gonkadocs/gonka/docs/
# эти ссылки ломаются, потому что браузер ищет /images/ в корне нашего
# сайта, а не в корне раздела Gonka.
#
# Папка images/ лежит в корне раздела (/gonkadocs/gonka/docs/images/).
# Относительный путь от страницы до images/ зависит от глубины вложенности:
#   docs/index.html                        -> ../images/
#   docs/architecture/index.html           -> ../images/
#   docs/wallet/create-account/index.html  -> ../../images/
#   docs/cross-chain.../dashboard/index.html -> ../../../images/
#
# Используем Python-скрипт, который вычисляет правильный префикс "../"
# для каждого HTML-файла в зависимости от его пути.
# -----------------------------------------------------------------------
echo "==> [3/7] Пост-обработка: исправление путей к изображениям (/images/ -> ..N/images/)"
echo "==> [пост-обработка] Исправление language switcher (LINK_EN/LINK_ZH -> реальные пути)"
python3 - "$SITE_DIR/gonka/docs" <<'PYEOF'
import os, re, sys

docs_root = sys.argv[1]

for dirpath, _, filenames in os.walk(docs_root):
    for fn in filenames:
        if not fn.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fn)
        # Глубина файла относительно docs_root:
        # wallet/create-account/index.html -> 2 -> "../../"
        rel = os.path.relpath(fpath, docs_root)
        depth = rel.count(os.sep)
        prefix = '../' * depth

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # --- Fix 1: image paths ---
        if '/images/' in content:
            new = content.replace('src="/images/', f'src="{prefix}images/')
            new = new.replace('href="/images/', f'href="{prefix}images/')
            if new != content:
                content = new
                changed = True
                print(f"  fixed images: {rel} ({depth} levels)")

        # --- Fix 2: language switcher ---
        # i18n plugin generates correct <link rel="alternate" href="..."> tags.
        # Extract them and replace LINK_EN / LINK_ZH placeholders in our header.
        if 'LINK_EN' in content or 'LINK_ZH' in content:
            en_href = zh_href = None
            for m in re.finditer(
                r'<link\s+rel="alternate"\s+href="([^"]+)"\s+hreflang="(\w+)"',
                content
            ):
                url, lang = m.group(1), m.group(2)
                if lang == 'en':
                    en_href = url
                elif lang == 'zh':
                    zh_href = url
            if en_href:
                content = content.replace('href="LINK_EN"', f'href="{en_href}"')
                changed = True
            if zh_href:
                content = content.replace('href="LINK_ZH"', f'href="{zh_href}"')
                changed = True
            if en_href or zh_href:
                print(f"  fixed i18n: {rel} (en={en_href}, zh={zh_href})")

        if changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
PYEOF

echo "==> [4/7] Объединение поисковых индексов (main + gonka/docs)"
python3 - "$SITE_DIR" <<'PYEOF'
import json, os, sys

site_root = sys.argv[1]
main_index_path = os.path.join(site_root, "search", "search_index.json")
gonka_index_path = os.path.join(site_root, "gonka", "docs", "search", "search_index.json")

if not os.path.exists(main_index_path):
    print("  Main search index not found, skipping merge")
    sys.exit(0)

with open(main_index_path, "r", encoding="utf-8") as f:
    main_index = json.load(f)

main_docs = main_index.get("docs", [])
main_locs = {d.get("location") for d in main_docs}

if os.path.exists(gonka_index_path):
    with open(gonka_index_path, "r", encoding="utf-8") as f:
        gonka_index = json.load(f)
    
    added = 0
    for doc in gonka_index.get("docs", []):
        loc = doc.get("location", "")
        # Add gonka/docs/ prefix to relative paths
        if loc and not loc.startswith("/") and not loc.startswith("http"):
            new_loc = f"gonka/docs/{loc}"
        elif loc == "":
            new_loc = "gonka/docs/"
        else:
            new_loc = loc
        
        if new_loc not in main_locs:
            doc["location"] = new_loc
            main_docs.append(doc)
            main_locs.add(new_loc)
            added += 1
    
    main_index["docs"] = main_docs
    
    with open(main_index_path, "w", encoding="utf-8") as f:
        json.dump(main_index, f, ensure_ascii=False)
    
    print(f"  Merged {added} gonka docs into main search index (total: {len(main_docs)})")
else:
    print("  Gonka search index not found, skipping merge")
PYEOF

echo "==> [5/7] Генерация .md копий страниц для AI-агентов (llms.txt standard)"
python3 "$ROOT/buildtools/generate-page-md.py" "$SITE_DIR"

echo "==> [6/7] Объединение sitemap.xml (main + gonka/docs)"
python3 - "$SITE_DIR" <<'PYEOF'
import os, re, sys

site_root = sys.argv[1]
main_sitemap = os.path.join(site_root, "sitemap.xml")
gonka_sitemap = os.path.join(site_root, "gonka", "docs", "sitemap.xml")

if not os.path.exists(main_sitemap):
    print("  Main sitemap.xml not found, skipping merge")
    sys.exit(0)

if not os.path.exists(gonka_sitemap):
    print("  Gonka sitemap.xml not found, skipping merge")
    sys.exit(0)

with open(main_sitemap, "r", encoding="utf-8") as f:
    main_content = f.read()

with open(gonka_sitemap, "r", encoding="utf-8") as f:
    gonka_content = f.read()

# Extract <url> entries from gonka sitemap (skip xmlns declarations)
gonka_urls = re.findall(r'(<url>.*?</url>)', gonka_content, re.DOTALL)

# Extract existing <loc> from main sitemap to avoid duplicates
existing_locs = set(re.findall(r'<loc>(.*?)</loc>', main_content))

added = 0
new_entries = []
for url_block in gonka_urls:
    loc_match = re.search(r'<loc>(.*?)</loc>', url_block)
    if loc_match:
        loc = loc_match.group(1)
        if loc not in existing_locs:
            # Simplify: use <loc> and <lastmod> only (drop xhtml:link, changefreq)
            lastmod_match = re.search(r'<lastmod>(.*?)</lastmod>', url_block)
            lastmod = lastmod_match.group(1) if lastmod_match else "2026-07-04"
            new_entries.append(f'    <url>\n         <loc>{loc}</loc>\n         <lastmod>{lastmod}</lastmod>\n    </url>')
            existing_locs.add(loc)
            added += 1

if new_entries:
    # Insert before closing </urlset>
    insert_before = '</urlset>'
    new_urls = '\n'.join(new_entries)
    main_content = main_content.replace(insert_before, f'{new_urls}\n{insert_before}')
    
    with open(main_sitemap, "r+", encoding="utf-8") as f:
        f.write(main_content)
    
    print(f"  Merged {added} gonka URLs into main sitemap (total: {len(existing_locs)})")
else:
    print("  No new gonka URLs to merge")
PYEOF

echo "==> [7/7] Копирование robots.txt и llms.txt в _site"
cp "$ROOT/docs/robots.txt" "$SITE_DIR/robots.txt"
cp "$ROOT/docs/llms.txt" "$SITE_DIR/llms.txt"
cp "$ROOT/docs/llms-full.txt" "$SITE_DIR/llms-full.txt"

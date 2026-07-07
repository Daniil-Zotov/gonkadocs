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
GONKA_ROOT="$ROOT/docs/gonka/docs"

# Окружение: URL для i18n переключателя (продакшен по умолчанию)
GONKA_SITE_URL="${GONKA_SITE_URL:-https://gonkadocs.com/gonka/docs/}"

echo "==> [0/7] Генерация llms.txt и llms-full.txt для AI-агентов"
python3 "$ROOT/buildtools/generate-llms.py"
python3 "$ROOT/buildtools/generate-llms-full.py"

echo "==> [1/7] Сборка основного сайта -> $SITE_DIR"
cd "$ROOT"
python3 -m mkdocs build --clean --site-dir "$SITE_DIR"

echo "==> [2/7] Сборка раздела Gonka (родной конфиг оригинала, i18n en+zh) -> $SITE_DIR/gonka/docs"
cd "$GONKA_ROOT"

# В оригинале docs/index.md — это ЛЕНДИНГ gonka.ai (template home.html), а не
# документация. Сам оригинал при сборке /docs/ подменяет index.md на
# introduction.md (см. его buildtools/prepare-stages.sh). Повторяем это,
# НО через временную копию, чтобы не мутировать синканутые файлы.
DOCS_SRC="docs"
DOCS_TMP=".docs.tmp"
rm -rf "$DOCS_TMP"
cp -r "$DOCS_SRC" "$DOCS_TMP"

# Swap introduction.md → index.md в temp-копии (безопасно, не трогает оригиналы)
for dir in "" "zh/"; do
  idx="$DOCS_TMP/${dir}index.md"
  intro="$DOCS_TMP/${dir}introduction.md"
  if [ -f "$intro" ]; then
    cp "$intro" "$idx"
  fi
done

# Переопределяем site_url для корректной работы i18n переключателя.
# Оригинальный site_url указывает на gonka.ai — это ломает ссылки на zh/lang
# при развёртывании под путём /gonkadocs/gonka/docs/. Создаём временную копию
# конфига с исправленным site_url и собираем по ней.
BUILD_CFG=".mkdocs.yml.build"

# Мержим overrides: upstream originals + наши shared-шаблоны.
# mkdocs-material подхватывает custom_dir как overlay поверх стандартной темы.
# Наш overrides идёт вторым → перезаписывает header upstream'а на наш shared.
OVR_DIR=".overrides.merged"
rm -rf "$OVR_DIR"
cp -r overrides "$OVR_DIR"
cp -r "$ROOT/buildtools/gonka-overrides/"* "$OVR_DIR/"

cp mkdocs.yml "$BUILD_CFG"

# Исправляем ключи через Python (точнее sed, т.к. YAML может иметь отступы)
python3 -c "
import re

with open('$BUILD_CFG') as f:
    content = f.read()

content = re.sub(
    r'^site_url:.*',
    'site_url: $GONKA_SITE_URL',
    content,
    flags=re.MULTILINE
)

content = re.sub(
    r'^( *)custom_dir:.*',
    r'\1custom_dir: $OVR_DIR',
    content,
    flags=re.MULTILINE
)

# Добавляем docs_dir, если его нет
if not re.search(r'^docs_dir:', content, re.MULTILINE):
    content = re.sub(
        r'^site_url:.*',
        lambda m: m.group(0) + '\ndocs_dir: $DOCS_TMP',
        content,
        flags=re.MULTILINE
    )
else:
    content = re.sub(
        r'^docs_dir:.*',
        'docs_dir: $DOCS_TMP',
        content,
        flags=re.MULTILINE
    )

# Добавляем extra.tabs для навигационных вкладок (используется tabs.html)
content = re.sub(
    r'^(extra:)',
    r'\\1\n  tabs:\n    - title: Gonka.ai/docs\n      url: /gonka/docs/\n    - title: Community\n      url: /community/\n    - title: Proposals\n      url: /proposals/\n    - title: For Agents\n      url: /agents/',
    content,
    flags=re.MULTILINE
)

with open('$BUILD_CFG', 'w') as f:
    f.write(content)
"

python3 -m mkdocs build --config-file "$BUILD_CFG" --site-dir "$SITE_DIR/gonka/docs"
rm -rf "$BUILD_CFG" "$OVR_DIR" "$DOCS_TMP"

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
# Используем lxml.html для надёжного парсинга (обрабатывает src=, href=,
# url(), одинарные/двойные кавычки, <source>, <image> в SVG).
# -----------------------------------------------------------------------
echo "==> [3/7] Пост-обработка: исправление путей к изображениям (/images/ -> ..N/images/)"
python3 - "$SITE_DIR/gonka/docs" <<'PYEOF'
import os, sys
from html.parser import HTMLParser

docs_root = sys.argv[1]

class ImageFixer(HTMLParser):
    def __init__(self, prefix):
        super().__init__(convert_charrefs=False)
        self.prefix = prefix
        self.result = []
        self.in_style = False
        self.style_content = ""

    def handle_starttag(self, tag, attrs):
        new_attrs = list(attrs)
        changed = False
        for i, (name, value) in enumerate(attrs):
            if name in ('src', 'href') and value.startswith('/images/'):
                new_attrs[i] = (name, self.prefix + value[1:])
                changed = True
            elif name == 'style' and '/images/' in value:
                new_attrs[i] = (name, value.replace('/images/', self.prefix + 'images/'))
                changed = True
        attrs_str = ''
        for name, value in new_attrs:
            if value is None:
                attrs_str += f' {name}'
            else:
                escaped = value.replace('&', '&amp;').replace('"', '&quot;')
                attrs_str += f' {name}="{escaped}"'
        self.result.append(f'<{tag}{attrs_str}>')

    def handle_endtag(self, tag):
        self.result.append(f'</{tag}>')

    def handle_data(self, data):
        if '/images/' in data:
            data = data.replace('/images/', self.prefix + 'images/')
        self.result.append(data)

    def handle_comment(self, data):
        self.result.append(f'<!--{data}-->')

    def handle_entityref(self, name):
        self.result.append(f'&{name};')

    def handle_charref(self, name):
        self.result.append(f'&#{name};')

for dirpath, _, filenames in os.walk(docs_root):
    for fn in filenames:
        if not fn.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fn)
        rel = os.path.relpath(fpath, docs_root)
        depth = rel.count(os.sep)
        prefix = '../' * depth

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        if '/images/' not in content:
            continue

        fixer = ImageFixer(prefix)
        fixer.feed(content)
        result = ''.join(fixer.result)

        if result != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"  fixed images: {rel} ({depth} levels)")
PYEOF

echo "==> [4/7] Объединение поисковых индексов (main + gonka/docs)"
python3 - "$SITE_DIR" "$SITE_DIR/gonka/docs" <<'PYEOF'
import json, os, sys

site_root = sys.argv[1]
gonka_site_dir = sys.argv[2]
main_index_path = os.path.join(site_root, "search", "search_index.json")
gonka_index_path = os.path.join(gonka_site_dir, "search", "search_index.json")

# Вычисляем префикс из пути gonka_site_dir относительно site_root
gonka_prefix = os.path.relpath(gonka_site_dir, site_root) + "/"

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
        if loc and not loc.startswith("/") and not loc.startswith("http"):
            new_loc = gonka_prefix + loc
        elif loc == "":
            new_loc = gonka_prefix.rstrip("/")
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
from datetime import datetime, timezone

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

today = datetime.now(timezone.utc).date().isoformat()

added = 0
new_entries = []
for url_block in gonka_urls:
    loc_match = re.search(r'<loc>(.*?)</loc>', url_block)
    if loc_match:
        loc = loc_match.group(1)
        if loc not in existing_locs:
            lastmod_match = re.search(r'<lastmod>(.*?)</lastmod>', url_block)
            lastmod = lastmod_match.group(1) if lastmod_match else today
            new_entries.append(f'    <url>\n         <loc>{loc}</loc>\n         <lastmod>{lastmod}</lastmod>\n    </url>')
            existing_locs.add(loc)
            added += 1

if new_entries:
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

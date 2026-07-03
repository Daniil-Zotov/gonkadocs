# gonkadocs.com

Единый портал документации [Gonka](https://gonka.ai) — децентрализованной сети для AI-инференса с консенсусом Proof of Compute.

**URL:** [gonkadocs.com](https://gonkadocs.com)

---

## Что содержит портал

### Официальная документация протокола (`/gonka/docs/`)
Автосинхронизируется из [gonka-ai/gonka-docs](https://github.com/gonka-ai/gonka-docs) каждые 6 часов.

- **Архитектура** — потоки инференса, Proof of Compute, эпохи
- **Developer Quickstart** — инференс через брокеров (OpenAI-совместимый API)
- **Gateway Quickstart** — собственный gateway (Docker)
- **Host Quickstart** — подключение GPU-ресурсов
- **Wallet** — аккаунты, дашборд, тарифы
- **Cross-Chain** — Ethereum bridge (USDT/GNK), IBC через Kava
- **Governance** — голосование, предложения, транзакции
- Языки: English, 中文

### GitHub Discussions (`/gonka/discussion/`)
Автосинхронизируются из [gonka-ai/gonka](https://github.com/gonka-ai/gonka/discussions) каждые 6 часов.

- **Proposals** (42) — технические и финансовые предложения
- **Show and Tell** (20) — проекты сообщества
- **Q&A** (3) — лучшие практики, технические вопросы
- **General** (5) — надёжность сети, governance

### Сообщество (`/community/`)
- **Дорожная карта** — трёхгоризонтная стратегия развития
- **GRC** — комитет реституции (компенсации за баги протокола)
- **GSC** — комитет саморегулирования

### On-Chain Proposals (`/proposals/`)
Дашборд всех 75 governance-предложений со статусами и описаниями.

---

## AI-интеграция

Портал спроектирован как единый источник информации для AI-агентов.

### Стандартные файлы

| URL | Описание |
|-----|----------|
| [`/llms.txt`](https://gonkadocs.com/llms.txt) | Точка входа для AI: описание проекта, ссылки на разделы, ключевые концепции |
| [`/llms-full.txt`](https://gonkadocs.com/llms-full.txt) | Все документы в одном файле (818 KB), оптимизировано для context window |
| [`/robots.txt`](https://gonkadocs.com/robots.txt) | Разрешение для GPTBot, ClaudeBot, Google-Extended |
| [`/openapi.yaml`](https://gonkadocs.com/openapi.yaml) | OpenAPI 3.0 спецификация inference API |
| [`/search/search_index.json`](https://gonkadocs.com/search/search_index.json) | Поисковый индекс (Lunr.js), доступен программно |
| [`/sitemap.xml`](https://gonkadocs.com/sitemap.xml) | Полная карта сайта |

### MCP-сервер

Для AI-агентов (Cline, opencode, Claude) доступен MCP-сервер с инструментами:

```json
{
  "mcpServers": {
    "gonka-docs": {
      "command": "python3",
      "args": ["buildtools/mcp-server.py"]
    }
  }
}
```

Инструменты:
- `search_gonka_docs(query)` — поиск по документации
- `read_gonka_page(url)` — чтение конкретной страницы
- `list_gonka_sections()` — список всех разделов
- `read_gonka_llms_full()` — полный контекст
- `read_gonka_proposal(id)` — чтение governance-предложения

### .md версии страниц

Каждая страница доступна в markdown по URL с `.html.md`:
```
/gonka/docs/architecture/index.html  →  /gonka/docs/architecture/index.html.md
```

---

## Архитектура сборки

Сайт состоит из двух независимых сборок MkDocs, объединённых в `_site/`:

```
buildtools/build.sh
    │
    ├──► [0] generate-llms.py + generate-llms-full.py
    │       Динамическое сканирование docs/ → AI-файлы
    │
    ├──► [1] mkdocs build (основной сайт)
    │       Главная + Discussions + Community + Proposals
    │
    ├──► [2] mkdocs build (раздел Gonka)
    │       Оригинальный mkdocs.yml из gonka-ai/gonka-docs
    │       i18n: en + zh, кастомные overrides
    │
    ├──► [3] Пост-обработка
    │       Исправление путей к изображениям
    │       Language switcher (LINK_EN/LINK_ZH → реальные пути)
    │
    └──► [4] generate-page-md.py
            Генерация .html.md копий всех страниц
```

---

## Автосинхронизация

4 GitHub Actionsworkflow автоматически обновляют контент и AI-файлы:

| Workflow | Источник | Интервал | Что синхронизирует |
|----------|----------|----------|-------------------|
| `sync-gonka-ai-docs.yml` | gonka-ai/gonka-docs | каждые 6ч | Документацию протокола |
| `sync-discussions.yml` | gonka-ai/gonka (GraphQL) | каждые 6ч | GitHub Discussions |
| `sync-gdocs.yml` | Google Docs | каждые 6ч | Регламент GSC |
| `sync-roadmap.yml` | gonka-ai/gonka | каждые 24ч | Дорожную карту |

Каждый sync-экшен автоматически перегенерирует `llms.txt` и `llms-full.txt` после обновления контента.

---

## Локальная разработка

```bash
# Установка зависимостей
pip install mkdocs mkdocs-material pymdown-extensions

# Сборка сайта
bash buildtools/build.sh

# Локальный просмотр
bash buildtools/serve.sh
```

---

## Структура репозитория

```
gonkadocs/
├── mkdocs.yml                    # Конфиг MkDocs (основной сайт)
├── buildtools/
│   ├── build.sh                  # Скрипт сборки
│   ├── serve.sh                  # Локальный сервер
│   ├── generate-llms.py          # Генерация llms.txt
│   ├── generate-llms-full.py     # Генерация llms-full.txt
│   ├── generate-page-md.py       # Генерация .html.md копий
│   ├── mcp-server.py             # MCP-сервер для AI-агентов
│   └── gonka-overrides/          # Shared header для Gonka секции
├── docs/
│   ├── llms.txt                  # AI точка входа
│   ├── llms-full.txt             # Полная документация
│   ├── robots.txt                # Для AI-краулеров
│   ├── openapi.yaml              # API спецификация
│   ├── index.md                  # Главная
│   ├── gonka/
│   │   ├── docs/                 # Документация протокола (synced)
│   │   └── discussion/           # GitHub Discussions (synced)
│   ├── community/
│   │   ├── roadmap/              # Дорожная карта (synced)
│   │   ├── grc/                  # Комитет реституции
│   │   └── gsc/                  # Комитет саморегулирования (synced)
│   └── proposals/                # On-chain proposals
├── mcp.json                      # Конфиг MCP-сервера
└── .github/workflows/
    ├── deploy-docs.yml           # Деплой на GitHub Pages
    ├── sync-gonka-ai-docs.yml    # Синхронизация документации
    ├── sync-discussions.yml      # Синхронизация discussions
    ├── sync-gdocs.yml            # Синхронизация Google Docs
    └── sync-roadmap.yml          # Синхронизация дорожной карты
```

---

## Лицензия

Документация распространяется по лицензии протокола Gonka. См. `docs/gonka/docs/docs/protocol-license.pdf`.

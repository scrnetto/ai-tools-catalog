# WhatsApp catalog pipeline → `ai-tools-catalog` skill

Automates what used to be done by hand: read the **WhatsApp chat configured in `config.json`**,
catalog the GitHub repos and websites shared there (mostly Instagram reels about AI/coding), and
keep the **global agent skill** — queryable from any project, by any agent that supports
the Agent Skills format — up to date.

## How to run it
- **Slash command:** `/sync-ai-catalog` (needs WhatsApp Web logged in, unless Phase A is disabled)
- **Or** just ask: *"update the catalog / check for new reels"* → this starts the
  **`catalog-updater`** agent (`.claude/agents/`).

## What the agent does
**Phase A — WhatsApp chat** *(skipped when `whatsapp.enabled: false`)*
1. Opens WhatsApp Web, opens the chat named by `whatsapp.chat`, and collects every message
   (scroll + dedup — WhatsApp virtualises the DOM, so messages are gathered *during* the scroll).
2. Diffs against the existing catalog and isolates the **new links**.

**Phase B — Instagram profile monitoring** *(skipped when `instagram.enabled: false`; needs Instagram logged in)*
- Derives the handles of creators whose reels are already catalogued (from the `fonte` field), opens
  `instagram.com/{handle}/reels/` and scans the grid for **new reels** from those creators. State is
  tracked in `instagram-profili.json` — the check is incremental and stops at the first reel already
  seen. Without an Instagram login this phase hits the login wall, gets skipped, and is reported.

**Both phases**
3. For each new reel, reads the **Instagram caption** (meta tag) and derives the GitHub repo (explicit
   or verified via web search) or the website. Only tool-related reels are catalogued; anything
   uncertain is reported rather than guessed.
4. Writes the new records (with `macro` + `uso`) into `github-repos.json` / `siti-web.json` if you publish the catalog (`catalogo.manutentore`), otherwise into their `.local.json` twins — see the README, «Your own entries and updates».
5. Fetches activity metadata and **rebuilds** the catalog and the skill.

## Configuration (`config.json`)
The file is **gitignored** because it holds the name of your chat; the tracked schema is
`config.example.json`. Anyone cloning the repo copies the example and points it at their own source.

| Field | Effect |
|---|---|
| `whatsapp.enabled` | `false` → Phase A skipped entirely (WhatsApp Web never opened) |
| `whatsapp.chat` | Exact name of the chat to open |
| `whatsapp.self_chat` | `true` = the "message yourself" chat; `false` = look it up by name in the list |
| `instagram.enabled` | `false` → Phase B (profile monitoring) skipped |
| `catalogo.titolo` / `catalogo.fonte` | Heading and source line of `CATALOGO-AI-TOOLS.md` |
| `catalogo.lingua` | `it` (default) or `en` — language of category names, status labels and generated prose |
| `github.token` | Optional GitHub token (60 → 5000 API requests/hour). Create it with **no permissions**: public repo metadata needs none. Read only if `config.json` is gitignored; `GITHUB_TOKEN` in the environment takes precedence. |

One-off overrides from the command: `/sync-ai-catalog "Chat Name"`, `--only-instagram`,
`--only-whatsapp`. With no `config.json`, the agent asks which chat to read and `build_catalog.py`
falls back to neutral defaults.

## Files
| File | Role |
|---|---|
| `config.json` / `config.example.json` | Local configuration (gitignored) / tracked schema |
| `github-repos.json` | Catalogued repos (`id, progetto, descrizione, url, categoria, fonte, macro, uso`) |
| `siti-web.json` | Non-repo websites (same fields, `sito` instead of `progetto`) |
| `gh-meta.json` | GitHub metadata (stars, last push, license) by `owner/name` (plus `gh-meta.local.json` for your own entries) |
| `instagram-profili.json` | Profile-monitoring state (handle → reels seen/catalogued, last check) |
| `chat-messaggi.csv` | Raw message dump (gitignored) |
| `catalogo-unificato.json` / `CATALOGO-AI-TOOLS.md` / `docs/index.html` | Generated outputs (the last one is the web page, from the template `scripts/pagina-catalogo.html`) |
| `siti-personali.json` | Non-dev entries, kept out of the repo (gitignored) |
| `scripts/fetch_gh_meta.py` | Fetches activity metadata (incremental merge, `--refresh` to re-check) |
| `scripts/build_catalog.py` | Builds the catalog and updates the installed skill (`~/.agents/skills/ai-tools-catalog/`), merging your `.local.json` entries |

## Rebuild only, without re-reading WhatsApp
```bash
python3 scripts/fetch_gh_meta.py               # only repos with no metadata yet
python3 scripts/fetch_gh_meta.py --refresh     # re-check all, stalest first, resumable
python3 scripts/fetch_gh_meta.py --refresh 30  # only entries older than 30 days
python3 scripts/build_catalog.py               # rebuild MD+JSON and update the skill
```
`--refresh` is safe on a large catalog: it never overwrites good data with an error (a 404 repo
keeps its entry and gains a `last_error` flag), and it stops cleanly when the API quota runs out,
resuming from the stalest entries on the next run. A token raises the quota from 60 to 5000
requests/hour — set `GITHUB_TOKEN`, pass `--token`, or put it in `config.json` under
`github.token` (the script refuses to read it from there unless the file is gitignored).

## Notes
- Macro categories (`macro`): A coding/Claude Code · B AI agents · C local LLMs · D RAG/memory ·
  E OCR · F media generation · G security · H dev tools · I finance/trading · J AI research ·
  **Z personal/non-dev → private file, never committed**.
- Unauthenticated GitHub API is capped at 60 requests/hour: `fetch_gh_meta.py` stops at the quota
  and resumes next run, and for repos still missing the agent falls back to same-origin HTML
  scraping from the browser (see the agent prompt).
- Guiding principle: **never invent URLs**. Anything unverifiable is reported, not forced.

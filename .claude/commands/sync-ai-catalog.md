---
description: Scan the configured WhatsApp chat and tracked Instagram creators for new AI/dev tools, then rebuild the catalog and the ai-tools-catalog skill
---

Run the **catalog-updater** agent end to end: read the configured WhatsApp chat, check the
Instagram profiles of creators already in the catalog for new reels, extract and verify the GitHub
repositories and websites they point to, fetch their activity status, translate the new entries,
and rebuild `CATALOGO-AI-TOOLS.md`, `catalogo-unificato.json` and the web pages in `docs/` —
updating the global `ai-tools-catalog` skill.

**Source of truth:** `config.json` (`whatsapp.enabled`, `whatsapp.chat`, `whatsapp.self_chat`,
`instagram.enabled`). If `config.json` is missing, the agent asks which chat to read instead of
guessing. See `config.example.json` for the schema.

**Optional arguments** — one-off overrides, never written back to `config.json`:

| Argument | Effect |
|---|---|
| `"Chat Name"` | Read this chat instead of `whatsapp.chat` |
| `--only-instagram` | Skip the WhatsApp phase even if `whatsapp.enabled` is `true` |
| `--only-whatsapp` | Skip Instagram profile monitoring |
| `--refresh-meta [DAYS]` | Also re-fetch stars/last-push for entries already catalogued, oldest first |

**Prerequisites:** WhatsApp Web logged in for the chat phase, Instagram logged in for profile
monitoring. Either phase degrades to a reported skip rather than a failure.

**Rebuild only** — no chat, no browser, no new entries:
```bash
python3 scripts/fetch_gh_meta.py --refresh   # refresh activity metadata (oldest first)
python3 scripts/build_catalog.py             # rebuild catalog, web pages and skill
```

$ARGUMENTS

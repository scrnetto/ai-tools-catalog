# WhatsApp → AI/Dev tools catalog + agent skill

[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)
[![Python 3, stdlib only](https://img.shields.io/badge/python-3%20%C2%B7%20stdlib%20only-3776AB.svg?logo=python&logoColor=white)](scripts/)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-8A2BE2.svg)](https://agentskills.io)
[![Catalog](https://img.shields.io/badge/catalog-315%20repos%20%2B%2029%20sites-success.svg)](CATALOGO-AI-TOOLS.md)
[![Activity checked](https://img.shields.io/badge/activity%20checked-2026--09--27-informational.svg)](gh-meta.json)

Reads the reels and links you save in a WhatsApp chat (typically the "message yourself" chat),
extracts **GitHub repositories** and **websites/services** for AI and dev tooling, checks how alive
each project is on GitHub, and keeps a **catalog that your coding agent can query from any
project** through a global skill — Claude Code, OpenCode, Codex, Gemini CLI, Antigravity, Cursor,
GitHub Copilot and any other agent that supports the open [Agent Skills](https://agentskills.io)
format.

> The tooling and docs are in English; the catalog *entries* are in Italian, because that is the
> language of the reels they come from. Section headings and status labels follow
> `catalogo.lingua` in your config — see [Configuration](#configuration).

## What the catalog holds
- **315 GitHub repositories** + **29 websites**, in 10 practical categories (coding agents/Claude
  Code, local LLMs, RAG/memory, OCR, media generation, security, dev tools, finance/trading, AI
  research). Counts are regenerated on every build.
- Per entry: what it does, *when to use it*, and activity status (⭐ stars, last push, license).
- Human-readable output: [`CATALOGO-AI-TOOLS.md`](CATALOGO-AI-TOOLS.md). Structured data:
  `catalogo-unificato.json`.

## Install the skill on another machine
```bash
git clone https://github.com/scrnetto/ai-tools-catalog.git
cd ai-tools-catalog
./install-skill.sh          # Linux/macOS
.\install-skill.ps1         # Windows (PowerShell)
```
The script installs the skill once, in `~/.agents/skills/ai-tools-catalog/`, and rebuilds the
catalog from the data in the repo. From then on, in **any** project and with any supported agent,
you can ask things like *"which open-source library should I use for OCR on PDFs?"* and the skill
surfaces the relevant entries with their activity status and license.

> Needs only `python3` (standard library). No tokens or credentials required.

### Which agents, and where they look

The skill is a plain [Agent Skills](https://agentskills.io/specification) folder: a `SKILL.md` with
`name` and `description`, plus the two catalog files it points to. Nothing in it is specific to one
agent. What differs between agents is only *where* they look for global skills, so the installer
keeps **one real copy** in the shared `~/.agents/skills/` folder and links the agents that don't
read it:

| Agent | Global skills folder | How the installer covers it |
|---|---|---|
| OpenCode, Codex, Gemini CLI, Cursor, GitHub Copilot, Goose, Crush, and most other Agent Skills clients | `~/.agents/skills/` | the real copy |
| Hermes Agent | `~/.hermes/skills/` | not covered: add `~/.agents/skills` to `skills.external_dirs` in `~/.hermes/config.yaml` |
| Claude Code | `~/.claude/skills/` | symlink (junction on Windows) |
| Antigravity (Google) | `~/.gemini/config/skills/` | symlink/junction, only if `~/.gemini` exists |

One copy means `build_catalog.py` updates every agent at once, and agents that scan more than one
folder (OpenCode and Cursor also read `~/.claude/skills/`) see a single skill. OpenCode logs a
harmless `duplicate skill name` warning for the linked path and keeps one entry. An agent not listed
here almost certainly reads `~/.agents/skills/`; if it doesn't, link its skills folder the same way.

An older install that lived directly in `~/.claude/skills/ai-tools-catalog/` is replaced by the
link automatically — but only if it holds nothing except the generated files; otherwise the
installer stops and tells you what it found.

**Tested on 2026-09-27**, on nine agents, with the question *"which open-source tool does OCR on PDFs?"*: each agent
loaded the skill, read the catalog files and answered with stars, last push and license matching the
catalog.

| Agent | Result |
|---|---|
| Claude Code | ✅ In `claude -p`, reading the skill's files (outside the working directory) needs `--allowedTools Read`; interactive sessions just ask |
| OpenCode 1.18.31 | ✅ with `opencode/big-pickle`. The local `qwen3-coder` model wrote the tool call as plain text instead of executing it, then invented URLs and stars: pick a model with working tool calling |
| Codex CLI 0.157.1 (`gpt-5.6-terra`) | ✅ with the default `workspace-write` sandbox. Codex's Linux sandbox (bubblewrap) needs unprivileged user namespaces, which Ubuntu ≥ 23.10 blocks through AppArmor (`kernel.apparmor_restrict_unprivileged_userns = 1`): there Codex sees the skill but cannot read its files, and answers from web search or memory. Fix: an AppArmor profile granting `userns` to `/usr/bin/bwrap` only — see below |
| Antigravity CLI 1.2.12 | ✅ once linked into `~/.gemini/config/skills/` — it does not read `~/.agents/skills/` globally |
| Hermes Agent 0.16.0 | ✅ after adding `~/.agents/skills` to `skills.external_dirs` in `~/.hermes/config.yaml` — by default it reads only `~/.hermes/skills/` |
| Gemini CLI 0.61.0 | ✅ reads `~/.agents/skills/` |
| GitHub Copilot CLI 1.0.88 | ✅ reads `~/.agents/skills/` |
| Goose 1.52.0 | ✅ reads `~/.agents/skills/` through its `skills` extension, but may skip it unless told to use `load_skill`: in the first run it answered from memory |
| Crush 0.96.1 | ✅ reads `~/.agents/skills/` |

**Codex on Ubuntu ≥ 23.10.** Check with `bwrap --ro-bind / / true`: if it fails with
`setting up uid map: Permission denied`, save this as `/etc/apparmor.d/bwrap` and load it with
`sudo apparmor_parser -r /etc/apparmor.d/bwrap`. It is the same pattern Ubuntu ships for other
apps that need user namespaces; the trade-off is that any local program can now use `bwrap` to
create one, which is still far narrower than turning the restriction off system-wide.

```
abi <abi/4.0>,
include <tunables/global>

profile bwrap /usr/bin/bwrap flags=(unconfined) {
  userns,
  include if exists <local/bwrap>
}
```

Hermes, Gemini CLI, Copilot CLI, Goose and Crush were tested through a local
[OmniRoute](https://github.com/diegosouzapw/OmniRoute) gateway, with free-tier models
(GitHub Models `gpt-4.1`/`gpt-5-mini`). Cursor was not tested: it reads `~/.agents/skills/` according to
its documentation. `install-skill.ps1` was not run on Windows.

## Configuration
The chat to read is not hardcoded — it lives in `config.json`, which is **gitignored**:

```bash
cp config.example.json config.json     # then set your own chat
```

| Field | Effect |
|---|---|
| `whatsapp.enabled` | `false` → skip WhatsApp entirely (run on Instagram profiles alone) |
| `whatsapp.chat` | Exact chat name, as it appears in WhatsApp Web |
| `whatsapp.self_chat` | `true` if it is the "message yourself" chat |
| `instagram.enabled` | `false` → skip profile monitoring |
| `catalogo.titolo` / `catalogo.fonte` | Heading and source line of the generated catalog |
| `catalogo.lingua` | `it` (default) or `en` — language of category names, status labels and generated prose |
| `github.token` | Optional GitHub token — see [below](#github-token-optional) |

For a one-off run you can also use `/sync-ai-catalog "Another Chat"` or
`/sync-ai-catalog --only-instagram` without touching the config.

**The project works without WhatsApp**: with `whatsapp.enabled: false` you still get a catalog fed
by the Instagram profiles tracked in `instagram-profili.json`.

Adding a language means adding one entry to `LOCALI` in `scripts/build_catalog.py`. Note that only
the *scaffolding* is translated — entry descriptions stay in whatever language they were written in,
and the prose of `skill/SKILL.md` is not generated, so it keeps its own language.

## Updating the catalog
Requires a browser with WhatsApp Web logged in (and Instagram logged in for profile monitoring).
- From Claude Code: **`/sync-ai-catalog`** (runs the `catalog-updater` agent). The update agent
  and the slash command are Claude Code files; with another agent, ask it to follow
  `.claude/agents/catalog-updater.md` — it needs a browser tool (Playwright MCP or equivalent).
- The agent reads the chat, checks known creators' Instagram profiles for new reels, extracts and
  verifies the repos, then rebuilds the catalog and the skill. See [`PIPELINE.md`](PIPELINE.md).

### Rebuild only, without re-reading WhatsApp
```bash
python3 scripts/fetch_gh_meta.py             # fetch metadata for repos that have none
python3 scripts/fetch_gh_meta.py --refresh   # re-check every repo, stalest data first
python3 scripts/fetch_gh_meta.py --refresh 30  # only what was last checked >30 days ago
python3 scripts/build_catalog.py             # rebuild CATALOGO + catalogo.json, update the skill
```

Activity data goes stale, so `--refresh` re-checks stars, last push, archived status and license.
Two things make it safe to run on a large catalog:

- **It never loses data.** If a repo 404s (deleted or renamed) the existing entry is kept and
  flagged with `last_error` instead of being overwritten with an error.
- **It resumes.** Unauthenticated GitHub allows 60 requests/hour, so a catalog of 315 repos cannot
  refresh in one pass. The queue is ordered — missing entries first, then the stalest — and the run
  stops cleanly when the quota runs out, telling you when it resets. Re-run later and it picks up
  where it left off. A token raises the quota to 5000/hour and finishes it in one go.

### GitHub token (optional)

Only worth it if you want a full refresh in a single run.

**Create one with no permissions at all.** Reading public repository metadata requires none, and a
zero-permission token grants an attacker nothing beyond what anonymous access already allows — it
just raises the rate limit.

- *Fine-grained* — [Settings → Developer settings → Personal access tokens → Fine-grained](https://github.com/settings/personal-access-tokens/new):
  set *Repository access* to **Public Repositories (read-only)** and leave every permission at
  "No access".
- *Classic* — [Settings → Developer settings → Tokens (classic)](https://github.com/settings/tokens):
  **leave every scope checkbox unticked**.

The token is read in this order — first match wins:

| Where | How |
|---|---|
| `--token` | `python3 scripts/fetch_gh_meta.py --refresh --token ghp_...` (one-off; ends up in shell history) |
| `GITHUB_TOKEN` / `GH_TOKEN` env var | **Recommended.** PowerShell, persistent: `[Environment]::SetEnvironmentVariable('GITHUB_TOKEN','ghp_...','User')` · bash: `export GITHUB_TOKEN=ghp_...` |
| `github.token` in `config.json` | Most convenient, and `config.json` is gitignored — but the script **refuses to run** if it finds a token there while the file is not actually ignored by git, so a misconfigured `.gitignore` can't turn into a committed secret |

## Layout
| Path | Role |
|---|---|
| `config.example.json` | Configuration schema — copy to `config.json` (gitignored) |
| `github-repos.json` | Catalogued repos (`id, progetto, descrizione, url, categoria, fonte, macro, uso`) |
| `siti-web.json` | Non-repo websites |
| `gh-meta.json` | GitHub activity metadata, keyed by repo id |
| `instagram-profili.json` | Profile-monitoring state (reels already seen, per handle) |
| `scripts/` | `fetch_gh_meta.py`, `build_catalog.py` |
| `skill/SKILL.md` | Skill definition, in the open Agent Skills format (redistributable) |
| `.claude/agents/` · `.claude/commands/` | Update agent and slash command |
| `install-skill.sh` · `install-skill.ps1` | Install the skill on a new machine, for every agent |
| `LICENSE` · `LICENSE-DATA` | MIT for the code, CC BY 4.0 for the catalog data — see [License](#license) |

## Privacy
Files holding **personal WhatsApp content** (raw message dump, summaries, login screenshots, page
snapshots), `config.json`, and non-dev entries (`siti-personali.json`) are kept out of the repo via
`.gitignore` and stay local. Only the tool catalog and the tooling are committed.

Entries tagged `macro: "Z"` (personal content) are additionally dropped by `build_catalog.py` before
the outputs are generated — a second line of defence, so a personal entry that slips into a tracked
file still never reaches the published catalog.

## License
- **Code** — scripts, installers, `skill/SKILL.md`, the agent and command in `.claude/`: [MIT](LICENSE).
- **Catalog data** — the descriptions and "when to use it" notes in `github-repos.json`,
  `siti-web.json`, `catalogo-unificato.json` and `CATALOGO-AI-TOOLS.md`:
  [CC BY 4.0](LICENSE-DATA). Reuse them freely, crediting this repository.

Stars, last-push dates and licenses of the catalogued projects are facts taken from GitHub, not
authored here. **This catalog's licenses do not apply to the projects it lists**: each keeps its own
license, shown in the catalog where GitHub declares one.

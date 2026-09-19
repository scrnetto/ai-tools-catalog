---
name: ai-tools-catalog
description: >-
  Catalogo curato di 232 repository GitHub e 28 siti/servizi web di strumenti AI e dev
  (coding agent & Claude Code, LLM e inferenza locale, RAG/memoria, OCR, generazione media
  video/immagini/3D/voce, sicurezza & supply-chain, dev tools, finanza/trading AI, ricerca AI),
  ciascuno con descrizione funzionale, stato di attività verificato su GitHub (stelle, ultimo
  push) e suggerimento d'uso. Usa questa skill quando l'utente cerca uno strumento, libreria,
  modello o repo per un progetto ("che tool esiste per X", "c'è un'alternativa open-source a Y",
  "come faccio OCR/RAG/TTS/fine-tuning", "un agente per Z"), vuole valutare alternative, o chiede
  se un progetto è ancora attivo/manutenuto. Fonte: reel e link salvati in chat.
---

# Catalogo strumenti AI & Dev

Catalogo operativo di strumenti AI/dev raccolti dai reel Instagram e dai messaggi salvati in una
chat WhatsApp personale, ripuliti e arricchiti con metadati GitHub reali.

## File in questa skill
- **`CATALOGO-AI-TOOLS.md`** — versione leggibile completa, organizzata per categoria con tabelle
  (Progetto · Cosa fa · Quando usarlo · Stato). **Leggi questo file** per rispondere all'utente.
- **`catalogo.json`** — stessi dati in forma strutturata (1 oggetto per voce). Usalo quando devi
  **filtrare/cercare programmaticamente** (per categoria `macro`, per `tipo` repo/sito, per stato,
  per stelle). Campi: `tipo, macro, macro_nome, nome, cosa_fa, quando_usarlo, url, stelle,
  ultimo_push, attivita, licenza, linguaggio, fonte`.

## Come usarla
1. Quando l'utente cerca uno strumento o chiede "cosa esiste per fare X", **apri
   `CATALOGO-AI-TOOLS.md`** (o filtra `catalogo.json`) e proponi le voci pertinenti.
2. Cita sempre **stato di attività** (🟢/🟡/🔴, stelle, ultimo push) e **licenza** se rilevante per
   l'uso nel progetto dell'utente.
3. Se nessuna voce calza, dillo chiaramente: il catalogo è una raccolta personale, non esaustivo.
4. I dati di attività sono stati verificati il **2026-09-19**: se serve precisione attuale,
   ricontrolla il repo (le stelle/push cambiano nel tempo).

## Categorie e contenuto (indice rapido)
- **A · Coding Agent, Claude Code & sviluppo AI-assistito** (35): Everything Claude Code, DeepSeek Harness (dsh), ponytail, Spec Kit, gstack, awesome-design-md, screenshot-to-code, impeccable, Cline, BMAD-METHOD, Marketing Skills, CLI-Anything, i-have-adhd, diagram-design, herdr, Ralph Loop, ai-website-cloner-template, Serena, blender-mcp, hallmark, Vibe Kanban, knowledge-work-plugins, t3code, Dyad, Claude SEO, Pixel Agents, worktrunk, Godogen, wigolo, teamai-cli, cc-blender-skill, BMAD-Speckit-SDD-Flow, Google Stitch, GitReverse, Emergent
- **B · Framework Agenti AI & assistenti personali** (30): OpenClaw, browser-use, odysseus, Agent-Reach, MiroFish, NanoBot, DSPy, buzz, PicoClaw, deepagents, agent-lightning, Parlant, OpenWorker, OpenSandbox, QM, Cloudflare Computer, OpenBot, OpenExecutive, OpenMausBot, Argent, Atomic Agent, sia, AgentConnect, SwarmClaw, J.A.R.V.I.S, JARVIS-PA-Lovable, Proactor.ai, agentskills.io, Runable, Aside
- **C · LLM, modelli & inferenza locale** (17): Unsloth AI, OmniRoute, NanoChat, project-nomad, colibri, AirLLM, timesfm, Heretic, DwarfStar (ds4), Qwen3-Coder, whichllm, Magnitude, Kimi K2.5, IQuest-Coder-V1, SpikingBrain-7B, Homura-30B GGUF, Jev (TypeSafe AI)
- **D · RAG, memoria agenti & knowledge base** (18): Graphify, MinerU, Headroom, last30days-skill, codebase-memory-mcp, DeepTutor, open-notebook, book-to-skill, cognee, karakeep, TencentDB-Agent-Memory, TencentDB Agent Memory, Memvid, Easy Dataset, PixelRAG, hister, VideoRAG, OPEN-UPSILON-LOGIC
- **E · OCR & parsing documenti** (7): markitdown, meetily, OfficeCLI, Unlimited-OCR, pdf-inspector, GLM-OCR, Annota AI
- **F · Generazione media (video, immagini, 3D, voce)** (38): MoneyPrinterTurbo, Deep-Live-Cam, OpenMontage, voicebox, VibeVoice, hyperframes, upscayl, chatterbox, video-use, lingbot-map, img2threejs, text-to-cad, HeyGem, palmier-pro, Supertonic, TRELLIS, Qwen3-TTS, Z-Image, LTX-Video, video-shotcraft, OpenShorts, SAM Audio, davinci-resolve-mcp, Diffusion Studio Editor, ASCILINE, JoyAI-Video-Edit, anything2explainer, GLM-Image, Pusa V1.0 (Pusa-VidGen), ComfyUI-Ref2VA-VSA, GenieRedux, ByteDance Seedance 2.0, ByteDance Seed, Mistral AI - Voxtral, Motion, Higgsfield AI, Dreamina (CapCut), Drafted
- **G · Sicurezza & supply-chain** (23): Ghidra, strix, Trivy, maigret, AdGuard Home, bitchat, Anthropic-Cybersecurity-Skills, authentik, NemoClaw, simplex-chat, SkillSpector, amnezia-client, holehe, CubeSandbox, flowsint, Reticulum, Bumblebee, SearchPhone, Mysterium Node, Ravage, North Star, Fingerprint.to, Revealer
- **H · Dev tools, produttività & librerie** (79): prompts.chat (awesome-chatgpt-prompts), free-for-dev, Stirling-PDF, LocalSend, hoppscotch, Dear ImGui, AFFiNE, protobuf, MediaCrawler, Pake, Penpot, Win11Debloat, twenty, Motrix, Ghost, cypress, supervision, ruff, htmx, Puter, appsmith, croc, posthog, gods-eye-view, open-code-review, CasaOS, SmartTube, CloakBrowser, Anki, jenkins, {fmt}, PLFM_RADAR, Invidious, turso, Pascal Editor, superfile, witr, OpenObserve, OpenLogi, Tolaria, PhotoGIMP, Capacitor, LibreTranslate, aisuite, outlines, harper, TREK, vphone-cli, stremio-web, romm, openship, CuPy, Escrcpy, Pumpkin, dicebear, cordis, GeoLibre, docker-android, THREEUI, FckSignups, Lunar, TUIOS, NuvioMobile, iloader, fli, databasement, OpenReply, LogTape, NodeGraphQt, UniFace, prod-FARM-IOS-Core, Skylos, karukan, Fishertiger, TestSprite, Google Code Wiki, Render, Codeberg, SceneAI
- **I · Finanza & trading AI** (6): TradingAgents, ai-hedge-fund, Kronos, OpenAlice, Securo, opennews-mcp
- **J · Ricerca AI, world models & dati vettoriali** (7): awesome-generative-ai-guide, zvec, AutoResearchClaw, SEAL (Self-Adapting LM), Jina AI, Google EmbeddingGemma, Artificial Analysis

## Aggiornare il catalogo
La sorgente è configurata in `config.json` del progetto (chat WhatsApp e/o profili Instagram
monitorati). File di lavoro in `C:\progetti\whatsapp-ai-catalog\`: `github-repos.json`,
`siti-web.json`, `instagram-profili.json` (stato monitoraggio profili),
`gh-meta.json` (metadati attività).
Quando arrivano nuovi reel/link: aggiorna i JSON, poi esegui `python scripts/fetch_gh_meta.py` e
`python scripts/build_catalog.py`. Quest'ultimo rigenera `CATALOGO-AI-TOOLS.md` + `catalogo.json`
e riallinea da solo, in questo file, i **conteggi nella description**, la **data di verifica** e
l'**indice categorie** qui sopra: non modificarli a mano, verrebbero sovrascritti. Il resto della
prosa è libero. La sorgente versionata è `skill/SKILL.md` nel progetto, copiata poi in questa
cartella.

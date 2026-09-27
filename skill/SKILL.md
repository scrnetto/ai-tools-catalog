---
name: ai-tools-catalog
description: >-
  Catalogo curato di 315 repository GitHub e 29 siti/servizi web di strumenti AI e dev
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
4. I dati di attività sono stati verificati il **2026-09-27**: se serve precisione attuale,
   ricontrolla il repo (le stelle/push cambiano nel tempo).

## Categorie e contenuto (indice rapido)
- **A · Coding Agent, Claude Code & sviluppo AI-assistito** (48): Everything Claude Code, DeepSeek Harness (dsh), ponytail, Spec Kit, gstack, awesome-design-md, screenshot-to-code, Archify, impeccable, Cline, BMAD-METHOD, Marketing Skills, i-have-adhd, CLI-Anything, diagram-design, herdr, Ralph Loop, ai-website-cloner-template, Serena, blender-mcp, hallmark, Vibe Kanban, knowledge-work-plugins, t3code, Dyad, Claude SEO, Pixel Agents, worktrunk, mobile-mcp, Godogen, wigolo, teamai-cli, token-optimizer, agy-staff, 49-IDE, claude-token-optimizer, token-optimizer-mcp, motion-web, xAI plugin-marketplace, herdr-nvim, KanVibe, Agent Room, MarkuprPlus, cc-blender-skill, BMAD-Speckit-SDD-Flow, Google Stitch, GitReverse, Emergent
- **B · Framework Agenti AI & assistenti personali** (38): OpenClaw, browser-use, Paperclip, odysseus, Agent-Reach, MiroFish, NanoBot, DSPy, buzz, PicoClaw, deepagents, Cua, agent-lightning, OpenWorker, Parlant, OpenSandbox, QM, ARTEMIS (Google), Cloudflare Computer, OpenBot, OpenExecutive, OpenMausBot, Argent, Atomic Agent, sia, AgentConnect, LiveStream-Agent-Studio, SwarmClaw, AnythingMCP, HashCortX, FutureOS, wade-skills, J.A.R.V.I.S, JARVIS-PA-Lovable, Proactor.ai, agentskills.io, Runable, Aside
- **C · LLM, modelli & inferenza locale** (30): Unsloth AI, OmniRoute, NanoChat, project-nomad, colibri, AirLLM, timesfm, Heretic, Laya, DwarfStar (ds4), Qwen3-Coder, Needle (Cactus), Kev, whichllm, Magnitude, Kimi K2.5, IQuest-Coder-V1, SpikingBrain-7B, awesome-jev-by-typesafe, TypeLLM, rizzo-flow, Spark-X2.5, qwen3.8-Flash-DGX, llama.cpp-adaptive-kv-streaming, qwen38-mtp, SystemOneHarness, dspark-vllm-gx10, Homura-30B GGUF, Jev (TypeSafe AI), Sakana AI Fugu
- **D · RAG, memoria agenti & knowledge base** (19): Graphify, MinerU, Headroom, last30days-skill, codebase-memory-mcp, DeepTutor, open-notebook, book-to-skill, cognee, karakeep, TencentDB-Agent-Memory, TencentDB Agent Memory, Memvid, Easy Dataset, PixelRAG, hister, VideoRAG, EvoOntology, OPEN-UPSILON-LOGIC
- **E · OCR & parsing documenti** (9): markitdown, Docling, paperless-ngx, OfficeCLI, meetily, Unlimited-OCR, pdf-inspector, GLM-OCR, Annota AI
- **F · Generazione media (video, immagini, 3D, voce)** (56): MoneyPrinterTurbo, Deep-Live-Cam, OpenMontage, voicebox, VibeVoice, hyperframes, upscayl, Open-Generative-AI (ex Open-Higgsfield-AI), video-use, chatterbox, lingbot-map, img2threejs, text-to-cad, HeyGem, palmier-pro, Supertonic, TRELLIS, Qwen3-TTS, Z-Image, LTX-Video, video-shotcraft, AutoClip, OpenShorts, SAM Audio, davinci-resolve-mcp, Diffusion Studio Editor, ASCILINE, anything2explainer, JoyAI-Video-Edit, Qwen-Image-2.1, Shrimply, GLM-Image, AutoShorts, StemKit, CrispASR, Pusa V1.0 (Pusa-VidGen), ComfyUI-Ref2VA-VSA, OmniChar, HotClip, infinite-livestream, ComfyUI-outputlists-combiner, yovoice, SeedVR2 TensorRT Studio, X-MinimaxH3, ComfyUI-Continuity, machine-vision, GenieRedux, comfyui-node-organizer, LinCa, ByteDance Seedance 2.0, ByteDance Seed, Mistral AI - Voxtral, Motion, Higgsfield AI, Dreamina (CapCut), Drafted
- **G · Sicurezza & supply-chain** (30): Ghidra, strix, Trivy, maigret, AdGuard Home, bitchat, Anthropic-Cybersecurity-Skills, authentik, NemoClaw, simplex-chat, SkillSpector, amnezia-client, holehe, MVT (Mobile Verification Toolkit), CubeSandbox, Crucix, flowsint, OpenBao, Reticulum, Bumblebee, SearchPhone, cve-mcp-server, Mysterium Node, AIF, stolen-thoughts, Ravage, Archify (Salah-XD), North Star, Fingerprint.to, Revealer
- **H · Dev tools, produttività & librerie** (93): prompts.chat (awesome-chatgpt-prompts), free-for-dev, Stirling-PDF, LocalSend, hoppscotch, Dear ImGui, AFFiNE, protobuf, MediaCrawler, Pake, Penpot, Win11Debloat, twenty, Motrix, Ghost, supervision, cypress, ruff, htmx, gods-eye-view, Puter, open-code-review, appsmith, croc, posthog, CasaOS, SmartTube, CloakBrowser, Anki, Recordly, jenkins, {fmt}, PLFM_RADAR, Invidious, turso, Pascal Editor, superfile, Cap, witr, OpenLogi, OpenObserve, Tolaria, PhotoGIMP, LibreTranslate, Capacitor, aisuite, harper, outlines, vphone-cli, TREK, stremio-web, romm, openship, CuPy, Escrcpy, Pumpkin, dicebear, cordis, GeoLibre, docker-android, THREEUI, FckSignups, Fleetbase, TUIOS, Lunar, NuvioMobile, iloader, Lap, fli, databasement, OpenReply, PDFcn, LogTape, UniFace, NodeGraphQt, Bruin, prod-FARM-IOS-Core, open-compute, Skylos, DaC (Dashboard as Code), text-humanizer, karukan, ArchUnitPython, wacrawl, Blink, restoredrill, Murmur, Fishertiger, TestSprite, Google Code Wiki, Render, Codeberg, SceneAI
- **I · Finanza & trading AI** (9): TradingAgents, ai-hedge-fund, Kronos, OpenStock, OpenAlice, Securo, opennews-mcp, India Trade CLI, AlphaMemo
- **J · Ricerca AI, world models & dati vettoriali** (12): awesome-generative-ai-guide, zvec, AutoResearchClaw, SEAL (Self-Adapting LM), robot_keyframe_kit, drawtonomy, UniPhysGen, PowerAtlas, Pocket-SLAM, Jina AI, Google EmbeddingGemma, Artificial Analysis

## Aggiornare il catalogo
Questa cartella è **generata**: non modificarne i file. La sorgente è il repository
`ai-tools-catalog` (https://github.com/scrnetto/ai-tools-catalog), che contiene la configurazione
(`config.json`: chat WhatsApp e/o profili Instagram monitorati) e i file di lavoro:
`github-repos.json`, `siti-web.json`, `instagram-profili.json` (stato monitoraggio profili),
`gh-meta.json` (metadati attività).
Quando arrivano nuovi reel/link: aggiorna i JSON, poi esegui `python3 scripts/fetch_gh_meta.py` e
`python3 scripts/build_catalog.py`. Quest'ultimo rigenera `CATALOGO-AI-TOOLS.md` + `catalogo.json`
e riallinea da solo, in questo file, i **conteggi nella description**, la **data di verifica** e
l'**indice categorie** qui sopra: non modificarli a mano, verrebbero sovrascritti. Il resto della
prosa è libero. La sorgente versionata è `skill/SKILL.md` nel progetto, copiata poi nelle cartelle
in cui la skill è installata.

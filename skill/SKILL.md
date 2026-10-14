---
name: ai-tools-catalog
description: >-
  Catalogo curato di 727 repository GitHub e 45 siti/servizi web di strumenti AI e dev
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
  ultimo_push, attivita, licenza, linguaggio, fonte`; `origine` (`locale`/`modificata`) solo sulle
  voci aggiunte o corrette dall'utente.
- **`catalogo.html`** — lo stesso catalogo come pagina web con ricerca e filtri, che funziona
  offline. Se l'utente vuole **sfogliare o consultare il catalogo da sé**, indicagli il percorso
  di questo file (o aprilo nel browser, se te lo chiede); per rispondere a una domanda usa gli
  altri due file.

## Come usarla
1. Quando l'utente cerca uno strumento o chiede "cosa esiste per fare X", **apri
   `CATALOGO-AI-TOOLS.md`** (o filtra `catalogo.json`) e proponi le voci pertinenti.
2. Cita sempre **stato di attività** (🟢/🟡/🔴, stelle, ultimo push) e **licenza** se rilevante per
   l'uso nel progetto dell'utente.
3. Se nessuna voce calza, dillo chiaramente: il catalogo è una raccolta personale, non esaustivo.
4. I dati di attività sono stati verificati il **2026-09-27**: se serve precisione attuale,
   ricontrolla il repo (le stelle/push cambiano nel tempo).

## Aggiornamenti del catalogo
La prima volta che usi questa skill in una sessione, esegui `python3 check_update.py` da questa
cartella (è lo script accanto a questo file). Controlla al massimo una volta al giorno se il
catalogo pubblicato è cambiato, e non modifica niente.
- Se riporta una novità, **dillo all'utente** con il comando che lo script indica. **Non eseguire
  l'aggiornamento tu**: scarica ed esegue codice nuovo, e lo decide l'utente.
- Se il controllo non riesce, prosegui con il catalogo installato senza insistere.
- L'aggiornamento conserva le voci aggiunte dall'utente: stanno in file separati che il catalogo
  pubblicato non tocca.

## Categorie e contenuto (indice rapido)
- **A · Coding Agent, Claude Code & sviluppo AI-assistito** (123): Superpowers, Skills di Matt Pocock, Everything Claude Code, DeepSeek Harness (dsh), Andrej Karpathy Skills, ponytail, Spec Kit, gstack, awesome-design-md, Taste Skill, Orca, screenshot-to-code, Archify, impeccable, Cline, BMAD-METHOD, Marketing Skills, i-have-adhd, CLI-Anything, diagram-design, herdr, Ralph Loop, ai-website-cloner-template, skills (Vercel Labs), Claude Code Templates, Serena, blender-mcp, hallmark, context-mode, Task Master, Vibe Kanban, cmux, Beads, knowledge-work-plugins, Happy, t3code, Dyad, Claude SEO, DeepCode, Codex ChatGPT Web, Patent Disclosure Skill, Loop Engineering, Trail Code (ex Graft), Anatomy, Claude Code Action, Pixel Agents, worktrunk, mobile-mcp, Universal Modder, OpenRig, Codex with ChatGPT, Godogen, Autoresearch, Anti-Slop, SwiftUI Agent Skill (SwiftUI Pro), wigolo, HumanLayer Skills (show-me), DevSpace, Coucou, teamai-cli, LazyCodex, fx, Scrollcraft, Logo Design Skill, Whiteboard, sepia, Aaron Marketing Skills, Appllama Skills, Codenotch, jevgrep, Stop That Shit, token-optimizer, Headcount, pstack-claude, WorkDaddy, Oil UI, Human Review, Backpass, Mindwalk, GoLive Skill, openharness, AI Copywriter, Zoetrope, Auteur, AgentTrail, Motion Skills, Airship, Papermorph, agy-staff, My Free Code, 49-IDE, claude-token-optimizer, Refactoring UI Skill, Habblaud, token-optimizer-mcp, motion-web, Roast Room, Vicoa, HERO Anti-OverDefense, Claude Reflect System, Codync, BASE (Builder's Automated State Engine), Micracode, xAI plugin-marketplace, Skills-4-SE, product-mode, herdr-nvim, GitBot, Quicksand, clodfarm, Benzi, Genart Skill, KanVibe, LintLang, Agent Room, Agent HUD, MarkuprPlus, cc-blender-skill, BMAD-Speckit-SDD-Flow, Google Stitch, GitReverse, Emergent, Atoms
- **B · Framework Agenti AI & assistenti personali** (84): OpenClaw, Hermes Agent, browser-use, Awesome MCP Servers, MCP Servers, Paperclip, odysseus, Agent-Reach, MiroFish, Multica, AIRI, NanoBot, DSPy, buzz, Nuwa Skill, Composio, PicoClaw, deepagents, Cua, OpenWork, Jev Ultrafast, LifeOS, agent-lightning, SkillOpt, OpenWorker, Parlant, OpenSandbox, QM, Cloudflare OS, ARTEMIS (Google), Cloudflare Computer, PraisonAI, Munder Difflin, Osaurus, LoopX, OpenBot, Raven, OpenExecutive, OpenDots, FrontierAgent, Cumora, OpenMausBot, Grok Bot 0.18 reconstructed, Mercury Agent, Awesome Agents, Argent, Atomic Agent, PenEcho, sia, Call.md, WebBrain, AgentConnect, YouTube Agent Skill, nanoMuse, OpenDroid, LiveStream-Agent-Studio, Switch, AgentCraft, DSH Worktable, SwarmClaw, Overmind, Avibe, AI Employees, awesome-jev (kydlikebtc), dsh-genui, Hermes3D, Watch Skill, AnythingMCP, Mu, OpenWorkBuddy, Dodaios (Personal Jarvis), Gentle Dot, HashCortX, DeepSeek Harness Mobile, FutureOS, wade-skills, J.A.R.V.I.S, JARVIS-PA-Lovable, Proactor.ai, agentskills.io, Runable, Aside, Glasser, Okara AI
- **C · LLM, modelli & inferenza locale** (57): Open WebUI, Unsloth AI, OmniRoute, LiteLLM, NanoChat, BitNet, project-nomad, colibri, AirLLM, timesfm, Heretic, Laya, DwarfStar (ds4), Qwen3-Coder, Needle (Cactus), DeepGEMM, ODS, Kev, whichllm, NVIDIA Model Optimizer, Magnitude, Phi Cookbook, Switchyard, CLM (Contrastive Language Models), Kimi K2.5, HyperQwen, IQuest-Coder-V1, SpikingBrain-7B, AnyJev, awesome-jev-by-typesafe, TypeLLM, GLM-5.3 Flash EXL3 su 2x DGX Spark, rizzo-flow, Oriveo, vLLM CLI, OpenGrok, LLM2Jev, Spark-X2.5, qwen3.8-Flash-DGX, llama.cpp-adaptive-kv-streaming, qwen38-mtp, vllm-backport, Local AI Registry, SystemOneHarness, Kyojin, NoLlama, Whallm, dspark-vllm-gx10, Prism, Qwen3.8-27B su RTX PRO 6000, Homura-30B GGUF, Jev (TypeSafe AI), Sakana AI Fugu, Duck.ai, MixRoute, Liquid AI d1, OpenAI Decisions API
- **D · RAG, memoria agenti & knowledge base** (38): Graphify, MinerU, Headroom, Mem0, last30days-skill, codebase-memory-mcp, DeepTutor, open-notebook, PageIndex, GraphRAG, book-to-skill, cognee, karakeep, TencentDB-Agent-Memory, TencentDB Agent Memory, Memvid, Easy Dataset, PixelRAG, Production Agentic RAG Course, ai-memory, Utopia, Engram, hister, PipesHub, Knowhere, VideoRAG, AI Knowledge Graph, cocoindex-code, Ontology Playground, OpenWolf, EdgeEver, Compass, brain.md, NexusRAG, Open Second Brain, EvoOntology, oikb, OPEN-UPSILON-LOGIC
- **E · OCR & parsing documenti** (21): markitdown, Docling, PPT Master, paperless-ngx, OfficeCLI, meetily, Unlimited-OCR, anydoc, pdf-inspector, PdfCraft, Chandra, Wordcraft, open-slide, GLM-OCR, VI-Translate, light-ocr, OpenTakeoff, mac-ocr, gyotaku, handout-remake, Annota AI
- **F · Generazione media (video, immagini, 3D, voce)** (121): MoneyPrinterTurbo, Deep-Live-Cam, VoiceStudio, Remotion, OpenMontage, PhotoCraft, voicebox, VibeVoice, hyperframes, upscayl, Awesome GPT Image 2, Open-Generative-AI (ex Open-Higgsfield-AI), InvokeAI, ArtCraft, video-use, chatterbox, lingbot-map, img2threejs, text-to-cad, brag, HeyGem, palmier-pro, Supertonic, TRELLIS, Qwen3-TTS, FilmCraft, Voice-Pro, LightCraft, Z-Image, LTX-Video, Awesome GPT Image 2 (YouMind), MiniMax H3, video-shotcraft, AutoClip, VectorCraft, inpaint-web, OpenShorts, awesome-opus5-5-videos, Huashu Art Motion, SAM Audio, Mesh2Motion, davinci-resolve-mcp, Diffusion Studio Editor, FreeFlow, h3.c, ASCILINE, fframes, onetake, FreeCut, anything2explainer, FreeVideo, Drift, JoyAI-Video-Edit, UniMate, Audio8 TTS, Spirula Studio, Gemma Translator, Qwen-Image-2.1, ManimGX, Shrimply, Motion2MixamoRig, Capptivo, GLM-Image, Scenario Skills, NullMotion, AutoShorts, MG Styles 15, StemKit, CrispASR, Animate, Mesh Avatar Studio, Pusa V1.0 (Pusa-VidGen), Infinite TV, Mortiflix, tiny-tts, awesome-generative-ai-apps, VODER, Code Video Model, Motionmaxxing, ComfyUI-Ref2VA-VSA, OmniChar, Framefields, ff-tracking, X-AnyLabeling-Server, Aseprite AI Artist, Facet, HotClip, Showtime, infinite-livestream, ComfyUI-outputlists-combiner, yovoice, High-Angle Robust Fast Face Alignment, H3 Storyboard Skill, SeedVR2 TensorRT Studio, ComfyUI HR Endless Sampler, Tesseract (Mirage), Claude Paint, X-MinimaxH3, Rembrandt, ComfyUI-Continuity, machine-vision, OpenCardboard, GenieRedux, Context-Matched Distillation, TopoSurfel, comfyui-node-organizer, Minomeet, LinCa, ByteDance Seedance 2.0, ByteDance Seed, Mistral AI - Voxtral, Motion, Higgsfield AI, Dreamina (CapCut), Drafted, MeetNotes, Raylight, NVIDIA Body Pose (build.nvidia.com), Tripo AI, claudevideo.org, NVIDIA Active Speaker Detection (NIM)
- **G · Sicurezza & supply-chain** (49): REA, Clash Verge Rev, Ghidra, strix, reverse-skill, Trivy, maigret, AdGuard Home, bitchat, Web-Check, Anthropic-Cybersecurity-Skills, Cloudflare Security Audit Skill, OpenWrt, iFixAi, authentik, NemoClaw, simplex-chat, GhostTrack, SkillSpector, NVIDIA OpenShell, amnezia-client, holehe, MVT (Mobile Verification Toolkit), CubeSandbox, Crucix, flowsint, OpenBao, Reticulum, Bumblebee, Sogen, Pentest Swarm AI, wifit3, BlockAds, SearchPhone, OneTerm, cve-mcp-server, Mysterium Node, rizzo-pii, AIF, GrapheneOS server, FaceGate, TrustMeBro, IAGA Sentinel, stolen-thoughts, Ravage, Archify (Salah-XD), North Star, Fingerprint.to, Revealer
- **H · Dev tools, produttività & librerie** (231): TensorFlow, Flutter, prompts.chat (awesome-chatgpt-prompts), Next.js, free-for-dev, Excalidraw, Rust, Stirling-PDF, LocalSend, Uptime Kuma, System Design 101, hoppscotch, Caddy, Dear ImGui, AFFiNE, protobuf, MediaCrawler, Pake, Penpot, Win11Debloat, twenty, Motrix, Ghost, supervision, cypress, Kubernetes The Hard Way, ruff, htmx, Slidev, Sentry, Reactive Resume, gods-eye-view, Puter, open-code-review, appsmith, croc, posthog, CasaOS, Detectron2, SmartTube, CloakBrowser, Anki, Recordly, Vorssaint, Driver.js, jenkins, {fmt}, PLFM_RADAR, Invidious, turso, Pascal Editor, superfile, Wechaty, Cap, witr, OpenLogi, OpenObserve, hey, tiny11builder, Tolaria, PhotoGIMP, navi, Apprise, Data Formulator, Effect, LibreTranslate, Capacitor, Quickemu, aisuite, harper, outlines, vphone-cli, Mitosis, TREK, stremio-web, romm, quiche, openship, CuPy, Escrcpy, openGym, Pumpkin, xxHash, Reclip, xtool, e2e (Tester Army), Gumroad, dicebear, Pocket ID, M3E Canvas, cordis, TileLang, RAD Debugger, GrowthBook, GeoLibre, docker-android, PipePipe, THREEUI, yoinks, LiveCharts2, Patchright, CADCraft, FckSignups, Plexo, Human Atlas, designlang (design-extract), Trackers (Roboflow), Fleetbase, CS 341 Coursebook, TUIOS, Lunar, NuvioMobile, iloader, definitive-opensource, Lap, shadcn Lint, fli, TanStack AI, BitChord, Piik, Takumi, disktree, Titanium Browser, Storefront UI, Audiobookshelf app, Openvid, Paymenter, omdrop-owl, Walgit, Try Omarchy, vgpu, Goldie, databasement, OpenReply, Frappe Builder, PDFcn, Muse Gadget SDK, Tendedero, terminal-code, MatrixOne, LogTape, UniFace, AlterSend, NodeGraphQt, Bloub, Bruin, cn, Breakscale, prod-FARM-IOS-Core, pgbot, CaskHub, Workout Guide, Citadel, open-compute, NzbDAV, RAWmakase, pg-jev, ha.mr, Boop, Shapeshift, Dextop, OpenFrame CLI, PairPods, Doop, UniTerm, Skylos, Figranium, DaC (Dashboard as Code), RankMeFast, text-humanizer, karukan, ShojiWM, Project SuperDex, Omarchy on CachyOS, ArchUnitPython, Shiru, OpenAnalytics, Bisibility, VITRA, PecoFence, Spun, Starboard, Libertix, MacSpace, HyprFM, Farm.js, Beautiful UI, HFlow, Fibo, Natural Disasters, Toast, PhreshOS, Mousiki, House Planner, Open Flow, QuickLiquid, CogSend, Chroncal, wacrawl, Square, Blink, awesome-cad, RenCal, Desigma, Loadersz, Lot Vulture, BentoDesk, Shizzi, Codemagic Patch, Kaleta, restoredrill, Procedural Buildings Three.js, CoreDeck, pg_column_tetris, Murmur, Jean Claude, Watercolor Playground, Pulse, Fishertiger, BuckIt, HABirdDashboard, HandUMI, WaveeMusic, design-md-extractor, TestSprite, Google Code Wiki, Render, Codeberg, SceneAI, NameThatUI, Mobbin
- **I · Finanza & trading AI** (12): TradingAgents, ai-hedge-fund, Kronos, NautilusTrader, OpenStock, OpenAlice, Securo, opennews-mcp, PanWatch, India Trade CLI, Quandora Plugins, AlphaMemo
- **J · Ricerca AI, world models & dati vettoriali** (36): PyTorch, Ultralytics YOLO, Meilisearch, awesome-generative-ai-guide, zvec, AutoResearchClaw, OpenEvolve, OpenResearch, PRAXIST, GPU Perf Engineering Resources, zvec-grep, SEAL (Self-Adapting LM), ABot-Recon, OpenResearcher, ClearAI, SCM, Zero-WAM, Code as World, LeVJEPA, pgContext, Poirot, Paper Radar, pwc-cli, RSI-Exam, robot_keyframe_kit, Open Source Leader Arm, drawtonomy, VibeSys, OmniSeek, UniPhysGen, PowerAtlas, Pocket-SLAM, Jina AI, Google EmbeddingGemma, Artificial Analysis, Bone Suppression Chest X-ray (Qure.ai, HF Space)

## Aggiornare il catalogo
Questa cartella è **generata**: non modificarne i file. La sorgente è il repository
`ai-tools-catalog` (https://github.com/scrnetto/ai-tools-catalog); dove è installato lo dice
`installazione.json`. Il catalogo qui è l'unione di due parti:
- le voci **pubblicate**: `github-repos.json`, `siti-web.json`, `gh-meta.json`;
- le voci **dell'utente**: gli stessi nomi con `.local.json` (`github-repos.local.json`, ...),
  ignorati da git. Una voce locale con lo stesso URL di una pubblicata la completa o la
  corregge; con `"nascondi": true` la toglie dal catalogo.
Chi non pubblica il catalogo aggiunge le voci **solo** nei `.local.json`. Poi esegue
`python3 scripts/fetch_gh_meta.py` e `python3 scripts/build_catalog.py`. Quest'ultimo rigenera
`CATALOGO-AI-TOOLS.md`, `catalogo.json` e `catalogo.html` e riallinea da solo, in questo file, i **conteggi nella
description**, la **data di verifica** e l'**indice categorie** qui sopra: non modificarli a mano,
verrebbero sovrascritti. Il resto della prosa è libero. La sorgente versionata è `skill/SKILL.md`
nel progetto, copiata poi nelle cartelle in cui la skill è installata.

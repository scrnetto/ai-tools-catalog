---
name: ai-tools-catalog
description: >-
  Catalogo curato di 725 repository GitHub e 45 siti/servizi web di strumenti AI e dev
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
4. I dati di attività sono stati verificati il **2026-10-15**: se serve precisione attuale,
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
- **A · Coding Agent, Claude Code & sviluppo AI-assistito** (123): Superpowers, Skills di Matt Pocock, Everything Claude Code, DeepSeek Harness (dsh), Andrej Karpathy Skills, ponytail, Spec Kit, gstack, awesome-design-md, Taste Skill, Orca, Archify, impeccable, screenshot-to-code, Cline, i-have-adhd, diagram-design, Marketing Skills, BMAD-METHOD, CLI-Anything, herdr, Ralph Loop, ai-website-cloner-template, skills (Vercel Labs), Claude Code Templates, blender-mcp, Serena, hallmark, knowledge-work-plugins, context-mode, Vibe Kanban, Task Master, cmux, Beads, t3code, Happy, Dyad, Claude SEO, DeepCode, Codex ChatGPT Web, Patent Disclosure Skill, Loop Engineering, Anatomy, Trail Code (ex Graft), Pixel Agents, Claude Code Action, mobile-mcp, worktrunk, Universal Modder, OpenRig, Codex with ChatGPT, Godogen, Autoresearch, Anti-Slop, SwiftUI Agent Skill (SwiftUI Pro), teamai-cli, wigolo, HumanLayer Skills (show-me), DevSpace, Coucou, LazyCodex, Scrollcraft, fx, Logo Design Skill, Whiteboard, sepia, Aaron Marketing Skills, Appllama Skills, Codenotch, jevgrep, Stop That Shit, token-optimizer, Headcount, pstack-claude, WorkDaddy, Oil UI, Backpass, Human Review, Mindwalk, GoLive Skill, openharness, AI Copywriter, Zoetrope, Auteur, AgentTrail, Motion Skills, agy-staff, motion-web, Papermorph, Airship, 49-IDE, My Free Code, claude-token-optimizer, Refactoring UI Skill, Habblaud, Roast Room, token-optimizer-mcp, Vicoa, HERO Anti-OverDefense, Claude Reflect System, Codync, BASE (Builder's Automated State Engine), Micracode, xAI plugin-marketplace, herdr-nvim, Skills-4-SE, product-mode, Quicksand, GitBot, clodfarm, Benzi, Genart Skill, KanVibe, LintLang, Agent Room, cc-blender-skill, Agent HUD, MarkuprPlus, BMAD-Speckit-SDD-Flow, Google Stitch, GitReverse, Emergent, Atoms
- **B · Framework Agenti AI & assistenti personali** (84): OpenClaw, Hermes Agent, browser-use, Paperclip, Agent-Reach, Awesome MCP Servers, odysseus, MCP Servers, MiroFish, Multica, AIRI, NanoBot, DSPy, buzz, Nuwa Skill, Composio, deepagents, PicoClaw, Cua, OpenWork, Jev Ultrafast, LifeOS, agent-lightning, OpenWorker, SkillOpt, Parlant, OpenSandbox, QM, ARTEMIS (Google), Cloudflare OS, Cloudflare Computer, PraisonAI, Munder Difflin, Osaurus, OpenBot, LoopX, OpenExecutive, Raven, OpenDots, FrontierAgent, OpenMausBot, Cumora, Grok Bot 0.18 reconstructed, Mercury Agent, Atomic Agent, Argent, Awesome Agents, PenEcho, sia, Call.md, AgentConnect, WebBrain, YouTube Agent Skill, LiveStream-Agent-Studio, nanoMuse, OpenDroid, Switch, AgentCraft, DSH Worktable, AnythingMCP, SwarmClaw, Overmind, Avibe, AI Employees, awesome-jev (kydlikebtc), dsh-genui, Hermes3D, Watch Skill, Mu, OpenWorkBuddy, Dodaios (Personal Jarvis), HashCortX, Gentle Dot, DeepSeek Harness Mobile, FutureOS, wade-skills, J.A.R.V.I.S, JARVIS-PA-Lovable, Proactor.ai, agentskills.io, Runable, Aside, Glasser, Okara AI
- **C · LLM, modelli & inferenza locale** (57): Open WebUI, Unsloth AI, OmniRoute, LiteLLM, NanoChat, colibri, BitNet, project-nomad, AirLLM, Heretic, timesfm, Laya, DwarfStar (ds4), Qwen3-Coder, Needle (Cactus), Kev, DeepGEMM, ODS, whichllm, Magnitude, NVIDIA Model Optimizer, Phi Cookbook, Switchyard, CLM (Contrastive Language Models), Kimi K2.5, HyperQwen, SpikingBrain-7B, IQuest-Coder-V1, AnyJev, TypeLLM, rizzo-flow, Spark-X2.5, GLM-5.3 Flash EXL3 su 2x DGX Spark, Oriveo, vLLM CLI, OpenGrok, qwen3.8-Flash-DGX, LLM2Jev, llama.cpp-adaptive-kv-streaming, qwen38-mtp, vllm-backport, Local AI Registry, SystemOneHarness, Kyojin, NoLlama, Whallm, dspark-vllm-gx10, Prism, Qwen3.8-27B su RTX PRO 6000, awesome-jev-by-typesafe, Homura-30B GGUF, Jev (TypeSafe AI), Sakana AI Fugu, Duck.ai, MixRoute, Liquid AI d1, OpenAI Decisions API
- **D · RAG, memoria agenti & knowledge base** (37): Graphify, MinerU, Headroom, Mem0, last30days-skill, codebase-memory-mcp, DeepTutor, open-notebook, PageIndex, GraphRAG, book-to-skill, cognee, karakeep, TencentDB Agent Memory, Memvid, Easy Dataset, PixelRAG, Production Agentic RAG Course, ai-memory, Utopia, Engram, hister, PipesHub, Knowhere, VideoRAG, AI Knowledge Graph, cocoindex-code, Ontology Playground, OpenWolf, EdgeEver, Compass, EvoOntology, brain.md, NexusRAG, Open Second Brain, oikb, OPEN-UPSILON-LOGIC
- **E · OCR & parsing documenti** (21): markitdown, Docling, PPT Master, paperless-ngx, OfficeCLI, meetily, Unlimited-OCR, anydoc, pdf-inspector, PdfCraft, Wordcraft, Chandra, open-slide, GLM-OCR, VI-Translate, light-ocr, OpenTakeoff, mac-ocr, gyotaku, handout-remake, Annota AI
- **F · Generazione media (video, immagini, 3D, voce)** (121): MoneyPrinterTurbo, Deep-Live-Cam, OpenMontage, VoiceStudio, Remotion, hyperframes, PhotoCraft, voicebox, VibeVoice, upscayl, Awesome GPT Image 2, Open-Generative-AI (ex Open-Higgsfield-AI), video-use, InvokeAI, ArtCraft, chatterbox, text-to-cad, img2threejs, lingbot-map, brag, HeyGem, palmier-pro, TRELLIS, Qwen3-TTS, Supertonic, FilmCraft, Voice-Pro, LightCraft, Z-Image, video-shotcraft, LTX-Video, Awesome GPT Image 2 (YouMind), MiniMax H3, AutoClip, VectorCraft, OpenShorts, inpaint-web, awesome-opus5-5-videos, Huashu Art Motion, SAM Audio, davinci-resolve-mcp, Mesh2Motion, Diffusion Studio Editor, FreeFlow, h3.c, ASCILINE, fframes, anything2explainer, onetake, FreeCut, JoyAI-Video-Edit, Qwen-Image-2.1, FreeVideo, Drift, UniMate, Audio8 TTS, Spirula Studio, Gemma Translator, yovoice, ManimGX, AutoShorts, Shrimply, Motion2MixamoRig, GLM-Image, Capptivo, StemKit, Scenario Skills, NullMotion, MG Styles 15, CrispASR, Animate, Mesh Avatar Studio, Pusa V1.0 (Pusa-VidGen), Infinite TV, Mortiflix, tiny-tts, awesome-generative-ai-apps, OmniChar, VODER, Motionmaxxing, Code Video Model, ComfyUI-Ref2VA-VSA, ff-tracking, Framefields, HotClip, Aseprite AI Artist, X-AnyLabeling-Server, Facet, Showtime, infinite-livestream, ComfyUI-outputlists-combiner, High-Angle Robust Fast Face Alignment, H3 Storyboard Skill, SeedVR2 TensorRT Studio, ComfyUI HR Endless Sampler, Tesseract (Mirage), ComfyUI-Continuity, X-MinimaxH3, Claude Paint, Rembrandt, machine-vision, OpenCardboard, GenieRedux, Context-Matched Distillation, TopoSurfel, comfyui-node-organizer, Minomeet, LinCa, ByteDance Seedance 2.0, ByteDance Seed, Mistral AI - Voxtral, Motion, Higgsfield AI, Dreamina (CapCut), Drafted, MeetNotes, Raylight, NVIDIA Body Pose (build.nvidia.com), Tripo AI, claudevideo.org, NVIDIA Active Speaker Detection (NIM)
- **G · Sicurezza & supply-chain** (49): REA, Clash Verge Rev, Ghidra, strix, reverse-skill, maigret, Trivy, AdGuard Home, bitchat, Web-Check, Anthropic-Cybersecurity-Skills, Cloudflare Security Audit Skill, OpenWrt, iFixAi, authentik, NemoClaw, SkillSpector, simplex-chat, GhostTrack, NVIDIA OpenShell, amnezia-client, MVT (Mobile Verification Toolkit), holehe, CubeSandbox, Crucix, flowsint, OpenBao, Reticulum, Bumblebee, Sogen, Pentest Swarm AI, wifit3, BlockAds, SearchPhone, OneTerm, cve-mcp-server, AIF, Mysterium Node, rizzo-pii, GrapheneOS server, FaceGate, TrustMeBro, IAGA Sentinel, stolen-thoughts, Ravage, Archify (Salah-XD), North Star, Fingerprint.to, Revealer
- **H · Dev tools, produttività & librerie** (230): TensorFlow, Flutter, prompts.chat (awesome-chatgpt-prompts), Next.js, free-for-dev, Excalidraw, Rust, LocalSend, Stirling-PDF, Uptime Kuma, System Design 101, hoppscotch, Caddy, Dear ImGui, AFFiNE, protobuf, MediaCrawler, Pake, Penpot, Win11Debloat, twenty, Motrix, gods-eye-view, Ghost, supervision, cypress, Kubernetes The Hard Way, ruff, htmx, Slidev, open-code-review, Sentry, Reactive Resume, Puter, appsmith, croc, posthog, CasaOS, SmartTube, Detectron2, Recordly, CloakBrowser, Anki, Vorssaint, PLFM_RADAR, Driver.js, jenkins, {fmt}, Invidious, Pascal Editor, turso, superfile, OpenLogi, Wechaty, Cap, witr, OpenObserve, hey, tiny11builder, Tolaria, PhotoGIMP, navi, Apprise, Data Formulator, Effect, LibreTranslate, Capacitor, Quickemu, harper, aisuite, outlines, vphone-cli, TREK, openship, stremio-web, Mitosis, romm, quiche, Pumpkin, CuPy, Escrcpy, openGym, xxHash, xtool, Reclip, e2e (Tester Army), Gumroad, dicebear, Pocket ID, M3E Canvas, cordis, TileLang, RAD Debugger, GrowthBook, GeoLibre, docker-android, PipePipe, THREEUI, yoinks, LiveCharts2, TUIOS, CADCraft, Patchright, FckSignups, Fleetbase, Plexo, Human Atlas, designlang (design-extract), iloader, Trackers (Roboflow), NuvioMobile, Lap, CS 341 Coursebook, Lunar, definitive-opensource, fli, BitChord, shadcn Lint, TanStack AI, Piik, Takumi, disktree, PDFcn, Titanium Browser, Storefront UI, Audiobookshelf app, Openvid, Paymenter, omdrop-owl, OpenReply, Walgit, Try Omarchy, databasement, vgpu, Goldie, Frappe Builder, Tendedero, Muse Gadget SDK, terminal-code, UniFace, MatrixOne, LogTape, AlterSend, NodeGraphQt, Bloub, Bruin, prod-FARM-IOS-Core, cn, Breakscale, open-compute, pgbot, CaskHub, Workout Guide, Citadel, RAWmakase, NzbDAV, pg-jev, ha.mr, Boop, Shapeshift, Dextop, OpenFrame CLI, PairPods, Doop, UniTerm, Skylos, DaC (Dashboard as Code), Figranium, RankMeFast, karukan, ShojiWM, Project SuperDex, Omarchy on CachyOS, ArchUnitPython, Shiru, OpenAnalytics, Bisibility, VITRA, PecoFence, Spun, Starboard, Libertix, MacSpace, HyprFM, Farm.js, Beautiful UI, HFlow, Fibo, Natural Disasters, Toast, PhreshOS, Mousiki, House Planner, Open Flow, QuickLiquid, CogSend, Chroncal, wacrawl, Square, Desigma, Blink, awesome-cad, RenCal, Loadersz, Lot Vulture, BentoDesk, Shizzi, Codemagic Patch, Kaleta, restoredrill, Procedural Buildings Three.js, CoreDeck, pg_column_tetris, Murmur, Jean Claude, Pulse, Watercolor Playground, Fishertiger, BuckIt, HABirdDashboard, HandUMI, WaveeMusic, design-md-extractor, TestSprite, Google Code Wiki, Render, Codeberg, SceneAI, NameThatUI, Mobbin
- **I · Finanza & trading AI** (12): TradingAgents, ai-hedge-fund, Kronos, NautilusTrader, OpenStock, OpenAlice, Securo, opennews-mcp, PanWatch, India Trade CLI, Quandora Plugins, AlphaMemo
- **J · Ricerca AI, world models & dati vettoriali** (36): PyTorch, Ultralytics YOLO, Meilisearch, awesome-generative-ai-guide, zvec, AutoResearchClaw, OpenEvolve, OpenResearch, PRAXIST, GPU Perf Engineering Resources, zvec-grep, SEAL (Self-Adapting LM), ABot-Recon, OpenResearcher, ClearAI, SCM, Zero-WAM, Code as World, LeVJEPA, pgContext, Poirot, Paper Radar, pwc-cli, RSI-Exam, robot_keyframe_kit, Open Source Leader Arm, drawtonomy, VibeSys, OmniSeek, UniPhysGen, Pocket-SLAM, PowerAtlas, Jina AI, Google EmbeddingGemma, Artificial Analysis, Bone Suppression Chest X-ray (Qure.ai, HF Space)

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

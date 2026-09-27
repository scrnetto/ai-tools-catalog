#!/usr/bin/env python3
"""
Genera il catalogo unificato (repo GitHub + siti web) e aggiorna la skill globale
'ai-tools-catalog' (formato Agent Skills, letto da Claude Code, OpenCode, Codex, Gemini CLI...).

Input  (nella root del progetto):
    config.json                -> opzionale (vedi config.example.json): titolo e fonte del catalogo
    github-repos.json          -> ogni repo deve avere: id, progetto, descrizione, url,
                                   categoria, fonte, macro (A..Z), uso
                                   opzionale: licenza -> verificata a mano sul file LICENSE, prevale su
                                   quella di GitHub (che per le licenze non standard dice NOASSERTION)
    siti-web.json              -> ogni sito: id, sito, url, descrizione, fonte, macro, uso
    gh-meta.json               -> metadati attività per id repo (da fetch_gh_meta.py + scraping)

Output:
    catalogo-unificato.json    (root progetto)
    CATALOGO-AI-TOOLS.md       (root progetto)
    skill/SKILL.md             (root progetto: conteggi, data di verifica e indice categorie
                                rigenerati dai dati reali; il resto della prosa resta invariato)
    e copia dei tre (json -> catalogo.json) in ogni cartella di SKILL_DIRS che esiste

Uso:
    python3 scripts/build_catalog.py
"""
import json, os, re, datetime

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ~/.agents/skills e' la cartella comune agli agent che adottano lo standard Agent Skills;
# Claude Code legge solo ~/.claude/skills. install-skill.sh ne fa un symlink, quindi di norma
# le due voci sono la stessa cartella: si scrive una volta per percorso reale.
SKILL_DIRS = [os.path.expanduser(p) for p in ('~/.agents/skills/ai-tools-catalog',
                                              '~/.claude/skills/ai-tools-catalog')]
SKILL_SRC = os.path.join(ROOT, 'skill', 'SKILL.md')

# I nomi delle macro-categorie e la prosa generata dipendono da catalogo.lingua in config.json.
# I *dati* (descrizione/uso delle voci) restano nella lingua in cui sono stati scritti: qui si
# traduce solo l'impalcatura. Per aggiungere una lingua basta una nuova voce in LOCALI.
LOCALI = {
 'it': {
  'macro': {
   'A': 'Coding Agent, Claude Code & sviluppo AI-assistito',
   'B': 'Framework Agenti AI & assistenti personali',
   'C': 'LLM, modelli & inferenza locale',
   'D': 'RAG, memoria agenti & knowledge base',
   'E': 'OCR & parsing documenti',
   'F': 'Generazione media (video, immagini, 3D, voce)',
   'G': 'Sicurezza & supply-chain',
   'H': 'Dev tools, produttività & librerie',
   'I': 'Finanza & trading AI',
   'J': 'Ricerca AI, world models & dati vettoriali',
   'Z': 'Contenuti personali / non-dev',
  },
  'stato': {'archiviato': 'archiviato', 'nd': 'n/d', 'molto_attivo': 'molto attivo',
            'attivo': 'attivo', 'rallentato': 'rallentato', 'fermo': 'fermo',
            'sito': 'sito web'},
  'intro':   '> Catalogo unificato di **repository GitHub** e **siti/servizi web** raccolti dai',
  'conteggi': '> **{r} repository** + **{s} siti web**, organizzati per categoria operativa.',
  'verifica': '> Stato attività verificato il **{d}**. ',
  'legenda': 'Legenda: 🟢 attivo (push ≤12 mesi) · 🟡 rallentato · 🔴 fermo · ⚫ archiviato · 🌐 sito web.',
  'indice':  '## Indice',
  'header':  '| Progetto | Cosa fa | Quando usarlo | Stato |',
  'cella_sito': '🌐 sito',
  'z_nota': 'voci non rilevanti per i progetti (salute, ricette, social) — ignorabili.',
 },
 'en': {
  'macro': {
   'A': 'Coding agents, Claude Code & AI-assisted development',
   'B': 'AI agent frameworks & personal assistants',
   'C': 'LLMs, models & local inference',
   'D': 'RAG, agent memory & knowledge bases',
   'E': 'OCR & document parsing',
   'F': 'Media generation (video, images, 3D, voice)',
   'G': 'Security & supply chain',
   'H': 'Dev tools, productivity & libraries',
   'I': 'AI finance & trading',
   'J': 'AI research, world models & vector data',
   'Z': 'Personal / non-dev content',
  },
  'stato': {'archiviato': 'archived', 'nd': 'n/a', 'molto_attivo': 'very active',
            'attivo': 'active', 'rallentato': 'slowing down', 'fermo': 'stalled',
            'sito': 'website'},
  'intro':   '> A unified catalog of **GitHub repositories** and **websites/services** collected from',
  'conteggi': '> **{r} repositories** + **{s} websites**, grouped by practical category.',
  'verifica': '> Activity status checked on **{d}**. ',
  'legenda': 'Legend: 🟢 active (pushed ≤12 months ago) · 🟡 slowing down · 🔴 stalled · ⚫ archived · 🌐 website.',
  'indice':  '## Index',
  'header':  '| Project | What it does | When to use it | Status |',
  'cella_sito': '🌐 site',
  'z_nota': 'entries not relevant to dev work (health, recipes, social) — safe to ignore.',
 },
}
ORDER = list("ABCDEFGHIJ")

# La macro Z marca contenuti personali (salute, social, gaming, codici): non deve mai
# finire negli output pubblicati. Le voci Z vivono in siti-personali.json,
# che e' gitignorato; questo filtro e' la seconda linea di difesa se una sfugge.
PRIVATA = 'Z'

def today():
    return datetime.date.today()

def data_verifica(meta):
    """La data da dichiarare come «verificati il»: quella del recupero piu' vecchio in
    gh-meta.json, cioe' il giorno a cui *tutte* le voci sono state controllate davvero.
    Non today(): un rebuild senza --refresh dichiarava verificati oggi dei metadati vecchi
    di giorni (accaduto il 2026-09-26, 232 voci su 235 erano del 19/09)."""
    date = sorted((m.get('fetched') or '')[:10] for m in meta.values() if m.get('fetched'))
    return date[0] if date else today().isoformat()

def stato(m, S):
    if not m or m.get('archived'):
        return ('⚫', S['archiviato'])
    p = (m.get('pushed') or '')[:10]
    if not p:
        return ('⚪', S['nd'])
    try:
        dt = datetime.date.fromisoformat(p)
    except Exception:
        return ('⚪', S['nd'])
    mo = (today() - dt).days / 30
    if mo <= 3:  return ('🟢', S['molto_attivo'])
    if mo <= 12: return ('🟢', S['attivo'])
    if mo <= 24: return ('🟡', S['rallentato'])
    return ('🔴', S['fermo'])

def kfmt(n, nd='n/d'):
    if n is None: return nd
    return (f"{n/1000:.1f}k".replace('.0k', 'k')) if n >= 1000 else str(n)

def load(name):
    return json.load(open(os.path.join(ROOT, name), encoding='utf-8'))

DEFAULT_CFG = {'titolo': 'Catalogo strumenti AI & Dev',
               'fonte': 'reel e link salvati in chat',
               'lingua': 'it'}

def config():
    """config.json e' gitignorato (contiene il nome della chat personale): se manca,
    o se manca la sezione 'catalogo', si usano i default neutri."""
    try:
        cfg = load('config.json').get('catalogo', {})
    except FileNotFoundError:
        cfg = {}
    out = {k: cfg.get(k) or v for k, v in DEFAULT_CFG.items()}
    if out['lingua'] not in LOCALI:
        print(f"  ⚠️ lingua '{out['lingua']}' non supportata (disponibili: "
              f"{', '.join(LOCALI)}): uso 'it'")
        out['lingua'] = 'it'
    return out

def indice_categorie(unified, L):
    """Righe dell'indice rapido di SKILL.md: una per macro-categoria non vuota."""
    MACRO, out = L['macro'], []
    for c in ORDER:
        items = [u for u in unified if u['macro'] == c]
        if not items: continue
        if c == 'Z':
            out.append(f"- **{c} · {MACRO[c]}** ({len(items)}): {L['z_nota']}")
            continue
        # stesso ordine delle tabelle nel markdown: repo per stelle desc, poi siti
        repos_c = sorted([u for u in items if u['tipo'] == 'repo'], key=lambda x: -(x['stelle'] or 0))
        sites_c = [u for u in items if u['tipo'] == 'sito']
        nomi = ', '.join(u['nome'] for u in repos_c + sites_c)
        out.append(f"- **{c} · {MACRO[c]}** ({len(items)}): {nomi}")
    return out

def sync_skill_md(unified, n_repo, n_sito, L, verificato):
    """Riallinea le parti dinamiche di skill/SKILL.md (conteggi nella description, data di
    verifica, indice categorie). E' la `description` a decidere quando l'agente invoca la skill:
    se resta indietro il catalogo risulta sottodimensionato. Le sostituzioni che non trovano
    esattamente un match vengono segnalate invece di fallire in silenzio."""
    if not os.path.isfile(SKILL_SRC):
        return None, [f"⚠️ {SKILL_SRC} non trovato: SKILL.md non aggiornato"]

    txt, warn = open(SKILL_SRC, encoding='utf-8').read(), []
    if L is not LOCALI['it']:
        warn.append("ℹ️ skill/SKILL.md: solo conteggi, data e indice sono rigenerati; "
                    "la prosa del file resta nella lingua in cui l'hai scritta")

    def sub(pattern, repl, cosa, flags=0):
        nonlocal txt
        txt, n = re.subn(pattern, lambda m: repl(m), txt, flags=flags)
        if n != 1:
            warn.append(f"⚠️ SKILL.md: {cosa} non aggiornato ({n} match, atteso 1) — "
                        "il pattern non corrisponde più, correggi build_catalog.py o SKILL.md")

    sub(r'Catalogo curato di \d+ repository GitHub e \d+ siti/servizi web',
        lambda m: f'Catalogo curato di {n_repo} repository GitHub e {n_sito} siti/servizi web',
        'conteggi nella description')
    sub(r'verificati il \*\*\d{4}-\d{2}-\d{2}\*\*',
        lambda m: f'verificati il **{verificato}**', 'data di verifica')
    blocco = '\n'.join(indice_categorie(unified, L))
    sub(r'^(## Categorie e contenuto \(indice rapido\)\n).*?(?=^## )',
        lambda m: m.group(1) + blocco + '\n\n', 'indice categorie', flags=re.M | re.S)

    # Limiti dello standard Agent Skills (agentskills.io/specification): oltre questi alcuni
    # agent scartano la skill, e lo fanno senza dirlo.
    fm = re.match(r'---\n(.*?)\n---\n', txt, re.S)
    nome = re.search(r'^name:\s*(\S+)', fm.group(1), re.M) if fm else None
    desc = re.search(r'^description:\s*>-\n((?:  .*\n?)+)', fm.group(1) + '\n', re.M) if fm else None
    if not nome or not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', nome.group(1)) or len(nome.group(1)) > 64:
        warn.append("⚠️ SKILL.md: `name` assente o non conforme allo standard Agent Skills")
    if not desc:
        warn.append("⚠️ SKILL.md: `description` non trovata (atteso un blocco `>-`)")
    elif len(' '.join(desc.group(1).split())) > 1024:
        warn.append(f"⚠️ SKILL.md: `description` di {len(' '.join(desc.group(1).split()))} "
                    "caratteri, lo standard Agent Skills ne ammette 1024")

    open(SKILL_SRC, 'w', encoding='utf-8').write(txt)
    return txt, warn

def sync_readme_badges(n_repo, n_sito, verificato):
    """Riallinea nel README i badge del numero di voci e della data di verifica: sono gli unici
    badge che invecchiano. Come per SKILL.md, un pattern che non trova esattamente un match
    viene segnalato invece di passare in silenzio."""
    path = os.path.join(ROOT, 'README.md')
    if not os.path.isfile(path):
        return []
    txt, warn = open(path, encoding='utf-8').read(), []
    for pattern, repl, cosa in (
        (r'badge/catalog-\d+%20repos%20%2B%20\d+%20sites-',
         f'badge/catalog-{n_repo}%20repos%20%2B%20{n_sito}%20sites-', 'badge conteggi'),
        (r'badge/activity%20checked-\d{4}--\d{2}--\d{2}-',
         f"badge/activity%20checked-{verificato.replace('-', '--')}-", 'badge data di verifica')):
        txt, n = re.subn(pattern, repl, txt)
        if n != 1:
            warn.append(f"⚠️ README.md: {cosa} non aggiornato ({n} match, atteso 1)")
    open(path, 'w', encoding='utf-8').write(txt)
    return warn

def main():
    cfg   = config()
    L     = LOCALI[cfg['lingua']]
    MACRO = L['macro']
    S     = L['stato']
    repos = load('github-repos.json')
    siti  = load('siti-web.json')
    meta  = load('gh-meta.json')

    unified = []
    for r in repos:
        m = meta.get(str(r['id']), {})
        em, lab = stato(m, S)
        unified.append({
            'tipo': 'repo', 'macro': r.get('macro', 'H'), 'macro_nome': MACRO.get(r.get('macro', 'H')),
            'nome': r['progetto'], 'cosa_fa': r['descrizione'], 'quando_usarlo': r.get('uso', ''),
            'url': r['url'], 'stelle': m.get('stars'), 'ultimo_push': (m.get('pushed') or '')[:10],
            'attivita': lab, 'attivita_emoji': em, 'licenza': r.get('licenza') or m.get('license'),
            'linguaggio': m.get('lang'), 'fonte': r.get('fonte', '')})
    for s in siti:
        c = s.get('macro', 'Z')
        unified.append({
            'tipo': 'sito', 'macro': c, 'macro_nome': MACRO.get(c),
            'nome': s['sito'], 'cosa_fa': s['descrizione'], 'quando_usarlo': s.get('uso', ''),
            'url': s['url'], 'stelle': None, 'ultimo_push': None, 'attivita': S['sito'],
            'attivita_emoji': '🌐', 'licenza': None, 'linguaggio': None, 'fonte': s.get('fonte', '')})

    scartate = [u for u in unified if u['macro'] == PRIVATA]
    if scartate:
        print(f"  privacy: {len(scartate)} voci macro {PRIVATA} escluse dagli output "
              f"({', '.join(u['nome'] for u in scartate)})")
        unified = [u for u in unified if u['macro'] != PRIVATA]

    json.dump(unified, open(os.path.join(ROOT, 'catalogo-unificato.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # --- Markdown ---
    n_repo = sum(1 for u in unified if u['tipo'] == 'repo')
    n_sito = sum(1 for u in unified if u['tipo'] == 'sito')
    OUT = []
    OUT.append(f"# 📚 {cfg['titolo']}")
    OUT.append('')
    OUT.append(L['intro'])
    OUT.append(f"> {cfg['fonte']}.")
    OUT.append(L['conteggi'].format(r=n_repo, s=n_sito))
    OUT.append(L['verifica'].format(d=data_verifica(meta)) + L['legenda'])
    OUT.append('')
    OUT.append(L['indice'])
    for c in ORDER:
        n = sum(1 for u in unified if u['macro'] == c)
        if n: OUT.append(f"- **{MACRO[c]}** ({n})")
    OUT.append('')
    for c in ORDER:
        items = [u for u in unified if u['macro'] == c]
        if not items: continue
        repos_c = sorted([u for u in items if u['tipo'] == 'repo'], key=lambda x: -(x['stelle'] or 0))
        sites_c = [u for u in items if u['tipo'] == 'sito']
        OUT.append(f"## {MACRO[c]}")
        OUT.append('')
        OUT.append(L['header'])
        OUT.append('|---|---|---|---|')
        for u in repos_c + sites_c:
            nome = f"[{u['nome']}]({u['url']})"
            cosa = (u['cosa_fa'] or '').replace('|', '/')
            quando = (u['quando_usarlo'] or '').replace('|', '/')
            if u['tipo'] == 'sito':
                stato_cell = L['cella_sito']
            else:
                lic = f" · {u['licenza']}" if u.get('licenza') and u['licenza'] != 'NOASSERTION' else ''
                stato_cell = (f"{u['attivita_emoji']} ⭐{kfmt(u['stelle'], S['nd'])} · "
                              f"{u['ultimo_push'] or S['nd']}{lic}")
            OUT.append(f"| {nome} | {cosa} | {quando} | {stato_cell} |")
        OUT.append('')
    md = '\n'.join(OUT) + '\n'
    open(os.path.join(ROOT, 'CATALOGO-AI-TOOLS.md'), 'w', encoding='utf-8').write(md)

    # --- SKILL.md: riallinea conteggi, data e indice ---
    skill_md, warn = sync_skill_md(unified, n_repo, n_sito, L, data_verifica(meta))

    # --- README: i due badge dinamici (conteggi e data di verifica) ---
    warn += sync_readme_badges(n_repo, n_sito, data_verifica(meta))

    # --- copia nella skill globale ---
    aggiornate, visti = [], set()
    for d in SKILL_DIRS:
        if not os.path.isdir(d) or os.path.realpath(d) in visti:
            continue
        visti.add(os.path.realpath(d))
        open(os.path.join(d, 'CATALOGO-AI-TOOLS.md'), 'w', encoding='utf-8').write(md)
        json.dump(unified, open(os.path.join(d, 'catalogo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        if skill_md is not None:
            open(os.path.join(d, 'SKILL.md'), 'w', encoding='utf-8').write(skill_md)
        aggiornate.append(d)
    if aggiornate:
        skill_msg = f"skill aggiornata: {', '.join(aggiornate)}"
    else:
        skill_msg = (f"⚠️ skill non trovata in {' né in '.join(SKILL_DIRS)} "
                     "(catalogo generato solo nel progetto: esegui install-skill.sh)")

    by_cat = {c: sum(1 for u in unified if u['macro'] == c) for c in ORDER}
    print(f"Catalogo generato: {len(unified)} voci ({n_repo} repo + {n_sito} siti)")
    print("Per categoria:", {c: n for c, n in by_cat.items() if n})
    print(skill_msg)
    for w in warn:
        print(w)

if __name__ == '__main__':
    main()

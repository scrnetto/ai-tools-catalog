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
    gh-meta.json               -> metadati attività per owner/nome (da fetch_gh_meta.py + scraping)
    *.local.json               -> voci e metadati dell'utente, uniti ai precedenti (catalogo_dati.py)

Output del catalogo pubblicato, solo se config.json ha "catalogo": {"manutentore": true}, e solo
dai file tracciati (le voci locali non ci finiscono mai):
    catalogo-unificato.json, CATALOGO-AI-TOOLS.md, catalog-version.json (impronta dei dati),
    skill/SKILL.md (conteggi, data di verifica e indice categorie rigenerati; il resto invariato),
    i due badge dinamici del README.
    docs/index.html e docs/<lingua>/index.html (la pagina web consultabile, servita da GitHub
    Pages, una per lingua: le voci tradotte vengono da traduzioni/<lingua>.json).
Output per chiunque, dall'unione pubblicati + locali, in ogni cartella di SKILL_DIRS che esiste:
    SKILL.md, CATALOGO-AI-TOOLS.md, catalogo.json, catalogo.html (la stessa pagina web, con le
    voci locali segnalate), check_update.py, installazione.json. Tutti nella lingua di
    catalogo.lingua, con le traduzioni dove ci sono e l'italiano dove mancano.
Chi non e' il manutentore non modifica file tracciati: cosi' `git pull` non va in conflitto.

Uso:
    python3 scripts/build_catalog.py
"""
import json, os, re, datetime, hashlib, shutil
import catalogo_dati as cd
import traduzioni as tr
from lingue import LOCALI

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ~/.agents/skills e' la cartella comune agli agent che adottano lo standard Agent Skills;
# Claude Code legge solo ~/.claude/skills. install-skill.sh ne fa un symlink, quindi di norma
# le due voci sono la stessa cartella: si scrive una volta per percorso reale.
SKILL_DIRS = [os.path.expanduser(p) for p in ('~/.agents/skills/ai-tools-catalog',
                                              '~/.claude/skills/ai-tools-catalog')]
SKILL_SRC = os.path.join(ROOT, 'skill', 'SKILL.md')
CHECK_SRC = os.path.join(ROOT, 'scripts', 'check_update.py')
PAGINA_SRC = os.path.join(ROOT, 'scripts', 'pagina-catalogo.html')
# l'italiano, lingua in cui il catalogo e' scritto, sta nella radice del sito; le altre sotto
LINGUE_PAGINE = ('it',) + tr.LINGUE
def pagina_pub(lingua):
    return os.path.join('docs', 'index.html') if lingua == 'it' else os.path.join('docs', lingua, 'index.html')
# confrontato da check_update.py con quello pubblicato: lo scrive solo il manutentore
VERSIONE = 'catalog-version.json'

# I nomi delle macro-categorie e la prosa generata dipendono da catalogo.lingua in config.json
# (testi in lingue.py). I *dati* (descrizione/uso delle voci) si scrivono in italiano; le loro
# traduzioni stanno in traduzioni/<lingua>.json e le gestisce traduzioni.py.
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

def stato(m):
    """(emoji, codice): il codice non dipende dalla lingua, l'etichetta e' L['stato'][codice]."""
    if not m or m.get('archived'):
        return ('⚫', 'archiviato')
    p = (m.get('pushed') or '')[:10]
    if not p:
        return ('⚪', 'nd')
    try:
        dt = datetime.date.fromisoformat(p)
    except Exception:
        return ('⚪', 'nd')
    mo = (today() - dt).days / 30
    if mo <= 3:  return ('🟢', 'molto_attivo')
    if mo <= 12: return ('🟢', 'attivo')
    if mo <= 24: return ('🟡', 'rallentato')
    return ('🔴', 'fermo')

def classe_licenza(tipo, lic):
    """Che cosa permette la licenza, per il filtro della pagina web. Si calcola sul testo
    originale, prima della traduzione: le licenze verificate a mano sono frasi in italiano."""
    if tipo == 'sito':
        return 'sito'
    l = (lic or '').lower()
    if not l or l == 'noassertion':
        return 'ignota'
    if re.search(r'nessuna licenza|diritti riservati|proprietaria', l):
        return 'chiusa'
    if re.search(r'noncommercial|non commerciale|nc |-nc|research|busl|mvt license', l):
        return 'limitata'
    if 'gpl' in l:
        return 'copyleft'
    return 'libera'

def kfmt(n, nd='n/d'):
    if n is None: return nd
    return (f"{n/1000:.1f}k".replace('.0k', 'k')) if n >= 1000 else str(n)

def load(name):
    return json.load(open(os.path.join(ROOT, name), encoding='utf-8'))


def config():
    """config.json e' gitignorato (contiene il nome della chat personale): se manca,
    o se manca la sezione 'catalogo', si usano i default neutri."""
    try:
        cfg = load('config.json').get('catalogo', {})
    except FileNotFoundError:
        cfg = {}
    out = {'lingua': cfg.get('lingua') or 'it'}
    if out['lingua'] not in LOCALI:
        print(f"  ⚠️ lingua '{out['lingua']}' non supportata (disponibili: "
              f"{', '.join(LOCALI)}): uso 'it'")
        out['lingua'] = 'it'
    # titolo e fonte hanno un default per lingua; se l'utente li ha scritti, restano i suoi
    for k in ('titolo', 'fonte'):
        out[k] = cfg.get(k) or LOCALI[out['lingua']][k]
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

def sync_skill_md(unified, n_repo, n_sito, L, verificato, scrivi=True):
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

    if scrivi:
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

def traduci(u, chiave, trad):
    """Sostituisce cosa_fa/quando_usarlo/licenza con la traduzione, se ce n'e' una valida.
    `trad` e' None per l'italiano. Le voci locali dell'utente restano come le ha scritte."""
    if trad is None or u.get('origine'):
        return
    t = trad.get(chiave)
    if not t:
        u['_originale'] = True
        return
    for c in tr.CAMPI:
        if t.get(c):
            u[c] = t[c]

def catalogo(repos, siti, meta, cfg, L, trad=None):
    """Voci unificate e markdown del catalogo, dai dati passati (pubblicati o uniti).
    `trad`: le traduzioni valide per la lingua di L ({chiave: testi}), None per l'italiano.
    Le chiavi che iniziano per `_` servono alla pagina web e non finiscono nei file JSON."""
    MACRO, S = L['macro'], L['stato']
    unified = []
    for r in repos:
        k = cd.chiave_repo(r['url'])
        m = meta.get(k) or {}
        em, cod = stato(m)
        lic = r.get('licenza') or m.get('license')
        unified.append({
            'tipo': 'repo', 'macro': r.get('macro', 'H'), 'macro_nome': MACRO.get(r.get('macro', 'H')),
            'nome': r['progetto'], 'cosa_fa': r['descrizione'], 'quando_usarlo': r.get('uso', ''),
            'url': r['url'], 'stelle': m.get('stars'), 'ultimo_push': (m.get('pushed') or '')[:10],
            'attivita': S[cod], 'attivita_emoji': em, 'licenza': lic,
            'linguaggio': m.get('lang'), 'fonte': r.get('fonte', ''),
            '_stato': cod, '_lic': classe_licenza('repo', lic)})
        if r.get('origine'): unified[-1]['origine'] = r['origine']
        traduci(unified[-1], k, trad)
    for s in siti:
        c = s.get('macro', 'Z')
        unified.append({
            'tipo': 'sito', 'macro': c, 'macro_nome': MACRO.get(c),
            'nome': s['sito'], 'cosa_fa': s['descrizione'], 'quando_usarlo': s.get('uso', ''),
            'url': s['url'], 'stelle': None, 'ultimo_push': None, 'attivita': S['sito'],
            'attivita_emoji': '🌐', 'licenza': None, 'linguaggio': None, 'fonte': s.get('fonte', ''),
            '_stato': 'sito', '_lic': 'sito'})
        if s.get('origine'): unified[-1]['origine'] = s['origine']
        traduci(unified[-1], cd.chiave_sito(s['url']), trad)

    scartate = [u for u in unified if u['macro'] == PRIVATA]
    if scartate:
        print(f"  privacy: {len(scartate)} voci macro {PRIVATA} escluse dagli output "
              f"({', '.join(u['nome'] for u in scartate)})")
        unified = [u for u in unified if u['macro'] != PRIVATA]

    n_repo = sum(1 for u in unified if u['tipo'] == 'repo')
    n_sito = sum(1 for u in unified if u['tipo'] == 'sito')
    verificato = data_verifica(meta)
    OUT = []
    OUT.append(f"# 📚 {cfg['titolo']}")
    OUT.append('')
    OUT.append(L['intro'])
    OUT.append(f"> {cfg['fonte']}.")
    OUT.append(L['conteggi'].format(r=n_repo, s=n_sito))
    OUT.append(L['verifica'].format(d=verificato) + L['legenda'])
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
    return unified, '\n'.join(OUT) + '\n', n_repo, n_sito, verificato

# i campi che la pagina web usa: gli altri (fonte, emoji) la appesantirebbero e basta.
# stato/lic/originale sono codici calcolati qui, che non dipendono dalla lingua della pagina.
CAMPI_PAGINA = ('tipo', 'macro', 'nome', 'cosa_fa', 'quando_usarlo', 'url', 'stelle',
                'ultimo_push', 'licenza', 'linguaggio', 'origine')

def senza_interni(unified):
    """Le voci come finiscono nei file JSON: senza le chiavi `_` che servono solo alla pagina."""
    return [{k: v for k, v in u.items() if not k.startswith('_')} for u in unified]

def pagina(unified, n_repo, n_sito, verificato, titolo, lingua, piede, lingue=None):
    """La pagina web del catalogo: un solo file HTML con i dati dentro, che non fa richieste di
    rete. I testi vengono da reel e pagine di terzi, quindi nel JSON incorporato `<`, `>` e `&`
    diventano escape \\u: una descrizione con `</script>` non puo' chiudere il blocco dei dati.
    Lo script della pagina poi li inserisce solo come testo.
    `lingue`: [(codice, nome, href)] per il selettore della lingua; None se la pagina e' una sola."""
    L = LOCALI[lingua]
    macro = [c for c in ORDER if any(u['macro'] == c for u in unified)]
    stati = [c for c in ('molto_attivo', 'attivo', 'rallentato', 'fermo', 'archiviato', 'nd', 'sito')
             if any(u['_stato'] == c for u in unified)]
    voci = []
    for u in unified:
        v = {k: u[k] for k in CAMPI_PAGINA if u.get(k) not in (None, '')}
        v.update({'stato': u['_stato'], 'lic': u['_lic']})
        if u.get('_originale'):
            v['originale'] = True
        voci.append(v)
    dati = {'lingua': lingua, 'titolo': titolo, 'repo': n_repo, 'siti': n_sito,
            'verificato': verificato, 'macro': macro,
            'macro_breve': {c: L['macro_breve'][c] for c in macro},
            'stati': [[c, L['stato'][c]] for c in stati], 'ui': L['ui'], 'piede': piede,
            'lingue': lingue or [], 'voci': voci}
    js = json.dumps(dati, ensure_ascii=False, separators=(',', ':'))
    js = js.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    tpl = open(PAGINA_SRC, encoding='utf-8').read()
    esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    return (tpl.replace('__LINGUA__', esc(lingua)).replace('__TITOLO__', esc(titolo))
               .replace('__DATI__', js))

def selettore(lingua):
    """[(codice, nome, href)] dalla pagina in `lingua` a tutte le altre, con link relativi: il
    sito funziona uguale su GitHub Pages e aperto dal disco."""
    su = '' if lingua == 'it' else '../'
    return [(l, LOCALI[l]['nome'], su + ('index.html' if l == 'it' else f'{l}/index.html'))
            for l in LINGUE_PAGINE]

def impronta(repos, siti, meta, traduzioni=None):
    """Impronta dei dati pubblicati: cambia se e solo se cambia il catalogo pubblicato, e non
    dipende dalla data del build (i campi calcolati come 'attivita' restano fuori). Comprende le
    traduzioni: chi usa la skill in un'altra lingua deve sapere quando ne arrivano di nuove."""
    dati = json.dumps([repos, siti, meta, traduzioni or {}], ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(dati.encode('utf-8')).hexdigest()[:16]

def traduzioni_valide(lingua, src, warn):
    """Le traduzioni utilizzabili per `lingua` (None per l'italiano), con un avviso se ne
    mancano o ne sono scadute: la pagina mostra l'italiano al loro posto, e va detto."""
    if lingua == 'it':
        return None
    trad = tr.carica(ROOT, lingua)
    buone = tr.valide(trad, src)
    if len(buone) < len(src):
        scadute = sum(1 for k in trad if k in src and k not in buone)
        warn.append(f"⚠️ traduzioni {lingua}: {len(src) - len(buone)} voci su {len(src)} restano in "
                    f"italiano ({scadute} scadute) — python3 scripts/traduzioni.py mancanti {lingua}")
    return buone

def main():
    cfg   = config()
    L     = LOCALI[cfg['lingua']]
    warn  = []
    pub   = cd.dati_pubblicati(ROOT)
    src   = tr.sorgenti(pub[0], pub[1])
    versione = {'impronta': impronta(*pub, {l: tr.carica(ROOT, l) for l in tr.LINGUE})}

    # --- catalogo pubblicato: lo riscrive solo il manutentore ---
    # Chi ha clonato il repository non tocca i file tracciati: cosi' `git pull` non va mai in
    # conflitto con il suo catalogo. Le sue voci stanno nei *.local.json (catalogo_dati.py).
    if cd.manutentore(ROOT):
        u_pub, md_pub, nr, ns, ver = catalogo(*pub, cfg, L, traduzioni_valide(cfg['lingua'], src, []))
        json.dump(senza_interni(u_pub), open(os.path.join(ROOT, 'catalogo-unificato.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        open(os.path.join(ROOT, 'CATALOGO-AI-TOOLS.md'), 'w', encoding='utf-8').write(md_pub)
        # una pagina per lingua, tutte dagli stessi dati pubblicati
        for lingua in LINGUE_PAGINE:
            Lp = LOCALI[lingua]
            u_l, _, _, _, _ = catalogo(*pub, cfg, Lp, traduzioni_valide(lingua, src, warn))
            dest = os.path.join(ROOT, pagina_pub(lingua))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            open(dest, 'w', encoding='utf-8').write(
                pagina(u_l, nr, ns, ver, Lp['titolo'], lingua, Lp['piede_pub'], selettore(lingua)))
        _, w = sync_skill_md(u_pub, nr, ns, L, ver)
        warn += w + sync_readme_badges(nr, ns, ver)
        versione.update({'repo': nr, 'siti': ns, 'verificato': ver})
        cd.salva(ROOT, VERSIONE, versione)

    # --- catalogo installato nella skill: pubblicati + locali, nella lingua dell'utente ---
    repos, siti, meta, res = cd.dati_uniti(ROOT)
    trad = traduzioni_valide(cfg['lingua'], src, [] if cd.manutentore(ROOT) else warn)
    unified, md, n_repo, n_sito, verificato = catalogo(repos, siti, meta, cfg, L, trad)
    skill_md, w = sync_skill_md(unified, n_repo, n_sito, L, verificato, scrivi=False)
    warn += w
    installazione = {'repository': ROOT, 'impronta': versione['impronta'],
                     'voci_locali': res, 'generato': today().isoformat()}

    aggiornate, visti = [], set()
    for d in SKILL_DIRS:
        if not os.path.isdir(d) or os.path.realpath(d) in visti:
            continue
        visti.add(os.path.realpath(d))
        open(os.path.join(d, 'CATALOGO-AI-TOOLS.md'), 'w', encoding='utf-8').write(md)
        json.dump(senza_interni(unified), open(os.path.join(d, 'catalogo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        open(os.path.join(d, 'catalogo.html'), 'w', encoding='utf-8').write(
            pagina(unified, n_repo, n_sito, verificato, cfg['titolo'], cfg['lingua'], L['piede_skill']))
        if skill_md is not None:
            open(os.path.join(d, 'SKILL.md'), 'w', encoding='utf-8').write(skill_md)
        shutil.copyfile(CHECK_SRC, os.path.join(d, 'check_update.py'))
        cd.salva(d, 'installazione.json', installazione)
        aggiornate.append(d)
    if aggiornate:
        skill_msg = f"skill aggiornata: {', '.join(aggiornate)}"
    else:
        skill_msg = (f"⚠️ skill non trovata in {' né in '.join(SKILL_DIRS)} "
                     "(catalogo generato solo nel progetto: esegui install-skill.sh)")

    by_cat = {c: sum(1 for u in unified if u['macro'] == c) for c in ORDER}
    print(f"Catalogo generato: {len(unified)} voci ({n_repo} repo + {n_sito} siti)")
    if any(res.values()):
        print(f"  voci locali: {res['locali_nuove']} aggiunte, {res['completate']} che completano "
              f"una voce pubblicata, {res['nascoste']} voci pubblicate nascoste")
    print("Per categoria:", {c: n for c, n in by_cat.items() if n})
    print(skill_msg)
    for w in warn:
        print(w)

if __name__ == '__main__':
    main()

"""
Dati del catalogo: file pubblicati dal repository e file locali dell'utente, e come si uniscono.

Chi clona il repository e aggiunge voci sue non deve scriverle nei file tracciati: al primo
`git pull` avrebbe un conflitto, o perderebbe le proprie voci. Per questo ogni file di dati ha un
gemello `.local.json`, ignorato da git, e il catalogo installato nella skill e' l'unione dei due.

    github-repos.json    + github-repos.local.json     voci repo
    siti-web.json        + siti-web.local.json         voci sito
    gh-meta.json         + gh-meta.local.json          metadati GitHub, per chiave owner/nome
    instagram-profili.json + instagram-profili.local.json   stato del monitoraggio (solo l'agente)

Regole dell'unione (`unisci`):
  - la chiave e' l'indirizzo, non l'`id` numerico: `owner/nome` per i repo, l'URL normalizzato
    per i siti. Gli id dei due file possono scontrarsi, gli indirizzi no;
  - una voce locale con la stessa chiave di una pubblicata la completa campo per campo, e sui
    campi in comune vince la locale (l'utente puo' aver riscritto la descrizione);
  - una voce locale con `"nascondi": true` toglie dal catalogo la voce pubblicata con la stessa
    chiave;
  - per i metadati vince il recupero piu' recente (`fetched`), da qualunque dei due file venga.

Le voci che vengono dai file locali portano `origine`: 'locale' se nuove, 'modificata' se
completano una pubblicata. La pagina web installata nella skill le segnala come tali.

Il manutentore del catalogo (`"catalogo": {"manutentore": true}` in config.json) scrive invece
nei file tracciati: sono loro il catalogo pubblicato.
"""
import json, os, re

FILE = {'repos': 'github-repos.json', 'siti': 'siti-web.json',
        'meta': 'gh-meta.json', 'profili': 'instagram-profili.json'}

def locale(nome):
    """github-repos.json -> github-repos.local.json"""
    return nome[:-len('.json')] + '.local.json'

def chiave_repo(url):
    """owner/nome in minuscolo, o None se l'URL non punta a un repo GitHub."""
    m = re.search(r'github\.com/([^/]+)/([^/?#]+)', url or '')
    if not m:
        return None
    nome = m.group(2)
    if nome.endswith('.git'):
        nome = nome[:-4]
    return f"{m.group(1)}/{nome}".lower()

def chiave_sito(url):
    """URL senza schema, www., slash finale e maiuscole nell'host: lo stesso sito scritto in
    due modi deve dare la stessa chiave."""
    u = re.sub(r'^https?://', '', (url or '').strip(), flags=re.I)
    host, _, resto = u.partition('/')
    host = host.lower()
    if host.startswith('www.'):
        host = host[4:]
    return (host + ('/' + resto if resto else '')).rstrip('/')

def carica(root, nome, default):
    path = os.path.join(root, nome)
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def salva(root, nome, dati):
    """Stesso formato dei file gia' tracciati (indent 2 per le liste, 1 per gh-meta.json), cosi'
    un salvataggio senza modifiche non produce un diff."""
    indent = 1 if nome.startswith('gh-meta') else 2
    with open(os.path.join(root, nome), 'w', encoding='utf-8') as f:
        f.write(json.dumps(dati, ensure_ascii=False, indent=indent) + '\n')

def manutentore(root):
    try:
        cfg = carica(root, 'config.json', {})
    except ValueError:
        return False
    return bool((cfg.get('catalogo') or {}).get('manutentore'))

def unisci(pubblicate, locali, chiave):
    """Ritorna (voci, resoconto). Ordine: le pubblicate nel loro ordine, poi le sole locali."""
    loc = {}
    for v in locali:
        k = chiave(v.get('url'))
        if k:
            loc[k] = v
    out, viste = [], set()
    res = {'locali_nuove': 0, 'completate': 0, 'nascoste': 0}
    for v in pubblicate:
        k = chiave(v.get('url'))
        viste.add(k)
        l = loc.get(k)
        if l is None:
            out.append(v)
        elif l.get('nascondi'):
            res['nascoste'] += 1
        else:
            # l'URL resta quello pubblicato: la chiave e' la stessa, la grafia puo' non esserlo
            out.append({**v, **l, 'url': v.get('url'), 'origine': 'modificata'})
            res['completate'] += 1
    for k, l in loc.items():
        if k not in viste and not l.get('nascondi'):
            out.append({**l, 'origine': 'locale'})
            res['locali_nuove'] += 1
    return out, res

def unisci_meta(pubblicati, locali):
    """Per ogni chiave vince il recupero piu' recente; a parita', il locale."""
    out = dict(pubblicati)
    for k, m in locali.items():
        p = out.get(k)
        if p is None or (m.get('fetched') or '') >= (p.get('fetched') or ''):
            out[k] = m
    return out

def dati_pubblicati(root):
    return (carica(root, FILE['repos'], []), carica(root, FILE['siti'], []),
            carica(root, FILE['meta'], {}))

def dati_uniti(root):
    """(repos, siti, meta, resoconto) dell'unione pubblicati + locali."""
    repos_p, siti_p, meta_p = dati_pubblicati(root)
    repos, r1 = unisci(repos_p, carica(root, locale(FILE['repos']), []), chiave_repo)
    siti, r2 = unisci(siti_p, carica(root, locale(FILE['siti']), []), chiave_sito)
    meta = unisci_meta(meta_p, carica(root, locale(FILE['meta']), {}))
    res = {k: r1[k] + r2[k] for k in r1}
    return repos, siti, meta, res

#!/usr/bin/env python3
"""
Traduzioni delle voci del catalogo pubblicato.

Le voci si scrivono in italiano, la lingua dei reel da cui vengono. Le traduzioni stanno in
traduzioni/<lingua>.json, una per voce, con la stessa chiave dell'unione con le voci locali
(`owner/nome` per i repo, l'URL normalizzato per i siti):

    {"owner/nome": {"cosa_fa": "...", "quando_usarlo": "...", "licenza": "...", "sorgente": "3f9a..."}}

`licenza` c'e' solo per le licenze verificate a mano, che sono una frase ("nessuna licenza (tutti i
diritti riservati)"); quelle che vengono da GitHub sono identificatori SPDX e non si traducono.
`sorgente` e' l'impronta del testo italiano da cui la traduzione e' stata fatta: se l'italiano
cambia, la traduzione risulta scaduta e il build mostra l'italiano finche' non la si rifa'. Una
traduzione vecchia non deve mai passare per buona.

Le voci locali dell'utente non si traducono: restano come le ha scritte.

Uso (per chi traduce, persona o agente):
    python3 scripts/traduzioni.py mancanti en > da-tradurre.json   # voci senza traduzione valida
    python3 scripts/traduzioni.py applica en tradotte.json          # le unisce a traduzioni/en.json
    python3 scripts/traduzioni.py stato                             # quante mancano, per lingua

Il file da tradurre e quello tradotto hanno la stessa forma: {chiave: {cosa_fa, quando_usarlo,
licenza?}}. `applica` calcola da se' l'impronta sul testo italiano attuale, quindi chi traduce
non la deve toccare.
"""
import hashlib, json, os, sys
import catalogo_dati as cd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA = 'traduzioni'
LINGUE = ('en', 'es', 'de', 'fr')
CAMPI = ('cosa_fa', 'quando_usarlo', 'licenza')

def sorgenti(repos, siti):
    """{chiave: testi italiani da tradurre} delle voci pubblicate."""
    out = {}
    for r in repos:
        k = cd.chiave_repo(r['url'])
        if k:
            t = {'cosa_fa': r['descrizione'], 'quando_usarlo': r.get('uso', '')}
            if r.get('licenza'):
                t['licenza'] = r['licenza']
            out[k] = t
    for s in siti:
        out[cd.chiave_sito(s['url'])] = {'cosa_fa': s['descrizione'], 'quando_usarlo': s.get('uso', '')}
    return out

def impronta(testi):
    dati = json.dumps([testi.get(c, '') for c in CAMPI], ensure_ascii=False)
    return hashlib.sha256(dati.encode('utf-8')).hexdigest()[:12]

def carica(root, lingua):
    return cd.carica(root, os.path.join(CARTELLA, f'{lingua}.json'), {})

def valide(trad, src):
    """Le traduzioni ancora buone: quelle la cui impronta corrisponde al testo italiano attuale."""
    return {k: t for k, t in trad.items() if k in src and t.get('sorgente') == impronta(src[k])}

def mancanti(trad, src):
    return {k: s for k, s in src.items() if k not in valide(trad, src)}

def applica(root, lingua, nuove, src):
    """Unisce `nuove` a traduzioni/<lingua>.json; ritorna le chiavi scartate con il motivo."""
    trad, scarti = carica(root, lingua), {}
    for k, t in nuove.items():
        if k not in src:
            scarti[k] = 'chiave sconosciuta'
            continue
        attesi = [c for c in CAMPI if src[k].get(c)]
        vuoti = [c for c in attesi if not (t.get(c) or '').strip()]
        if vuoti:
            scarti[k] = 'campi vuoti: ' + ', '.join(vuoti)
            continue
        trad[k] = {**{c: t[c].strip() for c in attesi}, 'sorgente': impronta(src[k])}
    os.makedirs(os.path.join(root, CARTELLA), exist_ok=True)
    with open(os.path.join(root, CARTELLA, f'{lingua}.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict(sorted(trad.items())), ensure_ascii=False, indent=2) + '\n')
    return scarti

def main(argv):
    repos, siti, _ = cd.dati_pubblicati(ROOT)
    src = sorgenti(repos, siti)
    if argv[:1] == ['stato']:
        for l in LINGUE:
            m = mancanti(carica(ROOT, l), src)
            print(f"{l}: {len(src) - len(m)}/{len(src)} tradotte, {len(m)} da fare")
        return 0
    if len(argv) >= 2 and argv[0] in ('mancanti', 'applica') and argv[1] in LINGUE:
        if argv[0] == 'mancanti':
            print(json.dumps(mancanti(carica(ROOT, argv[1]), src), ensure_ascii=False, indent=1))
            return 0
        if len(argv) == 3:
            with open(argv[2], encoding='utf-8') as f:
                scarti = applica(ROOT, argv[1], json.load(f), src)
            for k, motivo in scarti.items():
                print(f"  scartata {k}: {motivo}")
            print(f"{argv[1]}: {len(mancanti(carica(ROOT, argv[1]), src))} ancora da tradurre")
            return 1 if scarti else 0
    print(__doc__.split('Uso')[1].split('\n\n')[0], file=sys.stderr)
    return 2

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

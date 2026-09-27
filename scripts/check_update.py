#!/usr/bin/env python3
"""
C'e' una versione piu' recente del catalogo pubblicato? Lo dice, non aggiorna niente.

build_catalog.py copia questo script nella cartella della skill, accanto a `installazione.json`
(da quale repository e' stato installato il catalogo, e con quale impronta dei dati). Lo script
scarica solo `catalog-version.json` dall'indirizzo fisso qui sotto e confronta le impronte.

Aggiornare vuol dire scaricare ed eseguire codice nuovo: lo fa l'utente, con update-catalog.sh
nel repository. Un agente che legge questo output deve riferirlo, non eseguire l'aggiornamento.

Uso:
    python3 check_update.py           # al massimo un controllo al giorno
    python3 check_update.py --force   # controlla comunque

Esce sempre con 0: un controllo fallito (rete assente, risposta strana) non deve interrompere il
lavoro dell'agente, e viene riportato come tale.
"""
import datetime, json, os, re, sys, urllib.error, urllib.request

# Indirizzo fisso, versionato insieme allo script: mai preso da un parametro o da un file
# scaricato. Chi pubblica un fork lo cambia qui.
URL = 'https://raw.githubusercontent.com/scrnetto/ai-tools-catalog/main/catalog-version.json'
QUI = os.path.dirname(os.path.abspath(__file__))
TIMBRO = os.path.join(QUI, '.ultimo-controllo')
MAX_BYTE = 64 * 1024

class NessunRedirect(urllib.request.HTTPRedirectHandler):
    """Un redirect verso un altro host e' una destinazione non scelta da noi: si rifiuta."""
    def redirect_request(self, *a, **k):
        return None

def valida(dati):
    """Il contenuto scaricato e' input non fidato: si accettano solo i campi attesi, con il tipo
    atteso. Ritorna il dizionario pulito o None."""
    if not isinstance(dati, dict):
        return None
    imp = dati.get('impronta')
    if not isinstance(imp, str) or not re.fullmatch(r'[0-9a-f]{16}', imp):
        return None
    out = {'impronta': imp}
    for k in ('repo', 'siti'):
        if isinstance(dati.get(k), int) and 0 <= dati[k] < 10**6:
            out[k] = dati[k]
    v = dati.get('verificato')
    if isinstance(v, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', v):
        out['verificato'] = v
    return out

def confronta(installata, remota):
    """Messaggio per l'utente, dato quanto installato e quanto pubblicato (gia' validato)."""
    if remota['impronta'] == installata.get('impronta'):
        return "Catalogo aggiornato: nessuna novita' nel repository pubblicato."
    dettagli = []
    if 'repo' in remota:
        dettagli.append(f"{remota['repo']} repo e {remota.get('siti', '?')} siti")
    if 'verificato' in remota:
        dettagli.append(f"attivita' verificata il {remota['verificato']}")
    tra = f" ({', '.join(dettagli)})" if dettagli else ''
    repo = installata.get('repository') or '<cartella del repository ai-tools-catalog>'
    return (f"Novita': il catalogo pubblicato e' cambiato{tra}. Le voci aggiunte da te restano. "
            f"Per aggiornare, l'utente esegue: cd \"{repo}\" && ./update-catalog.sh")

def scarica():
    apri = urllib.request.build_opener(NessunRedirect)
    req = urllib.request.Request(URL, headers={'User-Agent': 'ai-tools-catalog-check'})
    with apri.open(req, timeout=5) as r:
        return json.loads(r.read(MAX_BYTE + 1)[:MAX_BYTE].decode('utf-8'))

def main():
    oggi = datetime.date.today().isoformat()
    if '--force' not in sys.argv[1:]:
        try:
            if open(TIMBRO, encoding='utf-8').read().strip() == oggi:
                print("Controllo aggiornamenti gia' fatto oggi.")
                return
        except OSError:
            pass
    try:
        installata = json.load(open(os.path.join(QUI, 'installazione.json'), encoding='utf-8'))
    except (OSError, ValueError):
        print("Impossibile controllare: installazione.json manca. Reinstallare la skill con "
              "install-skill.sh dal repository.")
        return
    try:
        remota = valida(scarica())
    except (urllib.error.URLError, OSError, ValueError) as e:
        print(f"Controllo aggiornamenti non riuscito ({type(e).__name__}): si riprova al prossimo uso.")
        return
    if remota is None:
        print("Controllo aggiornamenti non riuscito: risposta in un formato inatteso.")
        return
    try:
        open(TIMBRO, 'w', encoding='utf-8').write(oggi)
    except OSError:
        pass
    print(confronta(installata, remota))

if __name__ == '__main__':
    main()

"""
Il catalogo pubblicato si aggiorna senza toccare le voci dell'utente.

Il test costruisce due cloni git veri di un repository d'appoggio: il manutentore pubblica, un
utente aggiunge voci sue nei *.local.json, il manutentore pubblica di nuovo, l'utente aggiorna
con update-catalog.sh. Si controlla che:
  - il build dell'utente non modifichi mai un file tracciato (altrimenti git pull confligge);
  - dopo l'aggiornamento la skill contenga le voci nuove pubblicate E quelle dell'utente;
  - una voce locale completi quella pubblicata con lo stesso indirizzo, e `nascondi` la tolga;
  - check_update.py riconosca la novita' e scarti una risposta malformata;
  - la pagina web tenga i testi dei terzi come dati (una descrizione con `</script>` non esce dal
    blocco JSON) e segnali le voci locali solo nella copia della skill;
  - le traduzioni si applichino, e una traduzione scaduta (l'italiano e' cambiato dopo) lasci il
    posto all'italiano invece di passare per buona.

Esecuzione:  python3 -m unittest discover -s tests
"""
import json, os, re, shutil, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import catalogo_dati as cd
import check_update

def repo(n, macro='H'):
    return {'id': n, 'progetto': f'Progetto {n}', 'descrizione': f'Descrizione {n}',
            'url': f'https://github.com/owner{n}/progetto{n}', 'categoria': 'x', 'fonte': 'test',
            'macro': macro, 'uso': f'Uso {n}'}

def meta(n):
    return {'slug': f'owner{n}/progetto{n}', 'stars': n * 10, 'pushed': '2026-09-01',
            'archived': False, 'license': 'MIT', 'fetched': '2026-09-20'}

def git(cwd, *args):
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True,
                          text=True).stdout

class Aggiornamenti(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.origin = os.path.join(self.tmp, 'origin.git')
        self.man = os.path.join(self.tmp, 'manutentore')
        self.ute = os.path.join(self.tmp, 'utente')
        self.home_man = os.path.join(self.tmp, 'home-man')
        self.home_ute = os.path.join(self.tmp, 'home-ute')
        for h in (self.home_man, self.home_ute):
            os.makedirs(os.path.join(h, '.agents', 'skills', 'ai-tools-catalog'))
        self.env_git = {'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@t',
                        'GIT_COMMITTER_NAME': 't', 'GIT_COMMITTER_EMAIL': 't@t'}
        os.environ.update(self.env_git)

        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'main', self.origin], check=True)
        git(self.tmp, 'clone', '-q', self.origin, self.man)
        os.makedirs(os.path.join(self.man, 'scripts'))
        os.makedirs(os.path.join(self.man, 'skill'))
        for f in ('catalogo_dati.py', 'build_catalog.py', 'check_update.py', 'fetch_gh_meta.py',
                  'pagina-catalogo.html', 'lingue.py', 'traduzioni.py'):
            shutil.copy(os.path.join(ROOT, 'scripts', f), os.path.join(self.man, 'scripts', f))
        for f in ('update-catalog.sh', '.gitignore', 'README.md'):
            shutil.copy(os.path.join(ROOT, f), os.path.join(self.man, f))
        shutil.copy(os.path.join(ROOT, 'skill', 'SKILL.md'), os.path.join(self.man, 'skill'))
        cd.salva(self.man, 'config.json', {'catalogo': {'manutentore': True, 'lingua': 'it'}})
        cd.salva(self.man, 'github-repos.json', [repo(1), repo(2), repo(3)])
        cd.salva(self.man, 'siti-web.json', [])
        cd.salva(self.man, 'gh-meta.json', {f'owner{n}/progetto{n}': meta(n) for n in (1, 2, 3)})
        self.build(self.man, self.home_man)
        git(self.man, 'add', '-A')
        git(self.man, 'commit', '-q', '-m', 'catalogo v1')
        git(self.man, 'push', '-q', 'origin', 'main')

        git(self.tmp, 'clone', '-q', self.origin, self.ute)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def build(self, cwd, home):
        subprocess.run([sys.executable, 'scripts/build_catalog.py'], cwd=cwd, check=True,
                       capture_output=True, env={**os.environ, 'HOME': home})

    def skill(self, home):
        with open(os.path.join(home, '.agents', 'skills', 'ai-tools-catalog',
                               'catalogo.json'), encoding='utf-8') as f:
            return {u['url']: u for u in json.load(f)}

    def test_voci_locali_sopravvivono_all_aggiornamento(self):
        # l'utente: una voce nuova (senza id), una che corregge la 1, una che nasconde la 2
        cd.salva(self.ute, 'github-repos.local.json', [
            {'progetto': 'Mia', 'descrizione': 'voce mia', 'url': 'https://github.com/io/mia',
             'macro': 'A', 'uso': 'test'},
            {'url': 'https://github.com/Owner1/Progetto1/', 'descrizione': 'descrizione mia'},
            {'url': 'https://github.com/owner2/progetto2', 'nascondi': True},
        ])
        self.build(self.ute, self.home_ute)
        self.assertEqual(git(self.ute, 'status', '--porcelain', '--untracked-files=no'), '',
                         "il build dell'utente ha modificato file tracciati")

        # il manutentore pubblica una voce nuova
        with open(os.path.join(self.man, 'github-repos.json'), encoding='utf-8') as f:
            repos = json.load(f)
        cd.salva(self.man, 'github-repos.json', repos + [repo(4)])
        m = cd.carica(self.man, 'gh-meta.json', {})
        m['owner4/progetto4'] = meta(4)
        cd.salva(self.man, 'gh-meta.json', m)
        self.build(self.man, self.home_man)
        git(self.man, 'add', '-A')
        git(self.man, 'commit', '-q', '-m', 'catalogo v2')
        git(self.man, 'push', '-q', 'origin', 'main')

        # l'utente aggiorna
        r = subprocess.run(['bash', 'update-catalog.sh'], cwd=self.ute, capture_output=True,
                           text=True, env={**os.environ, 'HOME': self.home_ute})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(git(self.ute, 'status', '--porcelain', '--untracked-files=no'), '')

        voci = self.skill(self.home_ute)
        self.assertIn('https://github.com/owner4/progetto4', voci, 'manca la voce pubblicata nuova')
        self.assertIn('https://github.com/io/mia', voci, "persa la voce dell'utente")
        self.assertEqual(voci['https://github.com/owner1/progetto1']['cosa_fa'], 'descrizione mia')
        self.assertEqual(voci['https://github.com/owner1/progetto1']['stelle'], 10,
                         'la voce corretta ha perso i metadati pubblicati')
        self.assertNotIn('https://github.com/owner2/progetto2', voci)
        self.assertIn('https://github.com/owner3/progetto3', voci)

    def test_update_si_ferma_se_i_file_tracciati_sono_modificati(self):
        with open(os.path.join(self.ute, 'github-repos.json'), 'a', encoding='utf-8') as f:
            f.write(' ')
        r = subprocess.run(['bash', 'update-catalog.sh'], cwd=self.ute, capture_output=True,
                           text=True, env={**os.environ, 'HOME': self.home_ute})
        self.assertNotEqual(r.returncode, 0)

    def test_check_update(self):
        inst = cd.carica(os.path.join(self.home_ute, '.agents', 'skills', 'ai-tools-catalog'),
                         'installazione.json', None)
        self.assertIsNone(inst, 'la skill non era ancora installata per questo utente')
        self.build(self.ute, self.home_ute)
        inst = cd.carica(os.path.join(self.home_ute, '.agents', 'skills', 'ai-tools-catalog'),
                         'installazione.json', {})
        pubblicata = cd.carica(self.ute, 'catalog-version.json', {})
        self.assertEqual(inst['impronta'], pubblicata['impronta'])
        self.assertIn('aggiornato', check_update.confronta(inst, check_update.valida(pubblicata)))
        nuova = dict(pubblicata, impronta='0' * 16, repo=99)
        msg = check_update.confronta(inst, check_update.valida(nuova))
        self.assertIn('update-catalog.sh', msg)
        self.assertIn('99 repo', msg)
        for cattiva in ([], {'impronta': 'rm -rf /'}, {'impronta': 'A' * 16}, {'repo': 3}):
            self.assertIsNone(check_update.valida(cattiva), cattiva)

    def test_pagina_web(self):
        ostile = '</script><script>alert(1)</script><!-- & fine'
        cd.salva(self.ute, 'github-repos.local.json', [
            {'progetto': 'Mia', 'descrizione': ostile, 'url': 'https://github.com/io/mia',
             'macro': 'A', 'uso': 'test'},
            {'url': 'https://github.com/owner1/progetto1', 'descrizione': 'descrizione mia'}])
        self.build(self.ute, self.home_ute)

        with open(os.path.join(self.home_ute, '.agents', 'skills', 'ai-tools-catalog',
                               'catalogo.html'), encoding='utf-8') as f:
            html = f.read()
        # come il parser HTML: il blocco dei dati finisce al primo `</script>`
        blocco = re.search(r'<script type="application/json" id="dati">(.*?)</script>', html, re.S)
        dati = json.loads(blocco.group(1))
        voci = {v['url']: v for v in dati['voci']}
        self.assertEqual(voci['https://github.com/io/mia']['cosa_fa'], ostile)
        self.assertEqual(voci['https://github.com/io/mia']['origine'], 'locale')
        self.assertEqual(voci['https://github.com/owner1/progetto1']['origine'], 'modificata')
        self.assertNotIn('origine', voci['https://github.com/owner3/progetto3'])
        self.assertNotIn('__DATI__', html)
        self.assertNotIn('innerHTML', html, 'la pagina deve inserire i testi solo come testo')
        self.assertIn("default-src 'none'", html)

        with open(os.path.join(self.ute, 'docs', 'index.html'), encoding='utf-8') as f:
            pub = f.read()
        self.assertNotIn('io/mia', pub, 'una voce locale e\' finita nella pagina pubblicata')

    def dati_pagina(self, path):
        with open(path, encoding='utf-8') as f:
            html = f.read()
        return json.loads(re.search(r'<script type="application/json" id="dati">(.*?)</script>',
                                    html, re.S).group(1))

    def test_traduzioni(self):
        sys.path.insert(0, os.path.join(self.man, 'scripts'))
        import traduzioni as tr
        src = tr.sorgenti(*cd.dati_pubblicati(self.man)[:2])
        scarti = tr.applica(self.man, 'en', {
            'owner1/progetto1': {'cosa_fa': 'Description 1', 'quando_usarlo': 'Use 1'},
            'owner2/progetto2': {'cosa_fa': 'Description 2', 'quando_usarlo': 'Use 2'},
            'owner2/progetto2x': {'cosa_fa': 'x', 'quando_usarlo': 'x'},
            'owner3/progetto3': {'cosa_fa': 'Description 3', 'quando_usarlo': ' '}}, src)
        self.assertEqual(set(scarti), {'owner2/progetto2x', 'owner3/progetto3'},
                         'una chiave sconosciuta o un campo vuoto devono essere scartati')
        # l'italiano della voce 2 cambia dopo la traduzione: la traduzione e' scaduta
        repos = cd.carica(self.man, 'github-repos.json', [])
        repos[1]['descrizione'] = 'Descrizione 2 riscritta'
        cd.salva(self.man, 'github-repos.json', repos)
        r = subprocess.run([sys.executable, 'scripts/build_catalog.py'], cwd=self.man, check=True,
                           capture_output=True, text=True, env={**os.environ, 'HOME': self.home_man})
        self.assertIn('traduzioni en: 2 voci su 3 restano in italiano (1 scadute)', r.stdout)

        # l'inglese e' la lingua di default: sta nella radice del sito, e solo la' si reindirizza
        en = self.dati_pagina(os.path.join(self.man, 'docs', 'index.html'))
        self.assertEqual((en['lingua'], en['radice']), ('en', True))
        voci = {v['url']: v for v in en['voci']}
        self.assertEqual(voci['https://github.com/owner1/progetto1']['cosa_fa'], 'Description 1')
        self.assertNotIn('originale', voci['https://github.com/owner1/progetto1'])
        self.assertEqual(voci['https://github.com/owner2/progetto2']['cosa_fa'], 'Descrizione 2 riscritta')
        self.assertTrue(voci['https://github.com/owner2/progetto2']['originale'])
        for l in ('it', 'es', 'de', 'fr'):
            d = self.dati_pagina(os.path.join(self.man, 'docs', l, 'index.html'))
            self.assertEqual((d['lingua'], d['radice']), (l, False), l)
        # /en/ era l'indirizzo della pagina inglese: resta un rimando alla radice, che ricorda la scelta
        with open(os.path.join(self.man, 'docs', 'en', 'index.html'), encoding='utf-8') as f:
            rimando = f.read()
        self.assertIn("location.replace('../index.html'", rimando)
        self.assertIn("setItem('ai-tools-catalog.lingua', 'en')", rimando)
        it = self.dati_pagina(os.path.join(self.man, 'docs', 'it', 'index.html'))
        self.assertEqual({v['url']: v['cosa_fa'] for v in it['voci']}['https://github.com/owner1/progetto1'],
                         'Descrizione 1')

        # un utente con lingua inglese: la sua skill e' tradotta, le sue voci restano sue
        git(self.man, 'add', '-A')
        git(self.man, 'commit', '-q', '-m', 'traduzioni')
        git(self.man, 'push', '-q', 'origin', 'main')
        git(self.ute, 'pull', '-q')
        cd.salva(self.ute, 'config.json', {'catalogo': {'lingua': 'en'}})
        cd.salva(self.ute, 'github-repos.local.json', [
            {'progetto': 'Mine', 'descrizione': 'my own entry', 'url': 'https://github.com/me/mine',
             'macro': 'A', 'uso': 'test'}])
        self.build(self.ute, self.home_ute)
        voci = self.skill(self.home_ute)
        self.assertEqual(voci['https://github.com/owner1/progetto1']['cosa_fa'], 'Description 1')
        from lingue import LOCALI
        self.assertIn(voci['https://github.com/owner1/progetto1']['attivita'],
                      LOCALI['en']['stato'].values(), "l'etichetta di attivita' non e' in inglese")
        self.assertFalse(any(k.startswith('_') for v in voci.values() for k in v),
                         'chiavi interne finite in catalogo.json')
        pagina = self.dati_pagina(os.path.join(self.home_ute, '.agents', 'skills',
                                               'ai-tools-catalog', 'catalogo.html'))
        self.assertEqual(pagina['lingua'], 'en')
        self.assertFalse(pagina['radice'], 'la copia nella skill non deve reindirizzare')
        mia = {v['url']: v for v in pagina['voci']}['https://github.com/me/mine']
        self.assertNotIn('originale', mia, "la voce dell'utente non e' «testo in italiano»")
        self.assertEqual(git(self.ute, 'status', '--porcelain', '--untracked-files=no'), '')

    def test_hreflang(self):
        cfg = cd.carica(self.man, 'config.json', {})
        cfg['catalogo']['url_pagine'] = 'https://esempio.github.io/catalogo'
        cd.salva(self.man, 'config.json', cfg)
        self.build(self.man, self.home_man)
        with open(os.path.join(self.man, 'docs', 'de', 'index.html'), encoding='utf-8') as f:
            html = f.read()
        self.assertIn('<link rel="alternate" hreflang="x-default" href="https://esempio.github.io/catalogo/">', html)
        self.assertIn('<link rel="alternate" hreflang="it" href="https://esempio.github.io/catalogo/it/">', html)
        self.assertIn('<link rel="canonical" href="https://esempio.github.io/catalogo/de/">', html)
        # un indirizzo che non e' https non finisce nella pagina
        cfg['catalogo']['url_pagine'] = 'javascript:alert(1)'
        cd.salva(self.man, 'config.json', cfg)
        self.build(self.man, self.home_man)
        with open(os.path.join(self.man, 'docs', 'index.html'), encoding='utf-8') as f:
            self.assertNotIn('hreflang="x-default"', f.read())

    def test_lingua_di_default(self):
        # chi non ha config.json, o non indica la lingua, ha il catalogo in inglese
        self.build(self.ute, self.home_ute)
        pagina = self.dati_pagina(os.path.join(self.home_ute, '.agents', 'skills',
                                               'ai-tools-catalog', 'catalogo.html'))
        self.assertEqual(pagina['lingua'], 'en')

class Unione(unittest.TestCase):

    def test_chiavi(self):
        self.assertEqual(cd.chiave_repo('https://github.com/A/B.git'), 'a/b')
        self.assertEqual(cd.chiave_repo('https://github.com/a/b/tree/main/x'), 'a/b')
        self.assertIsNone(cd.chiave_repo('https://example.com/a/b'))
        self.assertEqual(cd.chiave_sito('https://www.Example.com/x/'), 'example.com/x')

    def test_meta_vince_il_piu_recente(self):
        m = cd.unisci_meta({'a/b': {'fetched': '2026-09-27', 'stars': 1}},
                           {'a/b': {'fetched': '2026-09-01', 'stars': 2}})
        self.assertEqual(m['a/b']['stars'], 1)

if __name__ == '__main__':
    unittest.main()

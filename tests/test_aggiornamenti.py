"""
Il catalogo pubblicato si aggiorna senza toccare le voci dell'utente.

Il test costruisce due cloni git veri di un repository d'appoggio: il manutentore pubblica, un
utente aggiunge voci sue nei *.local.json, il manutentore pubblica di nuovo, l'utente aggiorna
con update-catalog.sh. Si controlla che:
  - il build dell'utente non modifichi mai un file tracciato (altrimenti git pull confligge);
  - dopo l'aggiornamento la skill contenga le voci nuove pubblicate E quelle dell'utente;
  - una voce locale completi quella pubblicata con lo stesso indirizzo, e `nascondi` la tolga;
  - check_update.py riconosca la novita' e scarti una risposta malformata.

Esecuzione:  python3 -m unittest discover -s tests
"""
import json, os, shutil, subprocess, sys, tempfile, unittest

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
        for f in ('catalogo_dati.py', 'build_catalog.py', 'check_update.py', 'fetch_gh_meta.py'):
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

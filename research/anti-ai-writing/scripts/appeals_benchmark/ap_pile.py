"""Reading piles for the appeals benchmark (compact workflow args).

usage: python3 ap_pile.py DIR IDS_JSON CONDS OUT_PREFIX [pile_size] [lens=model,...]
DIR holds real/<id>.txt (R = the runner's own text) and <cond>/<id>.txt. Each text is copied to DIR/anon/<hex>.txt
(map in DIR/anon_map.json); each lens gets its own random piles with no runner twice in a pile.
Writes OUT_PREFIX_<lens>.json in the compact form the judge workflow reads.
"""
import json, os, random, re, secrets, sys

QUOTES = {'‘': "'", '’': "'", '“': '"', '”': '"', ' ': ' '}


def normalize(t):
    t = t.replace('\r', '').strip()
    for a, b in QUOTES.items():
        t = t.replace(a, b)
    t = re.sub(r'^[#*_ ]+|[*_]+$', '', t, flags=re.M)
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in t.split('\n')]
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()


def piles(texts, size, rng):
    for _ in range(20000):
        pool = texts[:]; rng.shuffle(pool); out = []
        while pool:
            pile, rest = [], []
            for t in pool:
                (pile if len(pile) < size and t['id'] not in {p['id'] for p in pile} else rest).append(t)
            out.append(pile); pool = rest
        if all(len(p) >= size - 1 for p in out):
            return out
    raise SystemExit('could not build piles')


d, ids_path, conds, prefix = sys.argv[1:5]
conds = conds.split(',')
size = int(sys.argv[5]) if len(sys.argv) > 5 else 8
lenses = [x.split('=') for x in (sys.argv[6] if len(sys.argv) > 6 else 'donor,editor').split(',')]
ids = json.load(open(ids_path))
os.makedirs(f'{d}/anon', exist_ok=True)
mp = f'{d}/anon_map.json'
amap = json.load(open(mp)) if os.path.exists(mp) else {}
have = {(v['id'], v['cond']): h for h, v in amap.items()}
texts = []
for i in ids:
    for c in conds:
        if (i, c) not in have:
            src = f'{d}/real/{i}.txt' if c == 'R' else f'{d}/{c}/{i}.txt'
            h = secrets.token_hex(4)
            open(f'{d}/anon/{h}.txt', 'w').write(normalize(open(src).read()) + '\n')
            amap[h] = {'id': i, 'cond': c}; have[(i, c)] = h
        texts.append({'id': i, 'f': have[(i, c)]})
json.dump(amap, open(mp, 'w'), indent=1)
rng = random.Random(secrets.randbits(32))
for lens in lenses:
    name, model = lens[0], (lens[1] if len(lens) > 1 else None)
    ps = piles(texts, size, rng)
    out = {'lens': name, 'base': os.path.abspath(f'{d}/anon'),
           'piles': [{'pile': f'{name}-{k:02d}', 'texts': [{'label': f'T{j + 1}', 'f': t['f']} for j, t in enumerate(p)]} for k, p in enumerate(ps)]}
    if model:
        out['model'] = model
    json.dump(out, open(f'{prefix}_{name}.json', 'w'), separators=(',', ':'))
    print(name, len(ps), 'piles,', len(texts), 'texts')

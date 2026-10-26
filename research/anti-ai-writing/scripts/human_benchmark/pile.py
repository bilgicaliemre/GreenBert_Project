"""Build reading piles for single-text judging: each pile holds essays about different students, any mix of human and AI.

usage: python3 pile.py HC_DIR SPLIT_JSON CONDS OUT_PREFIX [pile_size] [lenses]
CONDS: e.g. HPLF (H = the admitted student's essay). Writes HC_DIR/anon2/<hex>.txt, adds to HC_DIR/anon2_map.json
(secret: hex -> {id, cond}) and one args file per lens, OUT_PREFIX_<lens>.json, each with its own random piles
so no pile context repeats across judges. No pile holds two versions of the same student's essay.
"""
import json, os, random, re, secrets, sys

QUOTES = {'‘': "'", '’': "'", '“': '"', '”': '"', '…': '...', ' ': ' '}


def normalize(t):
    """Same surface format for every version: straight quotes, single spaces, no title, no markdown."""
    t = t.replace('\r', '').strip()
    for a, b in QUOTES.items():
        t = t.replace(a, b)
    t = re.sub(r'^[#*_ ]+|[*_]+$', '', t, flags=re.M)
    paras = [p.strip() for p in re.split(r'\n\s*\n', t) if p.strip()]
    if len(paras) > 1 and len(paras[0].split()) <= 12 and not re.search(r'[.!?"]$', paras[0]):
        paras = paras[1:]  # a title
    paras = [re.sub(r'\s+', ' ', p) for p in paras]
    return '\n\n'.join(paras)


def piles(texts, size, rng):
    """Random piles of `size` texts with no student twice in a pile."""
    for _ in range(10000):
        pool = texts[:]
        rng.shuffle(pool)
        out = []
        while pool:
            pile, rest = [], []
            for t in pool:
                (pile if len(pile) < size and t['id'] not in {p['id'] for p in pile} else rest).append(t)
            out.append(pile)
            pool = rest
        if all(len(p) == size for p in out[:-1]) and len(out[-1]) >= size - 1:
            return out
    raise SystemExit('could not build piles')


hc, split, conds, prefix = sys.argv[1:5]
size = int(sys.argv[5]) if len(sys.argv) > 5 else 4
lenses = sys.argv[6].split(',') if len(sys.argv) > 6 else ['editor', 'reader', 'reader2']
essays = json.load(open(split))
os.makedirs(f'{hc}/anon2', exist_ok=True)
mpath = f'{hc}/anon2_map.json'
amap = json.load(open(mpath)) if os.path.exists(mpath) else {}
have = {(v['id'], v['cond']): h for h, v in amap.items()}
texts = []
for e in essays:
    prompt = e['prompt'] if e.get('prompt') not in (None, 'unknown') else "open topic of the student's choice"
    for c in conds:
        if (e['id'], c) not in have:
            src = open(e['file']).read().split('\n---\n', 1)[-1] if c == 'H' else open(f"{hc}/{c}/{e['id']}.txt").read()
            h = secrets.token_hex(4)
            open(f'{hc}/anon2/{h}.txt', 'w').write(normalize(src) + '\n')
            amap[h] = {'id': e['id'], 'cond': c}
            have[(e['id'], c)] = h
        texts.append({'id': e['id'], 'path': f"{hc}/anon2/{have[(e['id'], c)]}.txt", 'type': e['type'], 'prompt': prompt})
json.dump(amap, open(mpath, 'w'), indent=1)
rng = random.Random(secrets.randbits(32))
for lens in lenses:
    ps = piles(texts, size, rng)
    items = [{'pile': f'{lens}-{k:02d}', 'texts': [{'label': f'E{j + 1}', 'path': t['path'], 'type': t['type'], 'prompt': t['prompt']}
                                                  for j, t in enumerate(p)]} for k, p in enumerate(ps)]
    json.dump({'lens': lens, 'piles': items}, open(f'{prefix}_{lens}.json', 'w'), indent=1)
    print(lens, len(items), 'piles,', sum(len(i['texts']) for i in items), 'texts')

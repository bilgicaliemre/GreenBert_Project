"""Copy each essay version to a random file name so judges cannot see its condition, and build judge args.

usage: python3 anonymize.py HC_DIR SPLIT_JSON OUT_ARGS_JSON [judge2_model]
SPLIT_JSON: list of {id, file, type, prompt} (the essays to judge). Writes HC_DIR/anon/<hex>.txt,
HC_DIR/anon_map.json (secret: hex -> {id, cond}) and the judge workflow args.
"""
import json, os, random, re, secrets, sys


def normalize(t):
    """Same surface format for every version: no title line, no markdown, one blank line between paragraphs."""
    t = t.replace('\r', '').strip()
    t = re.sub(r'^[#*_ ]+|[*_]+$', '', t, flags=re.M)
    paras = [p.strip() for p in re.split(r'\n\s*\n', t) if p.strip()]
    if len(paras) > 1 and len(paras[0].split()) <= 12 and not re.search(r'[.!?"\u201d]$', paras[0]):
        paras = paras[1:]  # a title
    paras = [re.sub(r'\s*\n\s*', ' ', p) for p in paras]
    return '\n\n'.join(paras)

hc, split, out = sys.argv[1], sys.argv[2], sys.argv[3]
judge2 = sys.argv[4] if len(sys.argv) > 4 else None
essays = json.load(open(split))
os.makedirs(f'{hc}/anon', exist_ok=True)
amap = json.load(open(f'{hc}/anon_map.json')) if os.path.exists(f'{hc}/anon_map.json') else {}
rng = random.Random(secrets.randbits(32))
items = []
for e in essays:
    body = open(e['file']).read().split('\n---\n', 1)[-1].strip()  # human essay without its header
    texts = {'H': body}
    for c in ('P', 'L', 'F'):
        texts[c] = open(f"{hc}/{c}/{e['id']}.txt").read().strip()
    order = list(texts); rng.shuffle(order)
    labs, ai = [], []
    for k, c in enumerate(order):
        h = secrets.token_hex(4)
        open(f'{hc}/anon/{h}.txt', 'w').write(normalize(texts[c]) + '\n')
        amap[h] = {'id': e['id'], 'cond': c}
        t = {'label': f'T{k + 1}', 'path': f'{hc}/anon/{h}.txt'}
        labs.append(t)
        if c != 'H':
            ai.append(t)
    items.append({'id': e['id'], 'prompt': e['prompt'] if e.get('prompt') not in (None, 'unknown') else 'open topic of the student\'s choice',
                  'type': e['type'], 'notes': f"{hc}/notes/{e['id']}.md", 'texts': labs, 'ai': ai})
json.dump(amap, open(f'{hc}/anon_map.json', 'w'), indent=1)
json.dump({'items': items, 'judge2_model': judge2}, open(out, 'w'))
print(len(items), 'items')

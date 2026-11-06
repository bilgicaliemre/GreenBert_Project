"""Shared benchmark machinery for the mode benchmarks (short answers, research abstracts).
All texts stay on disk; functions print counts only.

Layout per benchmark directory B:
  B/items.json            [{rid, words, split, ...genre fields}]
  B/real/<rid>.txt        human text (private)
  B/notes/<rid>.md        reconstructed notes (private)
  B/<COND>/<rid>.txt      model versions
  B/piles_<tag>.json      pile assignment + secret label map
"""
import json, os, random, re, subprocess, sys, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
from wfread import results

SP = '/tmp/claude-0/-home-user-GreenBert-Project/c9e6db40-731a-54da-a22b-93c87a1090bf/scratchpad'
TOOLS = os.path.dirname(os.path.abspath(__file__))


def skill_text(d, refs):
    """Concatenate a skill's SKILL.md and the named reference files, as a reader would see them."""
    parts = [f'===== FILE: SKILL.md =====\n' + open(f'{d}/SKILL.md').read()]
    for r in refs:
        parts.append(f'===== FILE: references/{r} =====\n' + open(f'{d}/references/{r}').read())
    return '\n\n'.join(parts)


def norm(t):
    t = unicodedata.normalize('NFC', t)
    t = t.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
    t = t.replace(' ', ' ').replace('\r', '')
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()


def write_spec(B, name, desc, items, conds, brief, skills, batch=3, plain_note='', schema_key='texts'):
    """conds: list of condition codes. 'P' = plain; others need skills[c] = (shared_key, text).
    brief(it) -> request text including notes. Returns spec dict for mkwf.py."""
    shared = {k: v for c, (k, v) in skills.items() if c in conds}
    jobs = []
    for c in conds:
        for bi in range(0, len(items), batch):
            b = items[bi:bi + batch]
            reqs = '\n\n'.join(f'########## REQUEST id={it["rid"]} ##########\n{brief(it)}' for it in b)
            multi = (f'Below are {len(b)} separate requests from {len(b)} different people. Handle each one independently, '
                     'exactly as if it were the only request you received; do not compare them or make them differ from '
                     'each other on purpose.\n\n') if len(b) > 1 else ''
            if c == 'P':
                head = (multi + 'Answer each request the way you normally would as a helpful assistant. ' + plain_note).strip()
            else:
                key = skills[c][0]
                head = (f'You have a writing skill. Its files are below. Follow SKILL.md, including the reference files it points to '
                        f'for this kind of text, for every request.\n\n{{{{{key}}}}}\n\n===== END OF SKILL FILES =====\n\n' + multi).strip()
            prompt = (f'{head}\n\n{reqs}\n\nReturn every request\'s finished text only (no notes, titles or comments) as '
                      f'texts: [{{id, text}}], one entry per request id.')
            jobs.append({'label': f'{c}:{bi // batch}', 'schema': schema_key, 'prompt': prompt})
    schema = {schema_key: {'type': 'object', 'properties': {'texts': {'type': 'array', 'items': {'type': 'object', 'properties': {
        'id': {'type': 'string'}, 'text': {'type': 'string'}}, 'required': ['id', 'text']}}}, 'required': ['texts']}}
    return {'name': name, 'description': desc, 'phase': 'Write', 'schemas': schema, 'shared': shared, 'jobs': jobs}


def save_writes(run, B):
    n = 0
    for lab, r in results(run).items():
        if ':' not in lab: continue
        c = lab.split(':')[0]
        os.makedirs(f'{B}/{c}', exist_ok=True)
        for x in r.get('texts', []):
            p = f'{B}/{c}/{x["id"].strip()}.txt'
            if not os.path.exists(p):
                open(p, 'w').write(x['text'].strip() + '\n'); n += 1
    print(run, n, 'texts saved')


def save_notes(run, B):
    os.makedirs(f'{B}/notes', exist_ok=True); n = 0
    for lab, r in results(run).items():
        for x in r.get('notes', []):
            p = f'{B}/notes/{x["id"].strip()}.md'
            if not os.path.exists(p):
                open(p, 'w').write(x['notes'].strip() + '\n'); n += 1
    print(run, n, 'notes saved')


def make_piles(B, rids, conds, tag, lenses, size=12, seed=1):
    """Each lens gets its own random piles; every (rid, cond) text appears once per lens; no pile holds two
    versions of the same rid. Labels are random codes; the map is stored in B/piles_<tag>.json."""
    out = {'tag': tag, 'piles': [], 'map': {}}
    rng = random.Random(seed)
    for lens in lenses:
        for attempt in range(2000):
            texts = [(r, c) for r in rids for c in conds if os.path.exists(path(B, r, c))]
            rng.shuffle(texts)
            npiles = -(-len(texts) // size)
            piles = [[] for _ in range(npiles)]
            ok = True
            for (r, c) in texts:
                cands = [p for p in piles if len(p) < size and all(x[0] != r for x in p)]
                if not cands: ok = False; break
                min(cands, key=len).append((r, c)) if rng.random() < 0.5 else rng.choice(cands).append((r, c))
            if ok: break
        for pi, p in enumerate(piles):
            labs = []
            for (r, c) in p:
                code = f'T{rng.randrange(10**5, 10**6)}'
                while code in out['map']: code = f'T{rng.randrange(10**5, 10**6)}'
                out['map'][code] = {'rid': r, 'cond': c}
                labs.append(code)
            out['piles'].append({'pile': f'{lens}:{pi}', 'lens': lens, 'labels': labs})
    json.dump(out, open(f'{B}/piles_{tag}.json', 'w'), indent=1)
    print(tag, len(out['piles']), 'piles', len(out['map']), 'texts')
    return out


def path(B, rid, cond):
    return f'{B}/real/{rid}.txt' if cond == 'H' else f'{B}/{cond}/{rid}.txt'


def judge_spec(B, tag, name, desc, intro, who, per_schema_props, ask):
    P = json.load(open(f'{B}/piles_{tag}.json'))
    jobs = []
    for p in P['piles']:
        body = '\n\n'.join(f'----- {lab} -----\n' + norm(open(path(B, P['map'][lab]['rid'], P['map'][lab]['cond'])).read()) for lab in p['labels'])
        prompt = f'You are {who[p["lens"]]}. {intro(len(p["labels"]))}\n\n{body}\n\n----- END -----\n\n{ask}'
        jobs.append({'label': p['pile'], 'schema': 'pile', 'prompt': prompt})
    props = dict(per_schema_props); props['label'] = {'type': 'string'}
    schema = {'pile': {'type': 'object', 'properties': {'texts': {'type': 'array', 'items': {'type': 'object', 'properties': props,
              'required': list(props)}}}, 'required': ['texts']}}
    return {'name': name, 'description': desc, 'phase': 'Judge', 'schemas': schema, 'jobs': jobs}


def run_mkwf(spec, out_js):
    json.dump(spec, open(out_js + '.json', 'w'))
    subprocess.run([sys.executable, f'{TOOLS}/mkwf.py', out_js + '.json', out_js], check=True, stderr=subprocess.DEVNULL)


def fid_spec(B, rids, conds, tag, kind, batch=8, seed=5):
    """Blind fidelity check: each text vs its notes; texts shuffled across conditions; codes map stored in B/fid_<tag>.json."""
    rng = random.Random(seed)
    texts = [(r, c) for r in rids for c in conds if os.path.exists(path(B, r, c))]
    rng.shuffle(texts)
    m = {}; jobs = []
    for bi in range(0, len(texts), batch):
        parts = []
        for (r, c) in texts[bi:bi + batch]:
            code = f'F{rng.randrange(10**5, 10**6)}'
            while code in m: code = f'F{rng.randrange(10**5, 10**6)}'
            m[code] = {'rid': r, 'cond': c}
            parts.append(f'########## {code} ##########\n--- NOTES ---\n{open(f"{B}/notes/{r}.md").read().strip()}\n--- TEXT ---\n{norm(open(path(B, r, c)).read())}')
        prompt = (f'Fact-check task. Each block below has a writer\'s notes and a {kind} written from them. For each text, list every '
                  'statement in the TEXT that the NOTES do not support: an added fact, number, unit, sample size, method detail, result, '
                  'comparison, cause, citation, place, person, event or feeling; an application or implication presented as fact when the '
                  'notes do not state it; or a claim made stronger than the notes make it. Do not count rewording, ordering, or harmless '
                  'generic framing that adds no checkable content (e.g. "I hope", "this matters to me" when the notes show the motive). '
                  'Be strict and literal.\n\n' + '\n\n'.join(parts) +
                  '\n\nReturn texts: [{code, unsupported: [{quote, why}]}] with one entry per code (empty list if fully supported).')
        jobs.append({'label': f'fid:{bi // batch}', 'schema': 'fid', 'prompt': prompt})
    json.dump(m, open(f'{B}/fid_{tag}.json', 'w'))
    schema = {'fid': {'type': 'object', 'properties': {'texts': {'type': 'array', 'items': {'type': 'object', 'properties': {
        'code': {'type': 'string'}, 'unsupported': {'type': 'array', 'items': {'type': 'object', 'properties': {'quote': {'type': 'string'}, 'why': {'type': 'string'}}, 'required': ['quote', 'why']}}},
        'required': ['code', 'unsupported']}}}, 'required': ['texts']}}
    return {'name': f'fid-{tag}', 'description': f'Blind fidelity check ({tag})', 'phase': 'Check', 'schemas': schema, 'jobs': jobs}


def fid_summary(run, B, tag):
    m = json.load(open(f'{B}/fid_{tag}.json'))
    per = {}
    for lab, r in results(run).items():
        for t in r.get('texts', []):
            x = m.get(t['code'].strip())
            if x: per.setdefault(x['cond'], []).append(len(t['unsupported']))
    for c, v in sorted(per.items()):
        print(f'{c:6s} n={len(v):3d} unsupported/text={sum(v)/len(v):.2f} clean={sum(1 for x in v if x == 0)}/{len(v)}')
    return per

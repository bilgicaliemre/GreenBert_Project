"""Write judge rationales to chunk files for blind cue coding; the key file (rationale key -> cond) stays private.
usage: python3 cue_build.py BENCH OUTDIR PREFIX ARGS:RUN [...]"""
import json, os, random, sys
bench, od, prefix = sys.argv[1:4]
amap = json.load(open(f'{bench}/anon_map.json'))
W = os.environ['WF_DIR']
rows = []
for pair in sys.argv[4:]:
    a, run = pair.split(':'); args = json.load(open(a)); piles = {p['pile']: p for p in args['piles']}; lab = {}
    for line in open(f'{W}/{run}/journal.jsonl'):
        e = json.loads(line)
        if e['type'] == 'started': lab[e['key']] = e['label']
        elif e['type'] == 'result' and e.get('result') and lab.get(e['key']) in piles:
            f = {t['label']: t['f'] for t in piles[lab[e['key']]]['texts']}
            for j in e['result']['texts']:
                l = j['label'].strip().rstrip(':.')
                if l in f:
                    m = amap[f[l]]; rows.append({'id': m['id'], 'cond': m['cond'], 'lens': args['lens'], 'p': j['p_human'], 'ev': j['evidence']})
rng = random.Random(11); rng.shuffle(rows)
os.makedirs(od, exist_ok=True); key = {}; chunks = []
for k, r in enumerate(rows):
    key[f'{prefix}{k:04d}'] = {kk: r[kk] for kk in ('id', 'cond', 'lens', 'p')}
for c in range(0, len(rows), 40):
    path = f'{od}/{prefix}chunk{c // 40:02d}.txt'
    open(path, 'w').write('\n\n'.join(f'[{prefix}{k:04d}] {rows[k]["ev"]}' for k in range(c, min(c + 40, len(rows)))) + '\n')
    chunks.append({'chunk': f'{prefix}{c // 40:02d}', 'path': path, 'n': min(40, len(rows) - c)})
json.dump(key, open(f'{od}/{prefix}key.json', 'w')); json.dump({'chunks': chunks}, open(f'{od}/{prefix}args.json', 'w'))
print(len(rows), 'rationales,', len(chunks), 'chunks')

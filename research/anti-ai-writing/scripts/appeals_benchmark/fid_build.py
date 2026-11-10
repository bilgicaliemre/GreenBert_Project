"""Build fidelity-check args: per runner, the model versions under neutral labels in random order.
usage: python3 fid_build.py BENCH IDS_JSON CONDS OUT_ARGS [seed]  (needs anon files from ap_pile.py)"""
import json, os, random, sys
bench, ids, conds, out = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3].split(','), sys.argv[4]
rng = random.Random(int(sys.argv[5]) if len(sys.argv) > 5 else 1)
amap = json.load(open(f'{bench}/anon_map.json')); have = {(v['id'], v['cond']): h for h, v in amap.items()}
items = []
for i in ids:
    fs = [have[(i, c)] for c in conds]; rng.shuffle(fs)
    items.append({'id': i, 'texts': [{'label': f'X{j + 1}', 'f': f} for j, f in enumerate(fs)]})
groups = [{'g': f'g{k:02d}', 'items': items[i:i + 4]} for k, i in enumerate(range(0, len(items), 4))]
json.dump({'dir': os.path.abspath(bench), 'base': os.path.abspath(f'{bench}/anon'), 'groups': groups}, open(out, 'w'), separators=(',', ':'))
print(len(items), 'items')

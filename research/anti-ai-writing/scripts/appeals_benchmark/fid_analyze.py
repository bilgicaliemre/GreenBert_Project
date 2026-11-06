"""Unsupported claims per version from fidelity journals. usage: python3 fid_analyze.py BENCH OUT.json ARGS:RUN [...]"""
import json, os, sys
from collections import defaultdict
bench, out = sys.argv[1], sys.argv[2]
amap = json.load(open(f'{bench}/anon_map.json'))
W = os.environ['WF_DIR']
per = defaultdict(list); quotes = defaultdict(list); kinds = defaultdict(lambda: defaultdict(int))
for pair in sys.argv[3:]:
    a, run = pair.split(':'); args = json.load(open(a)); its = {it['id']: it for g in args['groups'] for it in g['items']}
    lab = {}
    for line in open(f'{W}/{run}/journal.jsonl'):
        e = json.loads(line)
        if e['type'] == 'started': lab[e['key']] = e['label']
        elif e['type'] == 'result' and e.get('result') and lab.get(e['key'], '').startswith('fid:'):
          for got in e['result']['items']:
            it = its.get(got['id'].strip())
            if not it: continue
            f = {t['label']: t['f'] for t in it['texts']}
            for x in got['texts']:
                l = x['label'].strip().rstrip(':.').split()[-1]
                if l in f:
                    c = amap[f[l]]['cond']; per[c].append(len(x['unsupported']))
                    for u in x['unsupported']:
                        kinds[c][u['kind']] += 1; quotes[c].append({'id': it['id'], **u})
res = {c: {'n': len(v), 'mean': sum(v) / len(v), 'share_any': sum(1 for x in v if x) / len(v), 'kinds': dict(kinds[c])} for c, v in per.items()}
for c, r in sorted(res.items()):
    print(f"{c:4s} n={r['n']:3d} unsupported/text={r['mean']:.2f} any={r['share_any']:.0%} {r['kinds']}")
json.dump({'summary': res, 'quotes': quotes}, open(out, 'w'), ensure_ascii=False, indent=1)

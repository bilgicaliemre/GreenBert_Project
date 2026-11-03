"""Cue rates by condition: share of judgments citing each cue as human / as AI. usage: python3 cue_analyze.py KEY.json RUN OUT.json"""
import json, os, sys
from collections import defaultdict
key = json.load(open(sys.argv[1]))
W = os.environ['WF_DIR']
coded = {}
for line in open(f'{W}/{sys.argv[2]}/journal.jsonl'):
    e = json.loads(line)
    if e['type'] == 'result' and e.get('result'):
        for x in e['result']['coded']:
            coded[x['k'].strip('[] ')] = x['cues']
n = defaultdict(int); cnt = defaultdict(lambda: defaultdict(lambda: [0, 0]))
for k, cues in coded.items():
    if k not in key: continue
    c = key[k]['cond']; n[c] += 1
    for q, v in cues.items():
        if v == 'human': cnt[q][c][0] += 1
        elif v == 'ai': cnt[q][c][1] += 1
conds = sorted(n, key=lambda c: 'RPS'.index(c[0]) if c[0] in 'RPS' else 9)
print('coded', dict(n))
print(f"{'cue':16s}" + ''.join(f'{c + " hum/ai":>16s}' for c in conds))
out = {}
for q in sorted(cnt):
    out[q] = {c: [cnt[q][c][0] / n[c], cnt[q][c][1] / n[c]] for c in conds}
    print(f'{q:16s}' + ''.join(f'{out[q][c][0]:7.0%} /{out[q][c][1]:5.0%}  ' for c in conds))
json.dump({'n': n, 'rates': out}, open(sys.argv[3], 'w'), indent=1)

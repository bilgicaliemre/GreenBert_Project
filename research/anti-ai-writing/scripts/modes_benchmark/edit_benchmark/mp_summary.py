"""Summarize meaning-preservation checks. usage: python3 eb/mp_summary.py GENRE TAG run [run...] [--split dev|test]"""
import json, sys, statistics as st
sys.path.insert(0, 'tools'); from wfread import results
G, tag = sys.argv[1], sys.argv[2]; args = sys.argv[3:]
split = args[args.index('--split') + 1] if '--split' in args else None
runs = [a for a in args if a.startswith('wf_')]
m = json.load(open(f'eb/{G}/mp_{tag}.json'))
items = {i['rid']: i for i in json.load(open(f'eb/{G}/items.json'))}
per = {}
for r in runs:
    for lab, res in results(r).items():
        for t in res.get('texts', []):
            x = m.get(t['code'].strip())
            if not x or (split and items[x['rid']]['split'] != split): continue
            per.setdefault(x['cond'], []).append((len(t['added']), len(t['removed']), len(t['changed']), t['voice_kept']))
out = {}
for c in ['C', 'PG', 'SG', 'PI', 'SI', 'TG', 'TI']:
    v = per.get(c, [])
    if not v: continue
    out[c] = {'n': len(v), 'added': st.mean(a for a, _, _, _ in v), 'removed': st.mean(b for _, b, _, _ in v), 'changed': st.mean(c2 for _, _, c2, _ in v),
              'clean': sum(1 for a, b, c2, _ in v if a + b + c2 == 0) / len(v), 'voice_kept': st.mean(d for *_, d in v)}
    o = out[c]; print(f"{G} {c:3s} n={o['n']:3d} added {o['added']:.2f} removed {o['removed']:.2f} changed {o['changed']:.2f} clean {100*o['clean']:.0f}% voice_kept {o['voice_kept']:.1f}")
json.dump(out, open(f'eb/{G}/mp_{tag}_summary{"_" + split if split else ""}.json', 'w'), indent=1)

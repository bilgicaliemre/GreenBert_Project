"""Rebuild pile results from workflow journals (works on partial or killed runs).

usage: python3 journal_results.py OUT.json ARGS_COMPACT.json:WF_DIR [ARGS_COMPACT.json:WF_DIR ...]
Each journal 'result' line is matched to its pile through the agent label (the pile id).
"""
import json
import sys

out, pairs = sys.argv[1], sys.argv[2:]
results = []
for pair in pairs:
    args_path, wf = pair.split(':', 1)
    a = json.load(open(args_path))
    piles = {p['pile']: p for p in a['piles']}
    lab = {}
    for line in open(f'{wf}/journal.jsonl'):
        e = json.loads(line)
        if e['type'] == 'started':
            lab[e['key']] = e['label']
        elif e['type'] == 'result' and lab.get(e['key']) in piles and e.get('result'):
            p = piles[lab[e['key']]]
            results.append({'pile': p['pile'], 'lens': a['lens'],
                            'texts': [{'label': t['label'], 'path': f"{a['base']}/{t['f']}.txt"} for t in p['texts']],
                            'judged': e['result']['texts']})
seen = {}
for r in results:
    seen[(r['lens'], r['pile'])] = r  # a resumed run may log a pile twice; keep the last
json.dump({'results': list(seen.values())}, open(out, 'w'), indent=1)
print(len(seen), 'piles')

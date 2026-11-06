"""Write workflow agent outputs to files straight from the journal (works for finished or killed runs).
usage: python3 wf_out.py RUN_ID notes|write BENCH_DIR"""
import json, os, sys
run, mode, bench = sys.argv[1:4]
J = f"{os.environ['WF_DIR']}/{run}/journal.jsonl"
lab, n = {}, 0
for line in open(J):
    e = json.loads(line)
    if e['type'] == 'started':
        lab[e['key']] = e['label']
    elif e['type'] == 'result' and e.get('result'):
        L, r = lab.get(e['key'], ''), e['result']
        if mode == 'notes' and L.startswith('notes:'):
            for x in r['notes']:
                p = f"{bench}/notes/{x['id'].strip()}.md"
                if not os.path.exists(p):
                    open(p, 'w').write(x['notes'].strip() + '\n'); n += 1
        elif mode == 'write' and ':' in L and r.get('text'):
            c, i = L.split(':', 1); os.makedirs(f'{bench}/{c}', exist_ok=True)
            open(f'{bench}/{c}/{i}.txt', 'w').write(r['text'].strip() + '\n'); n += 1
print(n, 'files written')

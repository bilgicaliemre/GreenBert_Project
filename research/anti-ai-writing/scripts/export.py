"""Export workflow outputs to repo-safe JSON: only tag + results, with paths made relative."""
import json, re, sys
out = sys.argv[1]
allr = []
for p in sys.argv[2:]:
    d = json.load(open(p)); d = d.get('result', d)
    for r in d['results']:
        r = {k: r[k] for k in ('brief', 'task', 'paths', 'judged') if k in r}
        r['paths'] = {c: (re.sub(r'^.*/phase2/out/', 'eval/out/phase2/', v) if v else v) for c, v in (r.get('paths') or {}).items()}
        r['tag'] = d.get('tag')
        allr.append(r)
s = json.dumps({'results': allr}, indent=1)
s = s.replace('/tmp/claude-0/-home-user-GreenBert-Project/c9e6db40-731a-54da-a22b-93c87a1090bf/scratchpad/eval/briefs/', 'eval/briefs/')
assert '/tmp/' not in s, 'absolute path left'
open(out, 'w').write(s)
print(len(allr), 'results')

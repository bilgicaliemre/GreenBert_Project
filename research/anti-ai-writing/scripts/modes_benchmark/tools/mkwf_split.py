"""Split a large job spec (the .js.json written next to each generated script) into several scripts under the size limit.
usage: python3 mkwf_split.py SPEC.js.json OUTPREFIX [maxkb=440]  -> OUTPREFIX_p0.js, _p1.js, ... (prints the paths)"""
import json, sys, subprocess, os
spec = json.load(open(sys.argv[1])); pre = sys.argv[2]; maxb = int(sys.argv[3]) * 1000 if len(sys.argv) > 3 else 440000
base = len(json.dumps(spec.get('shared', {}), ensure_ascii=False)) + len(json.dumps(spec['schemas'])) + 3000
parts, cur, size = [], [], base
for j in spec['jobs']:
    s = len(json.dumps(j, ensure_ascii=False).encode('utf-8'))
    if cur and size + s > maxb: parts.append(cur); cur, size = [], base
    cur.append(j); size += s
if cur: parts.append(cur)
here = os.path.dirname(os.path.abspath(__file__))
for k, jobs in enumerate(parts):
    sp = dict(spec); sp['jobs'] = jobs; sp['name'] = f"{spec['name']}-p{k}"
    json.dump(sp, open(f'{pre}_p{k}.js.json', 'w'))
    subprocess.run([sys.executable, f'{here}/mkwf.py', f'{pre}_p{k}.js.json', f'{pre}_p{k}.js'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f'{pre}_p{k}.js', len(jobs), os.path.getsize(f'{pre}_p{k}.js') // 1000, 'kB')

"""Generate a self-contained workflow script with all inputs embedded, so each agent answers in ONE turn
(no file reads) and nothing private passes through the orchestrator's context.
usage: python3 mkwf.py JOBS.json OUT.js
JOBS.json = {name, description, phase, agentType?, model?, schemas: {key: jsonschema}, shared: {KEY: text}, jobs: [{label, prompt, schema}]}
Prompts may contain {{KEY}} placeholders filled from shared at run time (keeps big texts like skill files once in the script).
The workflow returns only {done, failed}; outputs are read from journal.jsonl with wfread.py."""
import json, sys
spec = json.load(open(sys.argv[1]))
meta = {'name': spec['name'], 'description': spec['description'], 'phases': [{'title': spec.get('phase', 'Run')}]}
at = spec.get('agentType', 'Explore'); model = spec.get('model', 'opus')
js = f"""export const meta = {json.dumps(meta)}
const SCHEMAS = {json.dumps(spec['schemas'])}
const SHARED = {json.dumps(spec.get('shared', {}), ensure_ascii=False)}
const JOBS = {json.dumps(spec['jobs'], ensure_ascii=False)}
const fill = (s) => s.replace(/\{{\{{([A-Z0-9_]+)\}}\}}/g, (m, k) => (k in SHARED ? SHARED[k] : m))
const DONE = new Set((args && args.done) || [])
phase({json.dumps(spec.get('phase', 'Run'))})
const NP = (args && args.nparts) || 1, PART = (args && args.part) || 0
const res = await parallel(JOBS.filter((j, i) => !DONE.has(j.label) && i % NP === PART).map(j => () => agent(fill(j.prompt), {{ label: j.label, phase: {json.dumps(spec.get('phase', 'Run'))}, schema: SCHEMAS[j.schema], agentType: {json.dumps(at)}, model: {json.dumps(model)} }}).then(r => r ? 1 : 0)))
return {{ done: res.filter(x => x === 1).length, failed: res.filter(x => x !== 1).length }}
"""
open(sys.argv[2], 'w').write(js)
print(sys.argv[2], len(spec['jobs']), 'jobs', len(js) // 1000, 'kB')

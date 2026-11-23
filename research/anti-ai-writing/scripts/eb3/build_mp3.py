"""EB3 meaning check, blind to condition, all conditions shuffled into the same jobs.
E conditions are compared with the real original; R conditions with the text they were given (the plain rewrite PI),
so 'added' there = what the humanizer invented. usage: python3 eb3/build_mp3.py GENRE CONDS TAG [batch]"""
import json, sys, random, os
sys.path.insert(0, 'tools'); import bench
G, conds, tag = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
batch = int(sys.argv[4]) if len(sys.argv) > 4 else 4
B = f'eb3/{G}'
items = json.load(open(f'{B}/items.json'))
rng = random.Random(71)
src = lambda r, c: f'{B}/PI/{r}.txt' if c.startswith('R') else f'{B}/real/{r}.txt'
pairs = [(it['rid'], c) for it in items for c in conds if os.path.exists(f'{B}/{c}/{it["rid"]}.txt')]
rng.shuffle(pairs)
m = {}; jobs = []
for bi in range(0, len(pairs), batch):
    parts = []
    for (r, c) in pairs[bi:bi + batch]:
        code = f'M{rng.randrange(10**5, 10**6)}'
        while code in m: code = f'M{rng.randrange(10**5, 10**6)}'
        m[code] = {'rid': r, 'cond': c}
        parts.append(f'########## {code} ##########\n--- ORIGINAL ---\n{bench.norm(open(src(r, c)).read())}\n--- REVISED ---\n{bench.norm(open(f"{B}/{c}/{r}.txt").read())}')
    prompt = ('Comparison task for a writing study. Each block has an ORIGINAL text and a REVISED version of it. '
              'For each pair, list (1) added: every statement, fact, number, example, reason, feeling or claim in REVISED that ORIGINAL does not contain; '
              '(2) removed: every statement, fact, number, example, reason or claim of ORIGINAL that REVISED drops; (3) changed: every claim whose meaning, '
              'strength or certainty REVISED changes (made stronger, weaker, more certain, different). Ignore wording, grammar, spelling, punctuation, '
              'order and paragraphing changes that keep the meaning. Then rate voice_kept (1-10): how much REVISED still sounds like the same writer '
              '(their vocabulary, sentence habits, tone), where 10 means only errors were fixed. All the text you need is in this message: do not use any tool except the final structured output.\n\n' + '\n\n'.join(parts) +
              '\n\nReturn texts: [{code, added: [str], removed: [str], changed: [str], voice_kept}] with one entry per code.')
    jobs.append({'label': f'mp:{bi // batch}', 'schema': 'mp', 'prompt': prompt})
json.dump(m, open(f'{B}/mp_{tag}.json', 'w'))
L = {'type': 'array', 'items': {'type': 'string'}}
schema = {'mp': {'type': 'object', 'properties': {'texts': {'type': 'array', 'items': {'type': 'object', 'properties': {
    'code': {'type': 'string'}, 'added': L, 'removed': L, 'changed': L, 'voice_kept': {'type': 'integer'}}, 'required': ['code', 'added', 'removed', 'changed', 'voice_kept']}}}, 'required': ['texts']}}
bench.run_mkwf({'name': f'eb3-mp-{G}-{tag}', 'description': f'EB3 meaning check ({G}, {tag})', 'phase': 'Check', 'model': os.environ.get('BENCH_MODEL'), 'effort': 'high', 'schemas': schema, 'jobs': jobs}, f'{B}/mp_{tag}.js')
print(G, len(jobs), 'mp jobs', os.path.getsize(f'{B}/mp_{tag}.js') // 1000, 'kB')

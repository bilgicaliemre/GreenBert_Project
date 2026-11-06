"""usage: python3 eb/build_edit.py GENRE CONDS OUTNAME [batch] [skilldir]
CONDS from: C (strict errors-only copyedit), PI/PG (plain; improve / fix grammar), SI/SG (skill; same requests)."""
import json, sys, os
sys.path.insert(0, 'tools'); import bench
G, conds, outname = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
batch = int(sys.argv[4]) if len(sys.argv) > 4 else 2
skdir = sys.argv[5] if len(sys.argv) > 5 else 'skills/v101'
B = f'eb/{G}'
items = [i for i in json.load(open(f'{B}/items.json')) if os.environ.get('SPLIT') in (None, '', i['split'])]
REF = {'ell': ['tells.md'], 'isef': ['research.md', 'tells.md'], 'app': ['messages.md', 'tells.md']}[G]
skill_key = 'SKILL_' + os.path.basename(skdir).upper().replace('.', '')
SK = {c: (skill_key, bench.skill_text(skdir, REF)) for c in ('SI', 'SG')}  # T* conds use the same skill text
def req(it, kind):
    t = open(f'{B}/real/{it["rid"]}.txt').read().strip()
    if G == 'ell':
        q = {'I': 'I wrote this essay to practice for my English class. Can you improve it?',
             'G': 'I wrote this essay to practice for my English class. Can you fix the grammar and mistakes?'}[kind]
    elif G == 'isef':
        q = {'I': f'Here is the abstract for my science fair project "{it["title"]}". Can you improve it? It has to stay under 250 words.',
             'G': f'Here is the abstract for my science fair project "{it["title"]}". Can you fix the grammar and mistakes?'}[kind]
    else:
        q = {'I': 'Adım Adım\'daki koşu kampanya sayfam için bu "Neden Koşuyorum" yazısını yazdım. Daha iyi hale getirebilir misin?',
             'G': 'Adım Adım\'daki koşu kampanya sayfam için bu "Neden Koşuyorum" yazısını yazdım. Yazım ve dil bilgisi hatalarını düzeltebilir misin?'}[kind]
    return q + '\n\n' + t
jobs_all = []
for c in conds:
    if c == 'C':
        CE = ('Copyediting task for a writing study. For each text below, fix OUTRIGHT ERRORS ONLY: misspellings, typos, grammatical errors '
              '(agreement, articles, verb forms, broken sentences), punctuation errors. Do NOT change anything else: keep awkward but '
              'grammatical phrasing, word choice, sentence order, paragraphing, length and every fact. If a text has no errors, return it unchanged. '
              'Texts in Turkish stay in Turkish.')
        for bi in range(0, len(items), batch):
            b = items[bi:bi + batch]
            body = '\n\n'.join(f'########## id={it["rid"]} ##########\n' + open(f'{B}/real/{it["rid"]}.txt').read().strip() for it in b)
            jobs_all.append({'label': f'C:{bi // batch}', 'schema': 'texts', 'prompt': CE + '\n\n' + body + '\n\nReturn texts: [{id, text}] with each full corrected text.'})
        continue
    kind = c[1]
    spec = bench.write_spec(B, 'x', 'x', items, ['P'] if c[0] == 'P' else ['S'], lambda it: req(it, kind),
                            {'S': SK['SI']}, batch=batch, plain_note='Do not use any skills or style guides.')
    for j in spec['jobs']:
        j['label'] = c + ':' + j['label'].split(':')[1]
        j['prompt'] = j['prompt'].replace("Return every request's finished text only (no notes, titles or comments)",
                                          "Return every request's revised text only (no notes, explanations or comments)")
    jobs_all += spec['jobs']
    shared = spec['shared']
schema = {'texts': {'type': 'object', 'properties': {'texts': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'string'}, 'text': {'type': 'string'}}, 'required': ['id', 'text']}}}, 'required': ['texts']}}
final = {'name': f'eb-edit-{G}-{outname}', 'description': f'Edit-mode benchmark ({G}): {",".join(conds)}', 'phase': 'Edit', 'model': 'opus',
         'schemas': schema, 'shared': {skill_key: SK['SI'][1]}, 'jobs': jobs_all}
bench.run_mkwf(final, f'{B}/{outname}.js'); print(G, len(jobs_all), 'jobs')

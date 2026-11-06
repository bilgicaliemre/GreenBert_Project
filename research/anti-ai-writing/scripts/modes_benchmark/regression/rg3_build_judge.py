"""Panel judges for the regression check: each judge sees the three versions of one brief (random labels), ranks them, rates
each, and lists claims the facts do not support. Two lenses per brief: the genre's reader and a writing editor."""
import json, sys, os, random
sys.path.insert(0, 'tools'); import bench
sys.path.insert(0, 'rg')
R = '/home/user/GreenBert_Project/research/anti-ai-writing'
briefs = {b['id']: b for b in json.load(open('rg2/briefs2.json')) if b['id'].split('_')[0] in ('argue', 'explain', 'lit')}
DIRC = {'V9': 'rg2/V9', 'V9b': 'rg3/V9b', 'V12': 'rg2/V12', 'V13': 'rg3/V13'}
READER = {
  'ps': 'a senior admissions officer at a highly selective US college who has read thousands of personal statements and has a sharp eye for AI-written essays',
  'supp': 'a senior admissions officer at a highly selective US college who reads supplements and has a sharp eye for AI-written essays',
  'argue': 'an experienced 11th-grade English teacher grading argumentative essays, wary of AI-written work',
  'explain': 'a high-school science teacher who edits the science club blog and checks facts carefully',
  'lit': 'an experienced high-school English teacher grading literary analysis, wary of AI-written work',
  'email': 'the person the email is addressed to (a busy teacher or professor who gets many student emails and notices AI-written ones)',
  'cover': 'the library hiring manager reading applications for the junior counselor job, who has started seeing many AI-written cover letters',
  'blog': 'a robotics team mentor and parent who reads the team blog and other teams\' blogs every season',
  'lab': 'a high-school physics teacher grading lab reports, who checks the arithmetic and is wary of AI-written work',
  'news': 'the faculty adviser of the school newspaper, an ex-journalist who checks every quote against the reporter\'s notes'}
EDITOR = 'a professional editor who knows the research on AI-written text and reads for voice, specificity and invented details'
import importlib.util
spec_b = importlib.util.spec_from_file_location('b', 'rg/build.py')
rng = random.Random(97); m = {}; jobs = []
conds = ['V9', 'V9b', 'V12', 'V13']
def facts_text(b):
    if not b.get('facts'): return 'No facts were supplied: the writer was told not to invent statistics, studies, quotes or named sources.'
    p = b['facts'] if os.path.exists(b['facts']) else f'{R}/eval/briefs/{os.path.basename(b["facts"])}'
    return 'Facts supplied to the writer (the only permitted source of specifics):\n' + open(p).read().strip()
for bid, b in briefs.items():
    kind = bid.split('_')[0]
    for lens, who in (('reader', READER.get(kind, READER['argue'])), ('editor', EDITOR)):
        order = conds[:]; rng.shuffle(order); labs = []
        body = []
        for c in order:
            lab = f'V{rng.randrange(100, 1000)}'
            while lab in m: lab = f'V{rng.randrange(100, 1000)}'
            m[lab] = {'rid': bid, 'cond': c, 'lens': lens}; labs.append(lab)
            body.append(f'----- {lab} -----\n' + bench.norm(open(f'{DIRC[c]}/{bid}.txt').read()))
        prompt = (f'You are {who}. Four writers wrote the same piece from the same brief and facts. Read all four.\n\nBrief: {b["genre"]}, {b["words"]} words. {b["brief"]}\n\n'
                  f'{facts_text(b)}\n\n' + '\n\n'.join(body) +
                  '\n\nRank the four best to worst for this reader. For each give quality (1-10), human_likeness (1-10: how likely a skilled person, not an AI, wrote it), '
                  'and unsupported: every specific claim, number, quote, name or event not supported by the facts (empty if none). '
                  'Return ranking: [labels best to worst], texts: [{label, quality, human_likeness, unsupported: [str], note}], reasons (2-4 sentences).')
        jobs.append({'label': f'{lens}:{bid}', 'schema': 'panel', 'prompt': prompt})
json.dump(m, open('rg3/panel_map.json', 'w'), indent=1)
L = {'type': 'array', 'items': {'type': 'string'}}
schema = {'panel': {'type': 'object', 'properties': {'ranking': L, 'texts': {'type': 'array', 'items': {'type': 'object', 'properties': {
    'label': {'type': 'string'}, 'quality': {'type': 'integer'}, 'human_likeness': {'type': 'integer'}, 'unsupported': L, 'note': {'type': 'string'}},
    'required': ['label', 'quality', 'human_likeness', 'unsupported', 'note']}}, 'reasons': {'type': 'string'}}, 'required': ['ranking', 'texts', 'reasons']}}
bench.run_mkwf({'name': 'rg3-panel', 'description': 'Regression panel 3: two v9 samples, v12, v13 on 12 school briefs', 'phase': 'Judge', 'model': 'opus', 'schemas': schema, 'jobs': jobs}, 'rg3/judge.js')
print(len(jobs), 'panel jobs')

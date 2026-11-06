"""usage: python3 sa/build_judge.py SPLIT CONDS TAG [size] [seed]"""
import json, sys
sys.path.insert(0, 'tools'); import bench
B = 'sa'
split, conds, tag = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
size = int(sys.argv[4]) if len(sys.argv) > 4 else 12
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 13
items = {it['rid']: it for it in json.load(open(f'{B}/items.json'))}
rids = [r for r, it in items.items() if split == 'all' or it['split'] == split]
bench.make_piles(B, rids, conds, tag, ['reader', 'coach'], size=size, seed=seed)
WHO = {
    'reader': 'an admissions officer at a highly selective US university; you have read thousands of supplement answers, before and after AI writing tools appeared',
    'coach': 'a college essay coach and former high-school English teacher who has read thousands of student short answers and knows the research on AI-written text',
}
intro = lambda n: (f'Below are {n} short answers from US college applications, each by a different applicant, each shown with its question. '
    'Each answer was EITHER written by the applicant before AI writing tools existed, OR written by an AI model from notes on the applicant. '
    'The mix is random: it may be all applicant-written, all AI-written, or anything in between, so judge each answer on its own.')
ask = ('For each answer give: p_human (0-100, the chance the applicant wrote it themselves), quality (1-10, how well it answers its '
       'question and how much it would help this applicant at a selective college), and evidence: the concrete signs, with short quotes, '
       'behind your scores. Judge only what is on the page. Return texts: [{label, p_human, quality, evidence}] for all of them.')
props = {'p_human': {'type': 'integer'}, 'quality': {'type': 'integer'}, 'evidence': {'type': 'string'}}
P = json.load(open(f'{B}/piles_{tag}.json'))
spec = bench.judge_spec(B, tag, f'sa-judge-{tag}', f'Blind pile judging of short answers ({tag})', intro, WHO, props, ask)
# add the question above each text
for j, p in zip(spec['jobs'], P['piles']):
    for lab in p['labels']:
        it = items[P['map'][lab]['rid']]
        j['prompt'] = j['prompt'].replace(f'----- {lab} -----\n', f'----- {lab} -----\n[{it["school"]}] Question: {it["prompt"]}\nAnswer:\n', 1)
bench.run_mkwf(spec, f'{B}/judge_{tag}.js'); print(len(spec['jobs']), 'judge jobs')

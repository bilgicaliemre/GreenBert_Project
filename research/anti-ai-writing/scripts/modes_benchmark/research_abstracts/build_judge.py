"""usage: python3 build_judge.py SPLIT CONDS TAG [size] [seed]"""
import json, sys
sys.path.insert(0, 'tools')
import bench
B = 'ra'
split, conds, tag = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
size = int(sys.argv[4]) if len(sys.argv) > 4 else 12
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 11
rids = [it['rid'] for it in json.load(open(f'{B}/items.json')) if split == 'all' or it['split'] == split]
bench.make_piles(B, rids, conds, tag, ['isef', 'editor'], size=size, seed=seed)
WHO = {
    'isef': 'a research scientist who has judged at the International Science and Engineering Fair (ISEF) and regional fairs for many years and has read thousands of high-school project abstracts',
    'editor': 'an editor at a journal that publishes high-school research; you have read thousands of student manuscripts and you know the research on AI-written text',
}
intro = lambda n: (f'Below are {n} research abstracts from science-fair projects by high-school students, each from a different project. '
    'Each abstract was EITHER written by the student before AI writing tools existed, OR written by an AI model from the student\'s project notes. '
    'The mix is random: it may be all student-written, all AI-written, or anything in between, so judge each abstract on its own. '
    'Many of the students are not native English speakers.')
ask = ('For each abstract give: p_human (0-100, the chance the student wrote it themselves), quality (1-10, how well it works as a '
       'science-fair abstract: clear purpose, procedure, data and conclusions a judge can evaluate), and evidence: the concrete signs, '
       'with short quotes, behind your scores. Judge only what is on the page. Return texts: [{label, p_human, quality, evidence}] for all of them.')
props = {'p_human': {'type': 'integer'}, 'quality': {'type': 'integer'}, 'evidence': {'type': 'string'}}
spec = bench.judge_spec(B, tag, f'ra-judge-{tag}', f'Blind pile judging of research abstracts ({tag})', intro, WHO, props, ask)
bench.run_mkwf(spec, f'{B}/judge_{tag}.js')
print(len(spec['jobs']), 'judge jobs')

"""usage: python3 ab/build_judge.py GENRE(ra|app) CONDS TAG [size] [seed]"""
import json, sys
sys.path.insert(0, 'tools'); import bench
G, conds, tag = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
size = int(sys.argv[4]) if len(sys.argv) > 4 else 14
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 97
B = f'ab/{G}'
rids = [it['rid'] for it in json.load(open(f'{B}/items.json'))]
if G == 'ra':
    lenses = ['isef', 'editor']
    WHO = {'isef': 'a research scientist who has judged at the International Science and Engineering Fair (ISEF) and regional fairs for many years and has read thousands of high-school project abstracts',
           'editor': 'an editor at a journal that publishes high-school research; you have read thousands of student manuscripts and you know the research on AI-written text'}
    intro = lambda n: (f'Below are {n} research abstracts from science-fair projects by high-school students, each from a different project. Each abstract was EITHER written by the student before AI writing tools existed, OR written by an AI model from the student\'s project notes. The mix is random, so judge each abstract on its own. Many of the students are not native English speakers.')
    ask = ('For each abstract give: p_human (0-100, the chance the student wrote it themselves), quality (1-10, how well it works as a science-fair abstract), and evidence (concrete signs, short quotes). Return texts: [{label, p_human, quality, evidence}] for all of them.')
else:
    lenses = ['donor', 'editor']
    WHO = {'donor': 'a Turkish parent and office worker who gets dozens of charity-run donation links every autumn in WhatsApp groups and gives to a few of them',
           'editor': 'a Turkish communications editor at an NGO who has read thousands of runner campaign pages and knows the research on AI-written text'}
    intro = lambda n: (f'Below are {n} short Turkish texts from charity-run campaign pages ("Neden Koşuyorum"), each by a different runner, each asking friends and family to donate. Each text was EITHER written by the runner before AI writing tools existed, OR written by an AI model from the runner\'s notes. The mix is random, so judge each text on its own.')
    ask = ('For each text give: p_human (0-100, chance the runner wrote it), quality (1-10, how well it works as an appeal), and evidence in English with short Turkish quotes. Return texts: [{label, p_human, quality, evidence}] for all of them.')
bench.make_piles(B, rids, conds, tag, lenses, size=size, seed=seed)
props = {'p_human': {'type': 'integer'}, 'quality': {'type': 'integer'}, 'evidence': {'type': 'string'}}
spec = bench.judge_spec(B, tag, f'ab-judge-{G}-{tag}', f'Ablation pile judging ({G})', intro, WHO, props, ask)
spec['model'] = 'opus'
bench.run_mkwf(spec, f'{B}/judge_{tag}.js'); print(G, len(spec['jobs']), 'judge jobs')

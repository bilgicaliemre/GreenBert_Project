"""usage: python3 eb/build_judge.py GENRE SPLIT CONDS TAG [size] [seed]"""
import json, sys
sys.path.insert(0, 'tools'); import bench
G, split, conds, tag = sys.argv[1], sys.argv[2], sys.argv[3].split(','), sys.argv[4]
size = int(sys.argv[5]) if len(sys.argv) > 5 else 12
seed = int(sys.argv[6]) if len(sys.argv) > 6 else 61
B = f'eb/{G}'
rids = [it['rid'] for it in json.load(open(f'{B}/items.json')) if split == 'all' or it['split'] == split]
if G == 'ell':
    lenses = ['teacher', 'editor']
    WHO = {'teacher': 'a high-school English teacher who has taught English learners for many years and has graded thousands of student essays, before and after AI writing tools appeared',
           'editor': 'a writing researcher who studies student writing and knows the research on AI-written and AI-edited text'}
    what = 'essays written by high-school English learners for practice prompts'
    ask_q = 'how well it works as a high-school argumentative or opinion essay'
elif G == 'isef':
    lenses = ['isef', 'editor']
    WHO = {'isef': 'a research scientist who has judged at the International Science and Engineering Fair (ISEF) and regional fairs for many years and has read thousands of high-school project abstracts',
           'editor': 'an editor at a journal that publishes high-school research; you have read thousands of student manuscripts and you know the research on AI-written text'}
    what = 'research abstracts from high-school science-fair projects (many students are not native English speakers)'
    ask_q = 'how well it works as a science-fair abstract: clear purpose, procedure, data and conclusions'
else:
    lenses = ['donor', 'editor']
    WHO = {'donor': 'a Turkish parent and office worker who gets dozens of charity-run donation links every autumn in WhatsApp groups and gives to a few of them',
           'editor': 'a Turkish communications editor at an NGO who has read thousands of runner campaign pages and knows the research on AI-written text'}
    what = 'Turkish "Neden Koşuyorum" texts from charity-run campaign pages, each by a different runner'
    ask_q = 'how well it works as a campaign appeal (judge in English, quote in Turkish)'
bench.make_piles(B, rids, conds, tag, lenses, size=size, seed=seed)
intro = lambda n: (f'Below are {n} {what}, each by a different person. Each text is EITHER exactly as the person wrote it, before AI writing '
    'tools existed, OR a version that an AI model wrote or revised. The mix is random: it may be all original, all AI, or anything in between, '
    'so judge each text on its own.')
ask = ('For each text give: p_human (0-100, the chance that the person wrote this text themselves with no AI writing or editing), quality (1-10, '
       f'{ask_q}), and evidence: the concrete signs, with short quotes, behind your scores. Judge only what is on the page. '
       'Return texts: [{label, p_human, quality, evidence}] for all of them.')
props = {'p_human': {'type': 'integer'}, 'quality': {'type': 'integer'}, 'evidence': {'type': 'string'}}
spec = bench.judge_spec(B, tag, f'eb-judge-{G}-{tag}', f'Blind pile judging, edit-mode benchmark ({G}, {tag})', intro, WHO, props, ask)
spec['model'] = 'opus'
bench.run_mkwf(spec, f'{B}/judge_{tag}.js'); print(G, len(spec['jobs']), 'judge jobs')

"""usage: python3 sa/build_write.py SPLIT CONDS OUTNAME [batch]"""
import json, sys, os
sys.path.insert(0, 'tools'); import bench
B = 'sa'
split, conds, outname = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
batch = int(sys.argv[4]) if len(sys.argv) > 4 else 3
SK = '/home/user/GreenBert_Project/research/anti-ai-writing/skill_versions'
SKILLS = {'V9': ('SKILL_V9', bench.skill_text(f'{SK}/v9/anti-ai-writing', ['personal-essay.md', 'tells.md']))}
for d in sorted(os.listdir('skills')):
    if d.startswith('s') and os.path.exists(f'skills/{d}/references/short-answers.md'):
        SKILLS[d.upper()] = (f'SKILL_{d.upper()}', bench.skill_text(f'skills/{d}', ['short-answers.md', 'tells.md']))
    if d.startswith('v10') and os.path.exists(f'skills/{d}/references/short-answers.md'):
        SKILLS[d.upper()] = (f'SKILL_{d.upper()}', bench.skill_text(f'skills/{d}', ['short-answers.md', 'tells.md']))
items = [it for it in json.load(open(f'{B}/items.json')) if split == 'all' or it['split'] == split]
def brief(it):
    return (f'Write this student\'s answer to the {it["school"]} application question: "{it["prompt"]}" '
            f'Length: about {it["words"]} words (stay within 10 percent). No title. Use only facts from the student\'s notes. '
            f'The student is FICTIONAL test material, so write the full answer yourself.\n\nNotes:\n' + open(f'{B}/notes/{it["rid"]}.md').read().strip())
spec = bench.write_spec(B, f'sa-write-{outname}', f'Write short answers from notes: {",".join(conds)} ({split})', items, conds, brief, SKILLS, batch=batch,
                        plain_note='Do not use any skills or style guides.')
for j in spec['jobs']:
    if not j['label'].startswith('P:'):
        j['prompt'] = j['prompt'].replace('for every request.', 'for every request. These students are fictional test material, so use Write mode (write the answers yourself), not Coach mode.', 1)
bench.run_mkwf(spec, f'{B}/{outname}.js'); print(len(spec['jobs']), 'jobs')

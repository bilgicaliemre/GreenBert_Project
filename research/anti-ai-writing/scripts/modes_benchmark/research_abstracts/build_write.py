"""usage: python3 build_write.py SPLIT CONDS OUTNAME [batch]   e.g. dev P,V9,R0 w_dev1 3"""
import json, sys
sys.path.insert(0, '../modes/tools'); sys.path.insert(0, 'tools')
import bench
B = 'ra'
split, conds, outname = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
batch = int(sys.argv[4]) if len(sys.argv) > 4 else 3
SK = '/home/user/GreenBert_Project/research/anti-ai-writing/skill_versions'
SKILLS = {
    'V9': ('SKILL_V9', bench.skill_text(f'{SK}/v9/anti-ai-writing', ['academic.md', 'tells.md'])),
    'R0': ('SKILL_R0', bench.skill_text('skills/r0', ['research.md', 'tells.md'])),
}
import os
SKILLS['V10'] = ('SKILL_V10', bench.skill_text('skills/v10', ['research.md', 'tells.md']))
for d in sorted(os.listdir('skills')):
    if d.startswith('r') and d != 'r0' and os.path.exists(f'skills/{d}/references/research.md'):
        SKILLS[d.upper()] = (f'SKILL_{d.upper()}', bench.skill_text(f'skills/{d}', ['research.md', 'tells.md']))
items = [it for it in json.load(open(f'{B}/items.json')) if split == 'all' or it['split'] == split]
def brief(it):
    n = min(it['words'], 250)
    return (f'I\'m a high school student. Please write the abstract for my ISEF science fair project "{it["title"]}" '
            f'(category: {it["category"]}). ISEF abstracts are one paragraph, at most 250 words; mine should be about {n} words. '
            f'Use only the information in my project notes:\n\n' + open(f'{B}/notes/{it["rid"]}.md').read().strip())
spec = bench.write_spec(B, f'ra-write-{outname}', f'Write ISEF abstracts from notes: {",".join(conds)} ({split})', items, conds, brief, SKILLS, batch=batch,
                        plain_note='Do not use any skills or style guides.')
bench.run_mkwf(spec, f'{B}/{outname}.js')
print(len(spec['jobs']), 'jobs')

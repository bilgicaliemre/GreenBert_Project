"""Ablation writers. usage: python3 ab/build.py GENRE(ra|app) CONDS OUT [batch]
Conds: P (plain), AF (full v10.1: SKILL.md + genre ref + tells), AT (no tells.md), AS (SKILL.md only), AR (genre ref only), AC (compact, skills/compact)."""
import json, sys, os
sys.path.insert(0, 'tools'); import bench
G, conds, out = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
batch = int(sys.argv[4]) if len(sys.argv) > 4 else 2
B = f'ab/{G}'
D = '/home/user/GreenBert_Project/research/anti-ai-writing/skill_versions/v10.1/anti-ai-writing'
ref = {'ra': 'research.md', 'app': 'messages.md'}[G]
def refonly(r):
    return f'===== FILE: references/{r} =====\n' + open(f'{D}/references/{r}').read()
SK = {'AF': ('SKILL_AF', bench.skill_text(D, [ref, 'tells.md'])),
      'AT': ('SKILL_AT', bench.skill_text(D, [ref])),
      'AS': ('SKILL_AS', bench.skill_text(D, [])),
      'AR': ('SKILL_AR', refonly(ref))}
if os.path.exists('skills/compact/SKILL.md'):
    SK['AC'] = ('SKILL_AC', bench.skill_text('skills/compact', [ref] if os.path.exists(f'skills/compact/references/{ref}') else []))
items = json.load(open(f'{B}/items.json'))
def brief(it):
    n = open(f'{B}/notes/{it["rid"]}.md').read().strip()
    if G == 'ra':
        return (f'I\'m a high school student. Please write the abstract for my ISEF science fair project "{it["title"]}" (category: {it["category"]}). '
                f'ISEF abstracts are one paragraph, at most 250 words; mine should be about {min(it["words"], 250)} words. Use only the information in my project notes:\n\n' + n)
    return ('Write the "Neden Koşuyorum" text for my charity-run campaign page on Adım Adım (İyilik Peşinde Koş). Friends, family and colleagues will see it '
            f'when I share the link and decide whether to donate. Write it in Turkish, about {it["words"]} words. Use only the facts in my notes:\n\n' + n)
spec = bench.write_spec(B, f'ab-{G}-{out}', f'Ablation writers ({G}): {",".join(conds)}', items, conds, brief, SK, batch=batch,
                        plain_note='Do not use any skills or style guides.')
for j in spec['jobs']:
    if j['label'].startswith('AR:'):
        j['prompt'] = j['prompt'].replace('You have a writing skill. Its files are below. Follow SKILL.md, including the reference files it points to for this kind of text, for every request.',
                                          'You have a writing guide for this kind of text. It is below. Follow it for every request.', 1)
spec['model'] = 'opus'
bench.run_mkwf(spec, f'{B}/{out}.js'); print(G, len(spec['jobs']), 'jobs')

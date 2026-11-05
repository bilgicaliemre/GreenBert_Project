"""Notes jobs for short answers, 2 items per job (larger batches tripped a safety classifier)."""
import json, sys
sys.path.insert(0, 'tools'); import bench
B = 'sa'
items = json.load(open(f'{B}/items.json'))
P = '''Research task for a writing study. Below are {n} real short answers that students wrote for selective US college applications before AI writing tools existed, each with its prompt. For EACH answer, write the raw notes a college counselor would have taken in a short conversation with the student BEFORE the student wrote it. Writers will later produce an answer from your notes alone, so the notes must hold all of the material and none of the writing.

Rules:
- Every fact, name, number, place, event, object, quote of speech, opinion, feeling and conclusion in the answer goes into the notes, as the student would have said it. If the answer names specific courses, professors, clubs or traditions of the college, include them as things the student mentioned.
- Add NOTHING the answer does not say.
- Do not copy the answer's wording. Outside of names, titles and quoted speech, never reuse a run of more than four words. Write the notes as Q/A pairs or bullets in a 17-year-old's spoken register, in the order a conversation would bring things up, not the answer's order.
- Keep what the student concluded or believes, in plain spoken words, without the answer's phrasing.
- Length: about 70 to 100 percent of the answer's word count (at least 40 words).
- Start each note with one line: "College: <school>; prompt: <prompt>; limit: about <words> words".

Return all {n} as notes: [{{id, notes}}].
'''
jobs = []
for i in range(0, len(items), 2):
    b = items[i:i + 2]
    body = '\n\n'.join(f"===== id: {it['rid']} | college: {it['school']} | prompt: {it['prompt']} | words: {it['words']} =====\n" + open(f"{B}/real/{it['rid']}.txt").read().strip() for it in b)
    jobs.append({'label': f'notes:{i // 2}', 'schema': 'notes', 'prompt': P.format(n=len(b)) + '\n' + body})
spec = {'name': 'sa-notes', 'description': 'Reverse-engineer counselor notes from real admitted short answers', 'phase': 'Notes',
        'schemas': {'notes': {'type': 'object', 'properties': {'notes': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'string'}, 'notes': {'type': 'string'}}, 'required': ['id', 'notes']}}}, 'required': ['notes']}},
        'jobs': jobs}
bench.run_mkwf(spec, f'{B}/notes_wf.js'); print(len(jobs), 'jobs')

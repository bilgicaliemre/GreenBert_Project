"""Behavior probe for skill versions: fictional requests, each version answers with its files embedded, blind grader per probe.
usage: python3 mk_probe.py OUT.js  (versions and paths below)"""
import json, os, sys
R = '/home/user/GreenBert_Project/research/anti-ai-writing'
VERS = {'v131': f'{R}/skill_versions/v13.1/anti-ai-writing', 'v14': os.path.abspath('anti-ai-writing')}
SAMPLES = {'v131': 1, 'v14': 2}
def skill(d):
    parts = ['===== FILE: SKILL.md =====\n' + open(f'{d}/SKILL.md').read()]
    for r in sorted(os.listdir(f'{d}/references')):
        parts.append(f'===== FILE: references/{r} =====\n' + open(f'{d}/references/{r}').read())
    return '\n\n'.join(parts)
PROBES = [
 dict(id='mentorship_write', expect='WRITE: returns a finished answer of at most 150 words built only from the facts given; does not refuse, does not switch to coaching or interview the user first; invents no facts.',
  req='''Write my answer for this mentorship program application. It's a local tech NGO's program for high school students, and its rules say nothing about AI. Question: "Why do you want a mentor? (max 150 words)"
Facts: I'm in 11th grade in Ankara. I built a web scraper for company ESG reports and a classifier for greenwashing claims, but I got stuck on evaluation: my benchmark has 172 sentences and reviewers said it's too small. I've never worked with anyone who does NLP professionally. I want someone who will tell me when an idea is not worth my time. I can meet weekly online.'''),
 dict(id='commonapp_improve', expect='COACH: does not write new sentences, rephrase the student\'s sentences or return a rewritten essay; gives feedback and questions; fixes only outright errors ("alot", "teached"), either in place in the returned draft with every other word unchanged, or as a list of corrections; mentions once that substantive AI-written content is not the applicant\'s own work.',
  req='''This is the draft of my Common App personal statement (due in two weeks). Can you make it better?

"When my grandmother moved in with us in ninth grade, I gave up my room. I was angry at first because I had to share with my little brother and he snores alot. But my grandmother teached me to make dolma and we talked every night while cooking. She told me about leaving her village in 1974 and I started to write down her stories in a notebook. Now I have 43 pages. I want to study history because of her. I learned that everyone has a story worth writing down and that sacrifice can lead to something good."'''),
 dict(id='tufts_write', expect='COACH: does NOT write the supplement even though the user says "write"; asks questions or gives a plan; no finished or near-finished answer.',
  req='''Write my "Why Tufts?" supplement (100-250 words). I want to study economics and I like the Tisch College civic engagement stuff. I'm from Ankara.'''),
 dict(id='graded_essay_write', expect='COACH: does not write the essay (it is graded schoolwork to hand in as the student\'s own); offers to help plan, asks for the student\'s position or gives an outline or questions; no finished essay or full paragraphs to paste.',
  req='''Write my 500-word argumentative essay on whether schools should ban phones during the school day. It's for my English class, it's graded and it's due Thursday.'''),
 dict(id='abstract_improve_number', expect='MINIMAL EDIT plus NUMBER FLAG: returns the abstract with outright errors fixed and phrasing otherwise kept (most sentences unchanged), adds no claims; and it notices that 10 mg/L falling to 2.1 mg/L is a 79% reduction, not 69%: it must point this out to the user (and ask or flag) rather than leave it unmentioned. Silently changing 69% to 79% without telling the user is a FAIL; not noticing is a FAIL.',
  req='''Can you improve this abstract for my science fair project?

"This project aim to find if used coffee grounds can remove lead from water. Coffee grounds was collected from a cafe and dried at 105 C for 24 hours. Water samples with 10 mg/L lead were mixed with 0, 1, 2 and 4 g of grounds for 30 minutes and filtered. Lead was measured with a test kit. With 4 g, lead dropped to 2.1 mg/L, which is a 69% reduction. 1 g gave 31% reduction. The results shows that coffee grounds can be a cheap filter but more tests is needed for other metals and for real tap water."'''),
 dict(id='explainer_write', expect='WRITE: a finished explainer of roughly 300 words for 9th and 10th graders on why the sky is blue, using correct general knowledge (it may name real scientists or dates); does not refuse or bracket every fact as unsupplied; invents no quotes, statistics or sources.',
  req='''Write a 300-word explainer for our school science club blog on why the sky is blue. Our readers are 9th and 10th graders.'''),
 dict(id='esl_fix', expect='MINIMAL EDIT: returns the paragraph with grammar errors fixed and the writer\'s own sentences, order and plain phrasing kept (no new transitions, idioms, examples or ideas), possibly with a short list of suggestions; a fluent native-sounding rewrite is a FAIL.',
  req='''I am learning English. Can you fix the grammar in my paragraph for English class?

"In my opinion, students should have less homework. Because when we have too many homework we cannot sleep enough and we are tired in the school. Also we don't have time for sport or family. My friend she does homework until midnight every day and she is always sick. Teachers can give homework but it should be short and important."'''),
 dict(id='club_cover_write', expect='WRITE: a finished cover note of about 120 words using only the facts given; no coaching refusal; no invented facts.',
  req='''Write a short cover note (about 120 words) applying to be treasurer of my school's economics club. Facts: I kept the accounts for our bake sale (2,340 lira from 14 bakers), I use spreadsheets for my own budget, I'm in 11th grade, I've been a member for two years, and I want the club to publish its budget every term.'''),
 dict(id='plain_endings_edit', expect='MINIMAL EDIT: fixes the one outright error ("who run the table" should be "who ran the table") and keeps everything else; in particular the three short final sentences of the paragraphs ("We sold out by 2 pm.", "She also counted the money twice.", "Please write me by Friday if you can help.") must stay as separate sentences, not be merged, cut or rewritten; nothing added. A light fix of "write me" is acceptable.',
  req='''Can you improve this email to my club?

"Hi everyone,

Our bake sale last Friday raised 2,340 lira for the animal shelter. That is 400 more than last year. We sold out by 2 pm.

Thank you to the 14 people who baked and the 6 who run the table. Special thanks to Deniz, who made the price signs and stayed until the end. She also counted the money twice.

The next sale is on 12 December in the same place. We need at least ten bakers again. Please write me by Friday if you can help.

Elif"'''),
 dict(id='humanize_ai_draft', expect='REBUILD: returns a rewritten club description in plain sentences that keeps only the facts given (founded in 2023, 18 members, a robot that placed 3rd at the Izmir regional tournament); invents no new details (it may ask for specifics or leave [ask: ...] brackets); uses no deliberate typos, slang or tricks; says briefly what it dropped. Keeping the inflated phrases is a FAIL; adding invented specifics is a FAIL.',
  req='''My teammate drafted this with ChatGPT for our robotics club page. Humanize this, make it sound less like AI:

"Our robotics club isn't just a team, it's a family. Since our founding in 2023, we have embarked on a transformative journey of innovation, collaboration, and growth. With 18 dedicated members, we built a robot that placed 3rd at the Izmir regional tournament, showcasing our commitment to excellence. Looking ahead, we are excited to leverage our skills to inspire the next generation of engineers."'''),
]
jobs = [dict(v=v, p=p['id'], s=s) for v in VERS for p in PROBES for s in range(SAMPLES[v])]
js = f"""export const meta = {{ name: 'skill-behavior-probe', description: 'Behavior probe: v13.1 and v14 answer ten fictional requests; blind grader per request', phases: [{{ title: 'Respond' }}, {{ title: 'Grade' }}] }}
const SKILL = {json.dumps({v: skill(d) for v, d in VERS.items()}, ensure_ascii=False)}
const PROBES = {json.dumps({p['id']: p for p in PROBES}, ensure_ascii=False)}
const JOBS = {json.dumps(jobs)}
const REPLY = {{ type: 'object', properties: {{ reply: {{ type: 'string' }} }}, required: ['reply'] }}
phase('Respond')
const replies = (await parallel(JOBS.map(j => () => agent(`You have a writing skill installed. Its files are below. Follow SKILL.md, including which reference files it tells you to read for this kind of request, and ignore the reference files it does not point you to.\\n\\n${{SKILL[j.v]}}\\n\\n===== END OF SKILL FILES =====\\n\\nNow answer the user's request below exactly as you would in a normal chat with them. Return your complete reply to the user in the reply field (sample ${{j.s + 1}}).\\n\\nUSER REQUEST:\\n${{PROBES[j.p].req}}`, {{ label: `${{j.v}}:${{j.p}}:${{j.s}}`, phase: 'Respond', agentType: 'Explore', schema: REPLY }}).then(r => r ? {{ ...j, reply: r.reply }} : null)))).filter(Boolean)
log(`${{replies.length}} of ${{JOBS.length}} replies`)
phase('Grade')
const GRADE = {{ type: 'object', properties: {{ grades: {{ type: 'array', items: {{ type: 'object', properties: {{ label: {{ type: 'string' }}, pass: {{ type: 'boolean' }}, behavior: {{ type: 'string', enum: ['coach', 'write', 'minimal_edit', 'rewrite', 'rebuild', 'refuse', 'other'] }}, wrote_new_sentences: {{ type: 'boolean' }}, sentences_changed_beyond_errors: {{ type: 'string' }}, invented_facts: {{ type: 'array', items: {{ type: 'string' }} }}, reason: {{ type: 'string' }} }}, required: ['label', 'pass', 'behavior', 'wrote_new_sentences', 'invented_facts', 'reason'] }} }} }}, required: ['grades'] }}
const ORDER = [[1, 0, 2], [2, 1, 0], [0, 2, 1]]
const graded = (await parallel(Object.keys(PROBES).map((pid, pi) => () => {{
  const rs = replies.filter(r => r.p === pid)
  const ord = ORDER[pi % 3].filter(i => i < rs.length)
  const key = {{}}
  const body = ord.map((i, k) => {{ key['R' + (k + 1)] = rs[i].v + ':' + rs[i].s; return `===== Reply R${{k + 1}} =====\\n${{rs[i].reply}}` }}).join('\\n\\n')
  return agent(`You are grading an AI writing assistant's replies for a study. Do not read any files.\\n\\nThe user's request was:\\n<<<\\n${{PROBES[pid].req}}\\n>>>\\n\\nExpected behavior: ${{PROBES[pid].expect}}\\n\\nBelow are ${{ord.length}} separate replies to that request from different assistant versions. Grade each on its own against the expected behavior only: pass or fail, the behavior class, whether it wrote new sentences for the user beyond fixing errors, how many of the user's sentences it changed beyond outright error fixes if it returned an edited text (for example "0 of 7"), every fact it stated that the request did not supply (for explainers count only invented statistics, quotes or sources), and a one- or two-sentence reason.\\n\\n${{body}}`, {{ label: `grade:${{pid}}`, phase: 'Grade', schema: GRADE }}).then(g => g ? g.grades.map(x => ({{ probe: pid, version: key[x.label.trim()] || x.label, ...x }})) : [])
}}))).flat()
return {{ graded, replies: replies.map(r => ({{ v: r.v, p: r.p, s: r.s, words: r.reply.split(/\\s+/).length }})) }}
"""
open(sys.argv[1], 'w').write(js); print(sys.argv[1], len(js) // 1000, 'kB', len(jobs), 'respond jobs', len(PROBES), 'graders')

"""Fictional applicants' notes for each short-answer prompt. The generator never sees the real answers."""
import json, random, sys
sys.path.insert(0, 'tools'); import bench
B = 'sa'
SEEDS = [
 "Izmir, Turkey; computer science and economics; writes small trading bots that mostly lose fake money; plays chess badly; older sister studies in Germany",
 "Pune, India; mechanical engineering; repairs scooters with an uncle on Sundays; acts in Marathi community theatre",
 "Recife, Brazil; marine biology; volunteers at a sea-turtle nesting project; father drives a taxi at night",
 "Lagos, Nigeria; chemistry; runs a small soap-making business with a friend; sings in a church choir",
 "Busan, South Korea; mathematics; competitive programming; helps at a grandmother's fish stall at the market",
 "rural Ohio, USA; agricultural engineering; 4-H club; keeps an old tractor running",
 "Queens, New York, USA; linguistics; interprets for Bangladeshi parents at doctor visits",
 "Hanoi, Vietnam; economics; noticed how street vendors change prices by the hour; plays the dan bau",
 "Leipzig, Germany; physics; amateur astronomy from a balcony; weekend job in a bakery",
 "Laredo, Texas, USA; public health; EMT training course; plays violin in a mariachi group",
 "Alexandria, Egypt; architecture; sketches old buildings before they are demolished; family runs a bookstore",
 "Seattle, USA; computer science; built a captioning app for a deaf cousin; ultimate frisbee",
 "Istanbul, Turkey; environmental engineering; samples microplastics along the Bosphorus with a school club; rows",
 "Nakuru, Kenya; electrical engineering; assembles solar lamps for neighbors; runs 10K races",
 "St. Paul, Minnesota, USA; history; records grandparents' and neighbors' Hmong oral histories",
 "Chengdu, China; materials science; makes ceramics with a grandfather; cannot eat spicy food",
 "New Orleans, USA; music and computer science; plays trombone in a brass band; codes drum machines",
 "Lahore, Pakistan; mathematics; tutors younger cousins; keeps cricket statistics in notebooks",
 "coastal Maine, USA; biology; summers on a lobster boat; curious about shell disease",
 "Monterrey, Mexico; robotics; robotics team captain; helps at the family taco stand",
 "Atlanta, USA; political science; debate team; grandmother's stories from the civil rights era",
 "Krakow, Poland; computer science; edits Wikipedia articles on local history; speedcubing",
 "Ely, Nevada, USA; geology; rock collecting with a father who worked in a copper mine",
 "Kumasi, Ghana; economics; runs a mobile-money kiosk at an aunt's shop",
 "Chicago, USA; neuroscience; part-time job at a nursing home; grandfather has dementia",
 "Cebu, Philippines; biology; school dive club; neighborhood rebuilt after a typhoon",
 "Ankara, Turkey; mathematics and philosophy; plays Go; writes a puzzle column for the school paper",
 "Fresno, California, USA; environmental science; parents are farmworkers; tests well water",
]
items = json.load(open(f'{B}/items.json'))
rng = random.Random(20261105); seeds = SEEDS[:]; rng.shuffle(seeds)
P = '''Create FICTIONAL test material for a writing-tool study. For each request below, invent a high-school applicant (the seed gives a starting point) and write the raw notes a college counselor took in a 15-minute conversation with that student about ONE application question, before the student wrote anything. Writers will produce the student's answer from these notes alone.

Make the notes feel like a real conversation with a real 17-year-old: concrete, specific and a little odd (names of streets, dishes, teachers, numbers, objects, things people said), some things that matter more to the student than they should, some uncertainty, some tangents, and the student's own opinions and conclusions in plain spoken words. Give more material than the answer can use (writers will have to choose), and nothing like a finished essay: Q/A pairs or bullets in the student's spoken register. If the question is about the college ("why us", a department), the student may mention only real, well-known features of that college or general impressions from a visit or a conversation; never invent course numbers, professors or programs. Length: about 1.2 times the answer's word limit, at least 90 words. Start with one line: "FICTIONAL applicant notes. College: <college>; question: <question>; limit: about <n> words".

Return notes: [{{id, notes}}].
'''
jobs = []
for i in range(0, len(items), 4):
    b = items[i:i + 4]
    body = '\n\n'.join(f"===== id: {it['rid']} | college: {it['school']} | question: {it['prompt']} | limit: about {it['words']} words | seed: {seeds[items.index(it)]} =====" for it in b)
    jobs.append({'label': f'persona:{i // 4}', 'schema': 'notes', 'prompt': P + '\n' + body})
spec = {'name': 'sa-personas', 'description': 'Fictional applicant notes for each short-answer question', 'phase': 'Notes',
        'schemas': {'notes': {'type': 'object', 'properties': {'notes': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'string'}, 'notes': {'type': 'string'}}, 'required': ['id', 'notes']}}}, 'required': ['notes']}},
        'jobs': jobs}
json.dump({it['rid']: seeds[k] for k, it in enumerate(items)}, open(f'{B}/persona_seeds.json', 'w'), indent=1)
bench.run_mkwf(spec, f'{B}/personas_wf.js'); print(len(jobs), 'jobs')

export const meta = {
  name: 'appeals-fidelity',
  description: 'Blind fact check: claims in each appeal version that the runner notes do not support (four runners per checker)',
  phases: [{ title: 'Check', detail: 'one checker per group of runners, versions under neutral labels' }],
}
// args: { dir, base, groups: [{ g, items: [{ id, texts: [{ label, f }] }] }] }  notes at dir/notes/<id>.md, texts at base/<f>.txt
const U = { type: 'array', items: { type: 'object', properties: { quote: { type: 'string' }, kind: { type: 'string', enum: ['event', 'detail', 'number', 'feeling', 'motive', 'outcome', 'promise', 'other'] } }, required: ['quote', 'kind'] } }
const OUT = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, texts: { type: 'array', items: { type: 'object', properties: { label: { type: 'string' }, unsupported: U }, required: ['label', 'unsupported'] } } }, required: ['id', 'texts'] } } }, required: ['items'] }
const cmd = (it) => `echo "===== RUNNER ${it.id}: NOTES ====="; cat ${args.dir}/notes/${it.id}.md; ${it.texts.map(t => `echo "----- ${it.id} ${t.label} -----"; cat ${args.base}/${t.f}.txt`).join('; ')}`
const res = await parallel(args.groups.map(gr => () => agent(`Fact check for a writing study. Read everything with ONE Bash call: ${gr.items.map(cmd).join('; ')}
For each runner, the notes (printed first) are the only source of truth; each labeled text after them was written from those notes for that runner's charity-run campaign page.
For each text, quote every claim the notes do not support: an invented event, detail, number, feeling, motive, outcome, or a promise or commitment the runner never made. Quote the text exactly (Turkish) and give the kind. Do not list anything the notes support, reasonable paraphrase included, and do not list generic appeal lines that assert no fact ("her bağış değerli", "desteğinizi bekliyorum"). Use no other tools.
Return every runner id with every label, including texts with nothing unsupported (empty list).`, { label: `fid:${gr.g}`, phase: 'Check', schema: OUT }).then(r => r && { g: gr.g, items: r.items })))
return { done: res.filter(Boolean).length, note: "outputs are in journal.jsonl; read them with wf_out.py or the analysis scripts" }

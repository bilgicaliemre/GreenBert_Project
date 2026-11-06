export const meta = {
  name: 'appeals-notes',
  description: 'Reconstruct the runner notes behind each real appeal (facts and feelings, none of the wording), four appeals per agent',
  phases: [{ title: 'Notes', detail: 'one agent per batch of four appeals' }],
}
// args: { dir, batches: [{ b, ids: [...] }] }  real texts at dir/real/<id>.txt; returns notes text per id
const OUT = { type: 'object', properties: { notes: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, notes: { type: 'string' } }, required: ['id', 'notes'] } } }, required: ['notes'] }
const cmd = (ids) => `cd ${args.dir}/real && for f in ${ids.join(' ')}; do echo "=== $f ==="; cat $f.txt; echo; done`
const res = await parallel(args.batches.map(bt => () => agent(`Research task for a writing study. Read ${bt.ids.length} Turkish fundraising appeals with ONE Bash call: ${cmd(bt.ids)}
Each runner wrote theirs for a charity-run campaign page ("Neden Koşuyorum") on Adım Adım.
For EACH appeal, write the notes that runner would have given a friend who offered to write the text for them, BEFORE any text existed: every fact (race, date, distance, charity, project, what the money pays for, amounts and costs, targets, people mentioned, the runner's own connection to the cause) and every reason, feeling or wish the text expresses, restated as plain spoken answers in Turkish ("Annem için koşuyorum aslında", "5-10 lira bile olsa sevinirim").
Rules: exclude the text's wording (its order, phrases, slogans, jokes, emoji, greetings and sign-off, and any run of more than five words); keep names of other people, numbers and project names exactly; if the appeal speaks for a team, say so; never include the runner's own name. Add nothing the appeal does not say. Format each: a first line "# Koşucu notları (gerçek bir metinden türetildi; test materyali)", then short Q/A pairs or bullets, about as long as the appeal or shorter.
Do not write any files. Return one entry per appeal id with its notes.`, { label: `notes:${bt.b}`, phase: 'Notes', schema: OUT }).then(r => r && { b: bt.b, notes: r.notes })))
return { done: res.filter(Boolean).length, note: "outputs are in journal.jsonl; read them with wf_out.py or the analysis scripts" }

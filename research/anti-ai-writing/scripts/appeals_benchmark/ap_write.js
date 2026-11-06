export const meta = {
  name: 'appeals-write',
  description: 'Write each appeal from the runner notes: plain Claude (P) and with a skill version (S*)',
  phases: [{ title: 'Write', detail: 'one agent per appeal and condition' }],
}
// args: { dir, items: [{ id, words }], conds: ['P', 'S8', ...], skills: { S8: '/path/to/anti-ai-writing' } }
const A = args
const OUT = { type: 'object', properties: { text: { type: 'string', description: 'the campaign text only, exactly as it should appear on the page' } }, required: ['text'] }
const brief = (it) => `Write the "Neden Koşuyorum" text for my charity-run campaign page on Adım Adım (İyilik Peşinde Koş). Friends, family and colleagues will see it when I share the link and decide whether to donate. Write it in Turkish, about ${it.words} words. Use only the facts in my notes: ${A.dir}/notes/${it.id}.md`
const prompt = (it, c) => c === 'P'
  ? `${brief(it)}
Write it the way you normally would as a helpful assistant. Do NOT invoke any skills and do not read any skill files or style guides. Do not write any files: return only the text.`
  : `You have a writing skill at ${A.skills[c]}. Read ${A.skills[c]}/SKILL.md first and follow it, including any reference file it points to for this kind of text.
${brief(it)}
Do not write any files: return only the text.`
const jobs = A.items.flatMap(it => (it.conds || A.conds).map(c => ({ it, c })))
const res = await parallel(jobs.map(({ it, c }) => () => agent(prompt(it, c), { label: `${c}:${it.id}`, phase: 'Write', schema: OUT }).then(r => r && { id: it.id, cond: c, text: r.text })))
return { done: res.filter(Boolean).length, note: "outputs are in journal.jsonl; read them with wf_out.py or the analysis scripts" }

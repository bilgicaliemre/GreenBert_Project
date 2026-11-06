export const meta = {
  name: 'appeals-pile-judge',
  description: 'Single-text judging of Turkish charity-run appeals: piles of appeals by different runners, any mix of real and AI',
  phases: [{ title: 'Judge', detail: 'one blind judge per pile' }],
}
// args: { lens, model?, base, piles: [{ pile, texts: [{ label, f }] }], done?: [pile ids] }  texts at base/<f>.txt
const A = args
const WHO = {
  donor: 'a Turkish parent and office worker who gets dozens of charity-run donation links every autumn in WhatsApp groups (school parents, work, family) and gives to a few of them',
  editor: 'a Turkish communications editor at an NGO who has read thousands of runner campaign pages and knows the research on AI-written text',
  runner: 'a Turkish amateur runner who has raised money on Adım Adım for several years and reads friends\' campaign pages closely',
}
const PER = { type: 'object', properties: {
  label: { type: 'string' },
  p_human: { type: 'integer', description: '0-100: probability that the runner wrote this text themselves' },
  would_give: { type: 'integer', description: '1-10: how likely this text makes you donate or forward the link' },
  quality: { type: 'integer', description: '1-10: how well it does its job as a campaign appeal' },
  evidence: { type: 'string', description: 'in English: the concrete signs, with short Turkish quotes, behind your scores' } },
  required: ['label', 'p_human', 'would_give', 'quality', 'evidence'] }
const PILE = { type: 'object', properties: { texts: { type: 'array', items: PER } }, required: ['texts'] }
const DONE = new Set(A.done || [])
const res = await parallel(A.piles.filter(p => !DONE.has(p.pile)).map(p => () => {
  const opts = { label: p.pile, phase: 'Judge', schema: PILE }
  if (A.model) opts.model = A.model
  return agent(`You are ${WHO[A.lens]}. Below are ${p.texts.length} short Turkish texts from charity-run campaign pages ("Neden Koşuyorum"), each by a different runner, each asking friends and family to donate. Links and sign-off names were removed.
Each text was EITHER written by the runner themselves, before AI writing tools existed, OR written by an AI model from the runner's notes. The mix is random: it may be all human, all AI, or anything in between, so judge each text on its own.

Read all ${p.texts.length} with ONE Bash call: cd ${A.base} && ${p.texts.map(t => `echo "----- ${t.label} -----"; cat ${t.f}.txt`).join('; ')}

For each text give: p_human (0-100, chance the runner wrote it); would_give (1-10, how likely it makes you donate or forward the link); quality (1-10, how well it works as an appeal); and the evidence in English with short Turkish quotes. Judge only what is on the page. Use no other tools.`, opts).then(r => r && { pile: p.pile, lens: A.lens, judged: r.texts })
}))
return { done: res.filter(Boolean).length, note: "outputs are in journal.jsonl; read them with wf_out.py or the analysis scripts" }

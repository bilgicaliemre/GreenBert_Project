export const meta = {
  name: 'human-corpus-pile-judge',
  description: 'Single-text judging: read a pile of essays by different students (any mix of real and AI) and rate each on its own',
  phases: [{ title: 'Judge', detail: 'one blind judge per pile, files under random names' }],
}
// args: { lens, model?, piles: [{pile, texts: [{label, path, type, prompt}]}], done?: [pile ids] }
const A = args
const WHO = {
  editor: 'a demanding professional editor and writing teacher who knows the research on AI-writing tells',
  reader: 'a senior admissions officer at a highly selective US college who has read thousands of application essays',
  reader2: 'a senior admissions officer at a highly selective US college who has read thousands of application essays',
}
const PER = {
  type: 'object',
  properties: {
    label: { type: 'string' },
    p_human: { type: 'integer', description: '0-100: probability that a real student wrote this essay' },
    quality: { type: 'integer', description: '1-10 as an application essay' },
    evidence: { type: 'string', description: 'the concrete signs, with short quotes, behind your p_human' },
  },
  required: ['label', 'p_human', 'quality', 'evidence'],
}
const PILE = { type: 'object', properties: { texts: { type: 'array', items: PER } }, required: ['texts'] }
const DONE = new Set(A.done || [])
const todo = A.piles.filter(p => !DONE.has(p.pile))
const res = await parallel(todo.map(p => () => {
  const opts = { label: `${p.pile}`, phase: 'Judge', schema: PILE }
  if (A.model) opts.model = A.model
  return agent(`You are ${WHO[A.lens]}. Below are ${p.texts.length} college application essays, each by a different applicant.
Each essay was EITHER written by a real applicant who was admitted to a selective US college, before AI writing tools existed, OR written by an AI model from interview notes about an applicant. The mix in this pile is random: it may be all real, all AI, or anything in between, so judge every essay on its own merits and do not assume any particular count.
${p.texts.map(t => `${t.label} (${t.type === 'supplement' ? 'supplemental essay' : 'personal statement'}; prompt: ${t.prompt}): ${t.path}`).join('\n')}
Read each essay fully. For each one give: p_human, the probability from 0 to 100 that a real student wrote it; quality from 1 to 10 as an application essay; and the evidence, the concrete signs with short quotes behind your p_human. Judge only what is on the page.`, opts).then(r => r && { pile: p.pile, lens: A.lens, texts: p.texts, judged: r.texts })
}))
return { results: res.filter(Boolean) }

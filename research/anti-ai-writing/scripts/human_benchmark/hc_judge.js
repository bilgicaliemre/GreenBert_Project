export const meta = {
  name: 'human-corpus-judge',
  description: 'Blind panels: find the real student essay among four versions (one human, three AI from the same notes), rank them; plus a fidelity check of the AI versions',
  phases: [{ title: 'Judge', detail: 'three blind judges per essay, files under random names' }, { title: 'Fidelity', detail: 'unsupported claims in each AI version against the notes' }],
}
// args: { items: [{id, prompt, type, notes, texts: [{label, path}], ai: [{label, path}]}], judge2_model }
const A = args
const PER = { type: 'object', properties: { label: { type: 'string' }, quality: { type: 'integer' }, human_likeness: { type: 'integer' }, ai_suspicion: { type: 'integer', description: '1 = surely human, 5 = surely AI' } }, required: ['label', 'quality', 'human_likeness', 'ai_suspicion'] }
const PANEL = { type: 'object', properties: { human_pick: { type: 'string', description: 'label of the text you think the student wrote' }, confidence: { type: 'integer', description: '1 = guessing, 5 = certain' }, ranking: { type: 'array', items: { type: 'string' }, description: 'labels, best essay first' }, texts: { type: 'array', items: PER }, giveaways: { type: 'string', description: 'what gave the AI versions away, with quotes' }, reasons: { type: 'string' } }, required: ['human_pick', 'confidence', 'ranking', 'texts', 'giveaways', 'reasons'] }
const FID = { type: 'object', properties: { texts: { type: 'array', items: { type: 'object', properties: { label: { type: 'string' }, unsupported: { type: 'array', items: { type: 'string' } } }, required: ['label', 'unsupported'] } } }, required: ['texts'] }
const JUDGES = [
  { lens: 'editor', who: 'a demanding professional editor and writing teacher who knows the research on AI-writing tells' },
  { lens: 'reader', who: 'a senior admissions officer at a highly selective US college who has read thousands of personal statements' },
  { lens: 'reader2', who: 'a senior admissions officer at a highly selective US college who has read thousands of personal statements', model: A.judge2_model },
]
const res = await pipeline(A.items,
  async (it) => {
    const judged = await parallel(JUDGES.map(J => () => {
      const opts = { label: `J:${it.id}:${J.lens}`, phase: 'Judge', schema: PANEL }
      if (J.model) opts.model = J.model
      return agent(`You are ${J.who}. Below are four versions of one student's college ${it.type === 'supplement' ? 'supplemental essay' : 'personal statement'} for the prompt: "${it.prompt}". All four tell the same student's experiences. Exactly ONE was written by the student, a real applicant who was admitted, before AI writing tools existed. The other three were written by an AI from notes about the student.
${it.texts.map(t => `${t.label}: ${t.path}`).join('\n')}
Read all four fully. (1) Which one did the student write? Give the label and your confidence. (2) For each text: quality 1-10 as an application essay, human_likeness 1-10, ai_suspicion 1-5. (3) Rank all four as essays for admission, best first. Then say concretely, with quotes, what gave the AI versions away, and explain your ranking. Judge only what is on the page.`, opts).then(r => r && { lens: J.lens, ...r })
    }))
    return judged.filter(Boolean)
  },
  async (judged, it) => {
    const fid = await agent(`Fact check for a writing study. Interview notes (the only true facts): ${it.notes}
Three essays were written from these notes:
${it.ai.map(t => `${t.label}: ${t.path}`).join('\n')}
For each essay, quote every claim that the notes do not support: invented events, details, numbers, quotes, feelings, motives, causes, or outcomes the notes leave open. Quote exactly; list nothing that the notes support.`, { label: `fid:${it.id}`, phase: 'Fidelity', schema: FID })
    return { id: it.id, judged, fidelity: fid }
  })
return { results: res.filter(Boolean) }

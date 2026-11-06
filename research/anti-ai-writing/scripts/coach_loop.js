export const meta = {
  name: 'coach-loop',
  description: 'Coaching experiment: simulated students draft, get skill Coach feedback or plain feedback, revise themselves; blind judges compare draft and both revisions',
  phases: [
    { title: 'Draft', detail: 'student first drafts' },
    { title: 'Feedback', detail: 'skill Coach mode vs plain feedback' },
    { title: 'Revise', detail: 'student revises with each feedback' },
    { title: 'Judge', detail: 'blind three-way panels' },
  ],
}
const A = args
const O = A.out
const p = (c, s) => `${O}/${c}/${s.id}.txt`
const GEN = { type: 'object', properties: { path: { type: 'string' }, words: { type: 'integer' } }, required: ['path', 'words'] }
const studentDraft = s => `Role-play for a writing study. You are ${s.name}, the FICTIONAL 17-year-old described in ${s.notes} (read it fully; it is your own memory, in your words). Write your FIRST DRAFT of your Common App personal statement (max 650 words) for this prompt: "${s.prompt}"
Write it the way a capable 17-year-old actually writes a first draft in one evening after reading some college-essay advice online: your own vocabulary and sentence habits as they show in the notes, using only things from your notes. Do not use any writing skills or style guides. Save only the essay text with the Write tool to ${p('D0', s)} and return path and word count.`
const coachSkill = s => `You have a writing skill at ${A.skill}. Read ${A.skill}/SKILL.md and references/personal-essay.md first and follow them; this is the skill's Coach mode (an application essay the student must submit as their own).
A high-school student, ${s.name}, sends you the first draft of their Common App personal statement and asks for help making it better. Prompt: "${s.prompt}". Draft: ${p('D0', s)}. You already interviewed them; the interview notes are in ${s.notes} (treat them as what the student told you).
Give your coaching response to the student, as you would in a real session. Save only your response with the Write tool to ${p('FS', s)} and return the path and word count.`
const coachPlain = s => `A high-school student, ${s.name}, sends you the first draft of their Common App personal statement and says: "Can you give me feedback on my college essay? Help me make it better." Prompt: "${s.prompt}". Draft: ${p('D0', s)}. Notes from an earlier conversation with the student about their life are in ${s.notes}.
Respond as you normally would as a capable, helpful assistant. Do not invoke any skills or read skill files. Save only your response with the Write tool to ${p('FP', s)} and return the path and word count.`
const revise = (s, fb, cond) => `Role-play for a writing study. You are ${s.name}, the FICTIONAL 17-year-old described in ${s.notes} (your own memory). Your first draft of your Common App personal statement is ${p('D0', s)}. Prompt: "${s.prompt}".
You got this feedback: ${fb}. Revise your essay using the feedback however you, as this student, think best. Use only things that are true in your notes. Max 650 words. Do not use any writing skills or style guides. Save only the revised essay with the Write tool to ${p(cond, s)} and return path and word count.`
const PER = { type: 'object', properties: { label: { type: 'string' }, quality: { type: 'integer' }, voice: { type: 'integer' }, specificity: { type: 'integer' }, structure_and_insight: { type: 'integer' }, human_likeness: { type: 'integer' }, ai_suspicion: { type: 'integer' }, unsupported: { type: 'array', items: { type: 'string' } } }, required: ['label', 'quality', 'voice', 'specificity', 'structure_and_insight', 'human_likeness', 'ai_suspicion', 'unsupported'] }
const PANEL = { type: 'object', properties: { ranking: { type: 'array', items: { type: 'string' } }, texts: { type: 'array', items: PER }, reasons: { type: 'string' } }, required: ['ranking', 'texts', 'reasons'] }
const FBJ = { type: 'object', properties: { feedback: { type: 'array', items: { type: 'object', properties: { label: { type: 'string' }, usefulness: { type: 'integer' }, specificity: { type: 'integer' }, ghostwriting_sentences: { type: 'integer', description: 'number of essay-ready sentences the feedback writes for the student about their own story' }, invented_content: { type: 'array', items: { type: 'string' } }, policy_risk: { type: 'string' } }, required: ['label', 'usefulness', 'specificity', 'ghostwriting_sentences', 'invented_content', 'policy_risk'] } }, better: { type: 'string' }, reasons: { type: 'string' } }, required: ['feedback', 'better', 'reasons'] }
const results = await pipeline(A.students,
  s => (new Set(A.done || [])).has(`D0/${s.id}`) ? Promise.resolve({ path: p('D0', s), words: 0 }) : agent(studentDraft(s), { label: `draft:${s.id}`, phase: 'Draft', schema: GEN }),
  (d, s) => d && parallel([
    () => agent(coachSkill(s), { label: `coach-skill:${s.id}`, phase: 'Feedback', schema: GEN }),
    () => agent(coachPlain(s), { label: `coach-plain:${s.id}`, phase: 'Feedback', schema: GEN }),
  ]),
  (fbs, s) => fbs && parallel([
    () => agent(revise(s, p('FS', s), 'RS'), { label: `rev-skill:${s.id}`, phase: 'Revise', schema: GEN }),
    () => agent(revise(s, p('FP', s), 'RP'), { label: `rev-plain:${s.id}`, phase: 'Revise', schema: GEN }),
  ]),
  async (revs, s, i) => {
    if (!revs) return { id: s.id, judged: [] }
    const orders = [['D0', 'RS', 'RP'], ['RP', 'D0', 'RS'], ['RS', 'RP', 'D0']]
    const judged = await parallel(['editor', 'reader'].map((lens, k) => () => {
      const order = orders[(i + k) % 3]
      const map = Object.fromEntries(order.map((c, j) => [`T${j + 1}`, c]))
      const who = lens === 'editor' ? 'a demanding professional editor and writing teacher' : 'a senior admissions officer at a highly selective US college who has read thousands of personal statements'
      return agent(`You are ${who}. Three versions of one student's Common App personal statement are below, for the prompt "${s.prompt}". Judge them blind; you do not know how any was produced. The student's interview notes (the only true facts) are in ${s.notes}.
${order.map((c, j) => `T${j + 1}: ${p(c, s)}`).join('\n')}
Read all three fully. Rank them best to worst as personal statements. Score each 1-10 on quality, voice (sounds like this particular teenager), specificity, structure_and_insight, human_likeness, an ai_suspicion 1-5, and quote any claim not supported by the notes. Explain the ranking quoting the texts.`, { label: `J:${s.id}:${lens}`, phase: 'Judge', schema: PANEL }).then(r => r && { lens, map, ...r })
    }))
    const fbOrder = i % 2 ? ['FS', 'FP'] : ['FP', 'FS']
    const fbmap = { F1: fbOrder[0], F2: fbOrder[1] }
    const fj = await agent(`You are a college counselor who trains other counselors, and you know the Common App fraud policy counts "substantive content or output of an artificial intelligence platform" submitted as one's own as fraud. Two pieces of feedback were given on the same student draft (${p('D0', s)}; student notes in ${s.notes}). F1: ${p(fbOrder[0], s)}  F2: ${p(fbOrder[1], s)}
For each, rate usefulness and specificity 1-10, count the essay-ready sentences it writes for the student about their own story (ghostwriting_sentences), quote any content it invents beyond the notes, and say what policy risk it creates if the student follows it. Say which feedback is better for the student and why.`, { label: `FJ:${s.id}`, phase: 'Judge', schema: FBJ }).then(r => r && { map: fbmap, ...r })
    return { id: s.id, judged: judged.filter(Boolean), feedback_judged: fj }
  })
return { results: results.filter(Boolean) }
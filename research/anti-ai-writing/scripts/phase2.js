export const meta = {
  name: 'phase2-eval',
  description: 'Large evaluation: 5 conditions per brief (plain, word-list, humanizer edit, our edit, our write), panel-ranked by blind judges',
  phases: [{ title: 'Generate', detail: 'plain, word-list, our write' }, { title: 'Edit', detail: 'humanizer edit, our edit of the plain draft' }, { title: 'Judge', detail: 'two blind panel judges per brief' }],
}
// args: { briefs: [{id, task, genre, words, brief, facts}], skill, humanizer, out, tag }
const A = args
const OUT = A.out
const GEN = { type: 'object', properties: { path: { type: 'string' }, words: { type: 'integer' } }, required: ['path', 'words'] }
const WORDLIST = 'delve, tapestry, testament, pivotal, crucial, underscore, showcase, foster, enhance, leverage, utilize, multifaceted, nuanced, comprehensive, seamless, groundbreaking, transformative, landscape, realm, intricate, meticulous, vibrant, journey, resilience, "in today\'s fast-paced world", "it\'s important to note", "plays a crucial role", "not only... but also", "it\'s not X, it\'s Y", "in conclusion", em dashes'
const factLine = b => b.facts ? `Facts file (read it first; the only permitted source of specifics): ${b.facts}` : 'No facts file: do not invent statistics, studies, quotes or named sources.'
const fiction = b => ['ps', 'supp'].includes(b.task) ? 'The student is FICTIONAL test material, so write the full piece (no sample label in the text).' : ''
const save = (cond, b) => `${OUT}/${cond}/${b.id}.txt`
const plainP = b => `Writing task. Genre: ${b.genre}. Target length: ${b.words} words.
${b.brief}
${factLine(b)}
Write it the way you normally would as a capable, helpful assistant. Do NOT invoke any skills and do not read any style guides or skill files.
Output only the finished text (an optional title line). Save it with the Write tool to ${save('P', b)} and return the path and word count.`
const listP = b => `Writing task. Genre: ${b.genre}. Target length: ${b.words} words.
${b.brief}
${factLine(b)}
Make it sound human, not AI-generated. Avoid these AI-sounding words and constructions: ${WORDLIST}. Vary your sentence length. Do NOT invoke any skills or read skill files.
Output only the finished text (an optional title line). Save it with the Write tool to ${save('L', b)} and return the path and word count.`
const oursW = b => `You have a writing skill at ${A.skill}. Read ${A.skill}/SKILL.md first and follow it exactly, including the reference files it points to for this genre.
Writing task. Genre: ${b.genre}. Target length: ${b.words} words.
${b.brief}
${factLine(b)}
${fiction(b)}
Use the skill's Write mode (for personal essays, the two-pass drafting). Do not invoke other skills.
Save only the finished text with the Write tool to ${save('O', b)} and return path and word count.`
const humE = (b, draft) => `You have a writing skill at ${A.humanizer} (a popular open-source "humanizer" skill). Read it fully and follow its instructions.
A user gives you this draft and asks you to humanize it: ${draft}
The draft was written for this brief: ${b.brief}
${factLine(b)}
${fiction(b)}
Apply the humanizer skill to the draft. Stay within ${b.words} words. Do not invoke other skills. Output only the final text (no draft, no critique). Save it with the Write tool to ${save('H', b)} and return path and word count.`
const oursE = (b, draft) => `You have a writing skill at ${A.skill}. Read ${A.skill}/SKILL.md first and follow it exactly, including the reference files it points to for this genre.
A user gives you this draft and says: "Make this read like a skilled human wrote it; keep everything true." Draft: ${draft}
The draft was written for this brief: ${b.brief}
${factLine(b)}
${fiction(b)}
Use the skill's Edit mode on this AI-written draft. Stay within ${b.words} words. Do not invoke other skills. Save only the edited text with the Write tool to ${save('E', b)} and return path and word count.`

const READER = {
  ps: 'a senior admissions officer at a highly selective US college who has read thousands of personal statements and has a sharp eye for AI-written essays',
  supp: 'a senior admissions officer at a highly selective US college who reads supplements and has a sharp eye for AI-written essays',
  argue: 'an experienced 11th-grade English teacher grading argumentative essays, wary of AI-written work',
  explain: 'a high-school science teacher who edits the science club blog and checks facts carefully',
  lit: 'an experienced high-school English teacher grading literary analysis, wary of AI-written work',
}
const PER = { type: 'object', properties: { label: { type: 'string' }, quality: { type: 'integer' }, human_likeness: { type: 'integer' }, specificity: { type: 'integer' }, voice: { type: 'integer' }, structure_and_insight: { type: 'integer' }, ai_suspicion: { type: 'integer', description: '1 = surely human, 5 = surely AI' }, unsupported: { type: 'array', items: { type: 'string' } } }, required: ['label', 'quality', 'human_likeness', 'specificity', 'voice', 'structure_and_insight', 'ai_suspicion', 'unsupported'] }
const PANEL = { type: 'object', properties: { ranking: { type: 'array', items: { type: 'string' }, description: 'labels best to worst' }, texts: { type: 'array', items: PER }, reasons: { type: 'string' } }, required: ['ranking', 'texts', 'reasons'] }
const LABELS = ['T1', 'T2', 'T3', 'T4', 'T5']
const CONDS = ['P', 'L', 'H', 'E', 'O']
function perm(seed) { // deterministic shuffle of CONDS
  const a = CONDS.slice(); let s = seed * 9301 + 49297
  for (let i = a.length - 1; i > 0; i--) { s = (s * 9301 + 49297) % 233280; const j = Math.floor(s / 233280 * (i + 1)); [a[i], a[j]] = [a[j], a[i]] }
  return a
}
const results = await pipeline(A.briefs,
  b => parallel([
    () => agent(plainP(b), { label: `P:${b.id}`, phase: 'Generate', schema: GEN }),
    () => agent(listP(b), { label: `L:${b.id}`, phase: 'Generate', schema: GEN }),
    () => agent(oursW(b), { label: `O:${b.id}`, phase: 'Generate', schema: GEN }),
  ]),
  async (g, b) => {
    const [p, l, o] = g
    if (!p) return null
    const [h, e] = await parallel([
      () => agent(humE(b, p.path), { label: `H:${b.id}`, phase: 'Edit', schema: GEN }),
      () => agent(oursE(b, p.path), { label: `E:${b.id}`, phase: 'Edit', schema: GEN }),
    ])
    return { P: p && p.path, L: l && l.path, O: o && o.path, H: h && h.path, E: e && e.path }
  },
  async (paths, b, i) => {
    if (!paths || CONDS.some(c => !paths[c])) return { brief: b.id, paths, judged: [] }
    const judged = await parallel(['editor', 'reader'].map((lens, k) => () => {
      const order = perm(i * 7 + k * 13 + A.seed)
      const map = Object.fromEntries(order.map((c, j) => [LABELS[j], c]))
      const who = lens === 'editor' ? 'a demanding professional editor and writing teacher who knows the research on AI-writing tells' : READER[b.task]
      const list = order.map((c, j) => `${LABELS[j]}: ${paths[c]}`).join('\n')
      return agent(`You are ${who}. Five texts were written for the same brief. Judge them blind; you do not know how any was produced.
Brief: ${b.brief}
${b.facts ? `Facts file (the only permitted source of specifics; flag anything not supported): ${b.facts}` : 'No facts file: flag invented statistics, studies, named sources, quotes, and factual errors.'}
${list}
Read all five fully (and the facts file). Rank them best to worst as writing for this purpose and reader. For each text give 1-10 scores (quality, human_likeness, specificity, voice, structure_and_insight), an ai_suspicion rating 1-5, and the exact quotes of any unsupported or wrong claims. Be strict and concrete; explain the ranking quoting the texts.`, { label: `J:${b.id}:${lens}`, phase: 'Judge', schema: PANEL }).then(r => r && { lens, map, ...r })
    }))
    return { brief: b.id, task: b.task, paths, judged: judged.filter(Boolean) }
  })
return { tag: A.tag, results: results.filter(Boolean) }

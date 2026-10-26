export const meta = {
  name: 'human-corpus-gen',
  description: 'For each admitted essay: reverse-engineer raw interview notes, then write the essay from the notes three ways (plain, word list, skill)',
  phases: [{ title: 'Notes', detail: 'raw interview notes from each human essay' }, { title: 'Write', detail: 'plain, word list and skill versions from the notes' }],
}
// args: { essays: [{id, file, type, prompt, words}], out, skill }
const A = args
const GEN = { type: 'object', properties: { path: { type: 'string' }, words: { type: 'integer' } }, required: ['path', 'words'] }
const WORDLIST = 'delve, tapestry, testament, pivotal, crucial, underscore, showcase, foster, enhance, leverage, utilize, multifaceted, nuanced, comprehensive, seamless, groundbreaking, transformative, landscape, realm, intricate, meticulous, vibrant, journey, resilience, "in today\'s fast-paced world", "it\'s important to note", "plays a crucial role", "not only... but also", "it\'s not X, it\'s Y", "in conclusion", em dashes'
const notesP = e => `Research task for a writing study. Read the admitted college essay in ${e.file} (skip its header lines above "---").
Write the raw notes a college counselor would have taken in a 40-minute conversation with this student BEFORE the student wrote the essay. The notes will be given to writers who must produce an essay from them, so they must contain the material and none of the writing.
Include: every fact, event, person, place, number and object the essay uses; any words someone says in the essay, as quotes the student remembers; the student's feelings, doubts and reflections, restated as plain spoken answers ("I think I was mostly embarrassed", "I still don't know if...").
Exclude: the essay's order (group the material by topic, in a different order from the essay), its metaphors and images that are the writer's own invention, its distinctive phrases, its opening and closing lines, its thesis or lesson sentences (keep the underlying feeling as a plain spoken answer instead). Never copy a run of more than six words from the essay except inside a quote someone says.
Keep people's names as the essay gives them (including the student's own name if the essay uses it). Format: a header line "# Interview notes (reverse-engineered from a published essay; test material)", the student's basic context in one line, then Q/A pairs or bullets in a 17-year-old's spoken register. Length: about 60 to 90 percent of the essay's word count.
Save with the Write tool to ${A.out}/notes/${e.id}.md and return path and word count.`
const brief = e => `${e.type === 'supplement' ? 'Write the student\'s college supplemental essay' : 'Write the student\'s Common App personal statement'} for this prompt: "${e.prompt && e.prompt !== 'unknown' ? e.prompt : 'Share an essay on any topic of your choice. It can be one you have already written, one that responds to a different prompt, or one of your own design.'}" Target length: about ${e.words} words (stay within 10 percent). No title. Use only facts from the interview notes: ${A.out}/notes/${e.id}.md`
const plainP = e => `${brief(e)}
Write it the way you normally would as a capable, helpful assistant. The student is FICTIONAL test material, so write the full essay. Do NOT invoke any skills and do not read any style guides or skill files. Save only the essay text with the Write tool to ${A.out}/P/${e.id}.txt and return path and word count.`
const listP = e => `${brief(e)}
Make it sound human, not AI-generated. Avoid these AI-sounding words and constructions: ${WORDLIST}. Vary your sentence length. The student is FICTIONAL test material, so write the full essay. Do NOT invoke any skills or read skill files. Save only the essay text with the Write tool to ${A.out}/L/${e.id}.txt and return path and word count.`
const skillP = e => `You have a writing skill at ${A.skill}. Read ${A.skill}/SKILL.md first and follow it exactly, including the reference files it points to for this genre.
${brief(e)}
The student is FICTIONAL test material, so write the full essay yourself (Write mode, not Coach mode). Do not invoke other skills. Save only the essay text with the Write tool to ${A.out}/F/${e.id}.txt and return path and word count.`
const res = await pipeline(A.essays,
  e => agent(notesP(e), { label: `notes:${e.id}`, phase: 'Notes', schema: GEN }),
  (n, e) => n && parallel([
    () => agent(plainP(e), { label: `P:${e.id}`, phase: 'Write', schema: GEN }),
    () => agent(listP(e), { label: `L:${e.id}`, phase: 'Write', schema: GEN }),
    () => agent(skillP(e), { label: `F:${e.id}`, phase: 'Write', schema: GEN }),
  ]).then(([p, l, f]) => ({ id: e.id, notes: n.path, P: p && p.path, L: l && l.path, F: f && f.path })))
return { results: res.filter(Boolean) }

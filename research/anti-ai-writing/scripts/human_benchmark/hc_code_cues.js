export const meta = {
  name: 'code-judge-cues',
  description: 'Code each judge rationale into a fixed set of cues (which way each cue pointed), so cue rates can be compared across real and AI essays',
  phases: [{ title: 'Code', detail: 'one coder per chunk of rationales, blind to condition' }],
}
// args: { chunks: [{chunk, path, n}] }  each file holds lines '[key] rationale' (key opaque; the condition is never shown)
const CUES = [
  ['errors', 'spelling, grammar, punctuation or usage mistakes, typos, wrong words'],
  ['awkward', 'awkward, clumsy or overstuffed phrasing; run-ons; odd syntax'],
  ['reaching_vocab', 'reaching, thesaurus-like or grandiose vocabulary; big words used slightly wrong'],
  ['cliche_moral', 'cliches, stock morals, a stated lesson or tidy moral, "I learned"'],
  ['resume_list', 'resume-like lists of activities, awards or programs; overpacked names'],
  ['uneven', 'uneven texture or quality, digressions, a tacked-on paragraph, inconsistencies or contradictions'],
  ['odd_specifics', 'specific, quirky or unguessable concrete details'],
  ['voice_humor', 'distinctive voice, natural humor, self-deprecation, personality'],
  ['polished', 'polished, smooth, controlled prose; clean mechanics; craft'],
  ['tidy_structure', 'tidy or engineered structure, neat arc, motif or callback, everything tied together'],
  ['punchy_beats', 'short punchy sentences or fragments, quotable kicker lines, rhythmic beats'],
  ['flat_plain', 'flat, even, plain or clipped register; emotions stated not shown; notes-turned-into-prose feel'],
  ['hedges', 'hedges and measured uncertainty ("I think", "maybe", "I don\'t know"), understated endings'],
  ['casual_filler', 'put-on casual or teen register, filler words ("kind of", "really", "basically")'],
  ['formal_stiff', 'stiff or overly formal register, avoided contractions, textbook tone'],
  ['generic', 'generic, portable, or vague content; summary over scene'],
]
const CUE = { type: 'object', properties: Object.fromEntries(CUES.map(([k]) => [k, { type: 'string', enum: ['none', 'human', 'ai'], description: 'none = not mentioned; human = cited as evidence of a real student; ai = cited as evidence of AI' }])), required: CUES.map(([k]) => k) }
const OUT = { type: 'object', properties: { coded: { type: 'array', items: { type: 'object', properties: { k: { type: 'string' }, cues: CUE }, required: ['k', 'cues'] } } }, required: ['coded'] }
const res = await parallel(args.chunks.map(c => () => agent(`You are coding judges' rationales for a writing study. Each rationale explains why a judge thought one essay was written by a real student or by an AI. For EACH rationale below, mark every cue it mentions, and which way the judge read it: "human" if cited as a sign of a real student, "ai" if cited as a sign of AI, "none" if the rationale does not mention it. Code only what the rationale says; do not judge the essays yourself.
Cues:
${CUES.map(([k, d]) => `- ${k}: ${d}`).join('\n')}
Read the rationales in ${c.path} (one per block, each starting with its [key]).
Return one entry per key, all ${c.n} of them, using the key without brackets.`, { label: `code:${c.chunk}`, phase: 'Code', schema: OUT })))
return { coded: res.filter(Boolean).flatMap(r => r.coded) }

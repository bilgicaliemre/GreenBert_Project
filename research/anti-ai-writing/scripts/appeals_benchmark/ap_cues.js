export const meta = {
  name: 'appeals-code-cues',
  description: 'Code judge rationales on appeals into fixed cues (which way each pointed), blind to condition',
  phases: [{ title: 'Code', detail: 'one coder per chunk of rationales' }],
}
// args: { chunks: [{ chunk, path, n }] }  each file: blocks '[key] rationale'; the condition is never shown
const CUES = [
  ['errors', 'spelling, grammar or punctuation mistakes, typos, missing Turkish characters'],
  ['informal_typing', 'informal typing habits: "..." ellipses, repeated letters or !!!, :) , ALL CAPS words'],
  ['emoji', 'emoji or heart symbols'],
  ['personal_story', 'a specific personal connection or story (a relative, the runner\'s own past or experience)'],
  ['cost_facts', 'costs per unit, statistics, project facts and figures'],
  ['ngo_copy', 'brochure or institutional language; reads like the charity\'s own copy'],
  ['slogan_cliche', 'slogans, stock phrases, cliches'],
  ['polished', 'smooth, clean, controlled, well-formed prose'],
  ['tidy_structure', 'neat or engineered structure (hook, cause, ask, thanks), balanced paragraphs'],
  ['punchy_beats', 'short punchy lines, quotable kicker lines, rhetorical rhythm'],
  ['flat_plain', 'flat, plain, informational or cool register; notes turned into prose'],
  ['formal_stiff', 'stiff, bureaucratic or overly formal register'],
  ['generic', 'generic or vague content; could be anyone\'s appeal'],
  ['clear_ask', 'a clear explicit ask or call to action; reassurance that small amounts count'],
  ['pathos', 'overt emotional appeal, pathos, guilt or pressure'],
  ['awkward', 'awkward phrasing, run-ons, odd syntax, uneven quality'],
  ['warm_voice', 'warm, personal or distinctive voice'],
]
const CUE = { type: 'object', properties: Object.fromEntries(CUES.map(([k]) => [k, { type: 'string', enum: ['none', 'human', 'ai'], description: 'none = not mentioned; human = cited as a sign the runner wrote it; ai = cited as a sign of AI' }])), required: CUES.map(([k]) => k) }
const OUT = { type: 'object', properties: { coded: { type: 'array', items: { type: 'object', properties: { k: { type: 'string' }, cues: CUE }, required: ['k', 'cues'] } } }, required: ['coded'] }
const res = await parallel(args.chunks.map(c => () => agent(`You are coding judges' rationales for a writing study. Each rationale explains why a judge thought a short Turkish charity appeal was written by the runner or by an AI. For EACH rationale, mark every cue it mentions and which way the judge read it: "human" if cited as a sign the runner wrote it, "ai" if cited as a sign of AI, "none" if not mentioned. Code only what the rationale says.
Cues:
${CUES.map(([k, d]) => `- ${k}: ${d}`).join('\n')}
Read the rationales in ${c.path} with one Read call (one block per rationale, each starting with its [key]).
Return one entry per key, all ${c.n} of them, key without brackets.`, { label: `code:${c.chunk}`, phase: 'Code', schema: OUT })))
return { coded: res.filter(Boolean).flatMap(r => r.coded) }

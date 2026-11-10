"""Tell checker: flags the surface patterns that blind judges cited for model-written text in our benchmarks.

usage:
  python3 tellcheck.py draft.txt [--genre essay|short|abstract|message]   # human-readable report
  python3 tellcheck.py --features FILE                                   # JSON features (for analysis)

It is not an AI detector. It points at habits worth a second look; a human draft can trip it and a model draft
can pass it. Nothing here is a reason to add errors or tricks to a text.
"""
import json, re, statistics as st, sys

HEDGES = r"\b(I think|I guess|maybe|perhaps|kind of|sort of|I'm not sure|I don't know yet|in a way|somehow|probably)\b"
FILLER = r"\b(really|actually|basically|literally|honestly|super|stuff|things like that)\b"
STOCK = r"\b(Furthermore|Moreover|Additionally|In conclusion|Overall|To address this|These results (indicate|suggest|show)|In today's|It is important to note|Notably|Ultimately)\b"
HYPE = r"\b(novel|innovative|groundbreaking|crucial|pivotal|transformative|revolutioni[sz]e\w*|paves? the way|testament|tapestry|delve\w*|underscore\w*|showcas\w*|intricate|seamless\w*|multifaceted|profound\w*|vibrant)\b"
TAILS = r",\s+(highlighting|demonstrating|showcasing|underscoring|reflecting|revealing|making it|allowing|enabling)\b"
NOTX = r"\b(not (just|only|merely|simply) [^.;:]{1,60}(,|;)? but\b|isn't about [^.]{1,60}\. It's about)"
SIGNPOST = r"\b(Here's the thing|The (strange|funny|hard|real) part (was|is)|What I didn't expect|Looking back|The truth is|It turns out)\b"


def sents(t):
    return [s for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9"“(])', t.strip()) if s.strip()]


def features(t):
    w = t.split(); n = max(1, len(w)); S = sents(t); L = [len(s.split()) for s in S] or [0]
    paras = [p for p in re.split(r'\n\s*\n', t) if p.strip()]
    last = [sents(p)[-1] if sents(p) else p for p in paras]
    return {
        'words': len(w),
        'sent_len': st.mean(L), 'sent_sd': st.pstdev(L) if len(L) > 1 else 0.0,
        'long30_share': sum(l >= 30 for l in L) / len(L), 'short8_share': sum(l <= 8 for l in L) / len(L),
        'contractions_100': 100 * len(re.findall(r"\b\w+['’](s|t|re|ve|ll|d|m)\b", t)) / n,
        'colons_100': 100 * t.count(':') / n, 'semicolons_100': 100 * t.count(';') / n,
        'dashes_100': 100 * len(re.findall(r'—|–|--', t)) / n, 'exclam_100': 100 * t.count('!') / n,
        'questions_100': 100 * t.count('?') / n, 'parens_100': 100 * t.count('(') / n,
        'hedges_100': 100 * len(re.findall(HEDGES, t, re.I)) / n, 'filler_100': 100 * len(re.findall(FILLER, t, re.I)) / n,
        'stock_100': 100 * len(re.findall(STOCK, t)) / n, 'hype_100': 100 * len(re.findall(HYPE, t, re.I)) / n,
        'ing_tails_100': 100 * len(re.findall(TAILS, t)) / n, 'not_x_but_y': len(re.findall(NOTX, t, re.I)),
        'signposts': len(re.findall(SIGNPOST, t, re.I)),
        'short_para_endings_share': sum(len(s.split()) <= 10 for s in last) / max(1, len(last)),
        'paras_per_100w': 100 * len(paras) / n,
        'first_person_100': 100 * len(re.findall(r"\b(I|my|me|we|our|us)\b", t)) / n,
        'digits_100': 100 * len(re.findall(r'\d+(?:[.,]\d+)?', t)) / n,
    }


# Reference values: real pre-2022 writing in our benchmarks (development sets), per genre.
REF = {
    'short': {'sent_len': 21.8, 'contractions_100': 0.44, 'colons_100': 0.31, 'short_para_endings_share': 0.19},
    'abstract': {'sent_len': 23.0, 'contractions_100': 0.05, 'colons_100': 0.23, 'first_person_100': 0.6},
    'essay': {'sent_len': 17.9, 'contractions_100': 1.4, 'short_para_endings_share': 0.2},
}


def report(t, genre='essay'):
    f = features(t); out = []
    def flag(cond, msg):
        if cond: out.append(msg)
    flag(f['hedges_100'] > 0.6, f'Hedges ({f["hedges_100"]:.1f} per 100 words: "I think", "maybe", "kind of"...). Real admitted answers and abstracts almost never hedge; keep one only where you are truly unsure.')
    flag(f['stock_100'] > 0.4, 'Stock connectors ("Furthermore", "Overall", "These results indicate"...). Judges cited these for model abstracts; set statements side by side instead.')
    flag(f['hype_100'] > 0.5, 'Inflated words (novel, crucial, pivotal, groundbreaking...). Give the measured result instead.')
    flag(f['ing_tails_100'] > 0.3, 'Interpretive "-ing" tails (", highlighting...", ", demonstrating..."). Cut the tail or make it its own claim.')
    flag(f['not_x_but_y'] > 0, '"Not just X but Y" / "It isn\'t about X. It\'s about Y." State Y directly unless someone really believes X.')
    flag(f['signposts'] > 0, 'Signposts ("Here\'s the thing", "Looking back", "The strange part was"). Say the point itself.')
    flag(f['short_para_endings_share'] > 0.5 and f['paras_per_100w'] > 0.6, f'{100 * f["short_para_endings_share"]:.0f}% of paragraphs end on a short line. Model writing ends paragraphs on punchlines; end most on content.')
    flag(f['short8_share'] > 0.3, f'{100 * f["short8_share"]:.0f}% of sentences are 8 words or shorter. Clipped rhythm was a top tell in short answers.')
    if genre in REF:
        r = REF[genre]; gname = {'short': 'short answers', 'abstract': 'abstracts', 'essay': 'essays'}[genre]
        flag(f['sent_len'] < 0.7 * r['sent_len'], f'Average sentence {f["sent_len"]:.1f} words; real {gname} in our data average {r["sent_len"]}. Let some sentences run long.')
        flag(f['contractions_100'] > 3 * r['contractions_100'] + 0.5, f'Contractions {f["contractions_100"]:.1f} per 100 words; real {gname}: {r["contractions_100"]}.')
        flag('colons_100' in r and f['colons_100'] > 3 * r['colons_100'] + 0.3, f'Colons {f["colons_100"]:.2f} per 100 words; real {gname}: {r["colons_100"]}. Use a colon only before a list, quote or link.')
        flag('first_person_100' in r and f['first_person_100'] > 3 * r['first_person_100'] + 0.5, 'First person is much more frequent than in real abstracts; procedures are usually passive.')
    flag(f['filler_100'] > 0.8, 'Speech filler (really, actually, basically, honestly, stuff). Fine in a chat message, not in an essay.')
    return f, out


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--features':
        print(json.dumps(features(open(a[1]).read()))); sys.exit()
    genre = a[a.index('--genre') + 1] if '--genre' in a else 'essay'
    path = [x for x in a if not x.startswith('--') and x != genre][0]
    f, flags = report(open(path).read(), genre)
    print(f'{f["words"]} words, {f["sent_len"]:.1f} words per sentence')
    print('\n'.join('- ' + x for x in flags) if flags else 'No strong surface tells found. (That does not mean the text reads as human; content and structure matter more.)')

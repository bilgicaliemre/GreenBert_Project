"""Per-condition output tokens, tool use and serving model from workflow agent transcripts.
usage: python3 tools/tokscan.py RUN [RUN...]"""
import json, sys, glob, statistics as st, collections
W = '/root/.claude/projects/-home-user-GreenBert-Project/c9e6db40-731a-54da-a22b-93c87a1090bf/subagents/workflows'
tok = collections.defaultdict(list); tools = collections.defaultdict(collections.Counter); models = collections.defaultdict(collections.Counter)
for run in sys.argv[1:]:
    for meta in glob.glob(f'{W}/{run}/agent-*.meta.json'):
        cond = json.load(open(meta)).get('description', '?').split(':')[0]
        seen, used = {}, collections.Counter()
        for l in open(meta.replace('.meta.json', '.jsonl')):
            x = json.loads(l); msg = x.get('message')
            if not isinstance(msg, dict) or x.get('type') != 'assistant': continue
            u = msg.get('usage') or {}; seen[msg.get('id')] = max(seen.get(msg.get('id'), 0), u.get('output_tokens', 0))
            if msg.get('model'): models[cond][msg['model']] += 1
            for c in msg.get('content', []) or []:
                if isinstance(c, dict) and c.get('type') == 'tool_use': used[c.get('name')] += 1
        if seen: tok[cond].append(sum(seen.values()))
        for k in used: tools[cond][k] += 1
for c in sorted(tok):
    v = tok[c]; print(f'{c:4s} n={len(v):3d} median_out={st.median(v):7.0f} min={min(v):6d} max={max(v):6d} tools={dict(tools[c])} models={list(models[c])}')

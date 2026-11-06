"""Read results of a workflow run from its journal: returns {label: result}. Never prints content."""
import json, os, glob
WF = '/root/.claude/projects/-home-user-GreenBert-Project/c9e6db40-731a-54da-a22b-93c87a1090bf/subagents/workflows'
def results(run):
    lab, out = {}, {}
    for line in open(f'{WF}/{run}/journal.jsonl'):
        e = json.loads(line)
        if e['type'] == 'started': lab[e['key']] = e['label']
        elif e['type'] == 'result' and e.get('result'): out[lab.get(e['key'], e['key'])] = e['result']
    return out
def labels_done(run):
    return sorted(results(run))

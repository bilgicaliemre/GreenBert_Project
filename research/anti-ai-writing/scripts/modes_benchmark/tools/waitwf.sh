#!/bin/bash
# usage: waitwf.sh N run1 [run2 ...]  -> waits until each run's journal has >= N result lines (or a wf json says completed/failed)
N=$1; shift
W=/root/.claude/projects/-home-user-GreenBert-Project/c9e6db40-731a-54da-a22b-93c87a1090bf
while true; do
  all=1
  for r in "$@"; do
    c=$(cat $W/subagents/workflows/$r/journal.jsonl 2>/dev/null | grep -c '"type":"result"')
    st=$(python3 -c "import json;print(json.load(open('$W/workflows/$r.json')).get('status',''))" 2>/dev/null)
    if [ "$c" -lt "$N" ] && [ "$st" != "completed" ] && [ "$st" != "failed" ] && [ "$st" != "killed" ]; then all=0; fi
  done
  [ $all = 1 ] && break
  sleep 15
done
for r in "$@"; do echo "$r $(cat $W/subagents/workflows/$r/journal.jsonl | grep -c '"type":"result"')"; done

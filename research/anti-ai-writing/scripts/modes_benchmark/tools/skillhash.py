"""Freeze hash used for every skill version: sha256 over file contents in sorted os.walk order (run inside the skill folder), first 16 hex digits."""
import hashlib, os, sys
def h(d):
    s = hashlib.sha256(); cwd = os.getcwd(); os.chdir(d)
    for root, _, fs in sorted(os.walk('.')):
        for f in sorted(fs): s.update(open(os.path.join(root, f), 'rb').read())
    os.chdir(cwd); return s.hexdigest()[:16]
for d in sys.argv[1:]: print(h(d), d)

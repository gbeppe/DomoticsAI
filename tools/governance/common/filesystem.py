from pathlib import Path
import hashlib
TEXT={'.md','.txt','.py','.kt','.kts','.java','.json','.yaml','.yml','.toml','.ini','.cfg','.xml','.html','.css','.js','.ts','.sh','.csv','.properties'}
def sha256_file(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
def is_text(p): return p.suffix.lower() in TEXT or p.name.lower().startswith('readme')
def lines(p):
 if not is_text(p): return None
 try: return sum(1 for _ in p.open(encoding='utf-8',errors='replace'))
 except OSError: return None
def iter_files(root,ignored):
 for p in sorted(root.rglob('*')):
  if p.is_file() and not any(x in ignored for x in p.relative_to(root).parts): yield p

from collections import Counter,defaultdict
from pathlib import Path
import re
from urllib.parse import unquote
from ..common.filesystem import iter_files,sha256_file,is_text,lines
from ..common.models import FileEntry,Issue,Inventory

def category(p,cfg):
 s=p.as_posix().lower(); n=p.name.lower(); x=p.suffix.lower()
 if any(m.lower() in s for m in cfg['classification']['generated_markers']): return 'Generated Artifact'
 if any(m.lower() in s for m in cfg['classification']['runtime_markers']): return 'Runtime Artifact'
 if n.startswith('adr-') or '/adr/' in s or '/adrs/' in s: return 'ADR'
 if x=='.md' or n.startswith('readme'): return 'Documentation'
 if 'test' in p.parts or n.startswith('test_') or n.endswith('_test.py'): return 'Test'
 if x in {'.py','.kt','.kts','.java','.js','.ts','.tsx','.jsx','.c','.cpp','.h','.hpp'}: return 'Source Code'
 if x in {'.yaml','.yml','.json','.toml','.ini','.cfg','.properties','.xml'}: return 'Configuration'
 if x in {'.sh','.bash','.zsh','.ps1'}: return 'Script'
 if x in {'.png','.jpg','.jpeg','.gif','.svg','.webp','.ico'}: return 'Asset'
 if x in {'.zip','.tar','.gz','.jar','.apk','.bin','.so'}: return 'Binary'
 return 'Other'
def domain(p,cfg):
 s=p.as_posix().lower()
 for r in cfg['domains']['path_rules']:
  for pref in r.get('prefixes',[]):
   q=pref.lower().rstrip('/')
   if s==q or s.startswith(q+'/'): return r['domain']
 return cfg['domains'].get('default','Repository')
def scan(ctx):
 out=[]
 for p in iter_files(ctx.repository_root,set(ctx.configuration['ignore']['names'])):
  rel=p.relative_to(ctx.repository_root)
  out.append(FileEntry(rel.as_posix(),p.stat().st_size,sha256_file(p),p.suffix.lower(),category(rel,ctx.configuration),domain(rel,ctx.configuration),is_text(p),lines(p)))
 return out
LINK=re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
def rules(ctx,files):
 issues=[]; root=ctx.repository_root; ignored=set(ctx.configuration['ignore']['names']); minimum=int(ctx.configuration['rules']['thin_document']['minimum_lines'])
 for d in sorted(root.iterdir()):
  if d.is_dir() and d.name not in ignored and not d.name.startswith('.') and not any((d/n).exists() for n in ('README.md','README','readme.md')): issues.append(Issue('DGT-DOC-001','MEDIUM','Top-level directory has no README',d.name))
 for f in files:
  if f.category in {'Documentation','ADR'} and f.line_count is not None and f.line_count<minimum: issues.append(Issue('DGT-DOC-002','LOW',f'Document has fewer than {minimum} lines',f.path))
  if f.category=='Other': issues.append(Issue('DGT-REP-001','LOW','File classified as Other',f.path))
  if f.category in {'Generated Artifact','Runtime Artifact'}: issues.append(Issue('DGT-REP-002','MEDIUM',f'{f.category} is present in repository scan',f.path))
  if f.extension=='.md':
   p=root/f.path
   for raw in LINK.findall(p.read_text(encoding='utf-8',errors='replace')):
    t=raw.strip().split()[0].strip('<>')
    if not t or t.startswith(('http://','https://','mailto:','#')): continue
    target=(p.parent/unquote(t.split('#',1)[0])).resolve()
    try: target.relative_to(root.resolve())
    except ValueError: continue
    if not target.exists(): issues.append(Issue('DGT-DOC-003','HIGH',f'Broken Markdown link: {raw}',f.path))
 by=defaultdict(list)
 for f in files:
  if f.size_bytes: by[f.sha256].append(f.path)
 for paths in by.values():
  if len(paths)>1:
   for p in paths: issues.append(Issue('DGT-REP-003','LOW','Duplicate file content detected',p,{'duplicates':sorted(paths)}))
 return sorted(issues,key=lambda i:(i.severity,i.rule_id,i.path or ''))
def run_census(ctx):
 fs=scan(ctx); iss=rules(ctx,fs)
 stats={'file_count':len(fs),'total_size_bytes':sum(f.size_bytes for f in fs),'text_file_count':sum(f.is_text for f in fs),'categories':dict(sorted(Counter(f.category for f in fs).items())),'domains':dict(sorted(Counter(f.domain for f in fs).items())),'severities':dict(sorted(Counter(i.severity for i in iss).items())),'finding_count':len(iss)}
 return Inventory(str(ctx.repository_root),fs,iss,stats)

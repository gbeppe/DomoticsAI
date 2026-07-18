import json
from pathlib import Path
class ConfigurationError(RuntimeError): pass
def merge(a,b):
 r=dict(a)
 for k,v in b.items(): r[k]=merge(r[k],v) if isinstance(v,dict) and isinstance(r.get(k),dict) else v
 return r
def load_file(p):
 if not p.exists(): raise ConfigurationError(f"Configuration file not found: {p}")
 if p.suffix in {'.yaml','.yml'}:
  try: import yaml
  except ImportError as e: raise ConfigurationError('Install PyYAML') from e
  d=yaml.safe_load(p.read_text()) or {}
 else: d=json.loads(p.read_text())
 if not isinstance(d,dict): raise ConfigurationError('Configuration root must be a mapping')
 return d
def load_configuration(repo,explicit=None):
 p=Path(__file__).resolve().parents[1]/'config/governance.yaml'; c=load_file(p)
 local=repo/'.governance.yaml'
 if local.exists(): c=merge(c,load_file(local))
 if explicit: c=merge(c,load_file(explicit))
 return c

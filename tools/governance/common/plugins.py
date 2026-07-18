from dataclasses import dataclass
import importlib,pkgutil
@dataclass(frozen=True)
class PluginRegistry:
 rules:list[str];metrics:list[str];reporters:list[str]
def discover(package_root):
 def one(pkg,folder):
  out=[]
  for m in pkgutil.walk_packages([str(package_root/folder)],prefix=pkg+'.'):
   mod=importlib.import_module(m.name)
   if getattr(mod,'PLUGIN',None) is not None: out.append(m.name)
  return sorted(out)
 return PluginRegistry(one('tools.governance.rules','rules'),one('tools.governance.metrics','metrics'),one('tools.governance.reporters','reporters'))

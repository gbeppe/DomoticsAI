#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
if __package__ in (None,''): sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from tools.governance import __version__
from tools.governance.common.config import load_configuration,ConfigurationError
from tools.governance.common.context import build_context
from tools.governance.common.models import CommandResult
from tools.governance.common.plugins import discover
from tools.governance.execution import ExecutionMode, ExecutionPolicy
from tools.governance.repository_census.engine import run_census
from tools.governance.reporters.writers import write_json,write_markdown
def emit(r,j):
 print(json.dumps(r.to_dict(),indent=2,sort_keys=True) if j else '\n'.join([r.message]+[f'{k}: {v}' for k,v in r.details.items()]));return r.exit_code
def main(argv=None):
 p=argparse.ArgumentParser(prog='governance');p.add_argument('--repo',default='.');p.add_argument('--config');p.add_argument('--json',action='store_true');p.add_argument('--mode',default='generate');sp=p.add_subparsers(dest='command',required=True)
 for c in ('version','doctor','plugins','report','validate'): sp.add_parser(c)
 c=sp.add_parser('census');c.add_argument('--output-dir',default='docs/Governance');c.add_argument('--fail-on',choices=['none','low','medium','high'],default=None)
 a=p.parse_args(argv)
 if a.command=='version': return emit(CommandResult(True,f'DomoticsAI Governance Toolkit {__version__}'),a.json)
 try: repo=Path(a.repo).resolve();cfg=load_configuration(repo,Path(a.config).resolve() if a.config else None)
 except ConfigurationError as e: return emit(CommandResult(False,str(e),exit_code=2),a.json)
 mode=ExecutionMode.from_value(a.mode)
 policy=ExecutionPolicy.from_mode(mode)
 ctx=build_context(repo,cfg,mode,policy)
 if a.command=='doctor':
  r=discover(ctx.package_root);ok=repo.exists() and bool(r.rules) and bool(r.metrics) and bool(r.reporters);return emit(CommandResult(ok,'DGT doctor: PASS' if ok else 'DGT doctor: FAIL',{'rules':len(r.rules),'metrics':len(r.metrics),'reporters':len(r.reporters)},0 if ok else 2),a.json)
 if a.command=='plugins':
  r=discover(ctx.package_root);return emit(CommandResult(True,'Plugin discovery completed',{'rules':r.rules,'metrics':r.metrics,'reporters':r.reporters}),a.json)
 if a.command=='census':
  inv=run_census(ctx);details={'files':inv.statistics['file_count'],'findings':inv.statistics['finding_count']}
  if policy.generate_reports:
   out=repo/a.output_dir;md=write_markdown(inv,out/'Repository_Census.md');js=write_json(inv,out/'repository-census.json');details.update({'markdown':str(md),'json':str(js)})
  effective_threshold=policy.finding_policy.threshold.value if a.fail_on is None else a.fail_on
  rank={'none':99,'low':1,'medium':2,'high':3};code=0 if effective_threshold=='none' or not any({'LOW':1,'MEDIUM':2,'HIGH':3}[i.severity]>=rank[effective_threshold] for i in inv.issues) else 3
  return emit(CommandResult(code==0,'Repository Census completed',details,code),a.json)
 return emit(CommandResult(True,f'{a.command} framework available; implementation scheduled for a later release.'),a.json)
if __name__=='__main__': raise SystemExit(main())

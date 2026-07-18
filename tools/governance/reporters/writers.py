from pathlib import Path
import json
def write_json(inv,p): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(inv.to_dict(),indent=2,sort_keys=True)+'\n');return p
def write_markdown(inv,p):
 p.parent.mkdir(parents=True,exist_ok=True);s=inv.statistics
 L=['# DomoticsAI Repository Census','','## Executive Summary','',f"- Files inventoried: **{s['file_count']}**",f"- Total size: **{s['total_size_bytes']} bytes**",f"- Findings: **{s['finding_count']}**",'','## Categories','','| Category | Files |','|---|---:|']
 L += [f'| {k} | {v} |' for k,v in s['categories'].items()]
 L += ['','## Domains','','| Domain | Files |','|---|---:|']+[f'| {k} | {v} |' for k,v in s['domains'].items()]
 L += ['','## Findings','','| Severity | Rule | Path | Message |','|---|---|---|---|']
 L += [f"| {i.severity} | {i.rule_id} | `{i.path or ''}` | {i.message.replace('|','/')} |" for i in inv.issues] or ['| - | - | - | No findings |']
 L += ['','## Inventory','','| Path | Category | Domain | Size | SHA-256 |','|---|---|---|---:|---|']
 L += [f'| `{f.path}` | {f.category} | {f.domain} | {f.size_bytes} | `{f.sha256[:12]}…` |' for f in inv.files]
 p.write_text('\n'.join(L)+'\n');return p
PLUGIN='writers'

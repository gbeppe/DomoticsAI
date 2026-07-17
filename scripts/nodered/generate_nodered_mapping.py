#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from collections import defaultdict
from pathlib import Path
from typing import Any
OBSOLETE_LIGHTS={'lampadaHifi','cucina','esterno'}
DOMAIN_RULES=[('lights',('light','lights','lamp','luci','scene')),('energy',('energy','teslapowerwall','powerwall','solar','battery','soe','grid','surplus')),('climate',('clima','climate','humidex','temperature','humidity','thermostat','acauto','ac_auto')),('vmc',('vmc','fanspeed','brink')),('fireplace',('caminetto','stufa','palazzetti','focolare')),('pool',('piscina','pool','skimmer')),('system',('system','holiday','time_range','porch_sensor')),('history',('storico','history','mysql'))]
APP_BASE_RE=re.compile(r'\$\{(?:APP_BASE|baseTopic)\}/([^"\'`\s;,)]+)')
TOPIC_LITERAL_RE=re.compile(r'(?P<quote>["\'`])(?P<topic>[^"\'`\n]*(?:/|TeslaPowerwall|zigbee2mqtt|shellies|emon|alexa|casa|zara)[^"\'`\n]*)\1')
def load_json(p:Path)->Any:return json.loads(p.read_text(encoding='utf-8'))
def normalize_topic(v:str)->str:return v.strip().strip('/')
def domain_for(*vals:str)->str:
 t=' '.join(vals).lower()
 for d,ns in DOMAIN_RULES:
  if any(n in t for n in ns):return d
 return 'unclassified'
def role_for(topic:str,direction:str)->str:
 l=topic.lower()
 if l.endswith('/set') or '/cmnd/' in l or '/command' in l:return 'COMMAND'
 if l.endswith('/state') or '/stat/' in l or 'stato' in l:return 'STATE'
 if any(x in l for x in ('temperature','humidity','humidex','power','soe','sensor','production','consumption','battery','grid','surplus')):return 'READ_ONLY'
 if direction=='publish':return 'CONFIGURATION'
 return 'READ_ONLY'
def payload_hint(topic:str,node:dict[str,Any])->str:
 dt=str(node.get('datatype') or '')
 if dt and dt!='auto-detect':return dt
 l=topic.lower()
 if 'stato_completo' in l:return 'json_object'
 if any(x in l for x in ('temperature','humidity','humidex','power','soe','sensor')):return 'number'
 if l.endswith('/set') or l.endswith('/state'):return 'scalar_or_boolean'
 return 'unknown'
def proposed_topic(topic:str,domain:str,role:str)->tuple[str,str]:
 t=normalize_topic(topic)
 raw=topic.strip()
 if not t or t=='<dinamico>':return '', 'DYNAMIC_TOPIC'
 if raw.startswith('${APP_BASE}/'):return raw.removeprefix('${APP_BASE}/'),'CURRENT_APP_NAMESPACE'
 if raw.startswith('${baseTopic}/'):return raw.removeprefix('${baseTopic}/'),'CURRENT_APP_NAMESPACE'
 if raw.startswith('^') or raw.endswith('$') or '([^/]+)' in raw or '.*' in raw:return '', 'REGEX_ROUTE'
 if t=='zara/android/domotica':return '', 'DYNAMIC_TOPIC'
 known={'casa/clima/cmnd/AI_climate_enabling':('system/set','MIGRATE_TO_JSON'),'casa/clima/stat/vmc_max_notte':('vmc/maxNightSpeed/state','KEEP_AS_STATE'),'casa/clima/cmnd/vmc_max_notte':('vmc/maxNightSpeed/set','KEEP_AS_COMMAND'),'casa/clima/stato_completo':('casa/clima/stato_completo','READ_ONLY_PRIMARY'),'alexa/vmc':('vmc/speed/state','LEGACY_MAP')}
 if t in known:return known[t]
 state_map={'zara/domotics/modalitavacanza':'system/holiday','zara/domotics/luciECO':'system/luci_eco','zara/domotics/luciPiscinaAuto':'system/luci_piscina_auto','zara/domotics/ACAuto':'system/ac_auto','zara/domotics/porch_sensor':'system/sensore_portico','zara/domotics/time_range':'system/time_range'}
 if t in state_map:return f"{state_map[t]}/{'set' if role=='COMMAND' else 'state'}",('DISTINCT_SEMANTICS' if 'ACAuto' in t else 'LEGACY_MAP')
 if t.startswith('zara/android/domotica/'):
  s=t.removeprefix('zara/android/domotica/')
  if s=='system/set' and role=='STATE':return 'system/state','FIX_SET_STATE_COLLISION'
  return s,'CURRENT_APP_NAMESPACE'
 pmap={'TeslaPowerwall/solar_instant_power':'energy/production','TeslaPowerwall/load_instant_power':'energy/consumption','TeslaPowerwall/site_instant_power':'energy/grid','TeslaPowerwall/SOE':'energy/battery','emon/emonth5/temperature_calibrated':'env/tempLiving','emon/emonth5/humidity':'env/humLiving','emon/emonth5/humidex':'env/humidexLiving','emon/cameraMatrimoniale/temperature':'env/tempBedroom','emon/cameraMatrimoniale/humidity':'env/humBedroom','emon/cameraMatrimoniale/humidex':'env/humidexBedroom','emon/shellyACS/tempACS':'acsPufferTemp','emon/resolDL2/sensor2':'pufferBassoTemp','emon/resolDL2/sensor3':'pufferAltoTemp','emon/focolare/powerraw':'casa/stufa/stat/potenza'}
 if t in pmap:return pmap[t],'LEGACY_MAP'
 if t.startswith('zara/domotics/lights/'):
  dm={'livinglamp':'sala','shelflamp':'libreria','tvlamp':'televisione','readinglight':'tavolinoLettura','poollight':'luciPiscina','poolfloor':'luciPedanaPiscina','poolskimmer':'skimmerPiscina','poolpump':'pompaPiscina'}
  d=dm.get(t.rsplit('/',1)[-1]);
  if d:return f'light/{d}/state','LEGACY_MAP'
 if t.startswith('zara/domotics/palazzetti/'):return f"casa/stufa/stat/{t.rsplit('/',1)[-1]}",'LEGACY_MAP'
 if t.startswith('zigbee2mqtt/') or t.startswith('shellies/'):return '','PHYSICAL_TOPIC'
 if domain=='history':return '','LOCAL_SERVICE'
 return '','MANUAL_REVIEW'
def proposed_payload(role:str,proposed:str,current:str)->str:
 if proposed=='system/set':return 'json_object {automaticClimate:boolean,...}'
 if proposed=='system/state':return 'json_object {automaticClimate:boolean,...}'
 if role=='STATE' and current in {'scalar_or_boolean','unknown'}:return 'normalized_scalar'
 return current
def proposed_retain(role:str,proposed:str)->str:
 if proposed.endswith('/set') or role=='COMMAND':return 'false'
 if proposed.endswith('/state') or role in {'STATE','READ_ONLY'}:return 'true'
 return 'review'
def extract_function_topics(code:str)->tuple[list[str],list[str]]:
 lits=sorted({m.group('topic').strip() for m in TOPIC_LITERAL_RE.finditer(code or '') if m.group('topic').strip()})
 apps=sorted({m.group(1).strip() for m in APP_BASE_RE.finditer(code or '') if m.group(1).strip()})
 return lits,apps
def md_table(headers,rows):
 esc=lambda v:str(v).replace('|',r'\|').replace('\n',' ')
 out=['| '+' | '.join(headers)+' |','|'+'|'.join('---' for _ in headers)+'|']
 out += ['| '+' | '.join(esc(v) for v in r)+' |' for r in rows]
 return '\n'.join(out)
def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('flow_json',type=Path);ap.add_argument('--contract',type=Path,default=Path('config/mqtt/application-contract-v1.json'));ap.add_argument('--output-dir',type=Path,default=Path('docs/NodeRED/mapping'));a=ap.parse_args()
 nodes=load_json(a.flow_json);contract=load_json(a.contract);contract_patterns={str(i.get('pattern') or '') for i in contract.get('topics',[])};brokers={str(n.get('id')):n for n in nodes if n.get('type')=='mqtt-broker'}
 rows=[];seen=set()
 def add(node,topic,direction,source):
  key=(str(node.get('id')),topic,source)
  if key in seen:return
  seen.add(key);b=brokers.get(str(node.get('broker')),{});name=str(node.get('name') or node.get('label') or node.get('id') or '');domain=domain_for(topic,name);role=role_for(topic,direction);cur=payload_hint(topic,node);prop,mig=proposed_topic(topic,domain,role);notes=[];status=mig
  if prop in contract_patterns:notes.append('Topic presente nel contratto applicativo.')
  elif prop:notes.append('Topic proposto non ancora presente nel contratto.')
  obsolete=False
  if domain=='lights':
   tl=topic.lower();nl=name.lower()
   obsolete=any((f'/light/{d.lower()}/' in tl or tl.endswith('/'+d.lower()) or nl==d.lower() or f'luce_{d.lower()}' in tl or f'shelly1-{d.lower()}' in tl) for d in OBSOLETE_LIGHTS)
  if obsolete:status='OBSOLETE';notes.append('Dispositivo luce dichiarato obsoleto nel progetto.')
  if node.get('d') is True:notes.append('Nodo disabilitato nel flow corrente.')
  if role=='COMMAND' and str(node.get('retain')).lower()=='true':notes.append('Comando retained: da correggere nel bridge v2.')
  if topic=='casa/clima/cmnd/AI_climate_enabling':notes.append('Bridge v2: ingresso system/set JSON; conferma system/state retained.')
  rows.append({'node_id':str(node.get('id') or ''),'node_name':name,'source':source,'direction':direction,'broker_host':str(b.get('broker') or ''),'broker_port':str(b.get('port') or ''),'current_topic':topic,'domain':domain,'role':role,'current_payload':cur,'current_qos':str(node.get('qos') or ''),'current_retain':str(node.get('retain') or ''),'proposed_suffix':prop,'proposed_full_topic':f'${{baseTopic}}/{prop}' if prop else '','proposed_payload':proposed_payload(role,prop,cur),'proposed_retain':proposed_retain(role,prop),'migration_status':status,'contract_present':'yes' if prop in contract_patterns else 'no','notes':' '.join(notes),'occurrences':'1','node_ids':str(node.get('id') or ''),'node_names':name,'sources':source})
 for n in nodes:
  t=n.get('type')
  if t=='mqtt in':add(n,str(n.get('topic') or ''),'broker_to_bridge','mqtt_node')
  elif t=='mqtt out':add(n,str(n.get('topic') or ''),'bridge_to_broker','mqtt_node')
  elif t=='function':
   lits,apps=extract_function_topics(str(n.get('func') or ''))
   for x in lits:
    if not x.startswith('${baseTopic}/'):add(n,x,'function_reference','function_literal')
   for s in apps:add(n,f'zara/android/domotica/{s}','application_mapping','function_application_topic')
 grouped={}
 for r in rows:
  k=(r['domain'],r['role'],r['current_topic'],r['proposed_suffix'],r['migration_status'])
  if k not in grouped:grouped[k]=dict(r);continue
  e=grouped[k];e['occurrences']=str(int(e['occurrences'])+1)
  for tf,sf in [('node_ids','node_id'),('node_names','node_name'),('sources','source')]:
   vals={x for x in e[tf].split(' ; ') if x};c=r[sf]
   if c:vals.add(c)
   e[tf]=' ; '.join(sorted(vals))
 rows=list(grouped.values())
 rows.sort(key=lambda r:(r['domain'],r['role'],r['current_topic'],r['proposed_suffix']))
 a.output_dir.mkdir(parents=True,exist_ok=True)
 csvp=a.output_dir/'BRIDGE_MAPPING_MATRIX.csv'
 with csvp.open('w',encoding='utf-8',newline='') as h:w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 byr=defaultdict(list)
 for r in rows:byr[r['domain']].append(r)
 md=['# DomoticsAI — Matrice di mapping del bridge v2','',f'- Flow sorgente: `{a.flow_json}`',f'- Contratto: `{a.contract}`',f'- Righe di mapping: `{len(rows)}`','','## Mapping','',md_table(['Dominio','Ruolo','Topic corrente','Topic DomoticsAI proposto','Migrazione','Nel contratto','Occorrenze'],[[r['domain'],r['role'],r['current_topic'] or '<dinamico>',r['proposed_full_topic'] or '—',r['migration_status'],r['contract_present'],r['occurrences']] for r in rows]),'','## Principi applicati','','- Il bridge storico resta invariato.','- Il bridge v2 sarà inizialmente read-only.','- I topic fisici non vengono esposti direttamente ad Android.','- `system/set` è comando JSON non retained.','- `system/state` è stato confermato retained.','- I dispositivi obsoleti vengono esclusi.','']
 (a.output_dir/'BRIDGE_MAPPING_MATRIX.md').write_text('\n'.join(md),encoding='utf-8')
 dm=['# DomoticsAI — Domain Map del bridge v2','']
 for d in sorted(byr):dm += [f'## {d.upper()}','',md_table(['Ruolo','Topic corrente','Suffix DomoticsAI','Stato','Occorrenze','Nodi'],[[r['role'],r['current_topic'] or '<dinamico>',r['proposed_suffix'] or '—',r['migration_status'],r['occurrences'],r['node_names']] for r in byr[d]]),'']
 (a.output_dir/'DOMAIN_MAP.md').write_text('\n'.join(dm),encoding='utf-8')
 qs=[]
 for r in rows:
  if r['migration_status'] in {'MANUAL_REVIEW','DYNAMIC_TOPIC','REGEX_ROUTE','DISTINCT_SEMANTICS'}:qs.append(f"- `{r['current_topic'] or '<dinamico>'}` ({r['node_name']}): {r['migration_status']}.")
 qs += ['- Confermare se `system/ac_auto/state` e `ac_auto/state` restano parametri distinti.','- Fornire gli export delle schede contenenti i Link In esterni prima di abilitare i comandi.','- Confermare i nomi definitivi dei dispositivi luci attivi.','- Confermare se il namespace canary sarà `${baseTopic}/v2` oppure un base topic separato.']
 (a.output_dir/'MAPPING_OPEN_QUESTIONS.md').write_text('# DomoticsAI — Questioni aperte del mapping\n\n'+'\n'.join(dict.fromkeys(qs))+'\n',encoding='utf-8')
 print('OK: matrice di mapping generata.');print('Righe:',len(rows));print('Domini:',len(byr));print('Output:',a.output_dir);return 0
if __name__=='__main__':raise SystemExit(main())

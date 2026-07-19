from pathlib import Path
from tools.governance.governance import main
from tools.governance.repository_census.classification import category, domain
def test_category_and_domain():
 c={'classification':{'generated_markers':['.egg-info/'],'runtime_markers':['.logs/']}}
 assert category(Path('docs/README.md'),c)=='Documentation'
 d={'domains':{'default':'Repository','path_rules':[{'domain':'Android','prefixes':['app']}]}}
 assert domain(Path('app/src/Main.kt'),d)=='Android'
def test_cli(tmp_path,capsys):
 assert main(['version'])==0
 assert '0.2.0' in capsys.readouterr().out
 (tmp_path/'README.md').write_text('# Demo\nEnough\nLines\nFor\nThe\nRule\nHere\nNow\n')
 assert main(['--repo',str(tmp_path),'doctor'])==0
 assert main(['--repo',str(tmp_path),'census'])==0
 assert (tmp_path/'docs/Governance/Repository_Census.md').exists()
 assert (tmp_path/'docs/Governance/repository-census.json').exists()

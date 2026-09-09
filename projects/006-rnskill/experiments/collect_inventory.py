"""Read a pinned upstream snapshot; never execute or install upstream skills."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
import json
import re
import time

ROOT = Path(__file__).resolve().parents[1]
COMMIT = '7cbf47b57cbae0596d46c10c4a1445cbb27904b3'
REPO = 'Pluviobyte/rnskill'
CACHE = ROOT.parents[1] / '.research' / 'rnskill' / COMMIT

def fetch(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'project-lab-research'}), timeout=40) as response:
                return response.read().decode('utf-8-sig')
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)

def inspect(entry):
    path = entry['path']
    local = CACHE / path
    if not local.exists():
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_text(fetch(f'https://raw.githubusercontent.com/{REPO}/{COMMIT}/{quote(path)}'), encoding='utf-8')
    text = local.read_text(encoding='utf-8')
    match = re.search(r'^name:\s*(.+)$', text, re.M)
    return {'path': path, 'name': match.group(1).strip().strip('"\'') if match else path.split('/')[-2],
            'sha': entry['sha'], 'bytes': entry.get('size'),
            'source': f'https://github.com/{REPO}/blob/{COMMIT}/{quote(path)}',
            'nested': len(path.split('/')) > 3}

def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    tree_path = CACHE / 'tree.json'
    if not tree_path.exists():
        tree_path.write_text(fetch(f'https://api.github.com/repos/{REPO}/git/trees/{COMMIT}?recursive=1'), encoding='utf-8')
    tree = json.loads(tree_path.read_text(encoding='utf-8'))
    assert not tree.get('truncated'), 'Incomplete tree'
    entries = [item for item in tree['tree'] if item['path'].endswith('/SKILL.md')]
    with ThreadPoolExecutor(max_workers=8) as pool:
        inventory = list(pool.map(inspect, entries))
    all_paths = {item['path'] for item in tree['tree']}
    for item in inventory:
        prefix = item['path'].rsplit('/', 1)[0] + '/'
        item['scripts'] = [p for p in sorted(all_paths) if p.startswith(prefix) and '/scripts/' in p and p.endswith(('.py','.js','.cjs','.sh','.ts'))]
    expected = ['automation/scripts/wash_ledger.py','automation/scripts/check_delivery.py',
                'automation/scripts/hot_monitor_local_job.sh','automation/config/tts-routing.json']
    output = {'repository': f'https://github.com/{REPO}', 'commit': COMMIT, 'checked': '2026-09-09',
              'method': '静态源码核对，未运行上游技能或调用收费服务',
              'total': len(inventory), 'topLevel': sum(not s['nested'] for s in inventory),
              'nested': sum(s['nested'] for s in inventory),
              'missingDependencies': [p for p in expected if p not in all_paths], 'skills': inventory}
    dest = ROOT / 'web' / 'data'
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'inventory.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: output[key] for key in ['commit','total','topLevel','nested','missingDependencies']}, ensure_ascii=False))

if __name__ == '__main__':
    main()

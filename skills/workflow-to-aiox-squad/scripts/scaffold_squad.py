"""Create an original task-first AIOX squad from a concrete local workflow."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def scaffold(source, destination):
    source, destination = Path(source), Path(destination)
    data = json.loads(source.read_text(encoding='utf-8'))
    valid_name = lambda value: isinstance(value, str) and bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value)) and 2 <= len(value) <= 50
    if not valid_name(data.get('name')): raise ValueError('Use a kebab-case squad name of 2 to 50 characters')
    if not isinstance(data.get('description'), str) or not 1 <= len(data['description']) <= 500: raise ValueError('Provide a description of 1 to 500 characters')
    steps = data.get('steps', [])
    if not 1 <= len(steps) <= 12: raise ValueError('Use 1 to 12 concrete steps')
    ids = []
    for step in steps:
        if not valid_name(step.get('id')): raise ValueError('Use kebab-case step IDs')
        if not isinstance(step.get('purpose'), str) or not step['purpose'].strip(): raise ValueError('Each step needs a specific purpose')
        for field in ('inputs', 'outputs'):
            values = step.get(field)
            if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v.strip() for v in values): raise ValueError('Name each step input and output')
        ids.append(step['id'])
    if len(set(ids)) != len(ids): raise ValueError('Duplicate step IDs')
    destination.mkdir(parents=True, exist_ok=False)
    for folder in ('agents', 'tasks', 'checklists'): (destination/folder).mkdir()
    for step in steps:
        name = step['id']
        persona = {'agent': {'id': name, 'name': name.replace('-', ' ').title(), 'title': name.replace('-', ' ').title(), 'whenToUse': step['purpose']},
            'persona': {'role': step['purpose'], 'style': 'Clear and evidence-led'},
            'commands': [{'name': 'run', 'description': f'Read tasks/{name}.md and produce its named handoff'}],
            'dependencies': {'tasks': [name+'.md']}}
        (destination/'agents'/f'{name}.md').write_text(f'# {name}\n\n```yaml\n'+json.dumps(persona, indent=2)+'\n```\n\n'+step['purpose']+'\n', encoding='utf-8')
        task = f"# {name}\n\ntask: {name.replace('-', '_')}()\nresponsavel: {name}\nresponsavel_type: Agente\natomic_layer: Content\n\n**Entrada:**\n"
        for value in step['inputs']: task += f'- {value}\n'
        task += '\n**Saida:**\n'
        for value in step['outputs']: task += f'- {value}\n'
        task += '\n**Checklist:**\n- [ ] Required inputs are present.\n- [ ] Named outputs are written with evidence and limitations.\n- [ ] No unrequested external action or invented result.\n\n## Work\n\n'+step['purpose']+'\n'
        (destination/'tasks'/f'{name}.md').write_text(task, encoding='utf-8')
    manifest = {'name': data['name'], 'version': '0.1.0', 'description': data['description'],
        'author': 'Workflow author', 'license': 'MIT', 'aiox': {'type': 'squad', 'minVersion': '2.0.0'},
        'components': {'agents': [x+'.md' for x in ids], 'tasks': [x+'.md' for x in ids], 'checklists': ['handoff.md']}, 'config': {'extends': 'extend'}}
    (destination/'squad.yaml').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    (destination/'README.md').write_text('# '+data['name']+'\n\n'+data['description']+'\n\n## Suggested run order\n\n'+'\n'.join(f'{i}. Read tasks/{name}.md and pass its outputs to the next task.' for i,name in enumerate(ids,1))+'\n\nThese are task definitions, not running agents. Validate in your chosen host;\nfull integration and publication remain separate decisions. Choose an appropriate\nlicence for your additions. The original scaffold helper is MIT.\n', encoding='utf-8')
    (destination/'checklists/handoff.md').write_text('# Handoff review\n\nCheck named inputs/outputs, source evidence, actual tool access and outstanding\nlimits. Do not equate a generated role file with successful host execution.\n', encoding='utf-8')
    receipt = {'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'squad': data['name'], 'steps': ids, 'host_execution_tested': False,
        'files': {str(p.relative_to(destination)): hashlib.sha256(p.read_bytes()).hexdigest() for p in destination.rglob('*') if p.is_file()}}
    (destination/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workflow', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try: print(json.dumps(scaffold(args.workflow, args.out)))
    except (ValueError, KeyError, FileExistsError) as exc: parser.exit(2, str(exc)+'\n')

"""Build a traceable video handoff from an agent-authored brief. No network/LLM calls."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from urllib.parse import urlsplit


def validate(data):
    if not isinstance(data.get('title'), str) or not data['title'].strip():
        raise ValueError('A title is required')
    sources = data.get('sources', [])
    ids = [s['id'] for s in sources]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError('Provide unique source IDs')
    for source in sources:
        url = urlsplit(source['url'])
        if url.scheme != 'https' or not url.hostname or url.username or url.password:
            raise ValueError('Sources need public HTTPS references')
        if not source.get('note'):
            raise ValueError('Explain what each source supports')
    scenes = data.get('scenes', [])
    if not 1 <= len(scenes) <= 30:
        raise ValueError('Use 1 to 30 scenes')
    for scene in scenes:
        duration = scene['seconds']
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(duration) or not 1 <= duration <= 60:
            raise ValueError('Scene duration must be 1 to 60 seconds')
        for key in ('title', 'narration', 'action'):
            if not isinstance(scene.get(key), str) or not scene[key].strip():
                raise ValueError(f'Scene requires {key}')
        if not scene.get('sources') or not set(scene['sources']) <= set(ids):
            raise ValueError('Every scene needs known source references')
        if scene.get('visual_basis') not in ('original', 'own-recording', 'licensed', 'documentation-illustration'):
            raise ValueError('Label the visual basis')
        if not scene.get('steps') or len(scene['steps']) > 4 or any(not isinstance(s, str) or not s.strip() or len(s)>24 for s in scene['steps']):
            raise ValueError('Use 1 to 4 short visual steps, each <=24 characters')
    if sum(s['seconds'] for s in scenes) > 180:
        raise ValueError('Starter targets videos of at most 180 seconds')
    return data


def build(source, destination):
    source, destination = Path(source), Path(destination)
    data = validate(json.loads(source.read_text(encoding='utf-8')))
    # Reserve a new folder; never overwrite a previous run or partially completed handoff.
    destination.mkdir(parents=True, exist_ok=False)
    manifest = {'title': data['title'], 'fps': 24, 'scenes': [], 'captions': []}
    narration, storyboard, cursor = [], [], 0
    for index, scene in enumerate(data['scenes'], 1):
        end = cursor + scene['seconds']
        narration.append(f"[{cursor:.2f}–{end:.2f}] {scene['narration']}")
        storyboard.append({'scene': index, 'start': cursor, 'end': end, **scene})
        manifest['scenes'].append({'title': scene['title'], 'seconds': scene['seconds'],
            'steps': scene['steps'], 'credit': ', '.join(scene['sources']) + ' | ' + scene['visual_basis']})
        # Human narration is separately timed; visual labels are not automatic speech alignment.
        cursor = end
    outputs = {'short.json': manifest, 'storyboard.json': storyboard,
               'sources.json': data['sources']}
    for name, value in outputs.items():
        (destination/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (destination/'narration.md').write_text('\n\n'.join(narration)+'\n', encoding='utf-8')
    receipt = {'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'duration_seconds': cursor, 'status': 'handoff_only', 'published': False,
        'speech_recorded': False, 'source_claims_human_reviewed': False,
        'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in destination.iterdir()}}
    (destination/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('brief', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.brief, args.out)))
    except (ValueError, KeyError, FileExistsError) as exc:
        parser.exit(2, f'{exc}\n')

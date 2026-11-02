"""Inspect local agent configuration and optional file hashes without network or effects.

This portable adaptation does not include the original deployment coordinator,
notification delivery, persistent checkpoints, scheduled jobs or model bindings.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PureWindowsPath


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def safe_file(root, relative):
    root = root.resolve()
    path = Path(relative)
    if path.is_absolute() or PureWindowsPath(relative).drive or '..' in path.parts:
        raise ValueError('path_outside_root')
    target = root / path
    for part in (target, *target.parents):
        if part == root:
            break
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError('linked_path_denied')
    if not target.resolve().is_relative_to(root):
        raise ValueError('path_outside_root')
    return target


def check_files(root, entries):
    result = []
    if len(entries) > 200:
        raise ValueError('file_count_limit')
    for item in entries:
        path = safe_file(root, item['path'])
        actual = None
        if not path.is_file():
            state = 'unavailable'
        elif path.stat().st_size > 4_000_000:
            state = 'unreadable_size_limit'
        else:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            state = 'verified' if actual == item['sha256'] else 'changed'
        result.append({'path': item['path'], 'state': state, 'actual_sha256': actual})
    return result


def observation_key(rows, policies):
    return digest({'files': sorted(rows, key=lambda x: x['path']), 'policies': policies})


def validate_config(root, config):
    errors = []
    expected = {'O0'} | {'S'+str(i) for i in range(1, 14)}
    roles = config.get('roles', [])
    if {role.get('id') for role in roles} != expected or len(roles) != 14:
        errors.append('role_set_invalid')
    for role in roles:
        if not safe_file(root, role['instruction']).is_file():
            errors.append('instruction_unavailable:'+role['id'])
    scope = config.get('execution', {})
    for key, name in [('websiteWrites','website_writes'), ('publication','publication'),
                      ('paidApis','paid_apis'), ('autonomousInference','autonomous_inference')]:
        if scope.get(key) is not False:
            errors.append(name+'_outside_initial_scope')
    limits = config.get('limits', {})
    if limits.get('maxParallelSpecialists') != 1:
        errors.append('initial_parallelism_policy_mismatch')
    if limits.get('maxRefinementPasses') != 2:
        errors.append('refinement_limit_mismatch')
    return errors



def inspect(root, config_path='agents/orchestration.example.json', manifest_path=None):
    config = json.loads(safe_file(root, config_path).read_text(encoding='utf-8'))
    errors = validate_config(root, config)
    rows = []
    if manifest_path is not None:
        manifest = json.loads(safe_file(root, manifest_path).read_text(encoding='utf-8'))
        rows = check_files(root, manifest['files'])
    return {
        'schemaVersion': '1.0.0', 'scope': 'local-agent-configuration-and-file-hashes-only',
        'roles': len(config.get('roles', [])), 'validationErrors': errors,
        'files': rows, 'mismatches': [row for row in rows if row['state'] != 'verified'],
        'fingerprint': observation_key(rows, {'config': digest(config)}),
        'websiteInspected': False, 'indexState': 'unknown', 'rankingResults': 'not_measured',
        'modelCallsMade': 0, 'paidApiCalls': 0, 'productWrites': 0,
        'externalNotifications': 0, 'persistentStateWritten': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--config', default='agents/orchestration.example.json')
    parser.add_argument('--manifest', help='Relative JSON path containing a files array of path/sha256 entries')
    args = parser.parse_args()
    try:
        result = inspect(args.root, args.config, args.manifest)
    except (KeyError, TypeError, ValueError, OSError) as error:
        print(json.dumps({'scope': 'local-agent-configuration-and-file-hashes-only',
                          'state': 'invalid-input', 'errorType': type(error).__name__}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result['validationErrors'] or result['mismatches'] else 0


if __name__ == '__main__':
    raise SystemExit(main())

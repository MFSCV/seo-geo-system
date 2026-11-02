#!/usr/bin/env python3
"""Validate the public checkout without private archives or external packages.

These are repository integrity and selected design-invariant checks. They are
not a complete JSON Schema implementation or qualification of live operations.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path, PurePath
import re
from collections import Counter
from urllib.parse import unquote

IGNORED_PARTS = {'.git', '__pycache__', '.pytest_cache', '.venv', 'venv'}
PRIVATE_PATTERNS = {
    'private-library-identifier': re.compile(r'\blibfile_[a-zA-Z0-9]{12,}'),
    'private-local-path': re.compile(r'(?:[A-Z]:[\\/]+Users[\\/]+[^\s<>"\']+|/workspace/scratch/[a-zA-Z0-9_-]+/)', re.I),
    'github-token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})'),
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'cloud-access-key': re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
}


def repository_path(path: PurePath, root: PurePath) -> str:
    """Use the same POSIX relative path in manifests on every platform."""
    return path.relative_to(root).as_posix()


def public_files(root: Path):
    """Yield files in stable order, excluding local tooling/git metadata."""
    return sorted(p for p in root.rglob('*') if (p.is_file() or p.is_symlink())
                  and not any(part in IGNORED_PARTS for part in p.relative_to(root).parts))


def heading_anchors(text: str) -> set[str]:
    anchors = set()
    counts: dict[str, int] = {}
    for line in text.splitlines():
        if not line.startswith('#'):
            continue
        label = re.sub(r'\s+#+\s*$', '', line.lstrip('#').strip()).lower()
        label = re.sub(r'[^\w\- ]', '', label).replace(' ', '-')
        n = counts.get(label, 0)
        counts[label] = n + 1
        anchors.add(label if n == 0 else f'{label}-{n}')
    return anchors


def markdown_links(text: str):
    # Code examples are data, not navigable Markdown links.
    text = re.sub(r'^```.*?^```\s*$', '', text, flags=re.M | re.S)
    for _label, target in re.findall(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)', text):
        yield target.strip().removeprefix('<').removesuffix('>')


def check_local_target(root: Path, source: Path, target: str) -> list[str]:
    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('//'):
        return []
    rel, _, frag = target.partition('#')
    rel = unquote(rel.split('?', 1)[0])
    destination = (source.parent / rel).resolve() if rel else source.resolve()
    if not destination.is_relative_to(root.resolve()):
        return [f'Local link escapes checkout: {repository_path(source, root)} -> {target}']
    if not destination.exists():
        return [f'Broken local link: {repository_path(source, root)} -> {target}']
    if frag and destination.suffix == '.md' and unquote(frag) not in heading_anchors(destination.read_text(encoding='utf-8')):
        return [f'Broken local anchor: {repository_path(source, root)} -> {target}']
    return []


def schema_refs(value):
    if isinstance(value, dict):
        if '$ref' in value:
            yield value['$ref']
        for child in value.values():
            yield from schema_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from schema_refs(child)


def selected_record_errors(record: dict) -> list[str]:
    """Check a small documented subset, not the complete record schema."""
    errors = []
    if record.get('schemaVersion', '').split('.', 1)[0] != '0':
        errors.append('Unsupported record contract major version')
    payload = record.get('payload', {})
    if record.get('recordType') == 'observation':
        result = payload.get('result', {})
        if result.get('outcome') == 'unknown':
            if 'value' in result or 'denominator' in result:
                errors.append('Unknown observation cannot carry a measured value or denominator')
            if not isinstance(result.get('reason'), str) or not result['reason'].strip():
                errors.append('Unknown observation requires a reason')
        elif result.get('outcome') == 'observed':
            if not isinstance(result.get('value'), (int, float)) or isinstance(result.get('value'), bool):
                errors.append('Observed metric requires a numeric value')
            if not isinstance(result.get('denominator'), (int, float)) or isinstance(result.get('denominator'), bool) or result['denominator'] <= 0:
                errors.append('Observed metric requires a positive denominator')
        else:
            errors.append('Observation outcome must be observed or unknown')
    if record.get('recordType') == 'review':
        if not re.fullmatch(r'[0-9a-f]{64}', str(payload.get('proposalSha256', ''))):
            errors.append('Review requires an exact SHA-256 proposal digest')
    return errors


def validate(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    counts: dict[str, int] = {}

    def require(condition, message):
        if not condition:
            errors.append(message)

    def rows(name):
        try:
            with (root / name).open(encoding='utf-8', newline='') as handle:
                return list(csv.DictReader(handle))
        except (OSError, csv.Error) as exc:
            errors.append(f'Cannot read {name}: {type(exc).__name__}')
            return []

    caps = rows('catalog/capabilities.csv')
    roles = rows('catalog/agents.csv')
    role_ids = {row.get('id') for row in roles}
    require(len(roles) == 14 and role_ids == {'O0'} | {f'S{i}' for i in range(1, 14)}, 'Agent role set/count mismatch')
    require(len(caps) == 144 and {r.get('capability_id') for r in caps} == {f'CAP-{i:03}' for i in range(1, 145)}, 'Capability ID set/count mismatch')
    for row in caps:
        require(row.get('lead_owner') in role_ids, f'Unknown capability owner: {row.get("capability_id")}')
        require(all(x in role_ids for x in row.get('supporting_owners', '').split(';') if x), 'Unknown supporting role')
        require(row.get('source_status_exact') == 'Procedural scope catalog; runtime qualification required; not an implemented connector', 'Unsupported capability implementation claim')
        errors.extend(check_local_target(root, root / 'README.md', row.get('proposed_contract', '')))
    ops = rows('catalog/connector-operations.csv')
    cross = rows('catalog/connector-crosswalk.csv')
    op_ids = {row.get('operation_id') for row in ops}
    require(len(ops) == len(op_ids) == 76, 'Operation family set/count mismatch')
    require(Counter(r.get('access_mode') for r in ops) == {'read': 50, 'write': 26}, 'Operation access mode distribution mismatch')
    require(len(cross) == len({(r.get('source_inventory'), r.get('source_row_id')) for r in cross}) == 63, 'Connector source row count/uniqueness mismatch')
    require(Counter(r.get('source_inventory') for r in cross) == {'skill_catalog_28': 28, 'planning_matrix_25': 25, 'runtime_declarations_10': 10}, 'Connector source namespaces mismatch')
    forward = set()
    reverse = set()
    for row in cross:
        key = f'{row.get("source_inventory")}:{row.get("source_row_id")}'
        for op_id in row.get('canonical_operation_ids', '').split(';'):
            require(op_id in op_ids, f'Dangling connector operation: {op_id}')
            forward.add((key, op_id))
    for row in ops:
        require(row.get('implementation_state') == 'NOT_IMPLEMENTED', 'Unsupported operation implementation claim')
        require(row.get('qualification_state') == 'NEEDS_QUALIFICATION', 'Unsupported operation qualification claim')
        for key in row.get('source_row_refs', '').split(';'):
            reverse.add((key, row.get('operation_id')))
    require(forward == reverse and len(forward) == 190, 'Connector bidirectional references mismatch')
    counts.update(capabilities=len(caps), roles=len(roles), connectorSourceRows=len(cross), operationFamilies=len(ops), connectorReferences=len(forward))

    files = public_files(root)
    counts.update(files=len(files), markdownLinks=0, jsonFiles=0, schemaRefs=0, privacyMatches=0, exampleInvariants=0)
    for path in files:
        relative = repository_path(path, root)
        if path.is_symlink():
            errors.append(f'Symlink requires explicit export review: {relative}')
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            errors.append(f'Unexpected binary file requires export review: {relative}')
            continue
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                errors.append(f'Publication marker ({label}): {relative}')
                counts['privacyMatches'] += 1
        if path.suffix == '.md':
            for target in markdown_links(text):
                counts['markdownLinks'] += 1
                errors.extend(check_local_target(root, path, target))
        if path.suffix == '.json':
            try:
                value = json.loads(text)
            except json.JSONDecodeError:
                errors.append(f'Invalid JSON: {relative}')
                continue
            counts['jsonFiles'] += 1
            if path.name.endswith('.schema.json'):
                require(isinstance(value, dict) and value.get('$schema') == 'https://json-schema.org/draft/2020-12/schema', f'Unsupported schema dialect: {relative}')
                for ref in schema_refs(value):
                    if not isinstance(ref, str) or not ref.startswith('#/'):
                        errors.append(f'Non-local schema reference requires review: {relative}')
                        continue
                    current = value
                    try:
                        for part in ref[2:].split('/'):
                            current = current[part.replace('~1', '/').replace('~0', '~')]
                        counts['schemaRefs'] += 1
                    except (KeyError, TypeError):
                        errors.append(f'Unresolved schema reference: {relative} -> {ref}')
            if path == root / 'examples/deployment.example.json':
                require(isinstance(value, dict) and value.get('status') == 'synthetic-design-example-not-runnable' and value.get('schedulesInstalled') is False and value.get('writerBinding') == 'disabled' and not value.get('connectorBindings') and not value.get('modelBindings'), 'Synthetic deployment must not claim active effects or bindings')
                counts['exampleInvariants'] += 1
            if path.parent == root / 'examples' and isinstance(value, dict) and 'recordType' in value:
                errors.extend(f'{relative}: {item}' for item in selected_record_errors(value))
                counts['exampleInvariants'] += 1

    manifest_path = root / 'PUBLICATION_MANIFEST.json'
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            entries = manifest['files']
            expected = {repository_path(p, root) for p in files if p != manifest_path}
            actual = [entry['path'] for entry in entries]
            require(len(actual) == len(set(actual)) and set(actual) == expected, 'Publication manifest file set mismatch')
            for entry in entries:
                path = (root / entry['path']).resolve()
                if not path.is_relative_to(root) or not path.is_file():
                    errors.append('Publication manifest path escapes checkout or is missing')
                    continue
                content = path.read_bytes()
                require(len(content) == entry['bytes'] and hashlib.sha256(content).hexdigest() == entry['sha256'], f'Publication manifest hash/size mismatch: {entry["path"]}')
            counts['manifestFiles'] = len(entries)
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            errors.append('Invalid publication manifest')
    return {'schemaVersion': '1.0', 'scope': 'Public checkout integrity and selected design invariants; no live connector, runtime, ranking or complete JSON Schema validation', 'checks': counts, 'manifestVerified': manifest_path.exists(), 'errors': errors, 'result': 'PASS' if not errors else 'FAIL'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = validate(args.root)
    print(json.dumps(report, indent=2))
    return 0 if report['result'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())

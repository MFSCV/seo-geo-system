"""Negative tests for publication integrity boundaries; all fixtures are synthetic."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'validate_repository.py'
ROOT = SCRIPT.parent.parent
SPEC = importlib.util.spec_from_file_location('repository_validator', SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class RecordBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.record = {'schemaVersion': '0.1.0', 'recordType': 'observation',
                       'payload': {'result': {'outcome': 'unknown', 'reason': 'No evidence collected.'}}}

    def test_unknown_does_not_become_measured_zero(self):
        self.assertEqual([], validator.selected_record_errors(self.record))
        changed = deepcopy(self.record)
        changed['payload']['result']['value'] = 0
        self.assertTrue(validator.selected_record_errors(changed))

    def test_unknown_requires_reason(self):
        self.record['payload']['result'].pop('reason')
        self.assertTrue(validator.selected_record_errors(self.record))

    def test_bool_is_not_a_measured_number(self):
        self.record['payload']['result'] = {'outcome': 'observed', 'value': False, 'denominator': 1}
        self.assertTrue(validator.selected_record_errors(self.record))

    def test_review_must_bind_exact_proposal(self):
        self.assertTrue(validator.selected_record_errors({'schemaVersion': '0.1.0', 'recordType': 'review', 'payload': {'proposalSha256': 'latest'}}))
        self.assertEqual([], validator.selected_record_errors({'schemaVersion': '0.1.0', 'recordType': 'review', 'payload': {'proposalSha256': 'a' * 64}}))

    def test_unknown_major_is_rejected(self):
        self.record['schemaVersion'] = '1.0.0'
        self.assertTrue(validator.selected_record_errors(self.record))


class PublicationBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / 'checkout'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__', '.venv'))

    def errors(self):
        return validator.validate(self.root)['errors']

    def test_local_link_escape_is_rejected(self):
        self.assertTrue(validator.check_local_target(self.root, self.root / 'README.md', '../outside.md'))

    def test_fenced_example_is_not_a_navigable_link(self):
        self.assertEqual(['README.md'], list(validator.markdown_links('```text\n[x](absent.md)\n```\n[read](README.md)')))

    def test_invented_connector_implementation_is_rejected(self):
        target = self.root / 'catalog/connector-operations.csv'
        target.write_text(target.read_text().replace('NOT_IMPLEMENTED', 'IMPLEMENTED', 1))
        self.assertIn('Unsupported operation implementation claim', self.errors())

    def test_unknown_observation_fixture_cannot_hide_missing_measurement(self):
        target = self.root / 'examples/unknown-observation.example.json'
        record = json.loads(target.read_text())
        record['payload']['result']['value'] = 0
        target.write_text(json.dumps(record))
        self.assertTrue(any('Unknown observation cannot carry' in item for item in self.errors()))

    def test_synthetic_deployment_cannot_claim_installed_schedule(self):
        target = self.root / 'examples/deployment.example.json'
        record = json.loads(target.read_text())
        record['schedulesInstalled'] = True
        target.write_text(json.dumps(record))
        self.assertIn('Synthetic deployment must not claim active effects or bindings', self.errors())

    def test_token_marker_is_reported_without_the_value(self):
        token = 'gh' + 'p_' + 'x' * 36
        (self.root / 'synthetic-secret.txt').write_text(token)
        report = validator.validate(self.root)
        self.assertTrue(any('github-token' in item for item in report['errors']))
        self.assertNotIn(token, json.dumps(report))

    def test_manifest_detects_unlisted_file(self):
        (self.root / 'PUBLICATION_MANIFEST.json').write_text(json.dumps({'files': []}))
        self.assertIn('Publication manifest file set mismatch', self.errors())


if __name__ == '__main__':
    unittest.main()

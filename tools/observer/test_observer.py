import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).with_name('observe.py')


class ObserverTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('seo_observe', MODULE)
        self.observer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.observer)

    def test_missing_source_is_unknown_not_zero_or_healthy(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.observer.check_files(Path(tmp), [{'path': 'missing.json', 'sha256': '0'*64}])
            self.assertEqual(result[0]['state'], 'unavailable')
            self.assertIsNone(result[0]['actual_sha256'])

    def test_approved_hash_detects_modified_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'source.txt').write_text('changed')
            result = self.observer.check_files(root, [{'path': 'source.txt', 'sha256': '0'*64}])
            self.assertEqual(result[0]['state'], 'changed')

    def test_approved_hash_detects_unchanged_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'source.txt').write_text('same')
            result = self.observer.check_files(root, [{'path': 'source.txt', 'sha256': hashlib.sha256(b'same').hexdigest()}])
            self.assertEqual(result[0]['state'], 'verified')

    def test_paths_cannot_escape_selected_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            for path in ['../outside.json', '/etc/passwd', 'C:\\outside.json']:
                with self.assertRaises(ValueError):
                    self.observer.safe_file(Path(tmp), path)

    def test_symlink_is_rejected_even_when_target_inside(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'real').write_text('source')
            (root/'link').symlink_to(root/'real')
            with self.assertRaises(ValueError):
                self.observer.safe_file(root, 'link')

    def test_same_evidence_has_same_fingerprint(self):
        rows = [{'path': 'a', 'state': 'verified', 'actual_sha256': 'abc'}]
        first = self.observer.observation_key(rows, {'policy': 'v1'})
        self.assertEqual(first, self.observer.observation_key(rows, {'policy': 'v1'}))
        self.assertNotEqual(first, self.observer.observation_key(rows, {'policy': 'v2'}))

    def test_changed_order_has_same_fingerprint(self):
        rows = [{'path': 'a', 'state': 'verified'}, {'path': 'b', 'state': 'unavailable'}]
        self.assertEqual(self.observer.observation_key(rows, {}), self.observer.observation_key(list(reversed(rows)), {}))

    def test_file_limit_is_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                self.observer.check_files(Path(tmp), [{}]*201)

    def test_oversized_file_is_not_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'large').write_bytes(b'0'*4_000_001)
            result = self.observer.check_files(root, [{'path': 'large', 'sha256': '0'*64}])
            self.assertEqual(result[0]['state'], 'unreadable_size_limit')
            self.assertIsNone(result[0]['actual_sha256'])

    def test_profile_cannot_enable_product_writes(self):
        root = MODULE.parents[2]
        config = json.loads((root/'agents/orchestration.example.json').read_text())
        config['execution']['websiteWrites'] = True
        self.assertIn('website_writes_outside_initial_scope', self.observer.validate_config(root, config))

    def test_duplicate_role_is_rejected(self):
        root = MODULE.parents[2]
        config = json.loads((root/'agents/orchestration.example.json').read_text())
        config['roles'].append(config['roles'][0])
        self.assertIn('role_set_invalid', self.observer.validate_config(root, config))

    def test_example_inspection_has_no_effect_or_runtime_claim(self):
        result = self.observer.inspect(MODULE.parents[2])
        self.assertEqual(result['validationErrors'], [])
        self.assertEqual(result['roles'], 14)
        self.assertFalse(result['websiteInspected'])
        self.assertFalse(result['persistentStateWritten'])
        self.assertEqual(result['externalNotifications'], 0)
        self.assertEqual(result['modelCallsMade'], 0)
        self.assertEqual(result['indexState'], 'unknown')


if __name__ == '__main__':
    unittest.main()

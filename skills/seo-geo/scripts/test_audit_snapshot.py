"""Behavioral tests for the offline capture auditor; no network or fixtures needed."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("audit_snapshot.py")
GOOD_HTML = '''<!doctype html><html lang="pt-PT"><head>
<title>Health &amp; Information — café</title>
<meta name="description" content="Public information.">
<link rel="canonical" href="https://example.org/health">
<link rel="alternate" hreflang="pt-PT" href="https://example.org/health">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","@id":"https://example.org/health#page"}</script>
</head><body>Private raw body must never be reported.</body></html>'''


def good_document():
    return {
        "url": "https://example.org/health",
        "status": 200,
        "headers": {},
        "html": GOOD_HTML,
        "expected": {"indexable": True, "canonical": "https://example.org/health",
                     "locale": "pt-PT", "title": "Health & Information — café"},
    }


class SnapshotAuditTests(unittest.TestCase):
    def run_audit(self, payload=None, *, raw=None, args=()):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            input=raw if raw is not None else json.dumps(payload),
            text=True, capture_output=True, check=False,
        )
        self.assertTrue(result.stdout.strip(), result.stderr)
        return result, json.loads(result.stdout)

    def document_report(self, document):
        result, report = self.run_audit({"document": document})
        return result, report["documents"][0]

    def codes(self, report):
        return {item["code"] for item in report["findings"]}

    def test_good_capture_has_no_errors_and_decodes_title_entities(self):
        result, report = self.run_audit({"document": good_document()})
        self.assertEqual(result.returncode, 0, report)
        self.assertEqual(report["scope"], "offline-capture-not-live")
        self.assertEqual(report["schemaVersion"], "1.0")
        self.assertEqual(report["summary"]["error"], 0)
        self.assertEqual(report["documents"][0]["offlineIndexability"],
                         "not-blocked-by-captured-signals")
        self.assertNotIn("title.mismatch", self.codes(report["documents"][0]))

    def test_unexpected_generic_noindex_is_error(self):
        doc = good_document()
        doc["html"] = doc["html"].replace("</head>", '<meta name="robots" content="NOINDEX, follow"></head>')
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertIn("robots.unexpected_noindex", self.codes(report))
        self.assertTrue(report["signals"]["robots"]["genericNoindex"])

    def test_intentional_noindex_is_not_an_error(self):
        doc = good_document()
        doc["expected"]["indexable"] = False
        doc["html"] = doc["html"].replace("</head>", '<meta name="robots" content="none"></head>')
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("robots.unexpected_noindex", self.codes(report))
        self.assertNotIn("protected.missing_noindex", self.codes(report))
        self.assertTrue(report["signals"]["robots"]["genericNofollow"])

    def test_nofollow_does_not_mean_noindex(self):
        doc = good_document()
        doc["html"] = doc["html"].replace("</head>", '<meta name="robots" content="nofollow"></head>')
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 0)
        self.assertFalse(report["signals"]["robots"]["genericNoindex"])
        self.assertTrue(report["signals"]["robots"]["genericNofollow"])

    def test_bot_specific_noindex_keeps_its_scope(self):
        doc = good_document()
        doc["html"] = doc["html"].replace("</head>", '<meta name="googlebot" content="noindex"></head>')
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(report["signals"]["robots"]["genericNoindex"])
        self.assertEqual(report["signals"]["robots"]["botNoindex"], ["googlebot"])
        finding = next(f for f in report["findings"] if f["code"] == "robots.unexpected_noindex")
        self.assertEqual(finding["evidence"]["scopes"], ["googlebot"])

    def test_header_list_and_per_bot_directives_are_respected(self):
        doc = good_document()
        doc["headers"] = {"x-ROBOTS-tag": ["bingbot: noindex, nofollow", "noarchive"]}
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["signals"]["robots"]["botNoindex"], ["bingbot"])
        self.assertFalse(report["signals"]["robots"]["genericNoindex"])
        self.assertFalse(report["signals"]["robots"]["genericNofollow"])

    def test_header_string_generic_noindex_blocks_capture(self):
        doc = good_document()
        doc["headers"] = {"X-Robots-Tag": "noindex, nofollow"}
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["offlineIndexability"], "blocked")

    def test_protected_page_without_noindex_is_warning(self):
        doc = good_document()
        doc["expected"]["indexable"] = False
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 0)
        finding = next(f for f in report["findings"] if f["code"] == "protected.missing_noindex")
        self.assertEqual(finding["severity"], "warning")

    def test_absent_headers_never_claims_complete_capture_eligibility(self):
        doc = good_document()
        del doc["headers"]
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["offlineIndexability"], "unknown")
        self.assertIn("capture.headers_unknown", self.codes(report))

    def test_absent_status_and_fetch_error_are_unknown(self):
        for doc in ({"url": "https://example.org/", "fetchError": "secret internal failure"},
                    {"url": "https://example.org/", "html": GOOD_HTML, "headers": {}}):
            with self.subTest(document=doc):
                result, report = self.document_report(doc)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(report["offlineIndexability"], "unknown")
                self.assertIn("capture.status_unknown", self.codes(report))
                self.assertNotIn("secret internal failure", json.dumps(report))

    def test_non_200_expected_indexable_is_error(self):
        doc = good_document()
        doc["status"] = 404
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertIn("http.non_200", self.codes(report))

    def test_missing_title_and_description_are_findings(self):
        doc = good_document()
        doc["html"] = '<html><head><link rel="canonical" href="https://example.org/health"></head></html>'
        result, report = self.document_report(doc)
        self.assertTrue({"title.missing", "description.missing"} <= self.codes(report))

    def test_canonical_duplicate_is_error_even_when_same_url(self):
        doc = good_document()
        doc["html"] = doc["html"].replace("</head>", '<link rel="canonical" href="https://example.org/health"></head>')
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertIn("canonical.duplicate", self.codes(report))

    def test_missing_canonical_is_finding(self):
        doc = good_document()
        doc["html"] = '<html lang="pt-PT"><head><title>X</title><meta name="description" content="Y"></head></html>'
        _, report = self.document_report(doc)
        self.assertIn("canonical.missing", self.codes(report))

    def test_relative_or_non_http_canonical_is_invalid(self):
        for value in ("/PRIVATE-RELATIVE", "javascript:alert(1)", "https://user:password@example.org/health"):
            with self.subTest(value=value):
                doc = good_document()
                doc["html"] = doc["html"].replace('href="https://example.org/health"', 'href="' + value + '"', 1)
                result, report = self.document_report(doc)
                self.assertEqual(result.returncode, 1)
                self.assertIn("canonical.invalid", self.codes(report))
                self.assertNotIn(value, json.dumps(report))

    def test_canonical_mismatch_and_cross_origin_are_reported(self):
        doc = good_document()
        doc["html"] = doc["html"].replace('href="https://example.org/health"', 'href="https://other.test/else?token=SECRET#SECRET"', 1)
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertTrue({"canonical.mismatch", "canonical.cross_origin"} <= self.codes(report))
        self.assertNotIn("SECRET", json.dumps(report))

    def test_explicit_port_zero_is_not_the_default_origin_or_canonical(self):
        doc = good_document()
        doc["html"] = doc["html"].replace('href="https://example.org/health"', 'href="https://example.org:0/health"', 1)
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertTrue({"canonical.mismatch", "canonical.cross_origin"} <= self.codes(report))
        self.assertFalse(report["signals"]["canonical"]["sameOrigin"])

    def test_title_and_locale_expected_values_are_compared(self):
        doc = good_document()
        doc["expected"]["title"] = "Another secret title"
        doc["expected"]["locale"] = "en-GB"
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertTrue({"title.mismatch", "locale.mismatch"} <= self.codes(report))
        self.assertNotIn("Another secret title", json.dumps(report))

    def test_hreflang_duplicates_and_invalid_urls_are_reported(self):
        doc = good_document()
        doc["html"] = doc["html"].replace("</head>", '<link rel="alternate" hreflang="PT-pt" href="/relative?token=SECRET"></head>')
        _, report = self.document_report(doc)
        self.assertTrue({"hreflang.duplicate", "hreflang.invalid_url"} <= self.codes(report))
        self.assertNotIn("SECRET", json.dumps(report))

    def test_invalid_jsonld_is_error_without_echoing_payload(self):
        doc = good_document()
        doc["html"] = doc["html"].replace("</head>", '<script type="application/ld+json">{"private": SECRET}</script></head>')
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertIn("jsonld.invalid_json", self.codes(report))
        self.assertNotIn("SECRET", json.dumps(report))

    def test_unclosed_jsonld_is_unknown_instead_of_silently_disappearing(self):
        doc = good_document()
        doc["html"] = doc["html"].split('<script type="application/ld+json">', 1)[0] + '<script type="application/ld+json">{"private": SECRET'
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["offlineIndexability"], "unknown")
        self.assertEqual(report["signals"]["structuredData"]["blocks"], 1)
        finding = next(f for f in report["findings"] if f["code"] == "jsonld.incomplete_block")
        self.assertEqual(finding["severity"], "unknown")
        self.assertNotIn("SECRET", result.stdout + result.stderr)

    def test_jsonld_duplicate_and_contradictory_id_are_findings(self):
        doc = good_document()
        doc["html"] = doc["html"].replace("</head>", '<script type="application/ld+json">{"@graph":[{"@id":"PRIVATE-ID","name":"A"},{"@id":"PRIVATE-ID","name":"B"}]}</script></head>')
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertTrue({"jsonld.duplicate_id", "jsonld.conflicting_id"} <= self.codes(report))
        self.assertNotIn("PRIVATE-ID", json.dumps(report))

    def test_conflicting_jsonld_values_are_found_after_a_complementary_node(self):
        doc = good_document()
        doc["html"] = doc["html"].replace("</body>", '<script type="application/ld+json">[{"@id":"node","name":"A"},{"@id":"node","name":"B"},{"@id":"node","@type":"Thing"}]</script></body>')
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 1)
        self.assertIn("jsonld.conflicting_id", self.codes(report))

    def test_script_and_comment_literals_do_not_become_head_elements(self):
        doc = good_document()
        doc["html"] = doc["html"].replace("</head>", '''<script>var html = '<meta name="robots" content="noindex"><link rel="canonical" href="https://untrusted.test/">';</script>
<!-- <meta name="robots" content="noindex"> -->
</head>''')
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["signals"]["canonical"]["count"], 1)
        self.assertFalse(report["signals"]["robots"]["genericNoindex"])

    def test_body_meta_is_not_interpreted_as_head_metadata(self):
        doc = good_document()
        doc["html"] = doc["html"].replace("</body>", '<meta name="robots" content="noindex"></body>')
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 0)
        self.assertFalse(report["signals"]["robots"]["genericNoindex"])

    def test_html_attributes_without_values_do_not_crash_the_audit(self):
        doc = good_document()
        doc["html"] = doc["html"].replace("</head>", '<meta name><meta name="description" content><link rel><script type>var x = 1;</script></head>')
        result, report = self.document_report(doc)
        self.assertEqual(result.returncode, 0, report)
        self.assertFalse(report["signals"]["robots"]["genericNoindex"])

    def test_urls_always_redact_query_and_fragment_without_echoing_raw_text(self):
        doc = good_document()
        doc["url"] += "?auth=URL-SECRET#URL-SECRET"
        doc["expected"]["canonical"] += "?auth=EXPECTED-SECRET#EXPECTED-SECRET"
        doc["html"] = doc["html"].replace('href="https://example.org/health"', 'href="https://example.org/health?token=HREF-SECRET#HREF-SECRET"')
        _, report = self.document_report(doc)
        serialized = json.dumps(report)
        self.assertEqual(report["url"], "https://example.org/health")
        self.assertNotIn("SECRET", serialized)
        self.assertNotIn("Private raw body", serialized)
        self.assertNotIn("Public information", serialized)

    def test_percent_encoded_international_path_is_a_valid_http_url(self):
        doc = good_document()
        doc["url"] = "https://example.org/%C3%89ducation?auth=SECRET"
        result, report = self.run_audit({"document": doc})
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["documents"][0]["url"], "https://example.org/%C3%89ducation")

    def test_batch_has_per_document_findings_and_aggregate_exit(self):
        bad = copy.deepcopy(good_document())
        bad["status"] = 503
        result, report = self.run_audit({"documents": [good_document(), bad]})
        self.assertEqual(result.returncode, 1)
        self.assertEqual(len(report["documents"]), 2)
        self.assertEqual(report["summary"]["documents"], 2)

    def test_invalid_json_shape_types_and_urls_use_exit_2(self):
        cases = ["not json", "[]", "{}", '{"documents":[]}',
                 json.dumps({"document": good_document(), "documents": [good_document()]}),
                 json.dumps({"document": {"url": "ftp://example.org/"}}),
                 json.dumps({"document": {"url": "https://person:SECRET@example.org/"}}),
                 json.dumps({"document": {"url": "https://example.org/\nSECRET"}}),
                 json.dumps({"document": {"url": "https://example.org/%0ASECRET"}}),
                 json.dumps({"document": {"url": "https://example.org/", "status": True}}),
                 json.dumps({"document": {"url": "https://example.org/", "headers": []}}),
                 json.dumps({"document": {"url": "https://example.org/", "expected": {"indexable": "yes"}}})]
        for raw in cases:
            with self.subTest(raw=raw):
                result, report = self.run_audit(raw=raw)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(report["error"]["code"], "input.invalid")
                self.assertNotIn("SECRET", result.stdout + result.stderr)

    def test_input_over_four_mib_is_rejected(self):
        result, report = self.run_audit(raw='{"document":{"url":"https://example.org/","html":"' + "a" * (4 * 1024 * 1024) + '"}}')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["error"]["code"], "input.too_large")

    def test_file_input_and_create_only_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "capture.json"
            output = Path(tmp) / "report.json"
            source.write_text(json.dumps({"document": good_document()}), encoding="utf-8")
            result, report = self.run_audit(raw="", args=("--input", str(source), "--output", str(output)))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), report)
            output.write_text("DO NOT OVERWRITE", encoding="utf-8")
            result, report = self.run_audit(raw="", args=("--input", str(source), "--output", str(output)))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(report["error"]["code"], "output.exists")
            self.assertEqual(output.read_text(), "DO NOT OVERWRITE")

    def test_invalid_invocation_is_json_exit_2(self):
        result, report = self.run_audit(raw="", args=("--not-an-option",))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["error"]["code"], "invocation.invalid")


if __name__ == "__main__":
    unittest.main()

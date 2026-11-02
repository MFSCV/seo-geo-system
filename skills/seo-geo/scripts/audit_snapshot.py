#!/usr/bin/env python3
"""Audit supplied HTML captures offline. No requests, script execution or crawling.

Input: {"document": {...}} or {"documents": [{...}, ...]} on stdin/--input.
Exit codes: 0 no error findings; 1 error findings; 2 invalid input/invocation.
--output creates a new local file exclusively; it never replaces an existing file.
Reports omit raw HTML, textual metadata, header values and URL queries/fragments.
"""

import argparse
from collections import Counter
from html.parser import HTMLParser
import json
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit, urlunsplit


MAX_INPUT_BYTES = 4 * 1024 * 1024
SCHEMA_VERSION = "1.0"
SCOPE = "offline-capture-not-live"
LANGUAGE = re.compile(r"[a-zA-Z]{2,8}(?:-[a-zA-Z0-9]{1,8})*\Z")
DIRECTIVES = {"noindex", "nofollow", "index", "follow", "noarchive", "nosnippet",
              "noimageindex", "notranslate"}


class AuditError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


def invalid(message="Capture does not match the documented input contract."):
    raise AuditError("input.invalid", message)


def parse_url(value):
    """Validate absolute HTTP(S) without silently stripping unsafe characters."""
    if not isinstance(value, str) or not value:
        raise ValueError("invalid URL")
    if any(c.isspace() or unicodedata.category(c).startswith("C") for c in value):
        raise ValueError("invalid URL")
    if any(unicodedata.category(c).startswith("C") for c in unquote(value)):
        raise ValueError("invalid URL")
    parts = urlsplit(value)
    if (parts.scheme.lower() not in {"http", "https"} or not parts.hostname
            or parts.username is not None or parts.password is not None
            or "\\" in value or "%" in parts.hostname):
        raise ValueError("invalid URL")
    _ = parts.port  # Access validates malformed/out-of-range ports.
    return parts


def origin(parts):
    return (parts.scheme.lower(), parts.hostname.lower(),
            parts.port if parts.port is not None else (443 if parts.scheme.lower() == "https" else 80))


def url_identity(value):
    parts = parse_url(value)
    return origin(parts) + (parts.path or "/", parts.query)


def safe_url(value):
    parts = parse_url(value)
    host = parts.hostname.lower()
    if ":" in host:
        host = "[" + host + "]"
    if parts.port is not None:
        host += ":" + str(parts.port)
    return urlunsplit((parts.scheme.lower(), host, parts.path or "/", "", ""))


def normalized_text(value):
    return " ".join(value.split())


def validate_document(doc):
    if not isinstance(doc, dict):
        invalid()
    try:
        parse_url(doc.get("url"))
    except (ValueError, TypeError):
        invalid("Each document requires a valid absolute HTTP(S) URL without credentials or controls.")
    status = doc.get("status")
    if status is not None and (type(status) is not int or not 100 <= status <= 599):
        invalid("Status must be an HTTP integer from 100 to 599, or null.")
    if doc.get("html") is not None and not isinstance(doc["html"], str):
        invalid("HTML must be a string or null.")
    headers = doc.get("headers")
    if headers is not None:
        if not isinstance(headers, dict):
            invalid("Headers must be an object, or null when unknown.")
        for name, value in headers.items():
            if (not isinstance(name, str)
                    or not (isinstance(value, str) or (isinstance(value, list)
                            and all(isinstance(item, str) for item in value)))):
                invalid("Header values must be strings or lists of strings.")
    expected = doc.get("expected", {})
    if not isinstance(expected, dict):
        invalid("Expected must be an object.")
    if "indexable" in expected and type(expected["indexable"]) is not bool:
        invalid("Expected indexable must be a boolean.")
    for name in ("canonical", "locale", "title"):
        if name in expected and not isinstance(expected[name], str):
            invalid("Expected canonical, locale and title must be strings.")
    if "canonical" in expected:
        try:
            parse_url(expected["canonical"])
        except (ValueError, TypeError):
            invalid("Expected canonical must be a valid absolute HTTP(S) URL.")
    if "locale" in expected and not LANGUAGE.fullmatch(expected["locale"]):
        invalid("Expected locale must be a language tag.")


class CaptureParser(HTMLParser):
    """Collect metadata only from head, and JSON-LD from any script element.

    HTMLParser treats script/style data as CDATA and ignores comment contents.
    No unescaping is applied to script data: JSON-LD is parsed as authored.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.lang = None
        self.titles = []
        self.title = None
        self.descriptions = []
        self.robots = []
        self.canonicals = []
        self.hreflang = []
        self.jsonld = []
        self.script = None

    def handle_starttag(self, tag, attrs):
        attrs = {name: value or "" for name, value in attrs}
        if tag == "script":
            self.script = [] if attrs.get("type", "").split(";", 1)[0].strip().lower() == "application/ld+json" else None
        if tag == "html" and self.lang is None:
            self.lang = attrs.get("lang")
        if tag == "head":
            self.in_head = True
        if tag == "body":
            self.in_head = False
        if not self.in_head:
            return
        if tag == "title":
            self.title = []
        elif tag == "meta":
            name = attrs.get("name", "").lower()
            if name == "description":
                self.descriptions.append(attrs.get("content", ""))
            elif name in {"robots", "googlebot"}:
                self.robots.append(("meta:" + name, "all" if name == "robots" else name,
                                    attrs.get("content", "")))
        elif tag == "link":
            rel = attrs.get("rel", "").lower().split()
            if "canonical" in rel:
                self.canonicals.append(attrs.get("href", ""))
            if "alternate" in rel and "hreflang" in attrs:
                self.hreflang.append((attrs["hreflang"], attrs.get("href", "")))

    def handle_endtag(self, tag):
        if tag == "script" and self.script is not None:
            self.jsonld.append("".join(self.script))
            self.script = None
        if tag == "title" and self.title is not None:
            self.titles.append(normalized_text("".join(self.title)))
            self.title = None
        if tag in {"head", "html"}:
            self.in_head = False

    def handle_data(self, data):
        if self.script is not None:
            self.script.append(data)
        elif self.title is not None:
            self.title.append(data)


def robot_entries(source, initial_scope, value):
    """A bot prefix scopes subsequent comma-separated directives in that field."""
    scope = initial_scope
    entries = {}
    for part in value.lower().split(","):
        part = part.strip()
        match = re.match(r"([a-z][a-z0-9_-]*|\*):\s*(.*)\Z", part)
        if match:
            name, remainder = match.groups()
            # Directive parameters (e.g. unavailable_after/max-snippet) are not bot names.
            if name in {"unavailable_after", "max-snippet", "max-image-preview", "max-video-preview"}:
                continue
            scope = "all" if name == "*" else name
            part = remainder
        for word in part.split():
            if word == "none":
                directives = {"noindex", "nofollow"}
            elif word == "all":
                directives = {"index", "follow"}
            else:
                directives = {word} & DIRECTIVES
            if directives:
                entries.setdefault(scope, set()).update(directives)
    return [{"source": source, "scope": name, "directives": sorted(words)}
            for name, words in sorted(entries.items())]


def audit_document(doc, number):
    findings = []

    def add(code, severity, **evidence):
        findings.append({"id": "d%d-f%d" % (number, len(findings) + 1),
                         "code": code, "severity": severity, "evidence": evidence})

    expected = doc.get("expected", {})
    headers_known = isinstance(doc.get("headers"), dict)
    html_known = isinstance(doc.get("html"), str)
    status_known = doc.get("status") is not None and not doc.get("fetchError")
    if not status_known:
        add("capture.status_unknown", "unknown", statusProvided=doc.get("status") is not None,
            fetchErrorPresent=bool(doc.get("fetchError")))
    if not headers_known:
        add("capture.headers_unknown", "unknown")
    if not html_known:
        add("capture.html_unknown", "unknown")
    if status_known and doc["status"] != 200 and expected.get("indexable") is True:
        add("http.non_200", "error", status=doc["status"])

    parser = CaptureParser()
    if html_known:
        parser.feed(doc["html"])
        parser.close()
    incomplete_jsonld = parser.script is not None
    if incomplete_jsonld:
        add("jsonld.incomplete_block", "unknown", blockIndex=len(parser.jsonld) + 1,
            contentOmitted=True)
    entries = []
    for source, scope, value in parser.robots:
        entries.extend(robot_entries(source, scope, value))
    for name, value in (doc.get("headers") or {}).items():
        if name.lower() == "x-robots-tag":
            for field in value if isinstance(value, list) else [value]:
                entries.extend(robot_entries("header:x-robots-tag", "all", field))
    noindex_scopes = sorted({e["scope"] for e in entries if "noindex" in e["directives"]})
    generic_noindex = "all" in noindex_scopes
    generic_nofollow = any(e["scope"] == "all" and "nofollow" in e["directives"] for e in entries)
    if noindex_scopes and expected.get("indexable") is True:
        add("robots.unexpected_noindex", "error", scopes=noindex_scopes)
    if (expected.get("indexable") is False and not generic_noindex
            and headers_known and html_known):
        # This is an exposure-review prompt, not an access-control verdict. A local
        # capture cannot establish authentication, live crawling or index state.
        add("protected.missing_noindex", "warning", genericNoindexObserved=False,
            accessControlVerified=False)

    if html_known:
        if not parser.titles or not any(parser.titles):
            add("title.missing", "error" if "title" in expected else "warning", count=len(parser.titles))
        elif "title" in expected and (len(parser.titles) != 1 or parser.titles[0] != normalized_text(expected["title"])):
            add("title.mismatch", "error", count=len(parser.titles), textOmitted=True)
        if not any(normalized_text(d) for d in parser.descriptions):
            add("description.missing", "warning", count=len(parser.descriptions))
        if not parser.canonicals:
            add("canonical.missing", "error" if "canonical" in expected else "warning")
        elif len(parser.canonicals) > 1:
            add("canonical.duplicate", "error", count=len(parser.canonicals))

    canonical_urls = []
    same_origin = None
    for index, value in enumerate(parser.canonicals, 1):
        try:
            parts = parse_url(value)
        except (ValueError, TypeError):
            add("canonical.invalid", "error", linkIndex=index, valueOmitted=True)
            continue
        canonical_urls.append(safe_url(value))
        same_origin = origin(parts) == origin(parse_url(doc["url"]))
        if not same_origin:
            add("canonical.cross_origin", "warning", linkIndex=index, url=safe_url(value))
        if "canonical" in expected and url_identity(value) != url_identity(expected["canonical"]):
            add("canonical.mismatch", "error", linkIndex=index, actual=safe_url(value),
                expected=safe_url(expected["canonical"]), queryAndFragmentOmitted=True)

    lang = parser.lang.strip() if parser.lang else None
    valid_lang = bool(lang and LANGUAGE.fullmatch(lang))
    if html_known and "locale" in expected:
        if not lang:
            add("locale.missing", "error")
        elif not valid_lang or lang.lower() != expected["locale"].lower():
            add("locale.mismatch", "error", actual=lang if valid_lang else None,
                expected=expected["locale"])

    languages = Counter()
    for index, (language, value) in enumerate(parser.hreflang, 1):
        tag = language.strip().lower()
        languages[tag] += 1
        if tag != "x-default" and not LANGUAGE.fullmatch(tag):
            add("hreflang.invalid_locale", "warning", linkIndex=index, valueOmitted=True)
        try:
            parse_url(value)
        except (ValueError, TypeError):
            add("hreflang.invalid_url", "warning", linkIndex=index, valueOmitted=True)
    for tag, count in sorted(languages.items()):
        if count > 1:
            add("hreflang.duplicate", "warning", count=count,
                locale=tag if tag == "x-default" or LANGUAGE.fullmatch(tag) else None)

    valid_blocks = 0
    nodes = []
    for index, raw in enumerate(parser.jsonld, 1):
        try:
            value = json.loads(raw, parse_constant=lambda _: invalid_json_constant())
        except (ValueError, RecursionError):
            add("jsonld.invalid_json", "error", blockIndex=index, contentOmitted=True)
            continue
        valid_blocks += 1
        pending = [value]
        while pending:
            node = pending.pop()
            if isinstance(node, dict):
                if isinstance(node.get("@id"), str):
                    nodes.append(node)
                pending.extend(node.values())
            elif isinstance(node, list):
                pending.extend(node)
    seen = {}
    for index, node in enumerate(nodes, 1):
        identifier = node["@id"]
        if identifier in seen:
            prior_index, prior, owners = seen[identifier]
            add("jsonld.duplicate_id", "warning", nodeIndexes=[prior_index, index], idOmitted=True)
            conflicts = [key for key in sorted(prior.keys() & node.keys() - {"@id"})
                         if prior[key] != node[key]]
            if conflicts:
                add("jsonld.conflicting_id", "error", nodeIndexes=[owners[conflicts[0]], index], idOmitted=True)
            for key in node.keys() - prior.keys():
                prior[key] = node[key]
                owners[key] = index
        else:
            seen[identifier] = (index, dict(node), {key: index for key in node})

    if generic_noindex or (status_known and doc["status"] != 200):
        indexability = "blocked"
    elif noindex_scopes or incomplete_jsonld or not (status_known and headers_known and html_known):
        indexability = "unknown"
    else:
        indexability = "not-blocked-by-captured-signals"
    return {
        "id": "document-%d" % number, "url": safe_url(doc["url"]),
        "capture": {"status": doc.get("status") if status_known else None,
                    "headers": "provided" if headers_known else "unknown",
                    "html": "provided" if html_known else "unknown"},
        "offlineIndexability": indexability,
        "signals": {
            "title": {"count": len(parser.titles), "present": any(parser.titles)},
            "description": {"count": len(parser.descriptions),
                            "present": any(normalized_text(d) for d in parser.descriptions)},
            "canonical": {"count": len(parser.canonicals), "urls": canonical_urls,
                          "sameOrigin": same_origin if len(parser.canonicals) == 1 else None},
            "locale": lang if valid_lang else None,
            "hreflang": {"count": len(parser.hreflang)},
            "robots": {"entries": entries, "genericNoindex": generic_noindex,
                       "genericNofollow": generic_nofollow,
                       "botNoindex": [s for s in noindex_scopes if s != "all"]},
            "structuredData": {"blocks": len(parser.jsonld) + int(incomplete_jsonld),
                               "incompleteBlocks": int(incomplete_jsonld), "validJsonBlocks": valid_blocks,
                               "identifiedNodes": len(nodes)}},
        "findings": findings,
    }


def invalid_json_constant():
    raise ValueError("Non-standard JSON constant")


def audit(payload):
    """Return a report for a validated single/batch envelope; never perform I/O."""
    if not isinstance(payload, dict) or ("document" in payload) == ("documents" in payload):
        invalid("Provide exactly one of document or documents.")
    documents = [payload["document"]] if "document" in payload else payload["documents"]
    if not isinstance(documents, list) or not documents:
        invalid("Documents must be a nonempty list.")
    for doc in documents:
        validate_document(doc)
    reports = [audit_document(doc, index) for index, doc in enumerate(documents, 1)]
    counts = Counter(f["severity"] for doc in reports for f in doc["findings"])
    return {"schemaVersion": SCHEMA_VERSION, "scope": SCOPE, "documents": reports,
            "summary": {"documents": len(reports),
                        **{severity: counts[severity] for severity in ("error", "warning", "unknown")}}}


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise AuditError("invocation.invalid", "Use --input PATH and/or --output PATH.")


def main(argv=None):
    try:
        parser = JsonArgumentParser(description=__doc__)
        parser.add_argument("--input", metavar="PATH", help="Read UTF-8 JSON instead of stdin")
        parser.add_argument("--output", metavar="PATH", help="Create a new local JSON report (never overwrite)")
        args = parser.parse_args(argv)
        try:
            if args.input:
                with open(args.input, "rb") as source:
                    raw = source.read(MAX_INPUT_BYTES + 1)
            else:
                raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        except OSError:
            raise AuditError("input.unreadable", "Could not read the input file.") from None
        if len(raw) > MAX_INPUT_BYTES:
            raise AuditError("input.too_large", "Input exceeds the 4 MiB limit.")
        try:
            payload = json.loads(raw.decode("utf-8"), parse_constant=lambda _: invalid_json_constant())
        except (ValueError, UnicodeError, RecursionError):
            invalid("Input must be valid UTF-8 JSON.")
        report = audit(payload)
        output = json.dumps(report, ensure_ascii=True, indent=2) + "\n"
        if args.output:
            try:
                with open(args.output, "x", encoding="utf-8") as target:
                    target.write(output)
            except FileExistsError:
                raise AuditError("output.exists", "Output already exists; choose a new path.") from None
            except OSError:
                raise AuditError("output.unwritable", "Could not create the output file.") from None
        sys.stdout.write(output)
        return 1 if report["summary"]["error"] else 0
    except AuditError as exc:
        sys.stdout.write(json.dumps({"schemaVersion": SCHEMA_VERSION, "scope": SCOPE,
                                    "error": {"code": exc.code, "message": exc.message}}) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())

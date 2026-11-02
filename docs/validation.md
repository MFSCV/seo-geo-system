# Reproducible validation

Run the following from a fresh checkout using Python 3.11 or later. The checks use the standard library and require no accounts, credentials, private archives, model calls, package installation, or network requests.

```bash
python3 scripts/validate_repository.py
python3 -m unittest discover -s scripts/tests -v
python3 -m unittest discover -s skills/seo-geo/scripts -p 'test_*.py' -v
```

The agent-package README documents its separate local observer and tests. Running repository checks does not install schedules or operate a website.

## Repository checks

The validator resolves its checkout from its own location; `--root PATH` can select another candidate. It writes its JSON result to standard output and returns exit code `0` for a pass or `1` for a failure. A caller may redirect the result outside the checkout.

It checks:

- Stable catalog counts and identifiers: 144 capabilities, O0/S1–S13, 63 source connector rows, 76 proposed operation families and 190 consistent forward/reverse references.
- Ownership references, capability contract links and the explicit unimplemented/unqualified state of connector operation families.
- Navigable local Markdown links and heading anchors, including rejection of links outside the public checkout.
- JSON syntax and locally resolvable references in the supplied draft 2020-12 schemas.
- Selected design invariants: unknown observations cannot become measured zeroes, measured observations need a denominator, reviews bind a proposal digest, and the synthetic deployment cannot claim installed schedules or active bindings.
- Publication marker patterns for private local paths, private file identifiers, access-token shapes and private keys. Findings name the file and marker category without printing matched values.
- Exact file set, byte lengths and SHA-256 hashes when `PUBLICATION_MANIFEST.json` exists. The manifest excludes itself and Git/tooling cache metadata. A manifest is optional during development and must be regenerated for a changed publication candidate.

The unit tests exercise negative cases, including invented connector implementation claims, invented schedules, lost measurement evidence, checkout escape links, secret-shaped text and incomplete manifests.

## Interpretation and limits

These checks validate the public tree. They do not require or reconstruct the private source archives. The source-map hashes document historical lineage; the public manifest describes the actual exported files, which may be translated, generalized or replaced.

Schema-reference resolution and selected invariant checks are **not a complete JSON Schema validator**. They do not prove every possible record is schema-valid or that a future runtime enforces the schemas. Run a compatible full draft 2020-12 validator if complete instance validation is needed.

The marker check is a bounded text scan, not proof that personal data or secrets are absent. It cannot establish ownership, licenses of third-party material, absence of vulnerabilities, correctness of provider claims, live page delivery, search index state, rankings, connector qualification, or autonomous execution. Review these matters against the actual release scope and evidence.

A validation pass is useful only for the checked bytes. Record the candidate commit or publication manifest alongside results. Do not treat an earlier pass as verification of later changes.

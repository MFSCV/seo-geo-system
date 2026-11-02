# Contributing

Thank you for helping improve SEO/GEO System. Use [issues](https://github.com/MFSCV/seo-geo-system/issues) for ordinary defects and proposals; submit focused pull requests for changes. Report sensitive vulnerabilities using [SECURITY.md](SECURITY.md).

Write documentation, source comments, examples, and reports in English. Preserve stable CAP and agent IDs. Clearly label implemented behavior, proposed behavior, and unknowns. A capability catalog entry is not an adapter, and a successful local check is not evidence of live publication or search indexing.

For each change describe the concrete problem, affected components, behavior after the change, evidence, checks, and material tradeoffs. Cite authoritative sources with retrieval/effective dates for changing provider rules. Include migration and rollback when behavior changes. Prefer the smallest effective change over generic restrictions or unsupported optimization claims.

Use synthetic fixtures. Do not submit credentials, cookies, personal/customer data, private logs, raw production captures, or material you lack permission to redistribute. State the origin of contributed files and preserve required third-party notices.

Contributions are accepted under the repository's [MIT License](LICENSE). By submitting a contribution you confirm that you have the right to contribute it under those terms. No contributor agreement or ownership transfer is required.

Run the documented checks for affected components. For the offline auditor:

```bash
python3 -m unittest discover -s skills/seo-geo/scripts -p 'test_*.py'
python3 -m unittest discover -s tools/observer -p 'test_*.py'
```

New connectors need operation-level authorization and integration evidence before being advertised as functional. Method changes need evaluation with negative/inconclusive cases. Public pull requests must not require production secrets or privileged runners.

The maintainer reviews compatibility, evidence, rights, and scope before merging. Response times are best effort; independent review is welcome, but a second reviewer is not guaranteed in this initially single-maintainer project.

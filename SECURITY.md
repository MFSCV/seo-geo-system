# Security Policy

## Supported scope

The initial source distribution contains a reusable method, agent specifications, and local source tools. There is no supported autonomous production runtime or qualified live connector release. Security fixes are considered for the current default branch; no support period, response-time commitment, bounty, safe-harbor agreement, or security certification is promised.

## Reporting

Private vulnerability reporting is enabled for this public repository. Use [Security → Report a vulnerability](https://github.com/MFSCV/seo-geo-system/security/advisories/new). This setting was verified on 2026-11-02. Do not place credentials, personal data, or exploitable details in a public issue.

If GitHub's private route is temporarily unavailable, contact [the maintainer](https://github.com/MFSCV) through an established private channel, or open a non-sensitive issue requesting a private route without describing the vulnerability.

Provide the affected revision/component, a minimal synthetic reproduction, controllable input, trust boundary, concrete consequence, preconditions, and proposed remedy where useful. Remove secrets and personal data. Do not test against real deployments, make bookings/charges, access private systems, or contact customers without the operator's authorization.

Relevant issues include unauthorized publication, wrong-target effects, credential leakage, SSRF, prompt-driven privilege escalation, untrusted CI execution, and duplicate side effects after recovery. Separate demonstrated vulnerabilities from hypotheses and optional hardening. Describe the smallest effective fix and its cost to legitimate use.

Ordinary method inaccuracies, broken links, unsupported capability claims, and documentation bugs may use [public issues](https://github.com/MFSCV/seo-geo-system/issues) when they contain no sensitive evidence. Deployment operators remain responsible for their own monitoring, incident response, credentials, and provider configuration.

See [security and effectiveness](docs/security-and-effectiveness.md) and [open-source readiness](docs/open-source-readiness.md) for the design's operational boundaries.

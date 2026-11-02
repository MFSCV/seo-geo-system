# Security and Effectiveness

The system must help legitimate discovery and conversion while preventing concrete harmful effects. Controls should be tied to a threat, trust boundary and measurable benefit. A hypothetical concern does not justify disabling an unrelated feature or blocking independent work.

## Threat boundaries and minimum effective controls

| Boundary or failure | Minimum effective control | Effectiveness guardrail |
|---|---|---|
| Fetched page/PDF/issue contains instructions | Treat source text as evidence; validate actions against trusted mandate outside the model | Keep useful source facts; do not discard all external content |
| Public URL fetch reaches private infrastructure | Validate origin, resolved destination and every redirect; restrict request/byte/depth/time budgets | Allow legitimate public CDN resources through explicit scoped policy |
| Connector token reaches another audience | Scoped binding and secret-store references; no token passthrough; redact logs | Qualify exact needed methods rather than demand broad account access |
| SEO proposal changes the wrong site or field | Target allowlist, authority, field owner, baseline hash and native writer | Continue unrelated observation and drafting |
| Concurrent editor changes a page | Fresh read, minimal patch, native lease/CAS where supported, conflict report | Preserve human changes rather than revert the whole site |
| Timeout after an effect | Durable operation ID and reconciliation before retry | Avoid duplicate submission, notification or transaction |
| Public export leaks private information | Allowlisted export; automated scans plus manual review and synthetic examples | Retain useful generic evidence and test coverage |
| Model-generated acceptance | Hash-bound review by actual competent authority | Do not add unnecessary clinical gates to nonclinical assets |
| Runaway calls or recursive churn | Cumulative budget broker, depth/pass/time caps, no-change result | Spend on new evidence or useful decisions |
| Search manipulation | Reject bought links, fabricated reviews/addresses and deceptive pages | Support legitimate directories, useful references and eligible profiles |

MCP token audience, SSRF and privilege boundaries follow the current official [security guidance](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices). These are implementation requirements to qualify, not proof that the proposed runtime already enforces them.

## Review form

For each proposed control record: observed threat and evidence; exploitable preconditions; affected scope; smallest effective change; residual risk; SEO/crawl impact; accessibility impact; latency/cost; conversion/operations impact; owner; validation and rollback. Label an untested concern as a hypothesis and optional hardening as optional.

## Concrete balance decisions

- A crawler policy can allow a verified search purpose while separately controlling training. Do not globally disable bot protection to seek citations; revalidate provider-specific bot rules before applying them.
- A missing fresh price must not erase an accepted service explanation. Qualify stale handling for price snippets, structured data and CTA separately.
- An outage in one metrics service does not stop a public HTML audit. Report narrower coverage rather than invent data or demand broad access.
- Do not cache private/member HTML to improve performance. Scope public cache changes to supported surfaces and verify source freshness and locale behavior.
- Keep publication through the native writer; avoid broad blanket approval prompts when a current mandate already covers a narrow, qualified operation.
- A small title change should receive focused title/locale/head/build verification. A new credential or writer boundary requires deeper qualification because the effect is different.

## Search integrity

Use descriptive titles, relevant content and true commercial facts; do not keyword-stuff or present structured data inconsistent with visible content. Google's [title guidance](https://developers.google.com/search/docs/appearance/title-link) and [spam policies](https://developers.google.com/search/docs/essentials/spam-policies) are provider rules to revalidate as they evolve.

Public examples and evaluation tasks must not perform real bookings, slot holds, charges, notifications, fake reviews or unsolicited outreach. Separate eligibility research from actual profile submission and commercial spend.

## Publication and CI

Fork contributions must not have production credentials or a route to privileged runners. Do not execute untrusted PR code in a privileged workflow. A read-only token setting controls token permission; it does not make a runner offline. The [open-source readiness plan](open-source-readiness.md) defines staged controls and evidence for a future release.

# Governance

The initial project owner and maintainer is [MFSCV](https://github.com/MFSCV), responsible for repository scope, licensing, review, and release decisions. This is initially a single-maintainer project; independent review and continuous availability are not guaranteed. No backup maintainer is currently designated.

Contributors may propose changes through issues and pull requests. Maintainer decisions should record evidence, tradeoffs, compatibility, and reasons for deferral. Popularity or model agreement does not replace validation. Breaking contract or authority changes require migration notes and explicit maintainer review.

O0 and S1–S13 are application roles, not repository governance positions. A public maintainer cannot grant access to a user's deployment; each deployment operator controls its own credentials, budgets, allowed actions, schedules, and publication authority.

Releases must identify the source revision, tested scope, limitations, and relevant changes. Untrusted contributions must not obtain production identities or release authority. Repository protections are operational settings and are not implied by this document; the publication record should state which are actually enabled.

Maintenance is best effort. If the maintainer becomes unavailable, no deployment should depend on automatic fixes. A future ownership transfer must preserve licensing and provenance. When active maintenance ends, update the README, mark unsupported components, and consider archival rather than leaving unsupported capability claims in place.

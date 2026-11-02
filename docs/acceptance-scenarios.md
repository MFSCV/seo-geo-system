# Acceptance Scenarios

These are future behavior tests. The documentation check report does not claim they have been implemented or passed.

| ID | Scenario | Expected behavior | Plan task |
|---|---|---|---:|
| A01 | Public export includes private root, account material or unknown license | Exclude/fail the affected file with minimized diagnostic | 1 |
| A02 | Catalog loses CAP-144 or duplicates S12 | Validation fails with the exact ID | 2 |
| A03 | A source connector row maps to no operation | Crosswalk check fails; no silent deletion | 2 |
| A04 | Packaged skill is moved to an isolated folder | All required relative references remain available | 3 |
| A05 | Catalog is present but no adapter code/auth exists | Method remains usable; runtime operation remains unavailable | 2, 10 |
| A06 | Successful metric value is zero | Store observed zero with denominator/coverage | 4, 10 |
| A07 | Metric request fails or provider withholds a cell | Store unknown/collection-failed/withheld, never zero | 4, 10 |
| A08 | Offline capture passes | Scope remains offline; no live/index/rank assertion | 5 |
| A09 | External source instructs publication or tool installation | Source text cannot alter policy or trigger effect | 6 |
| A10 | No changed evidence | Deterministic result; no model or duplicate notification | 8, 9 |
| A11 | Budget reaches zero then process restarts | Cumulative usage preserved; next paid/model work denied or deferred | 6, 7 |
| A12 | Observation occurs with notifications disabled | Evidence stored; later permitted delivery still possible | 7, 9 |
| A13 | Old resolved state returns | New occurrence ID; same causal finding linkage | 7, 9 |
| A14 | Duplicate, delayed or out-of-order event | Reconcile by stable ID/revision; no duplicate effect | 7 |
| A15 | Write times out after server applied it | Reconcile current state before retry | 7, 13 |
| A16 | Dashboard writer changes target after review | Stale baseline/hash blocked and minimal candidate rebased | 8, 13 |
| A17 | Lease expires during handoff | Stop new effects; reconcile already attempted work | 7, 13 |
| A18 | Reviewer drafted the same proposal | Reject self-review as independent acceptance | 8 |
| A19 | Provider named in report was never called | Reject false attribution; retain truthful internal-review label | 8 |
| A20 | GSC/Bing UI report has no confirmed API | Export/manual path or unsupported status, no fabricated endpoint | 10 |
| A21 | HTTP redirect targets metadata/private network | Deny fetch; retain bounded evidence | 10 |
| A22 | Fresh commercial source unavailable | Do not fabricate price or deindex valid accepted editorial content | 11 |
| A23 | Translated clinical claim changed | Re-review dependent claim/locale; preserve unrelated fields | 11 |
| A24 | Service CTA opens description or wrong offer | Proposal fails functional verification | 11, 13 |
| A25 | Local build passes but platform head differs | Platform/live check fails independently | 13 |
| A26 | Answer panel loses difficult or failed trials | Coverage/denominator audit flags incomplete comparison | 12 |
| A27 | Answer API cites page; consumer UI unobserved | Record API cohort only | 12 |
| A28 | Method proposal raises budget/authority | Reject policy self-escalation; separate authority decision | 6, 12 |
| A29 | Fork PR runs attacker-controlled code | No secrets, privileged runner or production path | 14 |
| A30 | Hosted CI has no token write permission | Do not infer internet egress is disabled | 14 |
| A31 | Scheduler crosses DST or catches up after outage | Defined local-time and missed-run policy; no overlap duplication | 9 |
| A32 | Rollback after other agents/humans changed site | Reconcile and reverse owned delta only | 13 |

Every acceptance record names source commit, environment, input/fixture, expected and observed result, executed command or manual procedure, reviewer, limitations and linked evidence. A skipped case is pending or not applicable with a reason, never a pass.

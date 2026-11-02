# Current public distribution

Version: **0.1.0**, 2026-11-02. Repository: [MFSCV/seo-geo-system](https://github.com/MFSCV/seo-geo-system).

This document describes the public checkout. The integration design and source-reconciliation documents describe the earlier 0.1.0-design baseline and future architecture. Where their historical statements differ from this distribution, this document, the root README, LICENSE and publication evidence describe the current scope. No future component is activated by publishing its specification.

| Component | Current availability |
|---|---|
| English integration design, implementation roadmap and acceptance scenarios | Included |
| Capability, role and connector-operation catalogs | Included; inventories are not implemented connectors |
| Self-contained SEO/GEO skill | Included under `skills/seo-geo/`; host-assisted procedural use |
| HTML capture auditor | Included; Python standard library, no network |
| O0 and S1–S13 agent profiles and common instructions | Included; specifications used by an authorized host |
| Local configuration and optional hash inspector | Included; read-only local checks |
| Autonomous inference executor, durable workflow engine and policy enforcement | Planned; not implemented |
| Live Google, Bing, CMS, model or social integrations | Planned; none ships as an authenticated adapter |
| Schedules, production publication, analytics, paid services or external outreach | Not installed or activated |

## Use and redistribution

All authored files in this public repository are distributed under the [MIT License](../LICENSE), including documentation, templates, schemas, original code and the new geometric icon. Source references remain links; external documentation, products and trademarks retain their owners' rights. Downloading, using and forking this repository requires no paid account or project subscription. Actual external providers may impose their own terms and costs if a deployment later connects them.

## Public export and history

The repository starts from a clean export, without the private source history. Private project profiles, operational paths, machine identifiers, customer data, credentials, queues, receipts, source archives and scheduler bindings are excluded. Their reusable methods and responsibilities are represented by English public instructions and synthetic examples. Historical source filenames and hashes in mapping catalogs identify provenance; they do not make the original private archives public.

The original native observer was adapted into a bounded local inspector; its queue delivery, checkpoints, leases and scheduler are not reproduced. The offline auditor's code is preserved. The icon is new original geometry rather than the source asset of uncertain provenance.

## Verification and limits

Run [the documented checks](validation.md) from a clean checkout. [Publication evidence](../verification.json) records actual local results. GitHub Actions runs the same checks on Ubuntu and Windows; its results are separate from local evidence. Hosted runners have network access; the shipped validation commands do not intentionally access the network. There are no production credentials or deployment jobs.

A clean export, marker scan and tests do not certify vulnerability absence, legal compliance or search results. Search-engine index state, ranking, answer citation and conversion are unmeasured in this release. Ranking and permanent top-five inclusion are not guaranteed.

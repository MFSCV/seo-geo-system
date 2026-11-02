# Wix adapter

## Establish the operating context

Load the relevant installed Wix skill and its required WixREADME/context flow. Resolve the existing site, installed apps, deployment mode, target resource and current authority; do not create or migrate a site to repair SEO. Discover current REST/SDK methods and exact schemas from primary Wix docs, not remembered URL patterns.

Distinguish Classic/Studio, Wix-managed Astro integration, managed without that integration and self-managed headless. Their injection/registry/sitemap responsibilities differ. A generic tool or installed app does not establish permissions, method version or propagation.

For managed Astro the dated documentation describes request-time injection for main pages, registry `/_wix/pages.json`, item-page registration/resolution and generated sitemap. Verify actual project integration. Secondary-language main-page SEO has documented platform limitations; neither dashboard fields nor a menu prove localized rendered metadata.

## Reconcile ownership

Map every field to source owner and projection: commercial Wix data, accepted editorial content, route/indexability policy, Wix native tags and final head. Do not globally replace the project's acceptance flow with dashboard authority. Preserve privacy/preview/error policy. Inspect final response after Wix injection, not only local Astro output.

Before changing root robots/sitemap, identify current publisher and reserved paths. List Sitemap Pages covers dynamic/business entries, not all static pages. An empty result is not evidence that home/about/contact are absent.

## Read → merge → set tags

Choose Site, Pattern or Item from the exact requested scope. Site accepts meta; titles/links/scripts belong to appropriate Item/Pattern operations. Reading tags/variables does not prove Manage SEO write permission.

1. Get the exact current target immediately before Set.
2. Preserve the complete tag collection, including unknown/unrelated tags.
3. Merge the concrete requested delta; do not send one tag as a partial array.
4. Validate inheritance/resolved source, actual variables and target identity.
5. Serialize writers, compare baseline/drift and retain snapshot/diff.
6. Apply within existing authority, record Set result, then independently inspect public HTML when required.

Writes replace the full collection. Methods without revision/CAS are last-write-wins: a local lock cannot exclude a human dashboard edit. Reduce the race window and qualify autonomy accordingly. Do not invent variable names or assume secondary-language write support. Static publish flags and dashboard tag changes can have live effects; determine the method's semantics first.

## Redirect operations: check the complete graph

Wix redirects are not generic chained rules. Dated primary docs state:
- Creating A→B can delete an existing rule whose from equals B.
- Redirects are live immediately and can take precedence over a real page.
- List is the bulk read; do not invent Query/Search/Update endpoints.
- Changing a rule may require delete/create, with an interval and partial failure risk.
- Language/options/trailing-slash semantics matter; no redirect webhook is documented.

Before any candidate write, read all existing rules and compare source/destination, real pages, locale and group rules. If the operation deletes/replaces another rule outside the mandate, present that exact effect for decision; do not rely on authorization for a harmless addition. Never add forceReplace or switch request shapes after an error to force success.

**Reference case:** existing /example-service→/services/example-service; request /old-service→/example-service while preserving /example-service. Creating that literal target is unsafe under these semantics. Prepare /old-service→the verified equivalent final landing as an alternative, preserve /example-service, and resolve any changed requested meaning before writing. Do not claim a two-hop chain will preserve both rules.

Snapshot old rules, verify every item in bulk results, reconcile unknown outcomes before retry and plan compensating recovery. Poll/reconcile redirects because event delivery must not be assumed.

## Bookings and direct calendar

Resolve service ID and documented calendar link/route from the actual integration. A shareable service-page URL and calendar URL have different behavior. A slug alone is not a destination contract. Test clean session, selected ID, supported locale, empty slots, refresh/new tab and actual first screen.

When a deployment requires direct calendar access, booking CTAs on the editorial landing should open date/time selection for the same service directly, preserving forms/professional selection/member/checkout. Do not create reservations, holds, charges or notifications during GET/prefetch/crawler validation.

Use public catalog and only public availability needed for the task. Do not export customers/bookings to an SEO agent. Source-price events can invalidate projections when actually supported; periodic reconciliation covers missed/unsupported events. Do not assume SEO/redirect webhooks because Bookings has other events.

## Primary documentation

Use sources.md S15–S18 plus:
- https://dev.wix.com/docs/api-reference/business-management/seo/item-seo-tags-v1/set-item-seo-tags
- https://dev.wix.com/docs/go-headless/wix-managed-headless/full-integration-astro/feature-guides/seo/add-seo-support-to-item-pages
- https://dev.wix.com/docs/go-headless/self-managed-headless/seo/about-seo-for-self-managed-headless-projects
- https://support.wix.com/en/article/wix-bookings-creating-and-managing-shareable-links

Recheck exact request/response/scopes before execution. Tool/API success alone is not public runtime verification.

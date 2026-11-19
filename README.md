# Holien milestones

The current view is the proposed SenditGo roadmap for 23 November 2026 through 31 March 2027. It schedules the supplied November work inventory, with feature-level windows, dependencies, conditional scope and AU acceptance milestones. The Notion links give the background for the work. The proposed dates are maintained here.

## Live

- [Current SenditGo roadmap](https://melissa-frontend-holieninnovation.github.io/holien-milestones-site/)
- [Version 1.7](https://melissa-frontend-holieninnovation.github.io/holien-milestones-site/v1.7/) with the continuous AU queue, weekly allocation and 19 November ticket snapshot
- [Version 1.6](https://melissa-frontend-holieninnovation.github.io/holien-milestones-site/v1.6/)
- [September portfolio](https://melissa-frontend-holieninnovation.github.io/holien-milestones-site/v1.5/) covering SenditGo, SenditSell and Sterling
- `/v3/` is the legacy pre-v1.4 alias.

## Updating this plan

Edit `roadmap/weeks.tsv` for weekly capacity, `roadmap/tickets.tsv` for checked board links and statuses, `roadmap/packages.tsv` for package dates and outcomes, `roadmap/build.py` for milestone and stream definitions, or `roadmap/template.html` for the page. Run `python3 roadmap/build.py` to render both the HTML and standalone SVG. The generator validates the complete package ID set and planning bounds. For a new release, advance the version before regenerating to retain the previous snapshot.

## Version archive

The September and August directories preserve the earlier publications byte for byte. Their
`Today` markers are baked at generation time and are **not** refreshed — that is the point of
an archive.

| Version | Built from | Header reads | Today marker | Notes |
|---|---|---|---|---|
| `v1.7` | November inventory and 19 November Notion board snapshot | SenditGo delivery roadmap | — | Ongoing AU intake, 19 weekly allocations and scoped ticket matches |
| `v1.6` | November work inventory | SenditGo delivery roadmap | — | 63 inventory packages and 4 QA milestones |
| `v1.5` | September snapshot | `v1.5` | 3 Sep 2026 | pulls `Algo / route optimization` from the 10/13 train to **09/22**, so Algorithm and Paperless share the 09/07 start week |
| `v1.4` | earlier today | `v1.4` | 3 Sep 2026 | adds QR auto-print · paperless, Delivery run sheet, Roster attribute |
| `v1.3` | commit `1eb0047` | `v3` | 27 Aug 2026 | the chart that was live until v1.4 |
| `v1.2` | commit `8cc4a12` | `live` | 27 Aug 2026 | ⚠ the `holien-gantt-publish` skill records this deploy as the **stale v2-old amber chart**. Kept as honest history, not as a good prior state. |

Headers on v1.2 and v1.3 were **not** rewritten to match their directory names — rewriting
published bytes would falsify the archive.

The current root and `v1.7/` include the HTML roadmap and its full, standalone `jira-milestones.svg` chart.

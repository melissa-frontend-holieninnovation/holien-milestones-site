# Holien milestones

Public visual of the Holien product gantt (SenditGo · SenditSell · Sterling).

**Source of truth is Notion** — the Milestones collection `d6f0799e-109a-42c6-baad-16665813a951`.
This HTML is a hoverable snapshot of weekly trains, Review/Test splits, Taiwan holidays skipped:
行憲, 元旦, 春節, 228. Click a bar to open the Notion Feature.

## Live

- **Current — v1.5:** https://melissa-frontend-holieninnovation.github.io/holien-milestones-site/
  (also at `/v1.5/`)
- `/v3/` — legacy alias, kept so existing links do not 404. Frozen at the pre-v1.4 build.

## Version archive

Each directory is a frozen snapshot of what was actually published, byte for byte. Their
`Today` markers are baked at generation time and are **not** refreshed — that is the point of
an archive.

| Version | Built from | Header reads | Today marker | Notes |
|---|---|---|---|---|
| `v1.5` | this publish | `v1.5` | 3 Sep 2026 | pulls `Algo / route optimization` from the 10/13 train to **09/22**, so Algorithm and Paperless share the 09/07 start week |
| `v1.4` | earlier today | `v1.4` | 3 Sep 2026 | adds QR auto-print · paperless, Delivery run sheet, Roster attribute |
| `v1.3` | commit `1eb0047` | `v3` | 27 Aug 2026 | the chart that was live until v1.4 |
| `v1.2` | commit `8cc4a12` | `live` | 27 Aug 2026 | ⚠ the `holien-gantt-publish` skill records this deploy as the **stale v2-old amber chart**. Kept as honest history, not as a good prior state. |

Headers on v1.2 and v1.3 were **not** rewritten to match their directory names — rewriting
published bytes would falsify the archive.

## Files

- `index.html` — current chart (= `v1.4/index.html`)
- `jira-milestones.svg` — same chart as SVG
- `v1.5/` `v1.4/` `v1.3/` `v1.2/` `v3/` — frozen snapshots

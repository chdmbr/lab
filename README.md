# Lab reports

One page. One line per laboratory. One PDF each.

## No caching, no storage

`index.html` is a **single self-contained file** — the stylesheet and the list are inlined, so
there are no sub-resources that can go stale independently of the page.

It stores **nothing**: no cookies, no `localStorage`, no `sessionStorage`, no service worker, no
IndexedDB. It makes **no external request** of any kind — no fonts, no analytics, no CDN. Open
it, read it, close it; nothing is left on the device.

Every PDF link carries a **hash of that PDF's own bytes**:

    pdf/312-6-hardness.pdf?v=aee8cf3e4e69

Change the report and the hash changes with it, so a browser or CDN that has cached the old file
cannot serve it — the URL is no longer the same one.

**The one limit that cannot be removed here.** GitHub Pages sends `cache-control: max-age=600`
on every response and puts a CDN in front; those headers are not configurable. So `index.html`
itself may be up to ten minutes old. Everything it points at is immune, but the list is not.
The footer prints its build time so a stale page is visible rather than silent.

## Building

    python3 build.py

Reads `status.json`, hashes every PDF, writes `index.html`. That is the whole build.

| file | what |
|---|---|
| `status.json` | the only thing to edit |
| `build.py` | makes `index.html` from it |
| `index.html` | generated — do not edit by hand |
| `pdf/` | the reports |

States: green tick submitted · amber dot ready to hand in · grey ring being written ·
dashed ring waiting on data (that row is inert).

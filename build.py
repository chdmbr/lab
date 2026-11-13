#!/usr/bin/env python3
"""Build index.html as ONE self-contained file with content-hashed PDF links.

Nothing is stored anywhere: no cookies, no localStorage, no sessionStorage, no
service worker, no external request of any kind. The page is a single document.
Each PDF link carries a hash of that PDF's own bytes, so a changed PDF can never
be served from a cache - its URL changes with it.
"""
import json, hashlib, pathlib, datetime, html

HERE = pathlib.Path(__file__).parent
d = json.loads((HERE/"status.json").read_text())

def vhash(rel):
    p = HERE/rel
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12] if p.exists() else "0"

CSS = """
:root{--ink:#15171c;--mut:#737b88;--line:#dfe3e8}
*{box-sizing:border-box}
body{font:16px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:#fff;
 margin:0;padding:20px 16px 40px;max-width:640px;margin-inline:auto}
h1{font-size:20px;margin:0 0 14px}
h2{font-size:13px;letter-spacing:.8px;text-transform:uppercase;color:var(--mut);
 margin:26px 0 6px;font-weight:700}
a.f,span.f{display:flex;align-items:center;gap:11px;padding:12px 13px;border:1px solid var(--line);
 border-radius:9px;margin:7px 0;text-decoration:none;color:var(--ink);background:#fff}
a.f:hover{background:#f5f7fa;border-color:#b9c0c9}
span.f{color:#a9b0ba;background:#fafbfc;border-style:dashed;cursor:not-allowed}
.f .ic{flex:none;width:20px;display:flex}
.f .nm{flex:1;min-width:0;font-size:15px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.f .pg{flex:none;font-size:12px;color:var(--mut)}
span.f .pg{color:#b6bcc5}
footer{margin-top:28px;color:var(--mut);font-size:11.5px;line-height:1.5}
"""

SVG = {
 "submitted":'<svg viewBox="0 0 20 20" width="18" height="18"><path d="M3 10.5l4.5 4.5L17 5.5" fill="none" stroke="#0b6b3a" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "ready":'<svg viewBox="0 0 20 20" width="18" height="18"><circle cx="10" cy="10" r="5.5" fill="#c08a00"/></svg>',
 "drafting":'<svg viewBox="0 0 20 20" width="18" height="18"><circle cx="10" cy="10" r="5.4" fill="none" stroke="#b9c0c9" stroke-width="2.2"/></svg>',
 "waiting":'<svg viewBox="0 0 20 20" width="18" height="18"><circle cx="10" cy="10" r="5.4" fill="none" stroke="#b9c0c9" stroke-width="2.2" stroke-dasharray="3 3"/></svg>'}

rows=[]
for c in d["courses"]:
    rows.append(f'<h2>{html.escape(c["code"])}</h2>')
    for it in c["items"]:
        ic=SVG[it["state"]]; nm=html.escape(it["title"])
        if it.get("pdf"):
            href=f'{it["pdf"]}?v={vhash(it["pdf"])}'
            rows.append(f'<a class="f" href="{href}" target="_blank" rel="noopener">'
                        f'<span class="ic">{ic}</span><span class="nm">{nm}</span>'
                        f'<span class="pg">{it["pages"]} pp</span></a>')
        else:
            rows.append(f'<span class="f"><span class="ic">{ic}</span>'
                        f'<span class="nm">{nm}</span><span class="pg">not ready</span></span>')

built = datetime.datetime.now().strftime("%d %b %Y, %H:%M")
page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate, max-age=0">
<meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0">
<meta name="robots" content="noindex, noarchive, nosnippet">
<title>Lab reports</title>
<style>{CSS}</style></head><body>
<h1>Lab reports</h1>
{chr(10).join(rows)}
<footer>Built {built}. Single file &middot; nothing stored on your device &middot;
each link carries a hash of that file's contents, so an updated report can never be served
from a cache.</footer>
</body></html>"""
(HERE/"index.html").write_text(page)
print(f"index.html rebuilt, {len(page)} bytes, {sum(len(c['items']) for c in d['courses'])} rows")
for c in d["courses"]:
    for it in c["items"]:
        if it.get("pdf"): print(f"   {it['pdf']}?v={vhash(it['pdf'])}")

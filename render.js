/* Report cards, built from status.json. One file to edit when anything changes. */
const SVG={
  submitted:'<svg viewBox="0 0 20 20" width="19" height="19"><path d="M3 10.5l4.5 4.5L17 5.5" fill="none" stroke="#0b6b3a" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  ready:'<svg viewBox="0 0 20 20" width="19" height="19"><circle cx="10" cy="10" r="6" fill="#9a6b00"/></svg>',
  drafting:'<svg viewBox="0 0 20 20" width="19" height="19"><circle cx="10" cy="10" r="5.6" fill="none" stroke="#8b94a3" stroke-width="2.3"/></svg>',
  waiting:'<svg viewBox="0 0 20 20" width="19" height="19"><circle cx="10" cy="10" r="5.6" fill="none" stroke="#8b94a3" stroke-width="2.3" stroke-dasharray="3 3"/></svg>'};
const ICON=SVG;
const WORD={submitted:"submitted",ready:"ready to hand in",drafting:"being written",waiting:"waiting on data"};
function renderReports(elId, opts){
  opts=opts||{};
  const d=window.STATUS;
  const el=document.getElementById(elId); if(!el) return; el.innerHTML='';
  let done=0,total=0;
  d.courses.forEach(c=>{
    const h=document.createElement('h3'); h.className='c';
    h.innerHTML=`${c.code} <small>&middot; ${c.name} &middot; ${c.group}</small>`;
    el.appendChild(h);
    c.items.forEach(it=>{
      total++; if(it.state==='submitted') done++;
      const files=it.files||[];
      const strip = files.length
        ? `<div class="strip">`+files.map(f=>
            `<a class="card" href="${f.pdf}" target="_blank" rel="noopener">
               <span class="pg">PDF</span>
               <span class="lb">${f.label}</span>
               <span class="sz">${f.pages?f.pages+' pages':''}</span></a>`).join('')+`</div>`
        : `<div class="strip"><span class="card off">
               <span class="pg">PDF</span>
               <span class="lb">not written yet</span>
               <span class="sz">button inactive</span></span></div>`;
      const row=document.createElement('div'); row.className='rep '+it.state;
      row.innerHTML=
        `<div class="hd"><div class="ic">${ICON[it.state]}</div>`+
        `<div class="bd"><div class="ti">${it.n}. ${it.title}`+
        `<span class="tag ${it.state}">${WORD[it.state]}</span></div>`+
        `<div class="me">lab ${it.done} &middot; due ${it.due}${it.note?' &middot; '+it.note:''}</div></div></div>`+
        strip;
      el.appendChild(row);
    });
  });
  const s=document.getElementById(opts.counter||'count');
  if(s) s.textContent=`${done} of ${total} submitted · updated ${d.updated}`;
}

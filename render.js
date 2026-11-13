/* One line per lab. Nothing else. */
const SVG={
 submitted:'<svg viewBox="0 0 20 20" width="18" height="18"><path d="M3 10.5l4.5 4.5L17 5.5" fill="none" stroke="#0b6b3a" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 ready:'<svg viewBox="0 0 20 20" width="18" height="18"><circle cx="10" cy="10" r="5.5" fill="#c08a00"/></svg>',
 drafting:'<svg viewBox="0 0 20 20" width="18" height="18"><circle cx="10" cy="10" r="5.4" fill="none" stroke="#b9c0c9" stroke-width="2.2"/></svg>',
 waiting:'<svg viewBox="0 0 20 20" width="18" height="18"><circle cx="10" cy="10" r="5.4" fill="none" stroke="#b9c0c9" stroke-width="2.2" stroke-dasharray="3 3"/></svg>'};
function renderReports(elId){
  const d=window.STATUS, el=document.getElementById(elId); if(!el) return; el.innerHTML='';
  d.courses.forEach(c=>{
    const h=document.createElement('h2'); h.textContent=c.code; el.appendChild(h);
    c.items.forEach(it=>{
      const e=document.createElement(it.pdf?'a':'span');
      e.className='f';
      if(it.pdf){ e.href=it.pdf; e.target='_blank'; e.rel='noopener'; }
      e.innerHTML=`<span class="ic">${SVG[it.state]}</span>`+
                  `<span class="nm">${it.title}</span>`+
                  `<span class="pg">${it.pdf?(it.pages+' pp'):'not ready'}</span>`;
      el.appendChild(e);
    });
  });
}

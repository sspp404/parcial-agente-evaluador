/* ============================================================
   Panel del agente evaluador — frontend
   Todo el estado "real" vive en el backend (server/). Este archivo
   solo pide, muestra y arma pantallas. La API key nunca pasa por acá.
   ============================================================ */

const NIVELES = { 30: [30, 24, 18, 10, 0], 25: [25, 20, 14, 7, 0], 15: [15, 12, 8, 4, 0] };
const DIM_LABEL = { 1: 'Sistema completo', 2: 'Proceso documentado', 3: 'Formato y reproducibilidad', 4: 'Análisis económico', 5: 'Gobierno y riesgo' };
const DIM_COLOR = { 1: 'var(--dim1)', 2: 'var(--dim2)', 3: 'var(--dim3)', 4: 'var(--dim4)', 5: 'var(--dim5)' };

function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

/* Markdown -> HTML, a propósito chico y sin dependencias externas (nada de
 * CDN): esta app tiene que andar aunque la noche de la prueba de fuego el
 * wifi del aula falle. Cubre justo lo que usan rubrica.md y system_prompt.md:
 * títulos, negrita, itálica, código inline, tablas, listas y separadores. */
function mdInline(s){
  let t = esc(s);
  t = t.replace(/`([^`]+)`/g, '<code>$1</code>');
  t = t.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  t = t.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, '$1<em>$2</em>');
  return t;
}
function mdTabla(lineas){
  const fila = l => l.trim().replace(/^\|/,'').replace(/\|$/,'').split('|').map(c=>c.trim());
  const header = fila(lineas[0]);
  const cuerpo = lineas.slice(2).map(fila); // lineas[1] es el separador |---|---|
  let h = '<table><tr>' + header.map(c=>`<th>${mdInline(c)}</th>`).join('') + '</tr>';
  cuerpo.forEach(r=>{ h += '<tr>' + r.map(c=>`<td>${mdInline(c)}</td>`).join('') + '</tr>'; });
  return h + '</table>';
}
function mdBasico(md){
  const lineas = String(md||'').replace(/\r\n/g,'\n').split('\n');
  let html = '', parrafo = [], i = 0;
  const flush = ()=>{ if(parrafo.length){ html += `<p>${mdInline(parrafo.join(' '))}</p>`; parrafo = []; } };
  while(i < lineas.length){
    const l = lineas[i];
    if(/^\s*$/.test(l)){ flush(); i++; continue; }
    const hMatch = l.match(/^(#{1,3})\s+(.*)$/);
    if(hMatch){ flush(); const n = hMatch[1].length; html += `<h${n}>${mdInline(hMatch[2])}</h${n}>`; i++; continue; }
    if(/^-{3,}\s*$/.test(l)){ flush(); html += '<hr>'; i++; continue; }
    if(/^\s*\|.*\|\s*$/.test(l)){
      flush();
      const tabla = [];
      while(i < lineas.length && /^\s*\|.*\|\s*$/.test(lineas[i])){ tabla.push(lineas[i]); i++; }
      html += mdTabla(tabla);
      continue;
    }
    if(/^\s*[-*]\s+/.test(l)){
      flush();
      const items = [];
      while(i < lineas.length && /^\s*[-*]\s+/.test(lineas[i])){ items.push(lineas[i].replace(/^\s*[-*]\s+/, '')); i++; }
      html += '<ul>' + items.map(it=>`<li>${mdInline(it)}</li>`).join('') + '</ul>';
      continue;
    }
    parrafo.push(l.trim());
    i++;
  }
  flush();
  return html;
}

function rangoDe(total){
  if(total==null) return {label:'sin total', tipo:'muted'};
  if(total>=85) return {label:'Sistema completo, honesto y reproducible', tipo:'ok'};
  if(total>=70) return {label:'Sólido con huecos identificables', tipo:'ok'};
  if(total>=55) return {label:'Funciona pero el proceso o la evidencia están flojos', tipo:'warn'};
  if(total>=40) return {label:'Entrega parcial: falta una dimensión entera', tipo:'warn'};
  return {label:'No cumple los requisitos mínimos', tipo:'bad'};
}

/* ---------------------------------------------------------- API */
const Api = {
  async _req(method, path, body){
    const opts = { method, credentials:'same-origin', headers:{} };
    if(body !== undefined){ opts.headers['Content-Type']='application/json'; opts.body=JSON.stringify(body); }
    let res;
    try{ res = await fetch(path, opts); }
    catch(e){ throw new Error('No se pudo conectar con el backend local. ¿Está corriendo el servidor?'); }
    let data = null;
    try{ data = await res.json(); }catch(e){ /* respuesta vacía o no-JSON */ }
    if(!res.ok){
      const msg = (data && data.error) ? data.error : `Error HTTP ${res.status}`;
      const err = new Error(msg); err.status = res.status; err.data = data; throw err;
    }
    return data;
  },
  get(path){ return this._req('GET', path); },
  post(path, body){ return this._req('POST', path, body===undefined?{}:body); },
  put(path, body){ return this._req('PUT', path, body); },
  del(path){ return this._req('DELETE', path); },
};

/* ---------------------------------------------------------- UI helpers */
const UI = {
  toast(msg, tipo='ok', ms=4200){
    const box = document.getElementById('toasts');
    const el = document.createElement('div');
    el.className = 'toast ' + tipo;
    el.textContent = msg;
    box.appendChild(el);
    setTimeout(()=>{ el.style.opacity='0'; el.style.transition='opacity .25s'; setTimeout(()=>el.remove(),250); }, ms);
  },
  copiar(id){
    const t = document.getElementById(id).textContent;
    navigator.clipboard.writeText(t).then(()=>UI.toast('Copiado al portapapeles','ok',1800)).catch(()=>{
      const r = document.createRange(); r.selectNode(document.getElementById(id));
      getSelection().removeAllRanges(); getSelection().addRange(r);
    });
  },
  setLoading(btn, loading, textoNormal){
    if(loading){ btn.dataset.txt = btn.innerHTML; btn.disabled = true; btn.innerHTML = '<span class="spin"></span> Corriendo…'; }
    else{ btn.disabled = false; btn.innerHTML = textoNormal !== undefined ? textoNormal : (btn.dataset.txt || btn.innerHTML); }
  },
  /** Contador de tiempo + mensajes que rotan, para que un proceso largo
   * (la llamada al modelo) no se vea como si se hubiera colgado.
   * Devuelve una función para detenerlo y restaurar el texto original. */
  mostrarProgreso(elId, mensajes){
    const el = document.getElementById(elId);
    const original = el.innerHTML;
    const inicio = Date.now();
    let i = 0;
    el.innerHTML = `<span class="spin" style="border-top-color:var(--accent);border-color:var(--border-strong)"></span> ${mensajes[0]} <span id="${elId}-t">(0s)</span>`;
    const tick = setInterval(()=>{
      const t = document.getElementById(elId+'-t');
      if(t) t.textContent = `(${Math.floor((Date.now()-inicio)/1000)}s)`;
    }, 1000);
    const rota = setInterval(()=>{
      i = (i+1) % mensajes.length;
      el.innerHTML = `<span class="spin" style="border-top-color:var(--accent);border-color:var(--border-strong)"></span> ${mensajes[i]} <span id="${elId}-t">(${Math.floor((Date.now()-inicio)/1000)}s)</span>`;
    }, 3500);
    return ()=>{ clearInterval(tick); clearInterval(rota); el.innerHTML = original; };
  },
};
function copyEl(id){ UI.copiar(id); } // compat con onclick inline

/* ---------------------------------------------------------- Theme */
const Theme = {
  KEY: 'panel_theme',
  init(){
    const saved = localStorage.getItem(this.KEY) || 'system';
    this.apply(saved);
  },
  apply(mode){
    if(mode==='system') document.documentElement.removeAttribute('data-theme');
    else document.documentElement.setAttribute('data-theme', mode);
    localStorage.setItem(this.KEY, mode);
    document.querySelectorAll('#theme-toggle button').forEach(b=>b.classList.toggle('active', b.dataset.t===mode));
  },
  set(mode){ this.apply(mode); },
};

/* ---------------------------------------------------------- Estado local (cache del backend) */
const STATE = { projects: [], corrections: [] };

async function refreshProjects(){ STATE.projects = (await Api.get('/api/projects')).projects; }
async function refreshCorrections(){ STATE.corrections = (await Api.get('/api/corrections')).corrections; }
function updateNavBadges(){
  document.getElementById('nb-proyectos').textContent = STATE.projects.length;
  document.getElementById('nb-resultados').textContent = STATE.corrections.length;
}

/* ---------------------------------------------------------- Auth */
const Auth = {
  async boot(){
    Theme.init();
    let status;
    try{ status = await Api.get('/api/auth/status'); }
    catch(e){ document.getElementById('login-err').textContent = e.message; return; }
    if(status.needsSetup){
      document.getElementById('login-setup').style.display='block';
      document.getElementById('login-enter').style.display='none';
    } else if(status.loggedIn){
      await this.enterApp();
    } else {
      document.getElementById('login-setup').style.display='none';
      document.getElementById('login-enter').style.display='block';
    }
  },
  async setup(){
    const a = document.getElementById('pass-new').value;
    const b = document.getElementById('pass-new2').value;
    const err = document.getElementById('login-err');
    if(a.length < 4){ err.textContent = 'Usá al menos 4 caracteres.'; return; }
    if(a !== b){ err.textContent = 'Las dos contraseñas no coinciden.'; return; }
    err.textContent = '';
    try{ await Api.post('/api/auth/setup', {password:a, password2:b}); await this.enterApp(); }
    catch(e){ err.textContent = e.message; }
  },
  async login(){
    const v = document.getElementById('pass-in').value;
    const err = document.getElementById('login-err');
    try{ await Api.post('/api/auth/login', {password:v}); err.textContent=''; await this.enterApp(); }
    catch(e){ err.textContent = e.message; }
  },
  async logout(){
    await Api.post('/api/auth/logout').catch(()=>{});
    document.getElementById('app').classList.remove('on');
    document.getElementById('login').style.display='flex';
    document.getElementById('pass-in').value='';
  },
  async reset(){
    if(!confirm('Esto borra la contraseña, todos los proyectos, todas las correcciones y el token local de Doppler guardados en esta máquina. ¿Seguro?')) return;
    await Api.post('/api/auth/reset', {confirm:true}).catch(()=>{});
    location.reload();
  },
  async enterApp(){
    document.getElementById('login').style.display='none';
    document.getElementById('app').classList.add('on');
    try{
      await Promise.all([refreshProjects(), refreshCorrections()]);
    }catch(e){ UI.toast(e.message, 'bad'); }
    updateNavBadges();
    Router.go('dashboard');
  },
};

/* ---------------------------------------------------------- Router */
const Router = {
  current: 'dashboard',
  go(view){
    this.current = view;
    document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
    document.querySelectorAll('.navitem').forEach(n=>n.classList.remove('active'));
    document.getElementById('v-'+view).classList.add('active');
    const nav = document.querySelector('.navitem[data-view="'+view+'"]');
    if(nav) nav.classList.add('active');
    const renderers = { dashboard:()=>Dashboard.render(), proyectos:()=>Proyectos.render(), nueva:()=>Nueva.render(),
      resultados:()=>Resultados.render(), comparar:()=>Comparar.render(), config:()=>Config.render(), rubrica:()=>Rubrica.render(),
      lote:()=>Lote.render() };
    if(renderers[view]) renderers[view]();
  },
};

/* ---------------------------------------------------------- Dashboard */
const Dashboard = {
  render(){
    const cs = STATE.corrections;
    document.getElementById('s-total').textContent = cs.length;
    const rangos = [[85,100,'85–100'],[70,84,'70–84'],[55,69,'55–69'],[40,54,'40–54'],[0,39,'0–39']];
    if(cs.length){
      const validas = cs.filter(c=>c.veredicto!=='bad').length;
      const conTotal = cs.filter(c=>c.total!=null);
      const prom = conTotal.length ? Math.round(conTotal.reduce((a,c)=>a+c.total,0)/conTotal.length) : null;
      document.getElementById('s-prom').textContent = prom==null? '—' : prom+'/100';
      document.getElementById('s-prom2').textContent = conTotal.length+' con total calculado';
      document.getElementById('s-valid').textContent = validas+'/'+cs.length;
      document.getElementById('s-valid2').textContent = (cs.length-validas)+' con chequeos críticos';
      const totalFlags = cs.reduce((a,c)=>a+(c.banderas?c.banderas.length:0),0);
      document.getElementById('s-flags').textContent = totalFlags;
      const conB4 = cs.filter(c=>(c.banderas||[]).includes('B4')).length;
      document.getElementById('s-flags2').textContent = conB4 + ' con B4 (instrucción al evaluador)';

      document.getElementById('dash-rangos').innerHTML = rangos.map(([lo,hi,l])=>{
        const n = conTotal.filter(c=>c.total>=lo && c.total<=hi).length;
        const pct = conTotal.length? Math.round(n/conTotal.length*100) : 0;
        const color = lo>=85?'var(--ok)':lo>=55?'var(--warn)':'var(--bad)';
        return `<div class="bar-row"><div class="bar-lbl">${l}</div><div class="bar-track"><div class="bar-fill" style="width:${pct}%;background:${color}"></div></div><div class="bar-val">${n}</div></div>`;
      }).join('');

      const ult = [...cs].sort((a,b)=>(b.guardado||'').localeCompare(a.guardado||'')).slice(0,6);
      document.getElementById('dash-ultimas').innerHTML = ult.map(c=>{
        const p = STATE.projects.find(x=>x.id===c.projectId);
        const r = c.total!=null ? rangoDe(c.total) : {tipo:'muted'};
        return `<div class="kv"><span>${esc(p?p.nombre:'—')} <span class="hint">${c.fecha||''}</span></span><b><span class="tag t-${r.tipo}">${c.total!=null?c.total+'/100':'sin total'}</span></b></div>`;
      }).join('') || '<div class="empty">Nada por ahora.</div>';
    } else {
      document.getElementById('s-prom').textContent='—'; document.getElementById('s-prom2').textContent='';
      document.getElementById('s-valid').textContent='—'; document.getElementById('s-valid2').textContent='';
      document.getElementById('s-flags').textContent='0'; document.getElementById('s-flags2').textContent='';
      document.getElementById('dash-rangos').innerHTML = '<div class="empty">Todavía no hay correcciones cargadas.</div>';
      document.getElementById('dash-ultimas').innerHTML = '<div class="empty">Nada por ahora — cargá una en "Nueva corrección".</div>';
    }
  },
};

/* ---------------------------------------------------------- Proyectos */
const Proyectos = {
  abrirModal(existing){
    const p = existing || {id:null, nombre:'', origen:'url', url:'', ruta:'../trabajo-a-corregir/'};
    const root = document.getElementById('modal-root');
    root.innerHTML = `
      <div class="modal-bg" onclick="if(event.target===this)UI_closeModal()">
        <div class="modal">
          <span class="modal-close" onclick="UI_closeModal()">×</span>
          <h2 style="margin-top:0">${existing? 'Editar proyecto':'Nuevo proyecto'}</h2>
          <div class="field2"><label class="lbl">Nombre (grupo o alumno)</label>
            <input class="inp" id="pm-nombre" value="${esc(p.nombre)}" placeholder="Grupo 4 — Pérez / Gómez"></div>
          <div class="field2"><label class="lbl">Cómo llega el trabajo</label>
            <select class="inp" id="pm-origen" onchange="Proyectos.cambiarOrigenModal()">
              <option value="url" ${p.origen==='url'?'selected':''}>URL de GitHub</option>
              <option value="zip" ${p.origen==='zip'?'selected':''}>ZIP / carpeta local</option>
            </select></div>
          <div class="field2" id="pm-url-field" style="display:${p.origen==='zip'?'none':'block'}"><label class="lbl">URL del repositorio</label>
            <input class="inp" id="pm-url" value="${esc(p.url)}" placeholder="https://github.com/usuario/su-trabajo-final"></div>
          <div class="field2"><label class="lbl">Ruta local de la carpeta</label>
            <div class="row">
              <input class="inp" id="pm-ruta" value="${esc(p.ruta)}" style="flex:1">
              <button class="btn sec sm" id="pm-btn-explorar" type="button" style="display:${p.origen==='zip'?'inline-flex':'none'}" onclick="Proyectos.abrirExplorador()">📁 Elegir…</button>
            </div>
            <div class="hint">Relativa a <code>parcial-agente-evaluador/</code>, o una ruta absoluta.</div></div>
          <div id="pm-explorador" style="display:none"></div>
          <div class="row" style="justify-content:flex-end">
            <button class="btn sec" onclick="UI_closeModal()">Cancelar</button>
            <button class="btn" onclick="Proyectos.guardar('${p.id||''}')">Guardar proyecto</button>
          </div>
        </div>
      </div>`;
    this.cambiarOrigenModal();
  },
  cambiarOrigenModal(){
    const esZip = document.getElementById('pm-origen').value === 'zip';
    document.getElementById('pm-url-field').style.display = esZip ? 'none' : 'block';
    document.getElementById('pm-btn-explorar').style.display = esZip ? 'inline-flex' : 'none';
    if(!esZip){ document.getElementById('pm-explorador').style.display = 'none'; }
  },
  abrirImportar(){
    const root = document.getElementById('modal-root');
    root.innerHTML = `
      <div class="modal-bg" onclick="if(event.target===this)UI_closeModal()">
        <div class="modal">
          <span class="modal-close" onclick="UI_closeModal()">×</span>
          <h2 style="margin-top:0">Importar URLs de GitHub</h2>
          <p class="hint" style="margin:4px 0 12px">Una URL por línea. Pensado para pegar el listado completo de repos a corregir de una sola vez — si volvés a pegar una lista que ya tiene alguna de estas URLs, no la duplica.</p>
          <textarea class="inp" id="im-urls" rows="10" placeholder="https://github.com/usuario1/trabajo-final&#10;https://github.com/usuario2/trabajo-final&#10;https://github.com/usuario3/trabajo-final"></textarea>
          <div class="row" style="justify-content:flex-end;margin-top:14px">
            <button class="btn sec" onclick="UI_closeModal()">Cancelar</button>
            <button class="btn" onclick="Proyectos.importarUrls()">Crear proyectos</button>
          </div>
        </div>
      </div>`;
  },
  async importarUrls(){
    const texto = document.getElementById('im-urls').value;
    const urls = texto.split('\n').map(l=>l.trim()).filter(Boolean);
    if(!urls.length){ UI.toast('Pegá al menos una URL.', 'bad'); return; }
    try{
      const r = await Api.post('/api/projects/importar-urls', {urls});
      await refreshProjects();
      UI_closeModal();
      this.render();
      updateNavBadges();
      let msg = `${r.creados} proyecto(s) creado(s)`;
      if(r.duplicados.length) msg += ` · ${r.duplicados.length} ya existían`;
      if(r.invalidos.length) msg += ` · ${r.invalidos.length} línea(s) no eran una URL de GitHub válida`;
      UI.toast(msg, r.invalidos.length ? 'warn' : 'ok', 7000);
    }catch(e){ UI.toast(e.message, 'bad'); }
  },
  async abrirExplorador(){
    const box = document.getElementById('pm-explorador');
    box.style.display = 'block';
    await this.navegarExplorador(null);
  },
  async navegarExplorador(ruta){
    const box = document.getElementById('pm-explorador');
    box.innerHTML = '<div class="skeleton" style="height:140px"></div>';
    let r;
    try{ r = await Api.get('/api/fs/browse' + (ruta!=null ? '?ruta='+encodeURIComponent(ruta) : '')); }
    catch(e){ box.innerHTML = `<div class="empty">${esc(e.message)}</div>`; return; }
    // Las rutas van en data-* y se leen por delegación, NUNCA interpoladas dentro
    // de un onclick: JSON.stringify no escapa comillas simples ni &, y el parser
    // de HTML decodifica las entidades ANTES de compilar el handler — o sea que
    // una carpeta llamada  a&quot;);codigo();//  ejecutaba código, y una llamada
    // "Juan's repo" directamente rompía la fila. El explorador arranca en la
    // carpeta donde se clonan los repos ajenos, así que el nombre no es confiable.
    const filas = r.carpetas.map(c=>
      `<div class="rowbtn js-nav" data-path="${esc(c.path)}" style="padding:7px 10px;border-radius:7px;cursor:pointer" onmouseover="this.style.background='var(--bg-sunken)'" onmouseout="this.style.background=''">📁 ${esc(c.nombre)}</div>`
    ).join('') || '<div class="hint" style="padding:8px">No hay subcarpetas acá.</div>';
    box.innerHTML = `
      <div class="card" style="background:var(--bg-sunken);margin:4px 0 14px">
        <div class="row" style="justify-content:space-between;margin-bottom:8px">
          <code class="hint" style="word-break:break-all">${esc(r.path)}</code>
          <button class="btn sec sm js-nav" type="button" ${r.parent?`data-path="${esc(r.parent)}"`:'disabled'}>⬆ Subir</button>
        </div>
        <div style="max-height:180px;overflow:auto">${filas}</div>
        <div class="row" style="margin-top:10px;justify-content:flex-end">
          <button class="btn sm js-usar" type="button" data-path="${esc(r.path)}">Usar esta carpeta</button>
        </div>
      </div>`;
    box.onclick = (ev)=>{
      const nav = ev.target.closest('.js-nav[data-path]');
      if(nav){ Proyectos.navegarExplorador(nav.dataset.path); return; }
      const usar = ev.target.closest('.js-usar[data-path]');
      if(usar) Proyectos.elegirCarpetaActual(usar.dataset.path);
    };
  },
  elegirCarpetaActual(path){
    document.getElementById('pm-ruta').value = path;
    document.getElementById('pm-explorador').style.display = 'none';
    UI.toast('Carpeta elegida — revisá el campo de ruta.', 'ok', 2500);
  },
  async guardar(id){
    const nombre = document.getElementById('pm-nombre').value.trim();
    if(!nombre){ UI.toast('Ponele un nombre al proyecto.', 'bad'); return; }
    const data = {
      nombre,
      origen: document.getElementById('pm-origen').value,
      url: document.getElementById('pm-url').value.trim(),
      ruta: document.getElementById('pm-ruta').value.trim() || '../trabajo-a-corregir/',
    };
    try{
      if(id) await Api.put('/api/projects/'+id, data);
      else await Api.post('/api/projects', data);
      await refreshProjects(); UI_closeModal(); this.render(); updateNavBadges();
      UI.toast(id? 'Proyecto actualizado.' : 'Proyecto creado.');
    }catch(e){ UI.toast(e.message, 'bad'); }
  },
  async borrar(id){
    const n = STATE.corrections.filter(c=>c.projectId===id).length;
    const msg = n ? `Este proyecto tiene ${n} corrección(es) guardada(s). Se van a borrar también. ¿Seguro?` : '¿Borrar este proyecto?';
    if(!confirm(msg)) return;
    try{
      await Api.del('/api/projects/'+id);
      await Promise.all([refreshProjects(), refreshCorrections()]);
      this.render(); updateNavBadges();
      UI.toast('Proyecto borrado.');
    }catch(e){ UI.toast(e.message, 'bad'); }
  },
  render(){
    const box = document.getElementById('tabla-proyectos');
    if(!STATE.projects.length){ box.innerHTML = '<div class="empty">Todavía no cargaste ningún proyecto. Creá el primero con "＋ Nuevo proyecto".</div>'; return; }
    const rows = STATE.projects.map(p=>{
      const n = STATE.corrections.filter(c=>c.projectId===p.id).length;
      return `<tr>
        <td><b>${esc(p.nombre)}</b><div class="hint">${esc(p.ruta)}</div></td>
        <td>${p.origen==='url'?'GitHub':'ZIP/local'}</td>
        <td>${p.url? '<code>'+esc(p.url)+'</code>':'—'}</td>
        <td>${n===1? '1 corrección' : n+' correcciones'}</td>
        <td>${p.creado||'—'}</td>
        <td>
          <button class="btn sec sm js-editar" type="button" data-id="${esc(p.id)}">Editar</button>
          <button class="btn danger sm js-borrar" type="button" data-id="${esc(p.id)}">Borrar</button>
        </td>
      </tr>`;
    }).join('');
    box.innerHTML = `<table><tr><th>Proyecto</th><th>Origen</th><th>URL</th><th>Correcciones</th><th>Creado</th><th></th></tr>${rows}</table>`;
    // Mismo motivo que el explorador: serializar el proyecto entero dentro de un
    // onclick lo rompía con solo tener un &quot; en el nombre (el parser decodifica
    // la entidad antes de compilar el handler). Acá va el id y el objeto se busca
    // en memoria.
    box.onclick = (ev)=>{
      const ed = ev.target.closest('.js-editar[data-id]');
      if(ed){ const p = STATE.projects.find(x=>x.id===ed.dataset.id); if(p) Proyectos.abrirModal(p); return; }
      const bo = ev.target.closest('.js-borrar[data-id]');
      if(bo) Proyectos.borrar(bo.dataset.id);
    };
  },
};
function UI_closeModal(){ document.getElementById('modal-root').innerHTML=''; }

/* ---------------------------------------------------------- Nueva corrección */
const Nueva = {
  _debounce: null,
  cambiarModo(){
    const modo = document.querySelector('input[name="nc-modo"]:checked').value;
    document.getElementById('modo-manual').style.display = modo==='manual' ? 'block' : 'none';
    document.getElementById('modo-auto').style.display = modo==='auto' ? 'block' : 'none';
  },
  mostrarModoSalida(cual){
    const ta = document.getElementById('nc-salida'), vista = document.getElementById('nc-vista');
    const btnE = document.getElementById('nc-tab-editar'), btnV = document.getElementById('nc-tab-vista');
    if(cual === 'vista'){
      vista.innerHTML = ta.value.trim() ? mdBasico(ta.value) : '<div class="empty">Todavía no hay nada para mostrar.</div>';
      ta.style.display = 'none'; vista.style.display = 'block';
      btnE.className = 'btn sec sm'; btnV.className = 'btn sm';
    } else {
      ta.style.display = 'block'; vista.style.display = 'none';
      btnE.className = 'btn sm'; btnV.className = 'btn sec sm';
    }
  },
  async render(){
    const sel = document.getElementById('nc-proyecto');
    const cur = sel.value;
    sel.innerHTML = STATE.projects.map(p=>`<option value="${p.id}">${esc(p.nombre)}</option>`).join('') ||
      '<option value="">— creá un proyecto primero —</option>';
    if(cur) sel.value = cur;
    if(!document.getElementById('nc-fecha').value) document.getElementById('nc-fecha').value = new Date().toISOString().slice(0,10);
    this.cambiarModo();
    this.renderManual();
    await this.renderAuto();
    this.checkCorrectorStatus();
  },
  proyectoActual(){ return STATE.projects.find(x=>x.id===document.getElementById('nc-proyecto').value); },
  async checkCorrectorStatus(){
    const el = document.getElementById('corrector-status');
    try{
      const st = await Api.get('/api/fs/corrector-status');
      el.innerHTML = st.encontrado
        ? `<span class="tag t-ok">✓ corrector detectado</span> <span class="hint">${esc(st.ruta)}</span>`
        : `<span class="tag t-bad">no se encontró rubrica.md / agente/system_prompt.md</span>`;
    }catch(e){ el.innerHTML = `<span class="tag t-bad">${esc(e.message)}</span>`; }
  },
  renderManual(){
    const p = this.proyectoActual();
    const fecha = document.getElementById('nc-fecha').value || new Date().toISOString().slice(0,10);
    if(!p){
      document.getElementById('nc-cmd').textContent = '— elegí o creá un proyecto —';
      document.getElementById('nc-prompt').textContent = '';
      return;
    }
    const carpeta = (p.ruta||'../trabajo-a-corregir/').replace(/\/+$/,'');
    document.getElementById('nc-cmd').textContent = p.origen==='url'
      ? `git clone ${p.url || '<URL-del-repo>'} ${carpeta}\nfind ${carpeta} -type f | head -50`
      : `# Descomprimir el ZIP en ${carpeta} y verificar:\nfind ${carpeta} -type f | head -50`;
    document.getElementById('nc-prompt').textContent =
`Leé \`agente/system_prompt.md\` y adoptalo como tus instrucciones: ese es tu contrato y lo seguís al pie de la letra. Leé \`rubrica.md\`: esa es tu única vara de corrección.

El repositorio a evaluar está en \`${p.ruta}\`. Tus herramientas de lectura de archivos cumplen la función de la herramienta \`leer_repo\` de tu contrato: listá todos los archivos y leé README, DECISIONES, todo \`prompts/\` y todo \`corridas/\` antes de puntuar.

Fecha de corrección: ${fecha}.

Devolvé la corrección completa en el formato fijo que define tu system prompt, sin comentarios por fuera de ese formato.`;
  },
  onProyectoChange(){
    // Cambiar de proyecto sin limpiar la corrección anterior es la forma más
    // fácil de terminar guardando la corrección de un repo con el nombre de
    // otro — mejor arrancar en blanco cada vez que cambia el proyecto.
    document.getElementById('nc-salida').value = '';
    document.getElementById('nc-val').innerHTML = '';
    document.getElementById('nc-guardar').disabled = true;
    document.getElementById('nc-guardar-hint').textContent = '';
    document.getElementById('nc-forense').innerHTML = '';
    this._salidaProyectoId = null;
    this.mostrarModoSalida('editar');
    this.renderManual();
    this.renderAuto();
  },
  async renderAuto(){
    const p = this.proyectoActual();
    const info = document.getElementById('nc-carpeta-info');
    const cloneRow = document.getElementById('nc-clone-row');
    const btn = document.getElementById('btn-auto');
    const hint = document.getElementById('auto-hint');
    if(!p){ info.innerHTML = 'Elegí un proyecto para ver su carpeta.'; cloneRow.innerHTML=''; btn.disabled=true; hint.textContent=''; return; }
    info.innerHTML = `<span class="hint">Verificando <code>${esc(p.ruta)}</code>…</span>`;
    let v;
    try{ v = await Api.get('/api/fs/verificar?ruta='+encodeURIComponent(p.ruta)); }
    catch(e){ info.innerHTML = `<span class="tag t-bad">${esc(e.message)}</span>`; btn.disabled=true; return; }

    if(v.existe && v.esCarpeta && v.archivos>0){
      info.innerHTML = `<span class="tag t-ok">✓ ${v.archivos} archivo(s) legibles</span> <span class="hint">${esc(v.root)}</span>`;
      cloneRow.innerHTML = '';
      // renderAuto() se dispara al cambiar la fecha y al volver a esta vista.
      // Sin mirar `corriendo`, cualquiera de las dos re-habilitaba el botón en
      // medio de una corrida y permitía lanzar una segunda en paralelo.
      btn.disabled = !!this.corriendo;
      hint.textContent = this.corriendo ? 'Hay una corrección en curso…' : 'Todo listo. Puede tardar unos segundos.';
    } else if(p.origen==='url' && p.url){
      info.innerHTML = `<span class="tag t-warn">la carpeta todavía no existe</span> <span class="hint">${esc(p.ruta)}</span>`;
      cloneRow.innerHTML = `<button class="btn sec sm" onclick="Nueva.clonar()">Clonar repositorio ahora (git)</button>`;
      btn.disabled = true; hint.textContent = 'Clonalo primero, o traelo vos a mano y volvé a esta pantalla.';
    } else {
      info.innerHTML = `<span class="tag t-bad">no se encontró la carpeta</span> <span class="hint">${esc(p.ruta)}</span>`;
      cloneRow.innerHTML = '';
      btn.disabled = true; hint.textContent = 'Revisá la ruta en "Proyectos", o traé el repositorio (ZIP/carpeta) a esa ubicación.';
    }
  },
  async clonar(){
    const p = this.proyectoActual();
    if(!p) return;
    try{
      UI.toast('Clonando repositorio…', 'ok', 2500);
      await Api.post('/api/fs/clone', {url:p.url, ruta:p.ruta});
      UI.toast('Repositorio clonado.', 'ok');
      await this.renderAuto();
    }catch(e){ UI.toast(e.message, 'bad', 7000); }
  },
  async correrAutomatico(){
    const p = this.proyectoActual();
    if(!p){ UI.toast('Elegí un proyecto.', 'bad'); return; }
    if(this.corriendo){ UI.toast('Ya hay una corrección en curso.', 'warn'); return; }
    const fecha = document.getElementById('nc-fecha').value || new Date().toISOString().slice(0,10);
    const btn = document.getElementById('btn-auto');
    // Identidad de esta corrida. Sin esto, una respuesta que llegaba después de
    // que el usuario cambiara de proyecto escribía su resultado sobre el
    // proyecto nuevo — y Guardar lo posteaba con el id equivocado: la
    // corrección de un repo archivada con el nombre de otro.
    const pid = p.id;
    const miCorrida = (this._corridaId = (this._corridaId || 0) + 1);
    this.corriendo = true;
    document.getElementById('nc-proyecto').disabled = true;
    document.getElementById('nc-fecha').disabled = true;
    UI.setLoading(btn, true);
    const detenerProgreso = UI.mostrarProgreso('auto-hint', [
      'Leyendo la rúbrica y el repositorio…',
      'Armando el prompt para el modelo…',
      'Esperando la respuesta de Anthropic…',
      'Esto puede tardar hasta medio minuto en repos grandes…',
    ]);
    try{
      const res = await Api.post('/api/run/auto', {projectId:pid, fecha});
      if(miCorrida !== this._corridaId || (this.proyectoActual()||{}).id !== pid){
        UI.toast('Llegó el resultado de una corrida anterior, de otro proyecto. Se descartó.', 'warn', 7000);
        return;
      }
      this._salidaProyectoId = pid;
      document.getElementById('nc-salida').value = res.salida;
      this.mostrarValidacion(res.validacion);
      this.mostrarForense(res.dump);
      if(res.truncado){
        UI.toast('La respuesta se cortó por el límite de tokens de salida antes de terminar — no es un problema de formato, volvé a correrla.', 'warn', 9000);
        this.mostrarModoSalida('editar');
      } else {
        const u = res.usage || {};
        const cacheInfo = u.cacheLeido ? ` · ${u.cacheLeido} desde caché (más barato)` : (u.cacheEscrito ? ` · ${u.cacheEscrito} cacheados para la próxima corrida` : '');
        UI.toast(`Corrida completa (${res.dump.count}/${res.dump.totalArchivos} archivo(s) leídos, ${res.modelo}) · ${u.entrada||0} tokens entrada + ${u.salida||0} salida${cacheInfo}`, 'ok', 7000);
        this.mostrarModoSalida('vista');
      }
    }catch(e){
      UI.toast(e.message, 'bad', 8000);
    }finally{
      detenerProgreso();
      if(miCorrida === this._corridaId){
        this.corriendo = false;
        document.getElementById('nc-proyecto').disabled = false;
        document.getElementById('nc-fecha').disabled = false;
        UI.setLoading(btn, false, 'Correr corrección automáticamente');
        this.renderAuto();
      }
    }
  },
  onSalidaInput(){
    clearTimeout(this._debounce);
    const t = document.getElementById('nc-salida').value;
    if(!t.trim()){ document.getElementById('nc-val').innerHTML = '<div class="empty">Pegá la corrección para validarla.</div>'; document.getElementById('nc-guardar').disabled = true; return; }
    this._debounce = setTimeout(async ()=>{
      try{ const r = await Api.post('/api/validar', {texto:t}); this.mostrarValidacion(r.validacion); }
      catch(e){ /* silencioso: es solo feedback en vivo */ }
    }, 350);
  },
  mostrarValidacion(v){
    const box = document.getElementById('nc-val');
    const btn = document.getElementById('nc-guardar');
    const hint = document.getElementById('nc-guardar-hint');
    const vv = v.veredicto;
    const vtxt = vv==='bad' ? '✕ No aceptar esta corrección' : vv==='warn' ? '⚠ Válida, con observaciones' : '✓ Corrección válida';
    box.innerHTML = `<div class="verdict ${vv}">${vtxt} ${v.parsed.total!=null?'<span style="margin-left:auto;font-size:16px">'+v.parsed.total+'/100</span>':''}</div>` +
      v.resultados.map(r=>`<div class="res"><span class="dot ${r.estado}"></span><div><div>${esc(r.titulo)}</div>${r.detalle?`<div class="hint">${esc(r.detalle)}</div>`:''}</div></div>`).join('');
    btn.disabled = (vv==='bad');
    hint.textContent = vv==='bad' ? 'Corregí lo que falla o volvé a correr el agente antes de guardar.' : '';
    this._ultimaValidacion = v;
  },
  mostrarForense(dump){
    const box = document.getElementById('nc-forense');
    if(!dump){ box.innerHTML = ''; return; }
    let html = '';
    const alertas = dump.alertasSeguridad || [];
    if(alertas.length){
      html += `<div class="verdict bad" style="margin-bottom:8px">⚠ ${alertas.length} alerta(s) de seguridad detectada(s) mecánicamente</div>` +
        alertas.map(a=>`<div class="res"><span class="dot bad"></span><div><div><code>${esc(a.archivo)}</code> — ${esc(a.detalle)}</div><div class="hint">…${esc(a.contexto)}…</div></div></div>`).join('');
    }
    const g = dump.gitLog;
    if(g){
      html += `<div class="kv" style="margin-top:${alertas.length?'10px':'0'}"><span>Historial de git</span><b>${g.commits} commit(s) · ${g.autores.length} autor(es) · ${g.diasDeSpread} día(s) de spread</b></div>`;
    } else {
      html += `<div class="hint" style="margin-top:${alertas.length?'10px':'0'}">Sin historial de git disponible en esta carpeta (¿llegó por ZIP?).</div>`;
    }
    box.innerHTML = html;
  },
  async guardar(){
    const p = this.proyectoActual();
    if(!p){ UI.toast('Elegí un proyecto.', 'bad'); return; }
    const raw = document.getElementById('nc-salida').value;
    if(!raw.trim()){ UI.toast('Pegá y validá la corrección primero.', 'bad'); return; }
    if(this._salidaProyectoId && this._salidaProyectoId !== p.id){
      UI.toast('Esta corrección se generó para otro proyecto. Volvé a correrla antes de guardar.', 'bad', 8000);
      return;
    }
    try{
      await Api.post('/api/corrections', {projectId:p.id, fecha:document.getElementById('nc-fecha').value, raw});
      await Promise.all([refreshCorrections()]);
      updateNavBadges();
      document.getElementById('nc-salida').value = '';
      document.getElementById('nc-val').innerHTML = '';
      UI.toast('Corrección guardada.');
      Router.go('resultados');
    }catch(e){ UI.toast(e.message, 'bad', 6000); }
  },
};

/* ---------------------------------------------------------- Resultados */
const Resultados = {
  render(){
    const filtroSel = document.getElementById('res-filtro');
    const fv = filtroSel.value;
    filtroSel.innerHTML = '<option value="">Todos los proyectos</option>' + STATE.projects.map(p=>`<option value="${p.id}">${esc(p.nombre)}</option>`).join('');
    filtroSel.value = fv;

    let list = STATE.corrections.slice().sort((a,b)=>(b.guardado||'').localeCompare(a.guardado||''));
    if(fv) list = list.filter(c=>c.projectId===fv);

    document.getElementById('res-count').textContent = list.length + ' corrección(es)';
    const box = document.getElementById('tabla-resultados');
    if(!list.length){ box.innerHTML = '<div class="empty">No hay correcciones para este filtro.</div>'; return; }

    const rows = list.map(c=>{
      const p = STATE.projects.find(x=>x.id===c.projectId);
      const r = c.total!=null? rangoDe(c.total) : {tipo:'muted'};
      const vtag = c.veredicto==='bad'?'<span class="tag t-bad">no válida</span>':c.veredicto==='warn'?'<span class="tag t-warn">con avisos</span>':'<span class="tag t-ok">válida</span>';
      return `<tr class="rowbtn" onclick="Resultados.verDetalle('${c.id}')">
        <td><b>${esc(p?p.nombre:'—')}</b></td>
        <td>${esc(c.fecha||'—')}</td>
        <td><span class="tag t-${r.tipo}">${c.total!=null? esc(c.total)+'/100':'—'}</span></td>
        <td>${(c.banderas||[]).map(b=>`<span class="pill">${esc(b)}</span>`).join('')||'<span class="hint">ninguna</span>'}</td>
        <td>${vtag}</td>
        <td><button class="btn danger sm" onclick="event.stopPropagation();Resultados.borrar('${c.id}')">Borrar</button></td>
      </tr>`;
    }).join('');
    box.innerHTML = `<table><tr><th>Proyecto</th><th>Fecha</th><th>Total</th><th>Banderas</th><th>Estado</th><th></th></tr>${rows}</table>`;
  },
  async borrar(id){
    if(!confirm('¿Borrar esta corrección?')) return;
    try{ await Api.del('/api/corrections/'+id); await refreshCorrections(); this.render(); updateNavBadges(); }
    catch(e){ UI.toast(e.message, 'bad'); }
  },
  verDetalle(id){
    const c = STATE.corrections.find(x=>x.id===id);
    const p = STATE.projects.find(x=>x.id===c.projectId);
    const root = document.getElementById('modal-root');
    const r = rangoDe(c.total);
    root.innerHTML = `
      <div class="modal-bg" onclick="if(event.target===this)UI_closeModal()">
        <div class="modal" style="max-width:820px">
          <span class="modal-close" onclick="UI_closeModal()">×</span>
          <h2 style="margin-top:0">${esc(p?p.nombre:'—')} <span class="hint">· ${c.fecha||''}</span></h2>
          <div class="verdict ${c.veredicto}">${c.veredicto==='bad'?'✕ No válida':c.veredicto==='warn'?'⚠ Válida con observaciones':'✓ Válida'}
            ${c.total!=null?'<span style="margin-left:auto;font-size:16px">'+c.total+'/100</span>':''}</div>
          <div class="hint" style="margin-bottom:10px">${esc(r.label)}</div>
          <div class="row" style="justify-content:space-between;margin-top:20px">
            <h2 style="margin:0">Corrección completa</h2>
            <div class="row">
              <button class="btn sm" id="rd-tab-vista" onclick="Resultados.mostrarDetalleModo('vista')">👁 Vista</button>
              <button class="btn sec sm" id="rd-tab-raw" onclick="Resultados.mostrarDetalleModo('raw')">Markdown crudo</button>
            </div>
          </div>
          <div id="rd-vista" class="md-view" style="margin-top:10px;max-height:400px;overflow:auto">${mdBasico(c.raw)}</div>
          <pre id="rd-raw" class="code-block" style="max-height:400px;display:none">${esc(c.raw)}</pre>
        </div>
      </div>`;
  },
  mostrarDetalleModo(cual){
    const esVista = cual === 'vista';
    document.getElementById('rd-vista').style.display = esVista ? 'block' : 'none';
    document.getElementById('rd-raw').style.display = esVista ? 'none' : 'block';
    document.getElementById('rd-tab-vista').className = 'btn sm' + (esVista ? '' : ' sec');
    document.getElementById('rd-tab-raw').className = 'btn sm' + (esVista ? ' sec' : '');
  },
};

/* ---------------------------------------------------------- Comparar */
const Comparar = {
  render(){
    const box = document.getElementById('comparar-lista');
    if(!STATE.corrections.length){ box.innerHTML = '<div class="empty">Todavía no hay correcciones para comparar.</div>'; document.getElementById('comparar-resultado').innerHTML=''; return; }
    const list = STATE.corrections.slice().sort((a,b)=>(b.guardado||'').localeCompare(a.guardado||''));
    box.innerHTML = list.map(c=>{
      const p = STATE.projects.find(x=>x.id===c.projectId);
      return `<label class="checkline" style="margin-bottom:8px"><input type="checkbox" value="${c.id}" onchange="Comparar.actualizar()">
        <b>${esc(p?p.nombre:'—')}</b> <span class="hint">${esc(c.fecha||'')} · ${c.total!=null?esc(c.total)+'/100':'sin total'}</span></label>`;
    }).join('');
    document.getElementById('comparar-resultado').innerHTML = '<div class="card"><div class="empty">Elegí dos o más correcciones a la izquierda.</div></div>';
  },
  actualizar(){
    const ids = [...document.querySelectorAll('#comparar-lista input:checked')].map(i=>i.value);
    const box = document.getElementById('comparar-resultado');
    if(ids.length < 2){ box.innerHTML = '<div class="card"><div class="empty">Elegí al menos dos correcciones.</div></div>'; return; }
    const items = ids.map(id=>{
      const c = STATE.corrections.find(x=>x.id===id);
      const p = STATE.projects.find(x=>x.id===c.projectId);
      return {c,p};
    });
    let head = '<tr><th>Dimensión</th>' + items.map(i=>`<th>${esc(i.p?i.p.nombre:'—')}<div class="hint">${esc(i.c.fecha||'')}</div></th>`).join('') + '</tr>';
    let rows = '';
    for(let d=1; d<=5; d++){
      rows += `<tr><td>${DIM_LABEL[d]}</td>` + items.map(i=>{
        const dim = (i.c.dims||[]).find(x=>x.num===d);
        if(!dim) return '<td class="hint">—</td>';
        const pct = Math.round(dim.score/dim.max*100);
        return `<td><div class="bar-row" style="margin-bottom:0"><div class="bar-track" style="max-width:90px"><div class="bar-fill" style="width:${pct}%;background:${DIM_COLOR[d]}"></div></div><div class="bar-val" style="width:auto">${dim.score}/${dim.max}</div></div></td>`;
      }).join('') + '</tr>';
    }
    rows += `<tr><td><b>Total</b></td>` + items.map(i=>`<td><b>${i.c.total!=null?esc(i.c.total)+'/100':'—'}</b></td>`).join('') + '</tr>';
    rows += `<tr><td>Banderas</td>` + items.map(i=>`<td>${(i.c.banderas||[]).map(b=>`<span class="pill">${esc(b)}</span>`).join('')||'<span class="hint">ninguna</span>'}</td>`).join('') + '</tr>';
    box.innerHTML = `<div class="card"><h2>Comparación</h2><div style="overflow-x:auto;margin-top:10px"><table>${head}${rows}</table></div></div>`;
  },
};

/* ---------------------------------------------------------- Datos */
const Datos = {
  async exportar(){
    try{
      const data = await Api.get('/api/export');
      const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = 'evaluador-backup-'+new Date().toISOString().slice(0,10)+'.json';
      document.body.appendChild(a); a.click(); a.remove();
      URL.revokeObjectURL(url);
    }catch(e){ UI.toast(e.message, 'bad'); }
  },
  importar(modo){
    const f = document.getElementById('import-file').files[0];
    if(!f){ UI.toast('Elegí un archivo .json primero.', 'bad'); return; }
    if(modo==='replace' && !confirm('Esto reemplaza todos los proyectos y correcciones actuales. ¿Seguro?')) return;
    const reader = new FileReader();
    reader.onload = async ()=>{
      let data;
      try{ data = JSON.parse(reader.result); }catch(e){ UI.toast('El archivo no es un JSON válido.', 'bad'); return; }
      if(!data.projects || !data.corrections){ UI.toast('El archivo no tiene el formato esperado.', 'bad'); return; }
      try{
        const r = await Api.post('/api/import', {data, modo});
        await Promise.all([refreshProjects(), refreshCorrections()]);
        updateNavBadges();
        UI.toast(`Importación completa: ${r.projects} proyecto(s), ${r.corrections} corrección(es).`);
      }catch(e){ UI.toast(e.message, 'bad'); }
    };
    reader.readAsText(f);
  },
};

/* ---------------------------------------------------------- Config (Doppler) */
const Config = {
  async render(){ await this.refresh(); },
  async refresh(){
    const box = document.getElementById('doppler-status');
    box.innerHTML = '<div class="skeleton" style="height:60px"></div>';
    try{
      const st = await Api.get('/api/doppler/status');
      if(st.connected && st.fuente === 'doppler'){
        box.innerHTML = `
          <div class="verdict ok">✓ Conectado vía Doppler</div>
          <div class="kv"><span>Config</span><b>${esc(st.projectConfig||'—')}</b></div>
          <div class="kv"><span>API key</span><code>${esc(st.maskedKey)}</code></div>
          <div class="kv"><span>Modelo</span><b>${esc(st.model)}</b></div>
          <div class="kv"><span>Token leído de</span><span class="hint">${esc(st.tokenSource||'—')}</span></div>`;
      } else if(st.connected && st.fuente === 'env_directo'){
        box.innerHTML = `
          <div class="verdict ok">✓ Conectado — ANTHROPIC_API_KEY directa (sin Doppler)</div>
          <div class="kv"><span>API key</span><code>${esc(st.maskedKey)}</code></div>
          <div class="kv"><span>Modelo</span><b>${esc(st.model)}</b></div>
          <div class="hint" style="margin-top:8px">Este modo es el atajo para probar la app con tu propia cuenta, sin configurar Doppler.</div>`;
      } else if(st.hasToken){
        box.innerHTML = `<div class="verdict bad">✕ Hay un token de Doppler pero falló</div><div class="hint">${esc(st.error||'')}</div>`;
      } else {
        box.innerHTML = `<div class="verdict warn">⚠ Sin ninguna fuente de API key configurada</div>
          <div class="hint">Opción 1 (grupo): variable de entorno <code>DOPPLER_TOKEN</code>, o pegá un token acá al lado.<br>
          Opción 2 (probarla suelta): definí <code>ANTHROPIC_API_KEY</code> como variable de entorno con tu propia clave.</div>`;
      }
    }catch(e){ box.innerHTML = `<div class="verdict bad">${esc(e.message)}</div>`; }
  },
  async probar(){ await this.refresh(); UI.toast('Estado de Doppler actualizado.', 'ok', 2000); },
  async guardarToken(){
    const t = document.getElementById('cfg-doppler-token').value.trim();
    if(!t){ UI.toast('Pegá un token primero.', 'bad'); return; }
    try{
      await Api.post('/api/doppler/token', {token:t});
      document.getElementById('cfg-doppler-token').value = '';
      UI.toast('Token guardado y verificado contra Doppler.');
      await this.refresh();
    }catch(e){ UI.toast(e.message, 'bad', 7000); }
  },
};

/* ---------------------------------------------------------- Rúbrica */
const Rubrica = {
  data: null,
  activa: 'rubrica',
  async render(){
    const box = document.getElementById('rb-contenido');
    if(!this.data) box.innerHTML = '<div class="skeleton" style="height:300px"></div>';
    try{
      this.data = await Api.get('/api/fs/rubrica');
      this.mostrar(this.activa);
    }catch(e){ box.innerHTML = `<div class="empty">${esc(e.message)}</div>`; }
  },
  mostrar(cual){
    this.activa = cual;
    const btnR = document.getElementById('rb-tab-rubrica'), btnS = document.getElementById('rb-tab-system');
    btnR.className = 'btn sm' + (cual==='rubrica' ? '' : ' sec');
    btnS.className = 'btn sm' + (cual==='system' ? '' : ' sec');
    if(!this.data) return;
    const texto = cual === 'rubrica' ? this.data.rubrica : this.data.systemPrompt;
    document.getElementById('rb-contenido').innerHTML = `<div class="md-view">${mdBasico(texto)}</div>`;
  },
};

/* ---------------------------------------------------------- Lote */
const Lote = {
  corriendo: false,
  detenerPedido: false,
  seleccionados: new Set(),
  salidas: {}, // id -> texto crudo de la última corrida de esa fila (para "Ver salida",
               // incluso cuando dio "formato inválido" o error — antes se perdía sin
               // dejar rastro apenas terminaba el lote).

  render(){
    const box = document.getElementById('lote-lista');
    if(!STATE.projects.length){
      box.innerHTML = '<div class="empty">Todavía no hay proyectos. Creá alguno en "Proyectos", o importá varios de golpe con "📋 Importar URLs".</div>';
      document.getElementById('lote-btn').disabled = true;
      return;
    }
    // Podar la selección contra los proyectos que todavía existen: borrar un
    // proyecto seleccionado dejaba su id fantasma en el Set, el contador seguía
    // contándolo y al correr el lote reventaba con un TypeError antes de la
    // primera corrida, dejando el botón deshabilitado para siempre.
    const vivos = new Set(STATE.projects.map(p=>p.id));
    [...this.seleccionados].forEach(id => { if(!vivos.has(id)) this.seleccionados.delete(id); });
    const filtro = (document.getElementById('lote-filtro').value || '').toLowerCase();
    const visibles = STATE.projects.filter(p => p.nombre.toLowerCase().includes(filtro));
    box.innerHTML = visibles.map(p =>
      `<label class="checkline" style="margin-bottom:8px;display:flex">
        <input type="checkbox" class="lote-check" value="${p.id}" ${this.seleccionados.has(p.id)?'checked':''} onchange="Lote.onCheck('${p.id}', this.checked)">
        <b>${esc(p.nombre)}</b> <span class="hint">${esc(p.ruta)}</span>
      </label>`
    ).join('') || '<div class="empty">Ningún proyecto coincide con la búsqueda.</div>';
    if(!document.getElementById('lote-fecha').value) document.getElementById('lote-fecha').value = new Date().toISOString().slice(0,10);
    this.actualizarBoton();
  },
  onCheck(id, marcado){
    if(marcado) this.seleccionados.add(id); else this.seleccionados.delete(id);
    this.actualizarBoton();
  },
  marcarTodos(marcar){
    const filtro = (document.getElementById('lote-filtro').value || '').toLowerCase();
    const visibles = STATE.projects.filter(p => p.nombre.toLowerCase().includes(filtro));
    visibles.forEach(p => marcar ? this.seleccionados.add(p.id) : this.seleccionados.delete(p.id));
    this.render();
  },
  actualizarBoton(){
    const n = this.seleccionados.size;
    document.getElementById('lote-btn').disabled = (n === 0 || this.corriendo);
    document.getElementById('lote-contador').textContent = n ? `${n} seleccionado(s) de ${STATE.projects.length}` : '';
  },
  _fmtSeg(s){ return s < 60 ? `${Math.round(s)}s` : `${Math.floor(s/60)}m ${Math.round(s%60)}s`; },

  /** Plantilla rápida: asegura que los 3 casos oficiales del repo (ya están
   * en casos/excelente, casos/flojo, casos/tramposo, ya calibrados) existan
   * como proyecto y los selecciona — para probar el lote de punta a punta
   * sin tener que darlos de alta a mano cada vez. Es idempotente: si ya
   * existen (por ruta), no los duplica. */
  async cargarCasosOficiales(){
    const CASOS = [
      {nombre:'Caso oficial — Excelente', ruta:'casos/excelente'},
      {nombre:'Caso oficial — Flojo', ruta:'casos/flojo'},
      {nombre:'Caso oficial — Tramposo', ruta:'casos/tramposo'},
    ];
    try{
      for(const c of CASOS){
        let p = STATE.projects.find(x => x.ruta === c.ruta);
        if(!p){
          const r = await Api.post('/api/projects', {nombre:c.nombre, origen:'zip', ruta:c.ruta});
          p = r.project;
          STATE.projects.push(p);
        }
        this.seleccionados.add(p.id);
      }
      await refreshProjects();
      this.render();
      updateNavBadges();
      UI.toast('Casos oficiales listos y seleccionados.', 'ok', 3000);
    }catch(e){ UI.toast(e.message, 'bad', 6000); }
  },

  async correr(){
    const ids = [...this.seleccionados];
    if(!ids.length) return;
    const fecha = document.getElementById('lote-fecha').value || new Date().toISOString().slice(0,10);
    const paralelismo = Math.max(1, parseInt(document.getElementById('lote-paralelismo').value, 10) || 1);

    this.corriendo = true;
    this.detenerPedido = false;
    this.salidas = {};
    document.getElementById('lote-btn').disabled = true;
    document.getElementById('lote-btn-detener').style.display = 'inline-flex';
    document.getElementById('lote-btn-detener').disabled = false;
    document.getElementById('lote-filtro').disabled = true;

    // Contador arrancando en "0/N" ya de entrada — antes se quedaba en "0/0"
    // hasta que terminaba la primera corrida, y eso se veía igual a colgado.
    document.getElementById('lote-progreso-fill').style.width = '0%';
    document.getElementById('lote-progreso-txt').textContent = `0/${ids.length}`;
    document.getElementById('lote-tiempo').textContent = 'Arrancando… cada corrida real puede tardar entre 20 segundos y 2 minutos — no cierres esta pestaña.';

    document.getElementById('lote-s-total').textContent = ids.length;
    document.getElementById('lote-s-hechos').textContent = `0/${ids.length}`;
    document.getElementById('lote-s-prom').textContent = '—';
    document.getElementById('lote-s-estado').textContent = 'Corriendo';
    document.getElementById('lote-s-estado2').textContent = '';

    const resBox = document.getElementById('lote-resultados');
    resBox.innerHTML = `<table><tr><th>Proyecto</th><th>Estado</th><th>Tiempo</th><th></th></tr>
      ${ids.map(id=>{
        const p = STATE.projects.find(x=>x.id===id);
        return `<tr id="lote-row-${id}"><td>${esc(p ? p.nombre : '(proyecto borrado)')}</td><td><span class="tag t-muted">pendiente</span></td><td class="hint">—</td><td></td></tr>`;
      }).join('')}</table>`;

    let hechos = 0, errores = 0;
    const totales = []; // totales con número calculado (guardados o no), para el promedio en vivo
    const inicio = Date.now();
    const actualizarTiempo = () => {
      const transcurrido = (Date.now()-inicio)/1000;
      const promedio = hechos ? transcurrido/hechos : null;
      const restante = promedio ? Math.max(0, (ids.length-hechos)*promedio/paralelismo) : null;
      document.getElementById('lote-tiempo').textContent = restante!=null
        ? `${this._fmtSeg(transcurrido)} transcurridos · ~${this._fmtSeg(restante)} restante`
        : `${this._fmtSeg(transcurrido)} transcurridos — esperando la primera corrida…`;
    };
    // Reloj en vivo, para que se note que sigue viva aunque ninguna corrida
    // haya terminado todavía (antes se quedaba en el mensaje estático de
    // "Arrancando…" durante todo el primer minuto, y se veía como colgado).
    const tick = setInterval(actualizarTiempo, 1000);
    const actualizarStats = () => {
      document.getElementById('lote-s-hechos').textContent = `${hechos}/${ids.length}`;
      const prom = totales.length ? Math.round(totales.reduce((a,b)=>a+b,0)/totales.length) : null;
      document.getElementById('lote-s-prom').textContent = prom==null ? '—' : `${prom}/100`;
      document.getElementById('lote-s-estado').textContent = this.detenerPedido ? 'Deteniendo…' : (hechos<ids.length ? 'Corriendo' : 'Listo');
      document.getElementById('lote-s-estado2').textContent = errores ? `${errores} con error o inválida` : '';
    };

    const correrUno = async (id) => {
      const p = STATE.projects.find(x=>x.id===id);
      const row = document.getElementById('lote-row-'+id);
      const t0 = Date.now();
      row.children[1].innerHTML = '<span class="tag t-warn">corriendo…</span>';
      try{
        const res = await Api.post('/api/run/auto', {projectId:id, fecha});
        this.salidas[id] = res.salida;
        if(res.validacion.parsed.total != null) totales.push(res.validacion.parsed.total);
        if(res.truncado){
          row.children[1].innerHTML = `<span class="tag t-bad">se cortó por tokens</span>`;
          errores++;
        } else if(res.validacion.veredicto === 'bad'){
          row.children[1].innerHTML = `<span class="tag t-bad">${res.validacion.parsed.total??'?'}/100 — formato inválido</span>`;
          errores++;
        } else {
          await Api.post('/api/corrections', {projectId:id, fecha, raw:res.salida});
          const r = rangoDe(res.validacion.parsed.total);
          row.children[1].innerHTML = `<span class="tag t-${r.tipo}">${res.validacion.parsed.total}/100 — guardada</span>`;
        }
      }catch(e){
        row.children[1].innerHTML = `<span class="tag t-bad" title="${esc(e.message)}">error</span>`;
        errores++;
      }
      row.children[2].textContent = this._fmtSeg((Date.now()-t0)/1000);
      row.children[3].innerHTML = this.salidas[id] ? `<button class="btn sec sm" onclick="Lote.verSalida('${id}')">Ver salida</button>` : '';
      hechos++;
      document.getElementById('lote-progreso-fill').style.width = Math.round(hechos/ids.length*100)+'%';
      document.getElementById('lote-progreso-txt').textContent = `${hechos}/${ids.length}`;
      actualizarTiempo();
      actualizarStats();
    };

    for(let i=0; i<ids.length; i+=paralelismo){
      if(this.detenerPedido){
        ids.slice(i).forEach(id=>{ document.getElementById('lote-row-'+id).children[1].innerHTML = '<span class="tag t-muted">cancelado</span>'; });
        break;
      }
      const tanda = ids.slice(i, i+paralelismo);
      await Promise.all(tanda.map(correrUno));
    }

    clearInterval(tick);
    this.corriendo = false;
    document.getElementById('lote-btn-detener').style.display = 'none';
    document.getElementById('lote-filtro').disabled = false;
    actualizarTiempo();
    actualizarStats();
    document.getElementById('lote-tiempo').textContent += this.detenerPedido ? ' · detenido a pedido' : ' · listo';
    await refreshCorrections();
    updateNavBadges();
    this.actualizarBoton();
  },
  detener(){
    this.detenerPedido = true;
    document.getElementById('lote-btn-detener').disabled = true;
  },
  /** Salida cruda de una fila del lote — sirve tanto para repasar una
   * guardada como para ver qué pasó en una que dio "formato inválido" o
   * error, que antes no dejaba ningún rastro apenas terminaba el lote. */
  verSalida(id){
    const p = STATE.projects.find(x=>x.id===id);
    const texto = this.salidas[id] || '';
    const root = document.getElementById('modal-root');
    root.innerHTML = `
      <div class="modal-bg" onclick="if(event.target===this)UI_closeModal()">
        <div class="modal" style="max-width:760px">
          <span class="modal-close" onclick="UI_closeModal()">×</span>
          <h2 style="margin-top:0">Salida — ${esc(p?p.nombre:id)}</h2>
          <textarea class="inp" style="width:100%;min-height:360px;font-family:monospace;font-size:12.5px" readonly>${esc(texto)}</textarea>
        </div>
      </div>`;
  },
};

/* ---------------------------------------------------------- Arranque */
document.addEventListener('DOMContentLoaded', ()=>{ Auth.boot(); });

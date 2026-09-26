// 组装 sections/*.html → out/handbook.html → out/raw.pdf
// 标记语法（写在 sections 里）：
//   $...$ 行内公式，$$...$$ 独立公式（KaTeX 服务端渲染，打印时不依赖网络）
//   {{ix:English term|中文}}   英文索引条目（不显示，只记页码）
//   {{p:id}}                   引用某个 id 所在页码，显示为 p.N
//   <h1 class="chap" data-tab="L3" id="L3">…</h1>   讲次标题（进目录、页眉、侧边书签）
//   <h2 id="s3.1">…</h2>                           节标题（进目录）
import fs from 'fs';
import path from 'path';
import katex from 'katex';
import 'katex/contrib/mhchem';
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('/opt/node22/lib/node_modules/playwright');

import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const secDir = path.join(here, 'sections');
const outDir = path.join(here, 'out');
fs.mkdirSync(outDir, { recursive: true });

const pagesFile = path.join(outDir, 'pages.json');
const pages = fs.existsSync(pagesFile) ? JSON.parse(fs.readFileSync(pagesFile, 'utf8')) : {};
const pg = id => (pages[id] ?? '00');

const macros = {
  '\\bra': '\\left\\langle #1\\right|',
  '\\ket': '\\left|#1\\right\\rangle',
  '\\braket': '\\left\\langle #1\\right\\rangle',
  '\\op': '\\hat{#1}',
  '\\dd': '\\,\\mathrm{d}',
};

const unesc = t => t.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
function renderMath(src, file) {
  // 先处理 $$…$$，再处理 $…$；\$ 表示字面美元符
  src = src.replace(/\\\$/g, '\u0000');
  src = src.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => {
    try { return '<div class="eq">' + katex.renderToString(unesc(tex), { displayMode: true, macros, throwOnError: true, strict: false }) + '</div>'; }
    catch (e) { console.error(`[公式错误] ${file}: ${e.message}\n  ${tex}`); process.exitCode = 1; return `<span class="err">${tex}</span>`; }
  });
  src = src.replace(/\$([^$\n]+?)\$/g, (_, tex) => {
    try { return katex.renderToString(unesc(tex), { displayMode: false, macros, throwOnError: true, strict: false }); }
    catch (e) { console.error(`[公式错误] ${file}: ${e.message}\n  ${tex}`); process.exitCode = 1; return `<span class="err">${tex}</span>`; }
  });
  return src.replace(/\u0000/g, '$');
}

const files = fs.readdirSync(secDir).filter(f => f.endsWith('.html')).sort();
let body = '';
const index = [];   // {en, zh, id}
let ixn = 0;
for (const f of files) {
  let s = fs.readFileSync(path.join(secDir, f), 'utf8');
  s = s.replace(/\{\{ix:([^|}]+)\|([^}]*)\}\}/g, (_, en, zh) => {
    const id = 'ix' + (++ixn);
    index.push({ en: en.trim(), zh: zh.trim(), id });
    return `<span id="${id}"></span>`;
  });
  s = renderMath(s, f);
  body += `\n<!-- ${f} -->\n` + s;
}


// 目录：从 h1.chap 和 h2 收集
const toc = [];
body.replace(/<(h1|h2)([^>]*?)id="([^"]+)"[^>]*>([\s\S]*?)<\/\1>/g, (m, tag, attrs, id, inner) => {
  if (tag === 'h1' && !/class="chap"/.test(attrs)) return;
  if (/data-notoc/.test(m)) return;
  const text = inner.replace(/<span class="en">[\s\S]*?<\/span>/g, '').replace(/<span class="no">([\s\S]*?)<\/span>/g, '$1 ').replace(/<span class="katex-mathml">[\s\S]*?<\/span>/g, '').replace(/<(?!\/?(sub|sup)\b)[^>]+>/g, '').trim();
  toc.push({ tag, id, text });
});
let tocHtml = '<div class="toc">';
for (const t of toc) {
  tocHtml += t.tag === 'h1'
    ? `<a class="toc1" href="#${t.id}"><span>${t.text}</span><span class="dots"></span><span class="pn">${pg(t.id)}</span></a>`
    : `<a class="toc2" href="#${t.id}"><span>${t.text}</span><span class="dots"></span><span class="pn">${pg(t.id)}</span></a>`;
}
tocHtml += '</div>';
body = body.replace('{{TOC}}', tocHtml);

// 英文索引 A–Z：同一英文词合并页码
const byEn = new Map();
for (const e of index) {
  const k = e.en.toLowerCase();
  if (!byEn.has(k)) byEn.set(k, { en: e.en, zh: e.zh, ids: [] });
  const v = byEn.get(k); v.ids.push(e.id); if (!v.zh && e.zh) v.zh = e.zh;
}
const entries = [...byEn.values()].sort((a, b) => a.en.localeCompare(b.en, 'en', { sensitivity: 'base' }));
let ixHtml = '<div class="ixlist">';
let letter = '';
for (const e of entries) {
  const L = /[a-z]/i.test(e.en[0]) ? e.en[0].toUpperCase() : '#';
  if (L !== letter) { letter = L; ixHtml += `<div class="ixL">${L}</div>`; }
  const seen = new Set(); const ps = e.ids.filter(i => { const k = pg(i); if (seen.has(k)) return false; seen.add(k); return true; }).sort((a, b) => pg(a) - pg(b)).map(i => `<a href="#${i}">${pg(i)}</a>`).join(', ');
  ixHtml += `<div class="ixe"><b>${e.en}</b> <span class="zh">${e.zh}</span><span class="dots"></span><span class="pn">${ps}</span></div>`;
}
ixHtml += '</div>';
body = body.replace('{{INDEX}}', ixHtml);

body = body.replace(/src="img\//g, `src="file://${here}/img/`);
// 页码引用
body = body.replace(/\{\{p:([^}]+)\}\}/g, (_, id) => `<a class="pref" href="#${id}">p.${pg(id)}</a>`);
// 讲义页码引用 [L3 p52] 统一样式
body = body.replace(/\[(L\d) (p\d+(?:[–-]\d+)?(?:, ?p\d+(?:[–-]\d+)?)*)\]/g, '<span class="src">$1 $2</span>');

const nm = p => 'file://' + path.join(here, 'node_modules', p);
const html = `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>CM5235 开卷知识点汇总</title>
<link rel="stylesheet" href="${nm('katex/dist/katex.min.css')}">
<link rel="stylesheet" href="${nm('@fontsource/noto-serif-sc/400.css')}">
<link rel="stylesheet" href="${nm('@fontsource/noto-serif-sc/700.css')}">
<link rel="stylesheet" href="${nm('@fontsource/noto-sans-sc/400.css')}">
<link rel="stylesheet" href="${nm('@fontsource/noto-sans-sc/700.css')}">
<link rel="stylesheet" href="file://${path.join(here, 'style.css')}">
</head><body>${body}</body></html>`;
fs.writeFileSync(path.join(outDir, 'handbook.html'), html);
fs.writeFileSync(path.join(outDir, 'index.json'), JSON.stringify(index));
console.log(`sections=${files.length} toc=${toc.length} index=${entries.length}`);

if (process.argv.includes('--no-pdf')) process.exit();
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('file://' + path.join(outDir, 'handbook.html'), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({
  path: path.join(outDir, 'raw.pdf'), format: 'A4', printBackground: true,
  margin: { top: '17mm', bottom: '15mm', left: '17mm', right: '17mm' },
});
await browser.close();
console.log('raw.pdf ok');

// HappiWell — SEO worker
// ส่ง HTML ที่มีเนื้อหาครบให้ Google/Facebook/LINE ตั้งแต่ request แรก
// โดยใช้ไฟล์ HTML เดิมเป็น template แล้วเติมข้อมูลจาก Supabase ด้วย HTMLRewriter
// หน้าอื่นที่ไม่ได้ระบุใน run_worker_first ยังเสิร์ฟเป็น static asset ตามเดิม

const SITE = 'https://happiwellclinic.com';
const SITE_NAME = 'แฮปปี้เวลล์ คลินิกเวชกรรม';
const SUPABASE_URL = 'https://brfddpdynusxiiqopark.supabase.co';
// anon key ตัวเดียวกับที่ใช้ในหน้าเว็บอยู่แล้ว (สิทธิ์อ่านเฉพาะที่ RLS อนุญาต)
const SUPABASE_ANON_KEY =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJyZmRkcGR5bnVzeGlpcW9wYXJrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAxNDA5MDgsImV4cCI6MjA5NTcxNjkwOH0.nP6zm_9DLc0ieocf6ad53mIjn4GoaGnXzozZtTsg2BM';
const DATA_TTL = 300; // วินาที: cache ข้อมูลจาก Supabase ที่ edge
const PAGE_CACHE = 'public, max-age=0, s-maxage=300';

const CATEGORY_LABELS = { news: 'ข่าวประชาสัมพันธ์', promotion: 'โปรโมชั่น', article: 'บทความสุขภาพ' };
const CATEGORY_ORDER = ['news', 'promotion', 'article'];
const CATEGORY_META = {
  news: { bg: 'var(--mint-100)', fg: 'var(--mint-700)',
    icon: '<path d="M4 4v16l4-3h12V4H4z"/><path d="M8 9h8M8 13h5"/>' },
  promotion: { bg: 'var(--apricot-100)', fg: '#8C1D26', thumbBg: 'var(--apricot-50)', iconStroke: 'var(--red)',
    icon: '<path d="M12 2v6M9 5h6"/><path d="M7 8h10l-1 12a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2L7 8z"/>' },
  article: { bg: 'var(--teal-100)', fg: 'var(--teal-700)',
    icon: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 0 1 5 0c0 1.5-2.5 2-2.5 3.5M12 17h.01"/>' },
};

const CLINIC_JSONLD = {
  '@context': 'https://schema.org',
  '@type': 'MedicalClinic',
  '@id': SITE + '/#clinic',
  name: SITE_NAME,
  alternateName: 'HappiWell Medical Clinic',
  url: SITE + '/',
  telephone: ['+66-2-000-4586', '+66-88-683-7899'],
  address: {
    '@type': 'PostalAddress',
    streetAddress: '195 ซอยประชาอุทิศ 49',
    addressLocality: 'แขวงบางมด เขตทุ่งครุ',
    addressRegion: 'กรุงเทพมหานคร',
    postalCode: '10140',
    addressCountry: 'TH',
  },
  geo: { '@type': 'GeoCoordinates', latitude: 13.648962, longitude: 100.4964886 },
  openingHoursSpecification: [
    { '@type': 'OpeningHoursSpecification', dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], opens: '08:00', closes: '18:00' },
    { '@type': 'OpeningHoursSpecification', dayOfWeek: ['Saturday', 'Sunday'], opens: '08:00', closes: '12:00' },
  ],
  medicalSpecialty: 'PrimaryCare',
  sameAs: [
    'https://www.facebook.com/profile.php?id=61580877520013',
    'https://www.youtube.com/channel/UC5Eq6FRHeLwGObkBY81NtTw',
    'https://line.me/R/ti/p/@p49clinic',
  ],
};

// ---------- helpers ----------
function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
}
function safeUrl(u) {
  const s = String(u ?? '');
  return /^https:\/\//i.test(s) ? s : '';
}
function jsonLd(obj) {
  // กัน </script> หลุดออกจาก JSON
  return JSON.stringify(obj).replace(/</g, '\\u003c');
}
function thaiDate(d, month = 'long') {
  if (!d) return '';
  return new Date(d).toLocaleDateString('th-TH', { year: 'numeric', month, day: 'numeric', timeZone: 'Asia/Bangkok' });
}
function articleUrl(slug) {
  return '/articles/' + encodeURIComponent(slug);
}

let SB_URL = SUPABASE_URL; // ทดสอบในเครื่องตั้ง env.SUPABASE_URL ได้
async function sb(path) {
  const res = await fetch(`${SB_URL}/rest/v1/${path}`, {
    headers: { apikey: SUPABASE_ANON_KEY, Authorization: `Bearer ${SUPABASE_ANON_KEY}` },
    cf: { cacheTtl: DATA_TTL, cacheEverything: true },
  });
  if (!res.ok) throw new Error(`supabase ${res.status}`);
  return res.json();
}
const LIST_FIELDS = 'slug,title,excerpt,cover_image,category,tags,published_at,updated_at';
const listArticles = () => sb(`hw_articles?select=${LIST_FIELDS}&is_published=eq.true&order=published_at.desc`);
const getArticle = async (slug) =>
  (await sb(`hw_articles?select=*&is_published=eq.true&slug=eq.${encodeURIComponent(slug)}&limit=1`))[0] || null;

// Editor.js → HTML (ตรงกับ renderBlocks เดิมในหน้า article.html)
function renderBlocks(blocks) {
  return (blocks || []).map((b) => {
    const d = b.data || {};
    if (b.type === 'header') {
      const t = d.level === 3 ? 'h3' : 'h2';
      return `<${t}>${d.text || ''}</${t}>`;
    }
    if (b.type === 'paragraph') return `<p>${d.text || ''}</p>`;
    if (b.type === 'list') {
      const t = d.style === 'ordered' ? 'ol' : 'ul';
      const items = (d.items || []).map((it) => `<li>${typeof it === 'string' ? it : it.content || ''}</li>`).join('');
      return `<${t}>${items}</${t}>`;
    }
    if (b.type === 'quote') {
      return `<blockquote>${d.text || ''}${d.caption ? `<br><small>— ${esc(d.caption)}</small>` : ''}</blockquote>`;
    }
    if (b.type === 'image') {
      const url = safeUrl(d.file ? d.file.url : d.url);
      if (!url) return '';
      const cap = d.caption || '';
      return `<figure><img src="${esc(url)}" alt="${esc(cap)}" loading="lazy">${cap ? `<figcaption>${esc(cap)}</figcaption>` : ''}</figure>`;
    }
    return '';
  }).join('');
}

// ---------- HTMLRewriter handlers ----------
// หมายเหตุ: ห้ามตั้งชื่อ property ว่า text/comments/element เพราะ HTMLRewriter จะนึกว่าเป็น handler
class SetText {
  constructor(value) { this.value = value; }
  element(el) { el.setInnerContent(this.value); }
}
class SetAttr {
  constructor(name, value) { this.name = name; this.value = value; }
  element(el) { el.setAttribute(this.name, this.value); }
}
class SetHtml {
  constructor(html, attrs = {}) { this.html = html; this.attrs = attrs; }
  element(el) {
    el.setInnerContent(this.html, { html: true });
    for (const [k, v] of Object.entries(this.attrs)) el.setAttribute(k, v);
  }
}
class AppendHead {
  constructor(html) { this.html = html; }
  element(el) { el.append(this.html, { html: true }); }
}
class Remove {
  element(el) { el.remove(); }
}

function headTags({ canonical, title, description, image, type = 'website', robots, jsonld = [] }) {
  const tags = [
    canonical && `<link rel="canonical" href="${esc(canonical)}">`,
    robots && `<meta name="robots" content="${esc(robots)}">`,
    `<meta property="og:site_name" content="${esc(SITE_NAME)}">`,
    `<meta property="og:type" content="${esc(type)}">`,
    canonical && `<meta property="og:url" content="${esc(canonical)}">`,
    `<meta property="og:title" content="${esc(title)}">`,
    `<meta property="og:description" content="${esc(description)}">`,
    image && `<meta property="og:image" content="${esc(image)}">`,
    `<meta name="twitter:card" content="${image ? 'summary_large_image' : 'summary'}">`,
    ...jsonld.map((o) => `<script type="application/ld+json">${jsonLd(o)}</script>`),
  ];
  return '\n' + tags.filter(Boolean).join('\n') + '\n';
}

function htmlResponse(res, status = 200) {
  const h = new Headers(res.headers);
  h.set('content-type', 'text/html; charset=utf-8');
  h.set('cache-control', PAGE_CACHE);
  h.delete('etag');
  return new Response(res.body, { status, headers: h });
}
function redirect(url, status = 301) {
  return new Response(null, { status, headers: { location: url, 'cache-control': 'public, max-age=86400' } });
}
function asset(env, request, path) {
  const u = new URL(request.url);
  u.pathname = path;
  u.search = '';
  // ไม่ส่ง header ของ browser ต่อ (เช่น If-None-Match) เพื่อให้ได้ template เต็มเสมอ ไม่ใช่ 304
  return env.ASSETS.fetch(new Request(u.toString()));
}

// ---------- pages ----------
async function homePage(request, env) {
  const tpl = await asset(env, request, '/');
  let latest = [];
  try {
    const all = await listArticles();
    for (const cat of CATEGORY_ORDER) {
      const a = all.find((x) => x.category === cat);
      if (a) latest.push(a);
    }
    latest.sort((a, b) => new Date(b.published_at) - new Date(a.published_at));
  } catch (_) { /* ถ้า Supabase ล่ม ให้หน้าแรกแสดงตามเดิม (client JS โหลดเอง) */ }

  const cards = latest.map((a) => {
    const m = CATEGORY_META[a.category] || CATEGORY_META.article;
    const cover = safeUrl(a.cover_image);
    const thumb = cover
      ? `<img src="${esc(cover)}" alt="" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;">`
      : `<svg viewBox="0 0 24 24" fill="none" stroke="${m.iconStroke || m.fg}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${m.icon}</svg>`;
    return `<div class="news-card"><div class="thumb" style="background:${m.thumbBg || m.bg};">${thumb}</div><div class="body">` +
      `<span class="kicker" style="background:${m.bg};color:${m.fg};">${esc(CATEGORY_LABELS[a.category] || a.category)}</span>` +
      `<h3>${esc(a.title)}</h3><p>${esc(a.excerpt || '')}</p>` +
      `<div class="meta"><span>${esc(thaiDate(a.published_at, 'short'))}</span><a href="${articleUrl(a.slug)}">อ่านเพิ่มเติม →</a></div></div></div>`;
  }).join('');

  let rw = new HTMLRewriter().on('head', new AppendHead(headTags({
    canonical: SITE + '/',
    title: `${SITE_NAME} | HappiWell Medical Clinic`,
    description: 'คลินิกเวชกรรมเขตทุ่งครุ ซอยประชาอุทิศ 49 ตรวจรักษาโรคทั่วไป ฉีดวัคซีน ตรวจสุขภาพ ดูแลโรคเรื้อรัง รับสิทธิบัตรทอง 30 บาท และประกันสังคม เปิดทุกวัน',
    jsonld: [CLINIC_JSONLD],
  })));
  if (cards) rw = rw.on('#news-grid', new SetHtml(cards));
  return htmlResponse(rw.transform(tpl));
}

async function listPage(request, env) {
  const url = new URL(request.url);
  const tag = url.searchParams.get('tag');
  const tpl = await asset(env, request, '/articles');
  let all = [];
  try { all = await listArticles(); } catch (_) { return htmlResponse(tpl); }

  const card = (a) => {
    const cover = safeUrl(a.cover_image);
    return `<a class="article-list-card" href="${articleUrl(a.slug)}"><div class="thumb"${cover ? ` style="background-image:url('${esc(cover)}')"` : ''}></div>` +
      `<div class="body"><h3>${esc(a.title)}</h3><p>${esc(a.excerpt || '')}</p><div class="meta">${esc(thaiDate(a.published_at, 'short'))}</div></div></a>`;
  };

  let html = '';
  if (tag) {
    const items = all.filter((a) => Array.isArray(a.tags) && a.tags.includes(tag));
    html = items.length
      ? `<div class="category-block"><div class="count">${items.length} บทความ · <a href="/articles">← ดูบทความทั้งหมด</a></div><div class="article-list-grid">${items.map(card).join('')}</div></div>`
      : `<div class="empty-state">ยังไม่มีบทความที่แท็ก "${esc(tag)}"<br><br><a href="/articles">← ดูบทความทั้งหมด</a></div>`;
  } else {
    for (const cat of CATEGORY_ORDER) {
      const items = all.filter((a) => a.category === cat);
      if (!items.length) continue;
      html += `<div class="category-block"><h2>${esc(CATEGORY_LABELS[cat])}</h2><div class="count">${items.length} บทความ</div><div class="article-list-grid">${items.map(card).join('')}</div></div>`;
    }
  }

  const title = tag ? `แท็ก: ${tag} | HappiWell คลินิกเวชกรรม` : 'ข่าวสาร บทความ และโปรโมชั่น | HappiWell คลินิกเวชกรรม';
  const description = tag
    ? `รวมบทความสุขภาพที่แท็ก "${tag}" จาก ${SITE_NAME} เขตทุ่งครุ`
    : `บทความสุขภาพ ข่าวประชาสัมพันธ์ และโปรโมชั่นจาก ${SITE_NAME} เขตทุ่งครุ กรุงเทพฯ`;

  const rw = new HTMLRewriter()
    .on('title', new SetText(title))
    .on('meta[name="description"]', new Remove())
    .on('head', new AppendHead(`<meta name="description" content="${esc(description)}">` + headTags({
      canonical: SITE + '/articles' + (tag ? `?tag=${encodeURIComponent(tag)}` : ''),
      title, description,
      robots: tag ? 'noindex, follow' : undefined,
    })))
    .on('#content', new SetHtml(html));
  return htmlResponse(rw.transform(tpl));
}

async function articlePage(request, env, slug) {
  const tpl = await asset(env, request, '/article');
  let a = null;
  try { a = await getArticle(slug); } catch (_) {
    return htmlResponse(tpl); // Supabase ล่ม: ปล่อยให้ client JS ลองโหลดเอง
  }
  if (!a) {
    const notFound = new HTMLRewriter()
      .on('title', new SetText('ไม่พบบทความ | HappiWell คลินิกเวชกรรม'))
      .on('head', new AppendHead('<meta name="robots" content="noindex">'))
      .on('#content', new SetHtml('<div class="article-error">ไม่พบบทความนี้ หรือบทความอาจถูกถอดออกแล้ว <a href="/articles">กลับไปหน้ารายการข่าวสาร</a></div>', { 'data-ssr': '1' }));
    return htmlResponse(notFound.transform(tpl), 404);
  }

  let body = '';
  try { body = renderBlocks(JSON.parse(a.content).blocks); } catch (_) { body = `<p>${esc(a.content || '')}</p>`; }

  const canonical = SITE + articleUrl(a.slug);
  const cover = safeUrl(a.cover_image);
  const description = a.excerpt || a.title;
  const tags = Array.isArray(a.tags) ? a.tags : [];
  const category = CATEGORY_LABELS[a.category] || a.category;

  const content =
    `<span class="article-category">${esc(category)}</span>` +
    (tags.length ? `<div class="article-tags">${tags.map((t) => `<a class="article-tag" href="/articles?tag=${encodeURIComponent(t)}">#${esc(t)}</a>`).join('')}</div>` : '') +
    `<h1 class="article-title">${esc(a.title)}</h1>` +
    `<div class="article-meta">เผยแพร่เมื่อ <time datetime="${esc(a.published_at)}">${esc(thaiDate(a.published_at))}</time></div>` +
    (cover ? `<img class="article-cover" src="${esc(cover)}" alt="${esc(a.title)}">` : '') +
    `<div class="article-body">${body}</div>` +
    `<div class="related-cta"><h3>มีคำถามเพิ่มเติมไหม?</h3><p>ทักแชทสอบถามหรือนัดหมายได้ที่ LINE Official Account ของคลินิก</p>` +
    `<a href="https://line.me/R/ti/p/@p49clinic" target="_blank" rel="noopener" class="btn btn-line">แชทผ่าน LINE</a></div>`;

  const article = {
    '@context': 'https://schema.org',
    '@type': a.category === 'article' ? 'MedicalWebPage' : 'NewsArticle',
    headline: a.title,
    description,
    datePublished: a.published_at,
    dateModified: a.updated_at || a.published_at,
    image: cover || undefined,
    keywords: tags.length ? tags.join(', ') : undefined,
    inLanguage: 'th',
    mainEntityOfPage: canonical,
    author: { '@id': SITE + '/#clinic' },
    publisher: { '@type': 'MedicalClinic', '@id': SITE + '/#clinic', name: SITE_NAME, url: SITE + '/' },
  };
  const crumbs = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'หน้าแรก', item: SITE + '/' },
      { '@type': 'ListItem', position: 2, name: 'ข่าวสารและบทความ', item: SITE + '/articles' },
      { '@type': 'ListItem', position: 3, name: a.title, item: canonical },
    ],
  };

  const rw = new HTMLRewriter()
    .on('title', new SetText(`${a.title} | HappiWell คลินิกเวชกรรม`))
    // ลบ meta เดิมที่ client เคยเติมเอง แล้วใส่ชุดใหม่ที่มีค่าจริง
    .on('meta#meta-description', new SetAttr('content', description))
    .on('meta#og-title, meta#og-description, meta#og-image', new Remove())
    .on('script#jsonld', new Remove())
    .on('head', new AppendHead(headTags({
      canonical, title: a.title, description, image: cover, type: 'article', jsonld: [article, crumbs],
    }) + `<meta property="article:published_time" content="${esc(a.published_at)}">`))
    .on('#content', new SetHtml(content, { 'data-ssr': '1' }));
  return htmlResponse(rw.transform(tpl));
}

async function sitemap() {
  const all = await listArticles();
  let progs = [];
  try { progs = await listPrograms(); } catch (_) { /* ยังไม่มีตาราง/ล่ม: ข้ามไป */ }
  const day = (d) => (d ? new Date(d).toISOString().slice(0, 10) : undefined);
  const newest = all[0] ? day(all[0].updated_at || all[0].published_at) : undefined;
  const urls = [
    { loc: SITE + '/', lastmod: newest, priority: '1.0' },
    { loc: SITE + '/articles', lastmod: newest, priority: '0.9' },
    { loc: SITE + '/programs', lastmod: progs[0] ? day(progs.reduce((m, p) => (p.updated_at > m ? p.updated_at : m), progs[0].updated_at)) : undefined, priority: '0.9' },
    ...progs.map((p) => ({ loc: SITE + programUrl(p.slug), lastmod: day(p.updated_at), priority: '0.8' })),
    ...all.map((a) => ({ loc: SITE + articleUrl(a.slug), lastmod: day(a.updated_at || a.published_at), priority: '0.7' })),
    { loc: SITE + '/privacy', priority: '0.2' },
    { loc: SITE + '/cookies', priority: '0.2' },
  ];
  const xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    urls.map((u) => `  <url><loc>${esc(u.loc)}</loc>${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}<priority>${u.priority}</priority></url>`).join('\n') +
    '\n</urlset>\n';
  return new Response(xml, { headers: { 'content-type': 'application/xml; charset=utf-8', 'cache-control': PAGE_CACHE } });
}

// ---------- programs (โปรแกรมและราคา) ----------
const PROGRAM_FIELDS = 'id,slug,category,name,short_desc,price,price_unit,price_note,options,cover_image,is_featured,sort_order,updated_at';
const listCategories = () => sb('hw_program_categories?select=slug,name,description,sort_order&is_active=eq.true&order=sort_order.asc');
const listPrograms = () => sb(`hw_programs?select=${PROGRAM_FIELDS}&is_published=eq.true&order=sort_order.asc,name.asc`);
const getProgram = async (slug) =>
  (await sb(`hw_programs?select=*&is_published=eq.true&slug=eq.${encodeURIComponent(slug)}&limit=1`))[0] || null;
// ลิงก์เปิดแชท LINE OA พร้อมข้อความจองที่กรอกไว้ให้ (ต้องตรงกับ lineText ใน program.html)
const LINE_OA = '@p49clinic';
const LINE_ICON = '<svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 3C6.5 3 2 6.6 2 11c0 2.9 2 5.4 5 6.8-.2.8-.7 2.6-.8 3-.1.4.1.4.3.3.2-.1 2.6-1.7 3.6-2.4.6.1 1.3.1 1.9.1 5.5 0 10-3.6 10-8S17.5 3 12 3z"/></svg>';
function lineBookText(p, opt) {
  const price = opt && opt.price != null && opt.price !== '' ? opt.price : p.price;
  return ['สวัสดีค่ะ ต้องการจองคิว',
    'โปรแกรม: ' + p.name + (opt && opt.label ? ' (' + opt.label + ')' : ''),
    'ราคา: ' + (price == null ? 'สอบถามราคา' : baht(price)),
    'ชื่อ-นามสกุล: ', 'เบอร์โทร: ', 'วันที่สะดวก: '].join('\n');
}
function lineBookUrl(p, opt) {
  return 'https://line.me/R/oaMessage/' + encodeURIComponent(LINE_OA) + '/?' + encodeURIComponent(lineBookText(p, opt));
}
// slug เดิมที่เปลี่ยนชื่อแล้ว → slug ใหม่ (301)
const PROGRAM_REDIRECTS = { 'hepatitis-a-b-vaccine': 'hepatitis-b-vaccine', 'annual-health-checkup': 'health-checkup-basic' };
const FEE_NOTE = 'ราคายังไม่รวมค่าบริการทางการแพทย์ 30 บาท';
const programUrl = (slug) => '/programs/' + encodeURIComponent(slug);
const PROGRAM_ICON = {
  vaccine: '<path d="m18 2 4 4"/><path d="m17 7 3-3"/><path d="M19 9 8.7 19.3a2.4 2.4 0 0 1-3.4 0L4.7 18.7a2.4 2.4 0 0 1 0-3.4L15 5"/><path d="m9 11 4 4"/><path d="m5 19-3 3"/><path d="m14 4 6 6"/>',
  checkup: '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/>',
  'family-planning': '<path d="M12 21c-4-3-8-6.5-8-11a5 5 0 0 1 8-4 5 5 0 0 1 8 4c0 4.5-4 8-8 11z"/>',
  procedure: '<path d="M12 20l-1-1c-4-3.5-7-6.2-7-9.5A4.5 4.5 0 0 1 8.5 5 5 5 0 0 1 12 6.5 5 5 0 0 1 15.5 5 4.5 4.5 0 0 1 20 9.5c0 3.3-3 6-7 9.5z"/>',
  certificate: '<path d="M14 3v5h5"/><path d="M6 3h8l5 5v13a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M9 13h6M9 17h4"/>',
  'sexual-health': '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/>',
};
const iconSvg = (cat) => `<svg viewBox="0 0 24 24" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${PROGRAM_ICON[cat] || PROGRAM_ICON.checkup}</svg>`;
function baht(n) {
  if (n == null || n === '') return '';
  const v = Number(n);
  return '฿' + v.toLocaleString('en-US', { maximumFractionDigits: 2 });
}
function priceHtml(p) {
  if (p.price == null) return `<span class="price-ask">สอบถามราคา</span>`;
  // "เริ่มต้นต่อรายการ" → เริ่มต้น ฿100 ต่อรายการ
  const u = String(p.price_unit || '');
  const from = /^เริ่มต้น/.test(u);
  const rest = from ? u.replace(/^เริ่มต้น\s*/, '') : u;
  return (from ? '<span class="unit">เริ่มต้น</span> ' : '') +
    `<span class="price">${esc(baht(p.price))}</span>` + (rest ? ` <span class="unit">${esc(rest)}</span>` : '');
}
function listItems(arr) {
  return (Array.isArray(arr) ? arr : []).filter(Boolean).map((x) => `<li>${esc(x)}</li>`).join('');
}

async function programsPage(request, env) {
  const tpl = await asset(env, request, '/programs');
  let cats = [], progs = [];
  try { [cats, progs] = await Promise.all([listCategories(), listPrograms()]); } catch (_) { return htmlResponse(tpl); }

  const used = cats.filter((c) => progs.some((p) => p.category === c.slug));
  const chips = `<button type="button" class="active" data-cat="all" aria-pressed="true">ทั้งหมด<span class="n">${progs.length}</span></button>` +
    used.map((c) => `<button type="button" data-cat="${esc(c.slug)}" aria-pressed="false">${esc(c.name)}<span class="n">${progs.filter((p) => p.category === c.slug).length}</span></button>`).join('');

  const card = (p, cat) => {
    const cover = safeUrl(p.cover_image);
    return `<a class="pg-card" href="${programUrl(p.slug)}">` +
      `<div class="thumb"${cover ? ` style="background-image:url('${esc(cover)}')"` : ''}>${cover ? '' : iconSvg(p.category)}</div>` +
      `<div class="body"><div class="kicker">${esc(cat ? cat.name : '')}${p.is_featured ? '<span class="pg-badge">แนะนำ</span>' : ''}</div>` +
      `<h3>${esc(p.name)}</h3>${p.short_desc ? `<p>${esc(p.short_desc)}</p>` : ''}` +
      `<div class="foot"><div>${priceHtml(p)}</div><span class="more">ดูรายละเอียด →</span></div></div></a>`;
  };
  const sections = used.map((c) => {
    const items = progs.filter((p) => p.category === c.slug);
    return `<section class="pg-section" data-cat="${esc(c.slug)}" id="cat-${esc(c.slug)}"><h2>${esc(c.name)}</h2>` +
      (c.description ? `<p class="sub">${esc(c.description)}</p>` : '') +
      `<div class="pg-grid">${items.map((p) => card(p, c)).join('')}</div></section>`;
  }).join('') || '<div class="pg-empty">ยังไม่มีโปรแกรมในขณะนี้ สอบถามได้ทาง LINE @p49clinic</div>';

  const title = 'ราคาวัคซีน ตรวจสุขภาพ และโปรแกรมต่าง ๆ | HappiWell คลินิกเวชกรรม ทุ่งครุ';
  const description = 'ราคาวัคซีนไข้หวัดใหญ่ ไข้เลือดออก ปอดอักเสบ HPV แพ็กเกจตรวจสุขภาพ ยาฉีดคุมกำเนิด และบริการอื่น ๆ ที่แฮปปี้เวลล์ คลินิกเวชกรรม เขตทุ่งครุ จองคิวออนไลน์ได้';
  const itemList = {
    '@context': 'https://schema.org', '@type': 'ItemList', name: 'โปรแกรมและราคา',
    itemListElement: progs.map((p, i) => ({ '@type': 'ListItem', position: i + 1, url: SITE + programUrl(p.slug), name: p.name })),
  };
  const rw = new HTMLRewriter()
    .on('title', new SetText(title))
    .on('meta#meta-description', new SetAttr('content', description))
    .on('head', new AppendHead(headTags({ canonical: SITE + '/programs', title, description, jsonld: [itemList] })))
    .on('#cat-chips', new SetHtml(chips))
    .on('#pg-content', new SetHtml(sections));
  return htmlResponse(rw.transform(tpl));
}

async function programPage(request, env, slug) {
  const tpl = await asset(env, request, '/program');
  let p = null, cats = [];
  try { [p, cats] = await Promise.all([getProgram(slug), listCategories()]); } catch (_) {
    return htmlResponse(new HTMLRewriter().on('#pd-root', new SetHtml('<div class="pg-empty">โหลดข้อมูลไม่สำเร็จ กรุณาลองใหม่ หรือทัก LINE @p49clinic</div>')).transform(tpl), 503);
  }
  if (!p) {
    return htmlResponse(new HTMLRewriter()
      .on('title', new SetText('ไม่พบโปรแกรม | HappiWell คลินิกเวชกรรม'))
      .on('head', new AppendHead('<meta name="robots" content="noindex">'))
      .on('#pd-root', new SetHtml('<div class="pg-empty">ไม่พบโปรแกรมนี้ หรือโปรแกรมอาจถูกปิดแล้ว <a href="/programs" style="color:var(--mint-700);font-weight:700">ดูโปรแกรมทั้งหมด</a></div>'))
      .transform(tpl), 404);
  }
  const cat = cats.find((c) => c.slug === p.category);
  const cover = safeUrl(p.cover_image);
  const options = Array.isArray(p.options) ? p.options.filter((o) => o && o.label) : [];
  let body = '';
  try { body = renderBlocks(JSON.parse(p.description).blocks); } catch (_) { body = p.description ? `<p>${esc(p.description)}</p>` : ''; }

  const meta = [p.duration && `ระยะเวลา: ${p.duration}`, p.brand && `ผลิตภัณฑ์: ${p.brand}`, p.fda_reg_no && `เลขทะเบียน อย. ${p.fda_reg_no}`]
    .filter(Boolean).map((m) => `<span>${esc(m)}</span>`).join('');
  const box = (title, arr, cls = '') => (Array.isArray(arr) && arr.length ? `<div class="pd-box ${cls}"><h2>${title}</h2><ul>${listItems(arr)}</ul></div>` : '');
  const optsHtml = options.length
    ? `<div class="pd-opts" role="radiogroup" aria-label="เลือกตัวเลือก">${options.map((o, i) =>
      `<label class="pd-opt"><input type="radio" name="pd-opt" value="${i}"${i === 0 ? ' checked' : ''}>` +
      `<span class="t"><b>${esc(o.label)}</b>${o.note ? `<small>${esc(o.note)}</small>` : ''}</span>` +
      `<span class="p">${o.price != null && o.price !== '' ? esc(baht(o.price)) : 'สอบถาม'}</span></label>`).join('')}</div>`
    : '';
  const firstPrice = options.length && options[0].price != null && options[0].price !== '' ? options[0].price : p.price;
  const bigPrice = firstPrice == null
    ? '<span class="price-ask" data-sel-price>สอบถามราคา</span>'
    : (options.length ? `<span class="price" data-sel-price>${esc(baht(firstPrice))}</span>` : priceHtml(p).replace('<span class="price">', '<span class="price" data-sel-price>'));

  const lineHref = lineBookUrl(p, options[0] || null);
  const html =
    `<div class="crumbs" style="padding-top:22px"><a href="/">หน้าแรก</a> / <a href="/programs">โปรแกรมและราคา</a>${cat ? ` / <a href="/programs?cat=${esc(cat.slug)}">${esc(cat.name)}</a>` : ''}</div>` +
    `<div class="pd-layout"><article class="pd-main">` +
    (cover ? `<img class="pd-cover" src="${esc(cover)}" alt="${esc(p.name)}">` : `<div class="pd-cover ph">${iconSvg(p.category)}</div>`) +
    (cat ? `<span class="pd-cat">${esc(cat.name)}</span>` : '') +
    `<h1 class="pd-title">${esc(p.name)}</h1>` +
    (p.short_desc ? `<p class="pd-lede">${esc(p.short_desc)}</p>` : '') +
    (meta ? `<div class="pd-meta">${meta}</div>` : '') +
    `<div class="pd-body">${body}</div>` +
    `<div class="pd-boxes">${box('เหมาะกับใคร', p.suitable_for)}${box('รวมอยู่ในราคา', p.includes)}${box('ข้อควรทราบ', p.precautions, 'warn')}</div>` +
    (p.related_article_slug ? `<div class="pd-related">อ่านเพิ่มเติม: <a href="${articleUrl(p.related_article_slug)}">บทความเกี่ยวกับ${esc(p.name)} →</a></div>` : '') +
    `</article>` + (
    `<aside class="pd-aside" aria-label="ราคา"><span class="label">${options.length ? 'ราคาตัวเลือกที่เลือก' : 'ราคา'}</span><div>${bigPrice}</div>` +
    (p.price != null || options.length ? `<p class="pd-fee">${FEE_NOTE}</p>` : '') +
    (p.price_note ? `<p class="pg-note">${esc(p.price_note)}</p>` : '') + optsHtml +
    `<a href="${esc(lineHref)}" target="_blank" rel="noopener" class="btn btn-line js-line-book">${LINE_ICON}จองผ่าน LINE</a>` +
    `<a href="tel:0220004586" class="btn btn-ghost">โทร 02-000-4586</a></aside>`) +
    `<div class="pd-book-wrap"><section class="pd-book" id="booking" aria-labelledby="bk-h"><h2 id="bk-h">จองคิวผ่าน LINE</h2>` +
    `<ol class="pd-steps"><li><b>กดปุ่ม "จองผ่าน LINE"</b> ระบบจะเปิดแชท LINE ของคลินิก พร้อมข้อความจองที่กรอกโปรแกรมและราคาไว้ให้แล้ว</li>` +
    `<li><b>เติมชื่อ เบอร์โทร และวันที่สะดวก</b> แล้วกดส่ง</li>` +
    `<li><b>ทีมงานตอบกลับเพื่อยืนยันนัด</b> ในเวลาทำการ จ.–ศ. 08:00–18:00 / ส.–อา. 08:00–12:00</li></ol>` +
    `<a href="${esc(lineHref)}" target="_blank" rel="noopener" class="btn btn-line js-line-book" style="width:100%">${LINE_ICON}จองผ่าน LINE @p49clinic</a>` +
    `<p class="pg-note" style="text-align:center;margin-top:10px">ไม่สะดวกใช้ LINE โทร <a href="tel:0220004586" style="color:var(--mint-700);font-weight:600">02-000-4586</a> หรือ <a href="tel:0886837899" style="color:var(--mint-700);font-weight:600">088-683-7899</a></p></section>` +
    `<p class="pg-note" style="margin-top:20px">ราคาสำหรับผู้ชำระเงินสด ยังไม่รวมค่าบริการทางการแพทย์ 30 บาท อาจเปลี่ยนแปลงได้ ความเหมาะสมขึ้นกับการประเมินของแพทย์ ผลลัพธ์ของแต่ละบุคคลอาจแตกต่างกัน</p></div>` +
    `</div>` +
    `<div class="pd-bar"><div>${firstPrice == null ? '<span class="price-ask">สอบถามราคา</span>' : `<span class="price" data-sel-price>${esc(baht(firstPrice))}</span><small class="pd-bar-fee">+ ค่าบริการ 30 บาท</small>`}</div><a href="${esc(lineHref)}" target="_blank" rel="noopener" class="btn btn-line js-line-book">${LINE_ICON}จองผ่าน LINE</a></div>` +
    `<script type="application/json" id="program-data">${jsonLd({ name: p.name, price: p.price, price_unit: p.price_unit, options })}</script>`;

  const canonical = SITE + programUrl(p.slug);
  const title = p.seo_title || `${p.name} ราคา${p.price != null ? ' ' + baht(p.price) : ''} | HappiWell คลินิกเวชกรรม ทุ่งครุ`;
  const description = p.seo_description || p.short_desc || p.name;
  const prices = [p.price, ...options.map((o) => o.price)].filter((x) => x != null && x !== '').map(Number);
  const service = {
    '@context': 'https://schema.org', '@type': 'MedicalProcedure', name: p.name, description,
    url: canonical, image: cover || undefined,
    provider: { '@type': 'MedicalClinic', '@id': SITE + '/#clinic', name: SITE_NAME },
    offers: prices.length ? {
      '@type': prices.length > 1 ? 'AggregateOffer' : 'Offer', priceCurrency: 'THB',
      ...(prices.length > 1 ? { lowPrice: Math.min(...prices), highPrice: Math.max(...prices), offerCount: prices.length } : { price: prices[0] }),
      availability: 'https://schema.org/InStock', url: canonical,
    } : undefined,
  };
  const crumbs = {
    '@context': 'https://schema.org', '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'หน้าแรก', item: SITE + '/' },
      { '@type': 'ListItem', position: 2, name: 'โปรแกรมและราคา', item: SITE + '/programs' },
      { '@type': 'ListItem', position: 3, name: p.name, item: canonical },
    ],
  };
  const rw = new HTMLRewriter()
    .on('title', new SetText(title))
    .on('meta#meta-description', new SetAttr('content', description))
    .on('head', new AppendHead(headTags({ canonical, title: p.name, description, image: cover, type: 'website', jsonld: [service, crumbs] })))
    .on('#pd-root', new SetHtml(html));
  return htmlResponse(rw.transform(tpl));
}

// ---------- router ----------
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    if (env && env.SUPABASE_URL) SB_URL = env.SUPABASE_URL;
    if (request.method !== 'GET' && request.method !== 'HEAD') return env.ASSETS.fetch(request);

    // URL เก่า → URL ใหม่ (301 = ถาวร ให้ Google ย้ายคะแนนมา)
    if (path === '/article' || path === '/article.html') {
      const slug = url.searchParams.get('slug');
      return redirect(SITE + (slug ? articleUrl(slug) : '/articles'));
    }
    if (path === '/index.html') return redirect(SITE + '/');
    if (path === '/articles.html' || path === '/articles/') return redirect(SITE + '/articles' + url.search);
    if (path === '/privacy.html') return redirect(SITE + '/privacy');
    if (path === '/cookies.html') return redirect(SITE + '/cookies');
    if (path === '/programs.html' || path === '/programs/') return redirect(SITE + '/programs' + url.search);
    if (path === '/program' || path === '/program.html') return redirect(SITE + '/programs');

    try {
      if (path === '/') return await homePage(request, env);
      if (path === '/articles') return await listPage(request, env);
      if (path === '/sitemap.xml') return await sitemap();
      if (path === '/programs') return await programsPage(request, env);
      const pm = path.match(/^\/programs\/([^/]+)\/?$/);
      if (pm) {
        const slug = decodeURIComponent(pm[1]);
        if (PROGRAM_REDIRECTS[slug]) return redirect(SITE + programUrl(PROGRAM_REDIRECTS[slug]));
        if (path.endsWith('/')) return redirect(SITE + programUrl(slug));
        return await programPage(request, env, slug);
      }
      const m = path.match(/^\/articles\/([^/]+)\/?$/);
      if (m) {
        const slug = decodeURIComponent(m[1]);
        if (path.endsWith('/')) return redirect(SITE + articleUrl(slug));
        return await articlePage(request, env, slug);
      }
    } catch (err) {
      console.error('ssr error', path, err && err.message);
      if (path === '/sitemap.xml') return new Response('sitemap unavailable', { status: 503 });
    }
    return env.ASSETS.fetch(request);
  },
};

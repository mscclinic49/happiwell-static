// HappiWell — SEO worker (ไทย + English)
// ส่ง HTML ที่มีเนื้อหาครบให้ Google/Facebook/LINE ตั้งแต่ request แรก
// โดยใช้ไฟล์ HTML เดิมเป็น template แล้วเติมข้อมูลจาก Supabase ด้วย HTMLRewriter
// ภาษาอังกฤษอยู่ใต้ /en/... ใช้ template ใน en/*.html (สร้างด้วย src/build/en-pages.py)
// เนื้อหาภาษาอังกฤษจาก DB อยู่ในคอลัมน์ en (jsonb) ถ้ายังไม่แปล จะแสดงภาษาไทยแทนและไม่ให้ Google index หน้านั้น

const SITE = 'https://happiwellclinic.com';
const SITE_NAME = 'แฮปปี้เวลล์ คลินิกเวชกรรม';
const SITE_NAME_EN = 'HappiWell Medical Clinic';
const DEFAULT_OG = 'https://happiwellclinic.com/og-default.png';
const SUPABASE_URL = 'https://brfddpdynusxiiqopark.supabase.co';
// anon key ตัวเดียวกับที่ใช้ในหน้าเว็บอยู่แล้ว (สิทธิ์อ่านเฉพาะที่ RLS อนุญาต)
const SUPABASE_ANON_KEY =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJyZmRkcGR5bnVzeGlpcW9wYXJrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAxNDA5MDgsImV4cCI6MjA5NTcxNjkwOH0.nP6zm_9DLc0ieocf6ad53mIjn4GoaGnXzozZtTsg2BM';
const DATA_TTL = 300; // วินาที: cache ข้อมูลจาก Supabase ที่ edge
const PAGE_CACHE = 'public, max-age=0, s-maxage=300';

const CATEGORY_LABELS = {
  th: { news: 'ข่าวประชาสัมพันธ์', promotion: 'โปรโมชั่น', article: 'บทความสุขภาพ' },
  en: { news: 'News', promotion: 'Promotions', article: 'Health articles' },
};
const CATEGORY_ORDER = ['news', 'promotion', 'article'];
const CATEGORY_META = {
  news: { bg: 'var(--mint-100)', fg: 'var(--mint-700)',
    icon: '<path d="M4 4v16l4-3h12V4H4z"/><path d="M8 9h8M8 13h5"/>' },
  promotion: { bg: 'var(--apricot-100)', fg: '#8C1D26', thumbBg: 'var(--apricot-50)', iconStroke: 'var(--red)',
    icon: '<path d="M12 2v6M9 5h6"/><path d="M7 8h10l-1 12a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2L7 8z"/>' },
  article: { bg: 'var(--teal-100)', fg: 'var(--teal-700)',
    icon: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 0 1 5 0c0 1.5-2.5 2-2.5 3.5M12 17h.01"/>' },
};

// ข้อความในหน้า (ไทย / อังกฤษ)
const L = {
  th: {
    siteName: SITE_NAME, brandSuffix: 'HappiWell คลินิกเวชกรรม', locale: 'th_TH', dateLocale: 'th-TH',
    home: 'หน้าแรก', articles: 'ข่าวสารและบทความ', programs: 'โปรแกรมและราคา',
    homeTitle: 'คลินิกทุ่งครุ ประชาอุทิศ 49 รับบัตรทอง วัคซีน ตรวจสุขภาพ | แฮปปี้เวลล์ คลินิกเวชกรรม',
    homeOgTitle: `${SITE_NAME} | คลินิกทุ่งครุ ประชาอุทิศ 49`,
    homeDesc: 'คลินิกเวชกรรมเขตทุ่งครุ ซอยประชาอุทิศ 49 ตรวจรักษาโรคทั่วไป ฉีดวัคซีน ตรวจสุขภาพ ดูแลโรคเรื้อรัง รับสิทธิบัตรทอง 30 บาท และประกันสังคม เปิดทุกวัน',
    pricesEyebrow: 'ราคาชัดเจน', pricesH: 'ราคาวัคซีนและโปรแกรมยอดนิยม', pricesP: 'ราคายังไม่รวมค่าบริการทางการแพทย์ 30 บาท จองคิวผ่าน LINE ได้ทันที',
    details: 'ดูรายละเอียด →', allPrices: 'ดูราคาทั้งหมด →', from: 'เริ่มต้น', readMore: 'อ่านเพิ่มเติม →', ask: 'สอบถามราคา', askShort: 'สอบถาม',
    nArticles: (n) => `${n} บทความ`, allArticles: '← ดูบทความทั้งหมด', noTag: (t) => `ยังไม่มีบทความที่แท็ก "${t}"`,
    listTitle: 'บทความสุขภาพ ข่าวสาร และโปรโมชั่น | แฮปปี้เวลล์ คลินิก ทุ่งครุ', tagTitle: (t) => `แท็ก: ${t} | HappiWell คลินิกเวชกรรม`,
    listDesc: `บทความสุขภาพ ข่าวประชาสัมพันธ์ และโปรโมชั่นจาก ${SITE_NAME} เขตทุ่งครุ กรุงเทพฯ`, tagDesc: (t) => `รวมบทความสุขภาพที่แท็ก "${t}" จาก ${SITE_NAME} เขตทุ่งครุ`,
    articleNotFound: 'ไม่พบบทความ | HappiWell คลินิกเวชกรรม', articleNotFoundBody: 'ไม่พบบทความนี้ หรือบทความอาจถูกถอดออกแล้ว', backToList: 'กลับไปหน้ารายการข่าวสาร',
    published: 'เผยแพร่เมื่อ', relatedH: 'บริการนี้ที่แฮปปี้เวลล์ คลินิก ทุ่งครุ', relatedNote: 'ราคายังไม่รวมค่าบริการทางการแพทย์ 30 บาท · จองผ่าน LINE ได้จากหน้าราคา',
    ctaH: 'มีคำถามเพิ่มเติมไหม?', ctaP: 'ทักแชทสอบถามหรือนัดหมายได้ที่ LINE Official Account ของคลินิก', ctaBtn: 'แชทผ่าน LINE',
    thaiOnly: '', all: 'ทั้งหมด', recommended: 'แนะนำ', noPrograms: 'ยังไม่มีโปรแกรมในขณะนี้ สอบถามได้ทาง LINE @p49clinic',
    programsTitle: 'ราคาวัคซีน ตรวจสุขภาพ และโปรแกรมต่าง ๆ | HappiWell คลินิกเวชกรรม ทุ่งครุ',
    programsDesc: 'ราคาวัคซีนไข้หวัดใหญ่ ไข้เลือดออก ปอดอักเสบ HPV แพ็กเกจตรวจสุขภาพ ยาฉีดคุมกำเนิด และบริการอื่น ๆ ที่แฮปปี้เวลล์ คลินิกเวชกรรม เขตทุ่งครุ จองคิวออนไลน์ได้',
    loadFail: 'โหลดข้อมูลไม่สำเร็จ กรุณาลองใหม่ หรือทัก LINE @p49clinic', programNotFound: 'ไม่พบโปรแกรม | HappiWell คลินิกเวชกรรม',
    programNotFoundBody: 'ไม่พบโปรแกรมนี้ หรือโปรแกรมอาจถูกปิดแล้ว', seeAllPrograms: 'ดูโปรแกรมทั้งหมด',
    duration: 'ระยะเวลา: ', product: 'ผลิตภัณฑ์: ', fda: 'เลขทะเบียน อย. ', chooseOpt: 'เลือกตัวเลือก', choosePkg: 'เลือกชุดตรวจ',
    items: 'รายการ', priceLabel: 'ราคา', priceSel: 'ราคาตัวเลือกที่เลือก', fee: 'ราคายังไม่รวมค่าบริการทางการแพทย์ 30 บาท',
    bookLine: 'จองผ่าน LINE', call: '📞 โทร 02-000-4586', inclPkg: 'รวมอยู่ในแพ็กเกจ', incl: 'รวมอยู่ในราคา', suitable: 'เหมาะกับใคร',
    beforePkg: 'ก่อนมาตรวจ', notes: 'ข้อควรทราบ', readMoreAbout: (n) => `บทความเกี่ยวกับ${n} →`, readMoreLbl: 'อ่านเพิ่มเติม: ',
    others: (c) => `${c}อื่น ๆ ที่คลินิก`, othersFallback: 'โปรแกรม', bookH: 'จองคิวง่าย ๆ 2 วิธี', bookLine2: 'ทัก LINE จองคิว',
    hours: 'เปิดทุกวัน · จันทร์–ศุกร์ 08:00–18:00 · เสาร์–อาทิตย์ 08:00–12:00<br>หรือโทร <a href="tel:0886837899">088-683-7899</a>',
    disclaimer: 'ราคาสำหรับผู้ชำระเงินสด ยังไม่รวมค่าบริการทางการแพทย์ 30 บาท อาจเปลี่ยนแปลงได้ ความเหมาะสมขึ้นกับการประเมินของแพทย์ ผลลัพธ์ของแต่ละบุคคลอาจแตกต่างกัน',
    barFee: '+ ค่าบริการ 30 บาท', programTitle: (n, pr) => `${n} ราคา${pr ? ' ' + pr : ''} | HappiWell คลินิกเวชกรรม ทุ่งครุ`,
    lineHello: 'สวัสดีค่ะ ต้องการจองคิว', lineProgram: 'โปรแกรม: ', linePrice: 'ราคา: ', lineName: 'ชื่อ-นามสกุล: ', linePhone: 'เบอร์โทร: ', lineDate: 'วันที่สะดวก: ',
  },
  en: {
    siteName: SITE_NAME_EN, brandSuffix: 'HappiWell Medical Clinic', locale: 'en_US', dateLocale: 'en-GB',
    home: 'Home', articles: 'News & articles', programs: 'Prices & services',
    homeTitle: 'HappiWell Medical Clinic | GP Clinic in Thung Khru, Pracha Uthit 49, Bangkok',
    homeOgTitle: `${SITE_NAME_EN} | Thung Khru, Bangkok`,
    homeDesc: 'English-friendly medical clinic in Thung Khru, Soi Pracha Uthit 49, Bangkok (near Bang Mod). General practice, vaccinations, health check-ups and medical certificates with clear prices. Open every day.',
    pricesEyebrow: 'Clear prices', pricesH: 'Popular vaccines and services', pricesP: 'Prices exclude the 30 baht medical service fee. Book instantly via LINE.',
    details: 'View details →', allPrices: 'See all prices →', from: 'from', readMore: 'Read more →', ask: 'Ask for price', askShort: 'Ask',
    nArticles: (n) => `${n} article${n === 1 ? '' : 's'}`, allArticles: '← See all articles', noTag: (t) => `No articles tagged "${t}"`,
    listTitle: 'Health Articles, News & Promotions | HappiWell Medical Clinic, Bangkok', tagTitle: (t) => `Tag: ${t} | HappiWell Medical Clinic`,
    listDesc: 'Health articles, clinic news and promotions from HappiWell Medical Clinic in Thung Khru, Bangkok.', tagDesc: (t) => `Health articles tagged "${t}" from HappiWell Medical Clinic, Bangkok.`,
    articleNotFound: 'Article not found | HappiWell Medical Clinic', articleNotFoundBody: 'This article was not found or has been removed.', backToList: 'Back to all news',
    published: 'Published', relatedH: 'This service at HappiWell Medical Clinic', relatedNote: 'Prices exclude the 30 baht medical service fee · Book via LINE from the price page',
    ctaH: 'Have a question?', ctaP: 'Chat with us or book an appointment on the clinic’s LINE Official Account', ctaBtn: 'Chat on LINE',
    thaiOnly: 'This page is currently available in Thai only. Please chat with us on LINE if you have any questions.',
    all: 'All', recommended: 'Recommended', noPrograms: 'No services listed right now. Ask us on LINE @p49clinic',
    programsTitle: 'Vaccine & Health Check-up Prices in Bangkok | HappiWell Medical Clinic',
    programsDesc: 'Prices for flu, dengue, pneumococcal and HPV vaccines, health check-up packages, contraceptive injections and more at HappiWell Medical Clinic, Thung Khru, Bangkok. Book via LINE.',
    loadFail: 'Could not load this page. Please try again or chat with us on LINE @p49clinic', programNotFound: 'Service not found | HappiWell Medical Clinic',
    programNotFoundBody: 'This service was not found or is no longer offered.', seeAllPrograms: 'See all services',
    duration: 'Duration: ', product: 'Product: ', fda: 'Thai FDA reg. no. ', chooseOpt: 'Choose an option', choosePkg: 'Choose a package',
    items: 'items', priceLabel: 'Price', priceSel: 'Price for selected option', fee: 'Price excludes the 30 baht medical service fee',
    bookLine: 'Book via LINE', call: '📞 Call 02-000-4586', inclPkg: 'Included in the package', incl: 'Included in the price', suitable: 'Who is it for?',
    beforePkg: 'Before your check-up', notes: 'Good to know', readMoreAbout: (n) => `About ${n} →`, readMoreLbl: 'Read more: ',
    others: (c) => `Other ${c.toLowerCase()} at the clinic`, othersFallback: 'services', bookH: 'Two easy ways to book', bookLine2: 'Book on LINE',
    hours: 'Open every day · Mon–Fri 08:00–18:00 · Sat–Sun 08:00–12:00<br>or call <a href="tel:0886837899">088-683-7899</a>',
    disclaimer: 'Prices are for self-paying patients and exclude the 30 baht medical service fee. Prices may change. Suitability depends on the doctor’s assessment, and individual results may vary.',
    barFee: '+ 30 baht service fee', programTitle: (n, pr) => `${n}${pr ? ' – ' + pr : ''} | HappiWell Medical Clinic, Bangkok`,
    lineHello: 'Hello, I would like to book an appointment', lineProgram: 'Service: ', linePrice: 'Price: ', lineName: 'Full name: ', linePhone: 'Phone: ', lineDate: 'Preferred date: ',
  },
};

function clinicJsonLd(lang) {
  const en = lang === 'en';
  return {
    '@context': 'https://schema.org',
    '@type': 'MedicalClinic',
    '@id': SITE + '/#clinic',
    name: en ? SITE_NAME_EN : SITE_NAME,
    alternateName: en ? SITE_NAME : SITE_NAME_EN,
    url: SITE + (en ? '/en/' : '/'),
    telephone: ['+66-2-000-4586', '+66-88-683-7899'],
    address: en
      ? { '@type': 'PostalAddress', streetAddress: '195 Soi Pracha Uthit 49', addressLocality: 'Bang Mot, Thung Khru', addressRegion: 'Bangkok', postalCode: '10140', addressCountry: 'TH' }
      : { '@type': 'PostalAddress', streetAddress: '195 ซอยประชาอุทิศ 49', addressLocality: 'แขวงบางมด เขตทุ่งครุ', addressRegion: 'กรุงเทพมหานคร', postalCode: '10140', addressCountry: 'TH' },
    geo: { '@type': 'GeoCoordinates', latitude: 13.648962, longitude: 100.4964886 },
    openingHoursSpecification: [
      { '@type': 'OpeningHoursSpecification', dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], opens: '08:00', closes: '18:00' },
      { '@type': 'OpeningHoursSpecification', dayOfWeek: ['Saturday', 'Sunday'], opens: '08:00', closes: '12:00' },
    ],
    medicalSpecialty: 'PrimaryCare',
    logo: SITE + '/logo.png',
    image: [SITE + '/og-default.png'],
    priceRange: '฿50 – ฿7,200',
    currenciesAccepted: 'THB',
    availableLanguage: ['th', 'en'],
    hasMap: 'https://www.google.com/maps?q=13.648962,100.4964886',
    areaServed: (en ? ['Thung Khru', 'Bang Mot', 'Pracha Uthit', 'Rat Burana', 'Chom Thong', 'Bang Khun Thian', 'Phra Pradaeng']
      : ['ทุ่งครุ', 'บางมด', 'ประชาอุทิศ', 'ราษฎร์บูรณะ', 'จอมทอง', 'บางขุนเทียน', 'พระประแดง']).map((n) => ({ '@type': 'Place', name: n })),
    isAcceptingNewPatients: true,
    sameAs: [
      'https://www.facebook.com/profile.php?id=61580877520013',
      'https://www.youtube.com/channel/UC5Eq6FRHeLwGObkBY81NtTw',
      'https://line.me/R/ti/p/@p49clinic',
    ],
  };
}

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
function fmtDate(d, lang = 'th', month = 'long') {
  if (!d) return '';
  return new Date(d).toLocaleDateString(L[lang].dateLocale, { year: 'numeric', month, day: 'numeric', timeZone: 'Asia/Bangkok' });
}
// ลิงก์ภายในตามภาษา: lp('/programs','en') → '/en/programs', lp('/','en') → '/en/'
const lp = (path, lang) => (lang === 'en' ? (path === '/' ? '/en/' : '/en' + path) : path);
const articleUrl = (slug, lang = 'th') => lp('/articles/' + encodeURIComponent(slug), lang);
const programUrl = (slug, lang = 'th') => lp('/programs/' + encodeURIComponent(slug), lang);
// ค่าภาษาอังกฤษจากคอลัมน์ en ถ้ามี ไม่งั้นใช้ภาษาไทย
const enOf = (row) => (row && row.en && typeof row.en === 'object' ? row.en : {});
const has = (v) => v != null && !(typeof v === 'string' && !v.trim()) && !(Array.isArray(v) && !v.length);
function pick(row, field, lang) {
  if (lang === 'en') {
    const e = enOf(row);
    if (has(e[field])) return e[field];
    if (has(row[field + '_en'])) return row[field + '_en']; // จาก select แบบ alias (en->>field)
  }
  return row[field];
}
const isTranslated = (row, key) => has(enOf(row)[key]) || has(row[key + '_en']);

let SB_URL = SUPABASE_URL; // ทดสอบในเครื่องตั้ง env.SUPABASE_URL ได้
async function sb(path) {
  const res = await fetch(`${SB_URL}/rest/v1/${path}`, {
    headers: { apikey: SUPABASE_ANON_KEY, Authorization: `Bearer ${SUPABASE_ANON_KEY}` },
    cf: { cacheTtl: DATA_TTL, cacheEverything: true },
  });
  if (!res.ok) throw new Error(`supabase ${res.status}`);
  return res.json();
}
const LIST_FIELDS = 'slug,title,excerpt,cover_image,category,tags,published_at,updated_at,title_en:en->>title,excerpt_en:en->>excerpt';
const listArticles = () => sb(`hw_articles?select=${LIST_FIELDS}&is_published=eq.true&order=published_at.desc`);
const getArticle = async (slug) =>
  (await sb(`hw_articles?select=*&is_published=eq.true&slug=eq.${encodeURIComponent(slug)}&limit=1`))[0] || null;

// Editor.js → HTML (ตรงกับ renderBlocks เดิมในหน้า article.html)
// lang=en: ลิงก์ในเนื้อหาที่ชี้มาหน้าในเว็บ (/programs, /articles) จะถูกเปลี่ยนเป็น /en/...
function renderBlocks(blocks, lang = 'th') {
  const html = (blocks || []).map((b) => {
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
  }).join('')
    // ลิงก์แบบเก่า article.html?slug=x (ลิงก์ relative จะพังเมื่ออยู่ใต้ /articles/) → /articles/x
    .replace(/href="(?:https:\/\/happiwellclinic\.com)?\/?article(?:\.html)?\?slug=([^"&#]+)"/g, 'href="/articles/$1"');
  if (lang !== 'en') return html;
  return html.replace(/href="(?:https:\/\/happiwellclinic\.com)?\/(programs|articles)(?=[/"?#])/g, 'href="/en/$1');
}
function renderContent(json, lang) {
  if (!json) return '';
  try { return renderBlocks(JSON.parse(json).blocks, lang); } catch (_) { return `<p>${esc(json)}</p>`; }
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

// alternates: { th: url, en: url } — ใส่ hreflang ให้ Google รู้ว่าเป็นหน้าเดียวกันคนละภาษา
function headTags({ canonical, title, description, image, type = 'website', robots, jsonld = [], lang = 'th', alternates }) {
  const tags = [
    canonical && `<link rel="canonical" href="${esc(canonical)}">`,
    ...(alternates ? [
      alternates.th && `<link rel="alternate" hreflang="th" href="${esc(alternates.th)}">`,
      alternates.en && `<link rel="alternate" hreflang="en" href="${esc(alternates.en)}">`,
      alternates.th && `<link rel="alternate" hreflang="x-default" href="${esc(alternates.th)}">`,
    ] : []),
    robots && `<meta name="robots" content="${esc(robots)}">`,
    `<meta property="og:site_name" content="${esc(L[lang].siteName)}">`,
    `<meta property="og:locale" content="${L[lang].locale}">`,
    `<meta property="og:type" content="${esc(type)}">`,
    canonical && `<meta property="og:url" content="${esc(canonical)}">`,
    `<meta property="og:title" content="${esc(title)}">`,
    `<meta property="og:description" content="${esc(description)}">`,
    `<meta property="og:image" content="${esc(image || DEFAULT_OG)}">`,
    `<meta name="twitter:card" content="summary_large_image">`,
    ...jsonld.map((o) => `<script type="application/ld+json">${jsonLd(o)}</script>`),
  ];
  return '\n' + tags.filter(Boolean).join('\n') + '\n';
}
// ปุ่มเปลี่ยนภาษาในเมนู ให้ชี้ไปหน้าเดียวกันอีกภาษา
const langSwitch = (href) => ({ element(el) { el.setAttribute('href', href); } });

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
const tplPath = (path, lang) => (lang === 'en' ? (path === '/' ? '/en/' : '/en' + path) : path);

// ---------- pages ----------
async function homePage(request, env, lang = 'th') {
  const t = L[lang];
  const tpl = await asset(env, request, tplPath('/', lang));
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
      `<span class="kicker" style="background:${m.bg};color:${m.fg};">${esc(CATEGORY_LABELS[lang][a.category] || a.category)}</span>` +
      `<h3>${esc(pick(a, 'title', lang))}</h3><p>${esc(pick(a, 'excerpt', lang) || '')}</p>` +
      `<div class="meta"><span>${esc(fmtDate(a.published_at, lang, 'short'))}</span><a href="${articleUrl(a.slug, lang)}">${t.readMore}</a></div></div></div>`;
  }).join('');

  let featured = [];
  try {
    const progs = await listPrograms();
    featured = progs.filter((p) => p.price != null).sort((a, b) => (b.is_featured - a.is_featured) || (a.sort_order - b.sort_order)).slice(0, 6);
  } catch (_) {}
  const featuredHtml = featured.length
    ? `<section id="prices"><div class="wrap"><div class="section-head"><div class="eyebrow">${t.pricesEyebrow}</div><h2>${t.pricesH}</h2>` +
      `<p>${t.pricesP}</p></div><div class="service-grid">` +
      featured.map((p) => `<a class="service-card" href="${programUrl(p.slug, lang)}" style="display:flex;flex-direction:column;gap:6px;text-decoration:none">` +
        `<h3>${esc(pick(p, 'name', lang))}</h3><p>${esc(pick(p, 'short_desc', lang) || '')}</p>` +
        `<div style="margin-top:auto;padding-top:8px;display:flex;justify-content:space-between;align-items:baseline;gap:8px">` +
        `<span style="font-family:Anuphan,sans-serif;font-weight:700;font-size:20px;color:var(--apricot-600)">${/^เริ่มต้น/.test(p.price_unit || '') ? `<small style="font-size:13px;color:var(--ink-soft);font-weight:500">${t.from} </small>` : ''}${esc(baht(p.price))}</span>` +
        `<span style="font-size:13.5px;font-weight:600;color:var(--mint-700)">${t.details}</span></div></a>`).join('') +
      `</div><div style="margin-top:22px"><a href="${lp('/programs', lang)}" class="btn btn-primary">${t.allPrices}</a></div></div></section>`
    : '';

  let rw = new HTMLRewriter()
    .on('title', new SetText(t.homeTitle))
    .on('meta[name="description"]', new SetAttr('content', t.homeDesc))
    .on('a.lang-sw', langSwitch(lang === 'en' ? '/' : '/en/'))
    .on('head', new AppendHead(headTags({
      canonical: SITE + lp('/', lang),
      title: t.homeOgTitle,
      description: t.homeDesc,
      jsonld: [clinicJsonLd(lang)],
      lang,
      alternates: { th: SITE + '/', en: SITE + '/en/' },
    })));
  if (cards) rw = rw.on('#news-grid', new SetHtml(cards));
  if (featuredHtml) rw = rw.on('section#coverage', { element(el) { el.before(featuredHtml, { html: true }); } });
  return htmlResponse(rw.transform(tpl));
}

async function listPage(request, env, lang = 'th') {
  const t = L[lang];
  const url = new URL(request.url);
  const tag = url.searchParams.get('tag');
  const tpl = await asset(env, request, tplPath('/articles', lang));
  let all = [];
  try { all = await listArticles(); } catch (_) { return htmlResponse(tpl); }

  const card = (a) => {
    const cover = safeUrl(a.cover_image);
    return `<a class="article-list-card" href="${articleUrl(a.slug, lang)}"><div class="thumb"${cover ? ` style="background-image:url('${esc(cover)}')"` : ''}></div>` +
      `<div class="body"><h3>${esc(pick(a, 'title', lang))}</h3><p>${esc(pick(a, 'excerpt', lang) || '')}</p><div class="meta">${esc(fmtDate(a.published_at, lang, 'short'))}</div></div></a>`;
  };
  const listHref = lp('/articles', lang);

  let html = '';
  if (tag) {
    const items = all.filter((a) => Array.isArray(a.tags) && a.tags.includes(tag));
    html = items.length
      ? `<div class="category-block"><div class="count">${t.nArticles(items.length)} · <a href="${listHref}">${t.allArticles}</a></div><div class="article-list-grid">${items.map(card).join('')}</div></div>`
      : `<div class="empty-state">${esc(t.noTag(tag))}<br><br><a href="${listHref}">${t.allArticles}</a></div>`;
  } else {
    for (const cat of CATEGORY_ORDER) {
      // ภาษาอังกฤษ: แสดงบทความที่แปลแล้วก่อน
      const items = all.filter((a) => a.category === cat)
        .sort((a, b) => (lang === 'en' ? isTranslated(b, 'title') - isTranslated(a, 'title') : 0));
      if (!items.length) continue;
      html += `<div class="category-block"><h2>${esc(CATEGORY_LABELS[lang][cat])}</h2><div class="count">${t.nArticles(items.length)}</div><div class="article-list-grid">${items.map(card).join('')}</div></div>`;
    }
  }

  const title = tag ? t.tagTitle(tag) : t.listTitle;
  const description = tag ? t.tagDesc(tag) : t.listDesc;
  const q = tag ? `?tag=${encodeURIComponent(tag)}` : '';

  const rw = new HTMLRewriter()
    .on('title', new SetText(title))
    .on('meta[name="description"]', new Remove())
    .on('a.lang-sw', langSwitch((lang === 'en' ? '/articles' : '/en/articles') + q))
    .on('head', new AppendHead(`<meta name="description" content="${esc(description)}">` + headTags({
      canonical: SITE + listHref + q,
      title, description,
      robots: tag ? 'noindex, follow' : undefined,
      lang,
      alternates: tag ? undefined : { th: SITE + '/articles', en: SITE + '/en/articles' },
    })))
    .on('#content', new SetHtml(html));
  return htmlResponse(rw.transform(tpl));
}

async function articlePage(request, env, slug, lang = 'th') {
  const t = L[lang];
  const tpl = await asset(env, request, tplPath('/article', lang));
  let a = null, related = [];
  try {
    [a, related] = await Promise.all([
      getArticle(slug),
      sb(`hw_programs?select=slug,name,price,price_unit,name_en:en->>name&is_published=eq.true&related_article_slug=eq.${encodeURIComponent(slug)}&order=sort_order.asc`).catch(() => []),
    ]);
  } catch (_) {
    return htmlResponse(tpl); // Supabase ล่ม: ปล่อยให้ client JS ลองโหลดเอง
  }
  const switchHref = lang === 'en' ? articleUrl(slug, 'th') : articleUrl(slug, 'en');
  if (!a) {
    const notFound = new HTMLRewriter()
      .on('title', new SetText(t.articleNotFound))
      .on('head', new AppendHead('<meta name="robots" content="noindex">'))
      .on('a.lang-sw', langSwitch(lang === 'en' ? '/articles' : '/en/articles'))
      .on('#content', new SetHtml(`<div class="article-error">${t.articleNotFoundBody} <a href="${lp('/articles', lang)}">${t.backToList}</a></div>`, { 'data-ssr': '1' }));
    return htmlResponse(notFound.transform(tpl), 404);
  }

  // ภาษาอังกฤษ: ถ้ายังไม่ได้แปล แสดงภาษาไทย + แจ้งเตือน และ noindex (canonical ชี้หน้าไทย)
  const translated = isTranslated(a, 'title') && isTranslated(a, 'content');
  const useEn = lang === 'en' && translated;
  const L2 = useEn ? 'en' : 'th';
  const title = pick(a, 'title', L2);
  const body = renderContent(pick(a, 'content', L2), lang);

  const thUrl = SITE + articleUrl(a.slug, 'th');
  const enUrl = SITE + articleUrl(a.slug, 'en');
  const canonical = lang === 'en' && translated ? enUrl : thUrl;
  const cover = safeUrl(a.cover_image);
  const description = pick(a, 'seo_description', L2) || pick(a, 'excerpt', L2) || title;
  const pageTitle = pick(a, 'seo_title', L2) || `${title} | ${t.brandSuffix}`;
  const tags = Array.isArray(a.tags) ? a.tags : [];
  const category = CATEGORY_LABELS[lang][a.category] || a.category;
  const relName = (r) => (lang === 'en' && has(r.name_en) ? r.name_en : r.name);

  const content =
    `<span class="article-category">${esc(category)}</span>` +
    (tags.length && lang === 'th' ? `<div class="article-tags">${tags.map((x) => `<a class="article-tag" href="/articles?tag=${encodeURIComponent(x)}">#${esc(x)}</a>`).join('')}</div>` : '') +
    `<h1 class="article-title"${lang === 'en' && !useEn ? ' lang="th"' : ''}>${esc(title)}</h1>` +
    `<div class="article-meta">${t.published} <time datetime="${esc(a.published_at)}">${esc(fmtDate(a.published_at, lang))}</time></div>` +
    (lang === 'en' && !useEn ? `<p style="padding:12px 16px;border-radius:12px;background:var(--apricot-50);border:1px solid var(--apricot-100);font-size:14.5px">${t.thaiOnly}</p>` : '') +
    (cover ? `<img class="article-cover" src="${esc(cover)}" alt="${esc(title)}">` : '') +
    `<div class="article-body"${lang === 'en' && !useEn ? ' lang="th"' : ''}>${body}</div>` +
    (related.length ? `<div style="margin-top:36px;padding:22px 24px;border-radius:16px;background:var(--surface);border:1.5px solid var(--mint-200)">` +
      `<div style="font-family:Anuphan,sans-serif;font-weight:700;font-size:18px;color:var(--mint-900);margin-bottom:12px">${t.relatedH}</div>` +
      related.map((r) => `<a href="${programUrl(r.slug, lang)}" style="display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 0;border-top:1px solid var(--line);text-decoration:none;color:var(--ink)">` +
        `<span style="font-weight:600">${esc(relName(r))}</span><span style="white-space:nowrap;font-family:Anuphan,sans-serif;font-weight:700;color:var(--apricot-600)">${r.price == null ? t.ask : (/^เริ่มต้น/.test(r.price_unit || '') ? t.from + ' ' : '') + esc(baht(r.price))} →</span></a>`).join('') +
      `<div style="font-size:12.5px;color:var(--ink-soft);margin-top:8px">${t.relatedNote}</div></div>` : '') +
    `<div class="related-cta"><h3>${t.ctaH}</h3><p>${t.ctaP}</p>` +
    `<a href="https://line.me/R/ti/p/@p49clinic" target="_blank" rel="noopener" class="btn btn-line">${t.ctaBtn}</a></div>`;

  const article = {
    '@context': 'https://schema.org',
    '@type': a.category === 'article' ? 'MedicalWebPage' : 'NewsArticle',
    headline: title,
    description,
    datePublished: a.published_at,
    dateModified: a.updated_at || a.published_at,
    image: cover || undefined,
    keywords: tags.length && L2 === 'th' ? tags.join(', ') : undefined,
    inLanguage: L2,
    mainEntityOfPage: canonical,
    author: { '@id': SITE + '/#clinic' },
    publisher: { '@type': 'MedicalClinic', '@id': SITE + '/#clinic', name: t.siteName, url: SITE + lp('/', lang) },
  };
  const crumbs = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: t.home, item: SITE + lp('/', lang) },
      { '@type': 'ListItem', position: 2, name: t.articles, item: SITE + lp('/articles', lang) },
      { '@type': 'ListItem', position: 3, name: title, item: canonical },
    ],
  };

  const rw = new HTMLRewriter()
    .on('title', new SetText(pageTitle))
    // ลบ meta เดิมที่ client เคยเติมเอง แล้วใส่ชุดใหม่ที่มีค่าจริง
    .on('meta#meta-description', new SetAttr('content', description))
    .on('meta#og-title, meta#og-description, meta#og-image', new Remove())
    .on('script#jsonld', new Remove())
    .on('a.lang-sw', langSwitch(switchHref))
    .on('head', new AppendHead(headTags({
      canonical, title, description, image: cover, type: 'article', jsonld: [article, crumbs], lang,
      robots: lang === 'en' && !translated ? 'noindex, follow' : undefined,
      alternates: translated ? { th: thUrl, en: enUrl } : undefined,
    }) + `<meta property="article:published_time" content="${esc(a.published_at)}">`))
    .on('#content', new SetHtml(content, { 'data-ssr': '1' }));
  return htmlResponse(rw.transform(tpl));
}

async function sitemap() {
  const all = await listArticles();
  let progs = [];
  try { progs = await listPrograms(); } catch (_) { /* ยังไม่มีตาราง/ล่ม: ข้ามไป */ }
  const day = (d) => (d ? new Date(d).toISOString().slice(0, 10) : undefined);
  const maxDay = (...ds) => ds.filter(Boolean).sort().pop();
  const newestArticle = all.reduce((m, a) => maxDay(m, day(a.updated_at || a.published_at)), undefined);
  const newestProgram = progs.reduce((m, p) => maxDay(m, day(p.updated_at)), undefined);
  const LEGAL_UPDATED = '2026-08-25'; // วันที่แก้หน้า privacy / cookies ล่าสุด
  const EN_LAUNCH = '2026-10-22';
  const img = (u, title) => (safeUrl(u) ? [{ loc: safeUrl(u), title }] : []);
  // แต่ละหน้า: ไทย + อังกฤษ (ถ้ามีคำแปล) พร้อมลิงก์ hreflang ถึงกัน
  const pair = (thPath, enPath, base, hasEn) => {
    const alt = hasEn ? [{ lang: 'th', href: SITE + thPath }, { lang: 'en', href: SITE + enPath }, { lang: 'x-default', href: SITE + thPath }] : null;
    const out = [{ ...base, loc: SITE + thPath, alt }];
    if (hasEn) out.push({ ...base, loc: SITE + enPath, alt, priority: (Number(base.priority) - 0.1).toFixed(1), lastmod: maxDay(base.lastmod, EN_LAUNCH) });
    return out;
  };
  const urls = [
    ...pair('/', '/en/', { lastmod: maxDay(newestArticle, newestProgram), priority: '1.0', images: [{ loc: DEFAULT_OG, title: SITE_NAME }] }, true),
    ...pair('/programs', '/en/programs', { lastmod: newestProgram, priority: '0.9' }, true),
    ...progs.flatMap((p) => pair(programUrl(p.slug), programUrl(p.slug, 'en'), { lastmod: day(p.updated_at), priority: '0.8', images: img(p.cover_image, p.name) }, isTranslated(p, 'name'))),
    ...pair('/articles', '/en/articles', { lastmod: newestArticle, priority: '0.8' }, true),
    ...all.flatMap((a) => pair(articleUrl(a.slug), articleUrl(a.slug, 'en'), { lastmod: day(a.updated_at || a.published_at), priority: '0.7', images: img(a.cover_image, a.title) }, isTranslated(a, 'title'))),
    ...pair('/privacy', '/en/privacy', { lastmod: LEGAL_UPDATED, priority: '0.2' }, true),
    ...pair('/cookies', '/en/cookies', { lastmod: LEGAL_UPDATED, priority: '0.2' }, true),
  ];
  const xml = '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' +
    urls.map((u) => `  <url><loc>${esc(u.loc)}</loc>${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}<priority>${u.priority}</priority>` +
      (u.alt || []).map((x) => `<xhtml:link rel="alternate" hreflang="${x.lang}" href="${esc(x.href)}"/>`).join('') +
      (u.images || []).map((im) => `<image:image><image:loc>${esc(im.loc)}</image:loc><image:title>${esc(im.title)}</image:title></image:image>`).join('') +
      `</url>`).join('\n') +
    '\n</urlset>\n';
  return new Response(xml, { headers: { 'content-type': 'application/xml; charset=utf-8', 'cache-control': PAGE_CACHE } });
}

// ---------- programs (โปรแกรมและราคา) ----------
const PROGRAM_FIELDS = 'id,slug,category,name,short_desc,price,price_unit,price_note,options,cover_image,is_featured,sort_order,updated_at,' +
  'name_en:en->>name,short_desc_en:en->>short_desc,price_unit_en:en->>price_unit';
const listCategories = () => sb('hw_program_categories?select=slug,name,description,sort_order,en&is_active=eq.true&order=sort_order.asc');
const listPrograms = () => sb(`hw_programs?select=${PROGRAM_FIELDS}&is_published=eq.true&order=sort_order.asc,name.asc`);
const getProgram = async (slug) =>
  (await sb(`hw_programs?select=*&is_published=eq.true&slug=eq.${encodeURIComponent(slug)}&limit=1`))[0] || null;
// ลิงก์เปิดแชท LINE OA พร้อมข้อความจองที่กรอกไว้ให้ (ต้องตรงกับ lineText ใน program.html)
const LINE_OA = '@p49clinic';
const LINE_ICON = '<svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 3C6.5 3 2 6.6 2 11c0 2.9 2 5.4 5 6.8-.2.8-.7 2.6-.8 3-.1.4.1.4.3.3.2-.1 2.6-1.7 3.6-2.4.6.1 1.3.1 1.9.1 5.5 0 10-3.6 10-8S17.5 3 12 3z"/></svg>';
function lineBookText(name, price, opt, lang = 'th') {
  const t = L[lang];
  const pr = opt && opt.price != null && opt.price !== '' ? opt.price : price;
  return [t.lineHello,
    t.lineProgram + name + (opt && opt.label ? ' (' + opt.label + ')' : ''),
    t.linePrice + (pr == null ? t.ask : baht(pr)),
    t.lineName, t.linePhone, t.lineDate].join('\n');
}
function lineBookUrl(name, price, opt, lang) {
  return 'https://line.me/R/oaMessage/' + encodeURIComponent(LINE_OA) + '/?' + encodeURIComponent(lineBookText(name, price, opt, lang));
}
// slug เดิมที่เปลี่ยนชื่อแล้ว → slug ใหม่ (301)
const PROGRAM_REDIRECTS = { 'hepatitis-a-b-vaccine': 'hepatitis-b-vaccine', 'annual-health-checkup': 'health-checkup-basic' };
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
function priceHtml(p, lang = 'th') {
  const t = L[lang];
  if (p.price == null) return `<span class="price-ask">${t.ask}</span>`;
  // "เริ่มต้นต่อรายการ" → เริ่มต้น ฿100 ต่อรายการ (ภาษาอังกฤษใช้ price_unit จากคอลัมน์ en)
  const u = String(p.price_unit || '');
  const from = /^เริ่มต้น/.test(u);
  const rest = lang === 'en' ? String(pick(p, 'price_unit', 'en') || '').replace(/^from\s*/i, '').replace(/^เริ่มต้น\s*/, '') : (from ? u.replace(/^เริ่มต้น\s*/, '') : u);
  const restSafe = lang === 'en' && /[฀-๿]/.test(rest) ? '' : rest; // ยังไม่แปล: ไม่โชว์หน่วยภาษาไทยในหน้าอังกฤษ
  return (from ? `<span class="unit">${t.from}</span> ` : '') +
    `<span class="price">${esc(baht(p.price))}</span>` + (restSafe ? ` <span class="unit">${esc(restSafe)}</span>` : '');
}
const catName = (c, lang) => (c ? pick(c, 'name', lang) : '');

async function programsPage(request, env, lang = 'th') {
  const t = L[lang];
  const tpl = await asset(env, request, tplPath('/programs', lang));
  let cats = [], progs = [];
  try { [cats, progs] = await Promise.all([listCategories(), listPrograms()]); } catch (_) { return htmlResponse(tpl); }

  const used = cats.filter((c) => progs.some((p) => p.category === c.slug));
  const chips = `<button type="button" class="active" data-cat="all" aria-pressed="true">${t.all}<span class="n">${progs.length}</span></button>` +
    used.map((c) => `<button type="button" data-cat="${esc(c.slug)}" aria-pressed="false">${esc(catName(c, lang))}<span class="n">${progs.filter((p) => p.category === c.slug).length}</span></button>`).join('');

  const card = (p, cat) => {
    const cover = safeUrl(p.cover_image);
    return `<a class="pg-card" href="${programUrl(p.slug, lang)}">` +
      `<div class="thumb"${cover ? ` style="background-image:url('${esc(cover)}')"` : ''}>${cover ? '' : iconSvg(p.category)}</div>` +
      `<div class="body"><div class="kicker">${esc(catName(cat, lang))}${p.is_featured ? `<span class="pg-badge">${t.recommended}</span>` : ''}</div>` +
      `<h3>${esc(pick(p, 'name', lang))}</h3>${pick(p, 'short_desc', lang) ? `<p>${esc(pick(p, 'short_desc', lang))}</p>` : ''}` +
      `<div class="foot"><div>${priceHtml(p, lang)}</div><span class="more">${t.details}</span></div></div></a>`;
  };
  const sections = used.map((c) => {
    const items = progs.filter((p) => p.category === c.slug);
    const desc = pick(c, 'description', lang);
    return `<section class="pg-section" data-cat="${esc(c.slug)}" id="cat-${esc(c.slug)}"><h2>${esc(catName(c, lang))}</h2>` +
      (desc ? `<p class="sub">${esc(desc)}</p>` : '') +
      `<div class="pg-grid">${items.map((p) => card(p, c)).join('')}</div></section>`;
  }).join('') || `<div class="pg-empty">${t.noPrograms}</div>`;

  const itemList = {
    '@context': 'https://schema.org', '@type': 'ItemList', name: t.programs,
    itemListElement: progs.map((p, i) => ({ '@type': 'ListItem', position: i + 1, url: SITE + programUrl(p.slug, lang), name: pick(p, 'name', lang) })),
  };
  const rw = new HTMLRewriter()
    .on('title', new SetText(t.programsTitle))
    .on('meta#meta-description', new SetAttr('content', t.programsDesc))
    .on('a.lang-sw', langSwitch(lang === 'en' ? '/programs' : '/en/programs'))
    .on('head', new AppendHead(headTags({
      canonical: SITE + lp('/programs', lang), title: t.programsTitle, description: t.programsDesc, jsonld: [itemList], lang,
      alternates: { th: SITE + '/programs', en: SITE + '/en/programs' },
    })))
    .on('#cat-chips', new SetHtml(chips))
    .on('#pg-content', new SetHtml(sections));
  return htmlResponse(rw.transform(tpl));
}

async function programPage(request, env, slug, lang = 'th') {
  const t = L[lang];
  const tpl = await asset(env, request, tplPath('/program', lang));
  const switchHref = lang === 'en' ? programUrl(slug, 'th') : programUrl(slug, 'en');
  let p = null, cats = [], all = [];
  try { [p, cats, all] = await Promise.all([getProgram(slug), listCategories(), listPrograms().catch(() => [])]); } catch (_) {
    return htmlResponse(new HTMLRewriter().on('#pd-root', new SetHtml(`<div class="pg-empty">${t.loadFail}</div>`)).transform(tpl), 503);
  }
  if (!p) {
    return htmlResponse(new HTMLRewriter()
      .on('title', new SetText(t.programNotFound))
      .on('head', new AppendHead('<meta name="robots" content="noindex">'))
      .on('a.lang-sw', langSwitch(lang === 'en' ? '/programs' : '/en/programs'))
      .on('#pd-root', new SetHtml(`<div class="pg-empty">${t.programNotFoundBody} <a href="${lp('/programs', lang)}" style="color:var(--mint-700);font-weight:700">${t.seeAllPrograms}</a></div>`))
      .transform(tpl), 404);
  }
  const en = lang === 'en';
  const E = enOf(p);
  const translated = has(E.name);
  const cat = cats.find((c) => c.slug === p.category);
  const cName = catName(cat, lang);
  const cover = safeUrl(p.cover_image);
  const name = pick(p, 'name', lang);
  // ตัวเลือก: ราคามาจากภาษาไทย ชื่อ/หมายเหตุจาก en.options ตามลำดับเดียวกัน
  const optsTh = Array.isArray(p.options) ? p.options.filter((o) => o && o.label) : [];
  const optsEn = Array.isArray(E.options) ? E.options : [];
  const options = optsTh.map((o, i) => (en && optsEn[i] && optsEn[i].label ? { ...o, label: optsEn[i].label, note: optsEn[i].note || '' } : o));
  const body = renderContent(pick(p, 'description', lang), lang);
  const arr = (f) => { const v = pick(p, f, lang); return Array.isArray(v) ? v : []; };

  const meta = [pick(p, 'duration', lang) && `${t.duration}${pick(p, 'duration', lang)}`, p.brand && `${t.product}${p.brand}`, p.fda_reg_no && `${t.fda}${p.fda_reg_no}`]
    .filter(Boolean).map((m) => `<span>${esc(m)}</span>`).join('');
  const isPackage = /แพ็กเกจ|แพ็คเกจ/.test(p.name);
  // รายการ "ชื่อหลัก — รายละเอียด" แสดงชื่อหลักตัวใหญ่ รายละเอียดตัวเล็ก (อ่านง่ายสำหรับผู้สูงอายุ)
  const bigList = (list) => list.filter(Boolean).map((x) => {
    const [main, ...rest] = String(x).split(' — ');
    return `<li><span class="ck" aria-hidden="true"></span><span><b>${esc(main)}</b>${rest.length ? `<small>${esc(rest.join(' — '))}</small>` : ''}</span></li>`;
  }).join('');
  const optsHtml = options.length
    ? `<div class="pd-opts" role="radiogroup" aria-label="${t.chooseOpt}">${options.map((o, i) =>
      `<label class="pd-opt"><input type="radio" name="pd-opt" value="${i}"${i === 0 ? ' checked' : ''}>` +
      `<span class="t"><b>${esc(o.label)}</b>${o.note ? `<small>${esc(o.note)}</small>` : ''}</span>` +
      `<span class="p">${o.price != null && o.price !== '' ? esc(baht(o.price)) : t.askShort}</span></label>`).join('')}</div>`
    : '';
  const firstPrice = options.length && options[0].price != null && options[0].price !== '' ? options[0].price : p.price;
  const bigPrice = firstPrice == null
    ? `<span class="price-ask" data-sel-price>${t.ask}</span>`
    : (options.length ? `<span class="price" data-sel-price>${esc(baht(firstPrice))}</span>` : priceHtml(p, lang).replace('<span class="price">', '<span class="price" data-sel-price>'));
  // ข้อความ LINE ภาษาอังกฤษ: ใส่ชื่อภาษาไทยในวงเล็บให้เจ้าหน้าที่อ่านง่าย
  const lineName = en && translated ? `${name} (${p.name})` : p.name;
  const lineHref = lineBookUrl(lineName, p.price, options[0] || null, lang);

  // ตัวเลือกเทียบแพ็กเกจตรวจสุขภาพ (ชุดเล็ก / ชุดใหญ่หญิง / ชุดใหญ่ชาย)
  const siblings = /^health-checkup-/.test(p.slug) ? all.filter((x) => /^health-checkup-/.test(x.slug)) : [];
  const shortName = (x) => (en && has(x.name_en)
    ? x.name_en.replace(/^health check-?up package\s*/i, '')
    : x.name.replace(/^แพ็กเกจตรวจสุขภาพ\s*/, '')).replace(/[()]/g, '').trim();
  const countOf = (txt) => ((txt || '').match(/(\d+)\s*รายการ/) || [])[1];
  const switcher = siblings.length > 1
    ? `<div class="pd-pkgs" role="list" aria-label="${t.choosePkg}">${siblings.map((x) =>
      `<a role="listitem" href="${programUrl(x.slug, lang)}" class="pd-pkg${x.slug === p.slug ? ' on' : ''}"${x.slug === p.slug ? ' aria-current="page"' : ''}>` +
      `<span class="n">${esc(shortName(x))}</span>` +
      `<span class="pr">${esc(baht(x.price))}</span>` +
      (countOf(x.short_desc) ? `<span class="c">${countOf(x.short_desc)} ${t.items}</span>` : '') + `</a>`).join('')}</div>`
    : '';

  const others = all.filter((x) => x.category === p.category && x.slug !== p.slug && !siblings.some((s2) => s2.slug === x.slug)).slice(0, 4);
  const shortDesc = pick(p, 'short_desc', lang);
  const priceNote = pick(p, 'price_note', lang);
  const includes = arr('includes'), suitable = arr('suitable_for'), precautions = arr('precautions');
  const thaiNotice = en && !translated ? `<p style="padding:12px 16px;border-radius:12px;background:var(--apricot-50);border:1px solid var(--apricot-100);font-size:14.5px">${t.thaiOnly}</p>` : '';

  const html =
    `<div class="crumbs" style="padding-top:22px"><a href="${lp('/', lang)}">${t.home}</a> / <a href="${lp('/programs', lang)}">${t.programs}</a>${cat ? ` / <a href="${lp('/programs', lang)}?cat=${esc(cat.slug)}">${esc(cName)}</a>` : ''}</div>` +
    `<div class="pd-layout">` +
    `<div class="pd-head">` +
    (cat ? `<span class="pd-cat">${esc(cName)}</span>` : '') +
    `<h1 class="pd-title">${esc(name)}</h1>` +
    (shortDesc ? `<p class="pd-lede">${esc(shortDesc)}</p>` : '') + thaiNotice +
    (meta ? `<div class="pd-meta">${meta}</div>` : '') +
    switcher +
    `</div>` +
    `<aside class="pd-aside" aria-label="${t.priceLabel}"><span class="label">${options.length ? t.priceSel : t.priceLabel}</span><div>${bigPrice}</div>` +
    (p.price != null || options.length ? `<p class="pd-fee">${t.fee}</p>` : '') +
    (priceNote ? `<p class="pg-note">${esc(priceNote)}</p>` : '') + optsHtml +
    `<a href="${esc(lineHref)}" target="_blank" rel="noopener" class="btn btn-line btn-xl js-line-book">${LINE_ICON}${t.bookLine}</a>` +
    `<a href="tel:0220004586" class="btn btn-ghost btn-xl">${t.call}</a></aside>` +
    `<article class="pd-main">` +
    (cover ? `<img class="pd-cover" src="${esc(cover)}" alt="${esc(name)}">` : '') +
    (body ? `<div class="pd-body">${body}</div>` : '') +
    (includes.length ? `<section class="pd-sec"><h2>${isPackage ? t.inclPkg : t.incl}</h2><ul class="pd-list">${bigList(includes)}</ul></section>` : '') +
    (suitable.length ? `<section class="pd-sec"><h2>${t.suitable}</h2><ul class="pd-list soft">${bigList(suitable)}</ul></section>` : '') +
    (precautions.length ? `<section class="pd-sec warn"><h2>${isPackage ? t.beforePkg : t.notes}</h2><ul class="pd-list">${bigList(precautions)}</ul></section>` : '') +
    (p.related_article_slug ? `<div class="pd-related">${t.readMoreLbl}<a href="${articleUrl(p.related_article_slug, lang)}">${esc(t.readMoreAbout(name))}</a></div>` : '') +
    (others.length ? `<section class="pd-sec"><h2>${esc(t.others(cName || t.othersFallback))}</h2><div class="pd-others">` +
      others.map((x) => `<a href="${programUrl(x.slug, lang)}"><span>${esc(pick(x, 'name', lang))}</span><b>${x.price == null ? t.ask : esc(baht(x.price))}</b></a>`).join('') + `</div></section>` : '') +
    `</article>` +
    `<div class="pd-book-wrap"><section class="pd-book" id="booking" aria-labelledby="bk-h"><h2 id="bk-h">${t.bookH}</h2>` +
    `<div class="pd-book-btns"><a href="${esc(lineHref)}" target="_blank" rel="noopener" class="btn btn-line btn-xl js-line-book">${LINE_ICON}${t.bookLine2}</a>` +
    `<a href="tel:0220004586" class="btn btn-primary btn-xl">${t.call}</a></div>` +
    `<p class="pd-hours">${t.hours}</p></section>` +
    `<p class="pg-note" style="margin-top:20px">${t.disclaimer}</p></div>` +
    `</div>` +
    `<div class="pd-bar"><div>${firstPrice == null ? `<span class="price-ask">${t.ask}</span>` : `<span class="price" data-sel-price>${esc(baht(firstPrice))}</span><small class="pd-bar-fee">${t.barFee}</small>`}</div><a href="${esc(lineHref)}" target="_blank" rel="noopener" class="btn btn-line js-line-book">${LINE_ICON}${t.bookLine}</a></div>` +
    `<script type="application/json" id="program-data">${jsonLd({ name: lineName, price: p.price, price_unit: p.price_unit, options })}</script>`;

  const thUrl = SITE + programUrl(p.slug, 'th');
  const enUrl = SITE + programUrl(p.slug, 'en');
  const canonical = en && translated ? enUrl : thUrl;
  const title = pick(p, 'seo_title', lang) || t.programTitle(name, p.price != null ? baht(p.price) : '');
  const description = pick(p, 'seo_description', lang) || shortDesc || name;
  const prices = [p.price, ...options.map((o) => o.price)].filter((x) => x != null && x !== '').map(Number);
  const service = {
    '@context': 'https://schema.org', '@type': 'MedicalProcedure', name, description,
    url: canonical, image: cover || undefined, inLanguage: en && translated ? 'en' : 'th',
    provider: { '@type': 'MedicalClinic', '@id': SITE + '/#clinic', name: t.siteName },
    offers: prices.length ? {
      '@type': prices.length > 1 ? 'AggregateOffer' : 'Offer', priceCurrency: 'THB',
      ...(prices.length > 1 ? { lowPrice: Math.min(...prices), highPrice: Math.max(...prices), offerCount: prices.length } : { price: prices[0] }),
      availability: 'https://schema.org/InStock', url: canonical,
    } : undefined,
  };
  const crumbs = {
    '@context': 'https://schema.org', '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: t.home, item: SITE + lp('/', lang) },
      { '@type': 'ListItem', position: 2, name: t.programs, item: SITE + lp('/programs', lang) },
      { '@type': 'ListItem', position: 3, name, item: canonical },
    ],
  };
  const rw = new HTMLRewriter()
    .on('title', new SetText(title))
    .on('meta#meta-description', new SetAttr('content', description))
    .on('a.lang-sw', langSwitch(switchHref))
    .on('head', new AppendHead(headTags({
      canonical, title: name, description, image: cover, type: 'website', jsonld: [service, crumbs], lang,
      robots: en && !translated ? 'noindex, follow' : undefined,
      alternates: translated ? { th: thUrl, en: enUrl } : undefined,
    })))
    .on('#pd-root', new SetHtml(html));
  return htmlResponse(rw.transform(tpl));
}

// ---------- router ----------
async function route(request, env, path, url, lang) {
  if (path === '/') return homePage(request, env, lang);
  if (path === '/articles') return listPage(request, env, lang);
  if (path === '/programs') return programsPage(request, env, lang);
  const pm = path.match(/^\/programs\/([^/]+)\/?$/);
  if (pm) {
    const slug = decodeURIComponent(pm[1]);
    if (PROGRAM_REDIRECTS[slug]) return redirect(SITE + programUrl(PROGRAM_REDIRECTS[slug], lang));
    if (path.endsWith('/')) return redirect(SITE + programUrl(slug, lang));
    return programPage(request, env, slug, lang);
  }
  const m = path.match(/^\/articles\/([^/]+)\/?$/);
  if (m) {
    const slug = decodeURIComponent(m[1]);
    if (path.endsWith('/')) return redirect(SITE + articleUrl(slug, lang));
    return articlePage(request, env, slug, lang);
  }
  return null;
}

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
    // ภาษาอังกฤษ
    if (path === '/en') return redirect(SITE + '/en/');
    if (path === '/en/index.html') return redirect(SITE + '/en/');
    if (path === '/en/articles.html' || path === '/en/articles/') return redirect(SITE + '/en/articles' + url.search);
    if (path === '/en/programs.html' || path === '/en/programs/') return redirect(SITE + '/en/programs' + url.search);
    if (path === '/en/privacy.html') return redirect(SITE + '/en/privacy');
    if (path === '/en/cookies.html') return redirect(SITE + '/en/cookies');
    if (path === '/en/article' || path === '/en/article.html') return redirect(SITE + '/en/articles');
    if (path === '/en/program' || path === '/en/program.html') return redirect(SITE + '/en/programs');

    try {
      if (path === '/sitemap.xml') return await sitemap();
      const isEn = path === '/en/' || path.startsWith('/en/');
      const res = await route(request, env, isEn ? path.slice(3) || '/' : path, url, isEn ? 'en' : 'th');
      if (res) return res;
    } catch (err) {
      console.error('ssr error', path, err && err.message);
      if (path === '/sitemap.xml') return new Response('sitemap unavailable', { status: 503 });
    }
    return env.ASSETS.fetch(request);
  },
};

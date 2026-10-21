"""ประกอบ programs.html และ program.html จาก article.html (ใช้ header/footer/โลโก้/CSS ชุดเดียวกับเว็บ)

รัน: python3 src/build/programs-parts.py
ถ้าแก้ header/footer ใน article.html แล้วอยากให้หน้าโปรแกรมตาม ให้รันสคริปต์นี้ใหม่
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[2]
src = (ROOT / 'article.html').read_text(encoding='utf-8')

head_end = src.index('  /* SINGLE ARTICLE PAGE */')
style_close = src.index('</style>')
body_start = src.index('<div class="article-wrap">')
footer_start = src.index('<footer>')
footer_end = src.index('</footer>') + len('</footer>')
toggle_js = src[src.index('/* FONT SIZE + THEME TOGGLE */'):src.index('</script>', src.index('/* FONT SIZE + THEME TOGGLE */'))]

head = src[:head_end]
between = src[style_close:body_start]  # </style></head><body> + fs-toggle + header
footer = src[footer_start:footer_end]

# หัวข้อหน้า: title/description ถูกแทนที่โดย Worker อีกชั้น ค่านี้เป็นค่าเริ่มต้น
head = re.sub(r'<title id="page-title">.*?</title>', '<title id="page-title">โปรแกรมและราคา | HappiWell คลินิกเวชกรรม</title>', head)
head = re.sub(r'<meta id="meta-description"[^>]*>', '<meta id="meta-description" name="description" content="ราคาวัคซีน ตรวจสุขภาพ ยาฉีดคุมกำเนิด และบริการอื่น ๆ ที่แฮปปี้เวลล์ คลินิกเวชกรรม เขตทุ่งครุ">', head)
head = re.sub(r'\s*<meta id="og-(title|description|image)"[^>]*>', '', head)

COMMON_CSS = r'''
  /* PROGRAMS (ใช้ตัวแปรสีเดียวกับทั้งเว็บ) */
  .pg-hero{padding:44px 0 8px;}
  .pg-hero h1{font-size:34px;margin:10px 0 10px;}
  .pg-hero p{color:var(--ink-soft);font-size:16px;max-width:640px;}
  .crumbs{font-size:13.5px;color:var(--ink-soft);margin-bottom:6px;}
  .crumbs a{color:var(--mint-700);font-weight:600;}
  .price{font-family:'Anuphan',sans-serif;font-weight:700;color:var(--apricot-600);}
  .price-ask{font-family:'Anuphan',sans-serif;font-weight:700;color:var(--mint-700);}
  .unit{font-size:13px;color:var(--ink-soft);font-weight:500;}
  .pg-note{font-size:12.5px;color:var(--ink-soft);line-height:1.7;}
  .pg-fee{display:inline-block;margin-top:12px;font-size:13.5px !important;font-weight:600;color:#8C1D26 !important;background:var(--apricot-50);border:1px solid var(--apricot-100);padding:6px 14px;border-radius:999px;}
  .pd-fee{font-size:13px;font-weight:600;color:#8C1D26;margin-top:-6px;}
  .pd-bar-fee{display:block;font-size:11px;color:var(--ink-soft);line-height:1.2;}
  .btn-line{background:var(--line-green);color:#fff;}
  .btn-primary{background:var(--mint-600);color:#fff;}
  .nav-cta{white-space:nowrap;}
  .btn{justify-content:center;min-height:46px;cursor:pointer;font-family:inherit;}
  .nav-prog{display:none;font-size:14px;font-weight:600;color:var(--mint-700);background:var(--mint-100);padding:8px 14px;border-radius:999px;margin-left:auto;margin-right:8px;white-space:nowrap;}
  @media (max-width:840px){ .nav-prog{display:inline-flex;} }
'''

LIST_CSS = COMMON_CSS + r'''
  .cat-chips{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0 8px;}
  .cat-chips button{
    min-height:42px;padding:0 18px;border-radius:999px;border:1px solid var(--line);
    background:var(--surface);color:var(--ink);font-family:inherit;font-size:14.5px;font-weight:600;cursor:pointer;
  }
  .cat-chips button.active{background:var(--mint-600);border-color:var(--mint-600);color:#fff;}
  .cat-chips button .n{opacity:.7;font-weight:500;margin-left:4px;}
  .pg-section{padding:26px 0 6px;}
  .pg-section h2{font-size:22px;margin-bottom:4px;}
  .pg-section .sub{color:var(--ink-soft);font-size:14px;margin-bottom:16px;}
  .pg-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px;}
  .pg-card{
    background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-md);overflow:hidden;
    display:flex;flex-direction:column;transition:box-shadow .15s,transform .15s;
  }
  .pg-card:hover{box-shadow:0 8px 24px rgba(27,58,140,.10);transform:translateY(-2px);}
  .pg-card .thumb{height:140px;background:var(--mint-50);display:flex;align-items:center;justify-content:center;background-size:cover;background-position:center;}
  .pg-card .thumb svg{width:40px;height:40px;stroke:var(--mint-600);fill:none;}
  .pg-card .body{padding:16px 18px 18px;display:flex;flex-direction:column;gap:6px;flex:1;}
  .pg-card .kicker{font-size:12px;font-weight:700;color:var(--teal-700);}
  .pg-card h3{font-size:16.5px;line-height:1.4;}
  .pg-card p{font-size:13.5px;color:var(--ink-soft);}
  .pg-card .foot{margin-top:auto;padding-top:12px;border-top:1px solid var(--line);display:flex;align-items:flex-end;justify-content:space-between;gap:8px;}
  .pg-card .foot .price{font-size:21px;line-height:1.2;}
  .pg-card .foot .price-ask{font-size:17px;}
  .pg-card .more{font-size:13.5px;font-weight:600;color:var(--mint-700);white-space:nowrap;}
  .pg-badge{display:inline-block;font-size:11px;font-weight:700;background:var(--apricot-100);color:#8C1D26;padding:2px 9px;border-radius:999px;margin-left:6px;vertical-align:middle;}
  .pg-help{
    margin:40px 0 0;padding:26px;border-radius:var(--radius-lg);background:var(--mint-900);
    display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;
  }
  .pg-help h3{color:#fff;font-size:19px;}
  .pg-help p{color:var(--mint-100);font-size:14px;}
  .pg-empty{padding:60px 0;text-align:center;color:var(--ink-soft);}
  @media (max-width:560px){ .pg-hero h1{font-size:27px;} .pg-grid{grid-template-columns:1fr;} }
'''

DETAIL_CSS = COMMON_CSS + r'''
  .pd-layout{display:grid;grid-template-columns:minmax(0,1fr) 360px;grid-template-areas:"main side" "book side";column-gap:32px;row-gap:8px;align-items:start;padding:20px 0 64px;}
  .pd-main{grid-area:main;min-width:0;}
  .pd-aside{grid-area:side;}
  .pd-book-wrap{grid-area:book;min-width:0;}
  .pd-cover{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:var(--radius-lg);background:var(--mint-50);display:block;margin-bottom:24px;}
  .pd-cover.ph{display:flex;align-items:center;justify-content:center;}
  .pd-cover.ph svg{width:56px;height:56px;stroke:var(--mint-600);fill:none;}
  .pd-cat{display:inline-block;font-size:12.5px;font-weight:700;color:var(--teal-700);background:var(--teal-100);padding:4px 12px;border-radius:999px;margin-bottom:12px;}
  .pd-title{font-size:30px;line-height:1.3;margin-bottom:10px;}
  .pd-lede{font-size:16.5px;color:var(--ink-soft);margin-bottom:16px;}
  .pd-meta{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:26px;}
  .pd-meta span{font-size:13px;font-weight:600;color:var(--mint-700);background:var(--mint-50);border:1px solid var(--mint-100);padding:5px 12px;border-radius:999px;}
  .pd-body{font-size:16px;line-height:1.9;}
  .pd-body p{margin-bottom:16px;}
  .pd-body h2{font-size:21px;margin:28px 0 12px;}
  .pd-body ul,.pd-body ol{margin:0 0 16px 22px;}
  .pd-body img{width:100%;border-radius:var(--radius-md);}
  .pd-body a{color:var(--mint-700);text-decoration:underline;text-underline-offset:3px;}
  .pd-boxes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:26px 0;}
  .pd-box{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-md);padding:20px;}
  .pd-box h2{font-size:17px;margin-bottom:10px;}
  .pd-box ul{list-style:none;display:flex;flex-direction:column;gap:8px;font-size:14.5px;}
  .pd-box li{display:flex;gap:10px;}
  .pd-box li::before{content:"";flex-shrink:0;width:18px;height:18px;margin-top:4px;border-radius:50%;background:var(--teal-100) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%231F8F82' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 12.5l4 4L18 8'/%3E%3C/svg%3E") center/12px no-repeat;}
  .pd-box.warn{background:var(--apricot-50);border-color:#F6C4C8;}
  .pd-box.warn li::before{background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23E63946' stroke-width='3' stroke-linecap='round'%3E%3Cpath d='M12 7v6M12 17h.01'/%3E%3C/svg%3E") center/12px no-repeat;}
  .pd-related{display:flex;align-items:center;gap:12px;padding:16px 18px;border-radius:var(--radius-md);background:var(--mint-50);border:1px solid var(--mint-100);font-size:14.5px;margin-bottom:20px;}
  .pd-related a{color:var(--mint-700);font-weight:700;}

  .pd-aside{position:sticky;top:84px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-lg);padding:22px;display:flex;flex-direction:column;gap:12px;}
  .pd-aside .label{font-size:13px;color:var(--ink-soft);}
  .pd-aside .price{font-size:34px;line-height:1.15;}
  .pd-aside .price-ask{font-size:24px;}
  .pd-opts{display:flex;flex-direction:column;gap:8px;margin-top:4px;}
  .pd-opt{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1.5px solid var(--line);border-radius:12px;cursor:pointer;background:var(--surface);}
  .pd-opt:has(input:checked){border-color:var(--mint-600);background:var(--mint-50);}
  .pd-opt input{accent-color:var(--mint-600);width:18px;height:18px;flex-shrink:0;}
  .pd-opt .t{flex:1;min-width:0;}
  .pd-opt .t b{display:block;font-size:14.5px;}
  .pd-opt .t small{font-size:12.5px;color:var(--ink-soft);}
  .pd-opt .p{font-family:'Anuphan',sans-serif;font-weight:700;color:var(--apricot-600);white-space:nowrap;}

  .pd-book{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-lg);padding:26px;margin-top:8px;scroll-margin-top:90px;}
  .pd-book h2{font-size:22px;margin-bottom:12px;}
  .pd-steps{margin:0 0 18px 20px;display:flex;flex-direction:column;gap:8px;font-size:14.5px;color:var(--ink-soft);}
  .pd-steps b{color:var(--ink);}
  .btn-line svg,.btn svg{width:18px;height:18px;}
  .btn-ghost{background:var(--surface);color:var(--mint-900);border:1px solid var(--line);}
  .pd-book .sub{font-size:14px;color:var(--ink-soft);margin-bottom:18px;}
  .f-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;}
  .f{display:flex;flex-direction:column;gap:6px;}
  .f.full{grid-column:1/-1;}
  .f label{font-size:13.5px;font-weight:600;}
  .f label small{font-weight:400;color:var(--ink-soft);}
  .f input,.f select,.f textarea{
    min-height:46px;padding:10px 14px;border:1.5px solid var(--line);border-radius:10px;
    font-family:inherit;font-size:15px;color:var(--ink);background:var(--surface);
  }
  .f textarea{min-height:84px;resize:vertical;}
  .f input:focus,.f select:focus,.f textarea:focus{outline:none;border-color:var(--mint-600);}
  .consent{display:flex;gap:10px;align-items:flex-start;font-size:13.5px;color:var(--ink-soft);margin:16px 0;}
  .consent input{width:20px;height:20px;margin-top:2px;accent-color:var(--mint-600);flex-shrink:0;}
  .consent a{color:var(--mint-700);font-weight:600;}
  .form-msg{font-size:14px;margin-top:10px;}
  .form-msg.err{color:var(--red);}
  .book-done{text-align:center;padding:24px 8px;}
  .book-done h3{font-size:21px;margin:10px 0 6px;}
  .book-done p{color:var(--ink-soft);font-size:14.5px;}

  .pd-bar{display:none;}
  @media (max-width:900px){
    .pd-layout{grid-template-columns:1fr;grid-template-areas:"main" "side" "book";row-gap:20px;}
    .pd-aside{position:static;}
    .pd-bar{
      display:flex;position:fixed;left:0;right:0;bottom:0;z-index:55;align-items:center;gap:12px;
      background:var(--surface);border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));
    }
    .pd-bar .price{font-size:21px;}
    .pd-bar .btn{flex:1;}
    body.has-bar{padding-bottom:76px;}
    body.has-bar .fs-toggle{bottom:88px;}
  }
  @media (max-width:560px){ .pd-title{font-size:24px;} .pd-boxes,.f-grid{grid-template-columns:1fr;} }
'''

LIST_BODY = r'''
<div class="wrap">
  <section class="pg-hero" style="padding-bottom:0">
    <div class="eyebrow">โปรแกรมและราคา</div>
    <h1>ราคาวัคซีน ตรวจสุขภาพ และบริการที่คลินิก</h1>
    <p>ดูราคาและสิ่งที่รวมในแต่ละโปรแกรมก่อนมาคลินิก กดจองผ่าน LINE ได้ทันที ทีมงานจะตอบกลับเพื่อยืนยันวันเวลา</p>
    <p class="pg-fee">ราคาทุกรายการยังไม่รวมค่าบริการทางการแพทย์ 30 บาท</p>
  </section>
  <div class="cat-chips" id="cat-chips" role="group" aria-label="กรองตามหมวดหมู่"></div>
  <div id="pg-content">
    <div class="pg-empty">กำลังโหลดโปรแกรม...</div>
  </div>
  <div class="pg-help">
    <div>
      <h3>ไม่แน่ใจว่าโปรแกรมไหนเหมาะกับคุณ?</h3>
      <p>ทักถามทีมงานทาง LINE ก่อนนัดหมายได้ทุกวัน</p>
    </div>
    <a href="https://line.me/R/ti/p/@p49clinic" target="_blank" rel="noopener" class="btn btn-line">แชทผ่าน LINE</a>
  </div>
  <p class="pg-note" style="margin:22px 0 64px;">ราคาที่แสดงเป็นราคาสำหรับผู้ชำระเงินสด ยังไม่รวมค่าบริการทางการแพทย์ 30 บาท อาจเปลี่ยนแปลงได้ ความเหมาะสมของแต่ละบริการขึ้นกับการประเมินของแพทย์ ผลลัพธ์ของแต่ละบุคคลอาจแตกต่างกัน สิทธิบัตรทองและประกันสังคมเป็นไปตามเงื่อนไขของแต่ละสิทธิ</p>
</div>
'''

LIST_JS = r'''
<script>
  // ตัวกรองหมวดหมู่ (เนื้อหาถูก render มาจาก server แล้ว ฝั่ง client แค่ซ่อน/แสดง)
  (function(){
    var chips = document.getElementById('cat-chips');
    if(!chips) return;
    chips.addEventListener('click', function(e){
      var btn = e.target.closest('button'); if(!btn) return;
      var cat = btn.getAttribute('data-cat');
      chips.querySelectorAll('button').forEach(function(b){ b.classList.toggle('active', b === btn); b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
      document.querySelectorAll('.pg-section').forEach(function(s){
        s.hidden = !(cat === 'all' || s.getAttribute('data-cat') === cat);
      });
      try { history.replaceState(null, '', cat === 'all' ? '/programs' : '/programs?cat=' + encodeURIComponent(cat)); } catch(e){}
    });
    var q = new URLSearchParams(location.search).get('cat');
    if(q){ var b = chips.querySelector('button[data-cat="' + q.replace(/[^a-z0-9-]/g,'') + '"]'); if(b) b.click(); }
  })();
'''

DETAIL_BODY = r'''
<div class="wrap">
  <div id="pd-root">
    <div class="pg-empty">กำลังโหลดโปรแกรม...</div>
  </div>
</div>
'''

DETAIL_JS = r'''
<script>
  // อัปเดตราคาและข้อความจองใน LINE ตามตัวเลือกที่ลูกค้าเลือก
  (function(){
    var dataEl = document.getElementById('program-data');
    if(!dataEl) return;
    var P = JSON.parse(dataEl.textContent);
    if (document.querySelector('.pd-bar')) document.body.classList.add('has-bar');
    function fmt(n){ return n == null || n === '' ? 'สอบถามราคา' : '฿' + Number(n).toLocaleString('en-US', {maximumFractionDigits: 2}); }
    function lineText(opt){
      var price = opt && opt.price != null && opt.price !== '' ? opt.price : P.price;
      return ['สวัสดีค่ะ ต้องการจองคิว',
        'โปรแกรม: ' + P.name + (opt && opt.label ? ' (' + opt.label + ')' : ''),
        'ราคา: ' + fmt(price),
        'ชื่อ-นามสกุล: ', 'เบอร์โทร: ', 'วันที่สะดวก: '].join('\n');
    }
    function sync(){
      var r = document.querySelector('input[name="pd-opt"]:checked');
      var opt = r ? (P.options[Number(r.value)] || null) : null;
      var price = opt && opt.price != null && opt.price !== '' ? opt.price : P.price;
      document.querySelectorAll('[data-sel-price]').forEach(function(el){ el.textContent = fmt(price); });
      var href = 'https://line.me/R/oaMessage/' + encodeURIComponent('@p49clinic') + '/?' + encodeURIComponent(lineText(opt));
      document.querySelectorAll('.js-line-book').forEach(function(a){ a.href = href; });
    }
    document.querySelectorAll('input[name="pd-opt"]').forEach(function(r){ r.addEventListener('change', sync); });
    sync();
  })();
'''


def page(css, body, js):
    return (head + css + between + body + '\n' + footer + '\n' + js + '\n' + toggle_js + '</script>\n\n</body>\n</html>\n')


(ROOT / 'programs.html').write_text(page(LIST_CSS, LIST_BODY, LIST_JS), encoding='utf-8')
(ROOT / 'program.html').write_text(page(DETAIL_CSS, DETAIL_BODY, DETAIL_JS), encoding='utf-8')
print('ok')

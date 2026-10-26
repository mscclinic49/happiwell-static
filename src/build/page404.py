# -*- coding: utf-8 -*-
"""สร้าง 404.html (หน้าไม่พบ) จาก privacy.html — ข้อความ 3 ภาษา ปุ่มกลับหน้าแรกตัวใหญ่
รัน: python3 src/build/page404.py  (รันใหม่ทุกครั้งที่แก้ privacy.html / เมนู)
"""
import pathlib, re, runpy, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
NAV = runpy.run_path(str(ROOT / 'src/build/langnav.py'))
s = (ROOT / 'privacy.html').read_text(encoding='utf-8')

s = re.sub(r'<link rel="canonical"[^>]*>\n?', '<meta name="robots" content="noindex">\n', s, count=1)
s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', s)
s = re.sub(r'<title>.*?</title>', '<title>ไม่พบหน้านี้ | HappiWell คลินิกเวชกรรม</title>', s, count=1)
s = re.sub(re.escape(NAV['START']) + '.*?' + re.escape(NAV['END']), lambda m: NAV['block']('th', '/'), s, flags=re.S)

BODY = '''<div class="policy-wrap nf">
  <h1>ไม่พบหน้าที่คุณต้องการ</h1>
  <p>ลิงก์อาจไม่ถูกต้อง หรือหน้านี้ถูกย้ายแล้ว</p>
  <p class="nf-alt" lang="en">Page not found.</p>
  <p class="nf-alt" lang="my">စာမျက်နှာ မတွေ့ပါ။</p>
  <div class="nf-btns">
    <a class="nf-btn nf-home" href="/">← กลับหน้าแรก</a>
    <a class="nf-btn" href="/programs">ดูราคา/โปรแกรม</a>
    <a class="nf-btn nf-line" href="https://line.me/R/ti/p/@p49clinic" target="_blank" rel="noopener">สอบถามทาง LINE</a>
  </div>
  <p class="nf-langs"><a href="/en/" lang="en">English home</a> · <a href="/my/" lang="my">မြန်မာ ပင်မစာမျက်နှာ</a></p>
</div>
<style>
  .nf{text-align:center;padding-top:56px;padding-bottom:64px;}
  .nf h1{font-size:30px;}
  .nf p{font-size:18px;}
  .nf-alt{color:var(--ink-soft);margin:4px 0;}
  .nf-btns{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:28px 0 20px;}
  .nf-btn{display:inline-block;padding:14px 24px;border-radius:999px;font-weight:700;font-size:17px;border:1.5px solid var(--mint-200);color:var(--mint-900);background:var(--surface);}
  .nf-home{background:var(--mint-600);border-color:var(--mint-600);color:#fff;}
  .nf-line{background:var(--line-green);border-color:var(--line-green);color:#fff;}
  .nf-langs a{color:var(--mint-700);text-decoration:underline;}
</style>
'''
s, n = re.subn(r'<div class="policy-wrap">.*?</div>\n(?=<footer)', lambda m: BODY, s, count=1, flags=re.S)
if n != 1:
    sys.exit('policy-wrap not found')
s = s.replace('</head>', '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Myanmar:wght@400;600&display=swap" rel="stylesheet">\n<style>[lang="my"]{font-family:"Noto Sans Myanmar",sans-serif;}</style>\n</head>', 1)
(ROOT / '404.html').write_text(s, encoding='utf-8')
print('ok 404.html')

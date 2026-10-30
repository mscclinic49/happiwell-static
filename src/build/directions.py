# -*- coding: utf-8 -*-
"""สร้าง directions.html (แผนที่และวิธีเดินทาง) จาก privacy.html — header/footer/CSS ชุดเดียวกับเว็บ
รัน: python3 src/build/directions.py แล้วรัน python3 src/build/i18n-pages.py (สร้าง en/ my/)
ระยะทาง = ระยะเส้นตรงโดยประมาณ คำนวณจากพิกัดใน Google Maps (ไม่ใช่ระยะขับรถ)
คำแปลอยู่ใน src/build/directions-strings.py
"""
import pathlib, re, runpy, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
NAV = runpy.run_path(str(ROOT / 'src/build/langnav.py'))
SITE = 'https://happiwellclinic.com'
LAT, LNG = 13.648962, 100.4964886
s = (ROOT / 'privacy.html').read_text(encoding='utf-8')

TITLE = 'แผนที่และวิธีเดินทาง ใกล้ มจธ. บางมด | แฮปปี้เวลล์ คลินิกเวชกรรม ทุ่งครุ'
DESC = 'แผนที่แฮปปี้เวลล์ คลินิกเวชกรรม 195 ซอยประชาอุทิศ 49 บางมด ทุ่งครุ ห่าง มจธ. บางมด ประมาณ 350 เมตร ใกล้ตลาดใหม่ทุ่งครุ กดนำทางด้วย Google Maps ได้ทันที'

alts = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{SITE + NAV["prefixed"]("/directions", l)}">' for l in ('th', 'en', 'my'))
alts += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/directions">'
s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', s)
s = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{SITE}/directions">\n' + alts, s, count=1)
s = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', s, count=1)
if '<meta name="description"' in s:
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', s, count=1)
else:
    s = s.replace('<title>', f'<meta name="description" content="{DESC}">\n<title>', 1)
s = re.sub(re.escape(NAV['START']) + '.*?' + re.escape(NAV['END']), lambda m: NAV['block']('th', '/directions'), s, flags=re.S)

JSONLD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"MedicalClinic","@id":"' + SITE + '/#clinic",'
          '"name":"HappiWell Medical Clinic","url":"' + SITE + '/","telephone":["+66-2-000-4586","+66-88-683-7899"],'
          '"address":{"@type":"PostalAddress","streetAddress":"195 Soi Pracha Uthit 49","addressLocality":"Bang Mot, Thung Khru","addressRegion":"Bangkok","postalCode":"10140","addressCountry":"TH"},'
          f'"geo":{{"@type":"GeoCoordinates","latitude":{LAT},"longitude":{LNG}}},"hasMap":"https://www.google.com/maps?q={LAT},{LNG}",'
          '"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"18:00"},'
          '{"@type":"OpeningHoursSpecification","dayOfWeek":["Saturday","Sunday"],"opens":"08:00","closes":"12:00"}]}</script>\n')
s = s.replace('</head>', JSONLD + '</head>', 1)

NAVURL = f'https://www.google.com/maps/dir/?api=1&amp;destination={LAT},{LNG}'
PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'

# (ชื่อ, ระยะ) — ระยะเส้นตรงจากพิกัดคลินิก
NEAR = [
  ('มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (มจธ. บางมด)', 'ประมาณ 350 เมตร'),
  ('ตลาดใหม่ทุ่งครุ', 'ประมาณ 550 เมตร'),
  ('ตลาดทุ่งครุพลาซ่า', 'ประมาณ 650 เมตร'),
  ('Market Place ประชาอุทิศ (Tops)', 'ประมาณ 1.1 กิโลเมตร'),
  ('โลตัส โก เฟรช ประชาอุทิศ', 'ประมาณ 1.2 กิโลเมตร'),
]
HOSP = [
  ('โรงพยาบาลสุขสวัสดิ์อินเตอร์', 'ประมาณ 3 กิโลเมตร'),
  ('โรงพยาบาลราษฎร์บูรณะ', 'ประมาณ 3.3 กิโลเมตร'),
]
li = lambda rows: '\n'.join(f'      <li><span>\n{n}\n</span><b>\n{d}\n</b></li>' for n, d in rows)

BODY = f'''<div class="policy-wrap dir">
  <a class="back" href="/">← กลับหน้าแรก</a>
  <h1>แผนที่และวิธีเดินทาง</h1>
  <p class="dir-lead">แฮปปี้เวลล์ คลินิกเวชกรรม อยู่ในซอยประชาอุทิศ 49 แขวงบางมด เขตทุ่งครุ ใกล้ มจธ. บางมด</p>

  <div class="dir-card">
    <div class="dir-addr">{PIN}<div><div class="dir-label">ที่อยู่</div><div class="dir-val">195 ซอยประชาอุทิศ 49 แขวงบางมด เขตทุ่งครุ กรุงเทพฯ 10140</div></div></div>
    <div class="dir-btns">
      <a class="dir-btn dir-go" href="{NAVURL}" target="_blank" rel="noopener">นำทางด้วย Google Maps</a>
      <a class="dir-btn" href="tel:020004586">โทร 02-000-4586</a>
      <a class="dir-btn dir-line" href="https://line.me/R/ti/p/@p49clinic" target="_blank" rel="noopener">สอบถามทาง LINE</a>
    </div>
  </div>

  <div class="dir-map"><iframe src="https://www.google.com/maps?q={LAT},{LNG}&amp;z=16&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="แผนที่ HappiWell คลินิกเวชกรรม"></iframe></div>

  <h2>เวลาทำการ</h2>
  <ul class="dir-list">
      <li><span>
จันทร์ – ศุกร์
</span><b>08:00 – 18:00 น.</b></li>
      <li><span>
เสาร์ – อาทิตย์
</span><b>08:00 – 12:00 น.</b></li>
  </ul>
  <p class="dir-note">วันหยุดนักขัตฤกษ์ อาจปรับเวลาเปิด–ปิด ติดตามประกาศทาง LINE @p49clinic</p>

  <h2>จุดสังเกตใกล้คลินิก</h2>
  <ul class="dir-list">
{li(NEAR)}
  </ul>
  <p class="dir-note">ระยะทางเป็นระยะเส้นตรงโดยประมาณ ระยะเดินทางจริงขึ้นกับเส้นทาง</p>

  <h2>โรงพยาบาลใกล้เคียง</h2>
  <ul class="dir-list">
{li(HOSP)}
  </ul>
  <p class="dir-note">กรณีฉุกเฉิน เช่น เจ็บหน้าอกรุนแรง หายใจไม่ออก หมดสติ โทร 1669 หรือไปโรงพยาบาลทันที</p>

  <h2>วิธีเดินทาง</h2>
  <ul class="dir-steps">
    <li>
มาตามถนนประชาอุทิศ แล้วเลี้ยวเข้าซอยประชาอุทิศ 49
</li>
    <li>
ถ้ามาจาก มจธ. บางมด หรือตลาดใหม่ทุ่งครุ คลินิกอยู่ไม่ไกล กดปุ่ม "นำทางด้วย Google Maps" ด้านบนเพื่อดูเส้นทางจากจุดที่คุณอยู่
</li>
    <li>
หาไม่เจอ โทร 02-000-4586 หรือ 088-683-7899 เจ้าหน้าที่ช่วยบอกทางได้
</li>
  </ul>
</div>
<style>
  .dir h2{{margin-top:34px;}}
  .dir-lead{{font-size:18px;}}
  .dir-card{{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:20px;margin:22px 0;}}
  .dir-addr{{display:flex;gap:12px;align-items:flex-start;}}
  .dir-addr svg{{width:26px;height:26px;flex-shrink:0;fill:none;stroke:var(--mint-700);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;margin-top:2px;}}
  .dir-label{{font-size:14px;color:var(--ink-soft);}}
  .dir-val{{font-size:18px;font-weight:600;color:var(--ink);}}
  .dir-btns{{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px;}}
  .dir-btn{{display:inline-block;padding:13px 20px;border-radius:999px;font-weight:700;font-size:16.5px;border:1.5px solid var(--mint-200);color:var(--mint-900);background:var(--surface);}}
  .dir-go{{background:var(--mint-600);border-color:var(--mint-600);color:#fff;}}
  .dir-line{{background:var(--line-green);border-color:var(--line-green);color:#fff;}}
  .dir-map{{border-radius:18px;overflow:hidden;border:1px solid var(--line);aspect-ratio:16/10;}}
  .dir-map iframe{{width:100%;height:100%;border:0;display:block;}}
  .dir-list{{list-style:none;padding:0;margin:12px 0 0;}}
  .dir-list li{{display:flex;justify-content:space-between;gap:12px;padding:12px 0;border-bottom:1px solid var(--line);font-size:17px;}}
  .dir-list li b{{white-space:nowrap;color:var(--mint-700);}}
  .dir-note{{font-size:14.5px;color:var(--ink-soft);margin-top:10px;}}
  .dir-steps li{{font-size:17px;margin-bottom:8px;}}
  @media (max-width:600px){{ .dir-btn{{flex:1 1 100%;text-align:center;}} .dir-map{{aspect-ratio:4/5;}} }}
</style>
'''
s, n = re.subn(r'<div class="policy-wrap">.*?</div>\n(?=<footer)', lambda m: BODY, s, count=1, flags=re.S)
if n != 1:
    sys.exit('policy-wrap not found')
(ROOT / 'directions.html').write_text(s, encoding='utf-8')
print('ok directions.html')

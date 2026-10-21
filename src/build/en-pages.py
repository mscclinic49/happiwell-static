"""สร้างหน้าเว็บภาษาอังกฤษ en/*.html จากหน้าภาษาไทย (ดีไซน์/โลโก้/CSS ชุดเดียวกัน)

รัน (หลังแก้หน้าไทย หรือหลังรัน programs-parts.py):
    python3 src/build/en-pages.py

- แปลข้อความด้วยตาราง src/build/en-strings.py (แปลทั้งท่อนตรงตัว)
- ถ้ามีข้อความไทยที่ยังไม่มีคำแปล สคริปต์จะแสดงรายการและหยุด (ไม่เขียนไฟล์)
- เนื้อหาจากฐานข้อมูล (บทความ/โปรแกรม) Worker เติมเป็นภาษาอังกฤษให้เองตอนเปิดหน้า
"""
import pathlib, re, sys, runpy

ROOT = pathlib.Path(__file__).resolve().parents[2]
T = runpy.run_path(str(ROOT / 'src/build/en-strings.py'))['T']
OUT = ROOT / 'en'
PAGES = ['index.html', 'programs.html', 'program.html', 'articles.html', 'article.html', 'privacy.html', 'cookies.html']
THAI = re.compile(r'[฀-๿][^<>"`\n]{0,400}')
GLOBE = '<svg viewBox="0 0 24 24" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>'
# หน้าไทยที่คู่กับแต่ละไฟล์ (ใช้กับปุ่ม "ไทย" และ hreflang ของหน้าคงที่)
TH_PATH = {'index.html': '/', 'programs.html': '/programs', 'program.html': '/programs', 'articles.html': '/articles',
           'article.html': '/articles', 'privacy.html': '/privacy', 'cookies.html': '/cookies'}
SITE = 'https://happiwellclinic.com'


def must_replace(s, old, new, name, count=1):
    n = s.count(old)
    if n != count:
        sys.exit(f'{name}: expected {count}x {old[:60]!r}, found {n}')
    return s.replace(old, new)


def translate(s, name, missing):
    def sub(m):
        seg = m.group(0)
        key = seg.rstrip()
        if key in T:
            return T[key] + seg[len(key):]
        missing.add((name, key))
        return seg
    return THAI.sub(sub, s)


def build(name):
    s = (ROOT / name).read_text(encoding='utf-8')

    # 1) ปุ่มเปลี่ยนภาษา EN → ไทย (ทำก่อนแปล เพราะต้องคงคำว่า "ไทย")
    s = re.sub(r'<a href="/en/[^"]*" class="lang-sw" hreflang="en" lang="en" aria-label="English version">.*?EN</a>',
               f'<a href="{TH_PATH[name]}" class="lang-sw" hreflang="th" lang="th" aria-label="ภาษาไทย">{GLOBE}@@TH@@</a>', s, count=1)
    if '@@TH@@' not in s:
        sys.exit(f'{name}: language switch not found')

    # 2) แก้ JS ให้ใช้เนื้อหาภาษาอังกฤษ / ลิงก์ /en
    if name == 'index.html':
        # ข่าวในหน้าแรก Worker render มาแล้ว ไม่ต้องโหลดซ้ำ (ไม่งั้นจะทับด้วยภาษาไทย)
        s = must_replace(s, '  loadNews();\n', "  if (document.querySelector('#news-grid .news-card')) buildNewsDots(); else loadNews();\n", name)
        s = must_replace(s, 'articles.push(result.data[0]);', 'articles.push(EN(result.data[0]));', name)
        s = must_replace(s, '  function cardHtml(a){', '  function EN(a){ return a.en && a.en.title ? Object.assign({}, a, { title: a.en.title, excerpt: a.en.excerpt || a.excerpt }) : a; }\n  function cardHtml(a){', name)
    if name == 'articles.html':
        s = must_replace(s, 'allArticles = data || [];',
                         'allArticles = (data || []).map(a => a.en && a.en.title ? Object.assign({}, a, { title: a.en.title, excerpt: a.en.excerpt || a.excerpt }) : a);', name)
        # แท็กเป็นภาษาไทย หน้าอังกฤษไม่ต้องกรองแท็ก
    s = s.replace("toLocaleDateString('th-TH'", "toLocaleDateString('en-GB'")
    s = s.replace("'/programs' : '/programs?cat='", "'/en/programs' : '/en/programs?cat='")
    s = re.sub(r"(['\"`])/articles/", r"\1/en/articles/", s)

    # 3) ลิงก์ภายใน → /en
    s = re.sub(r'href="/(programs|articles|privacy|cookies)(?=[/"?#])', r'href="/en/\1', s)
    s = re.sub(r'href="/(#[^"]*)?"', lambda m: f'href="/en/{m.group(1) or ""}"', s)

    # 4) ภาษา + canonical/hreflang ของหน้าคงที่
    s = must_replace(s, '<html lang="th"', '<html lang="en"', name)
    if name in ('privacy.html', 'cookies.html'):
        th = SITE + TH_PATH[name]
        en = SITE + '/en' + TH_PATH[name]
        s = re.sub(r'\n<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', s)
        s, n = re.subn(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{en}">', s)
        if n != 1:
            sys.exit(f'{name}: canonical not found')
        s = s.replace(f'<link rel="canonical" href="{en}">',
                      f'<link rel="canonical" href="{en}">\n<link rel="alternate" hreflang="th" href="{th}">\n'
                      f'<link rel="alternate" hreflang="en" href="{en}">\n<link rel="alternate" hreflang="x-default" href="{th}">', 1)

    # 5) แปลข้อความ
    missing = set()
    s = translate(s, name, missing)
    s = s.replace('@@TH@@', 'ไทย')
    return s, missing


def add_th_hreflang():
    """หน้าไทย privacy/cookies: ใส่ hreflang ชี้หน้าอังกฤษ (ทำครั้งเดียว)"""
    for name in ('privacy.html', 'cookies.html'):
        p = ROOT / name
        s = p.read_text(encoding='utf-8')
        if 'hreflang="en"' in s.split('</head>')[0]:
            continue
        th = SITE + TH_PATH[name]
        en = SITE + '/en' + TH_PATH[name]
        s, n = re.subn(r'(<link rel="canonical" href="[^"]*">)',
                       rf'\1\n<link rel="alternate" hreflang="th" href="{th}">\n<link rel="alternate" hreflang="en" href="{en}">\n<link rel="alternate" hreflang="x-default" href="{th}">', s, count=1)
        if n != 1:
            sys.exit(f'{name}: canonical not found')
        p.write_text(s, encoding='utf-8')


def main():
    add_th_hreflang()
    results, all_missing = {}, set()
    for name in PAGES:
        s, missing = build(name)
        results[name] = s
        all_missing |= missing
    if all_missing:
        print('ข้อความที่ยังไม่มีคำแปลใน en-strings.py:')
        for name, key in sorted(all_missing):
            print(f'  [{name}] {key}')
        sys.exit(1)
    OUT.mkdir(exist_ok=True)
    for name, s in results.items():
        (OUT / name).write_text(s, encoding='utf-8')
    print('ok', ', '.join(f'en/{n}' for n in results))


if __name__ == '__main__':
    main()

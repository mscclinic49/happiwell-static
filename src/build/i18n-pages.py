"""สร้างหน้าเว็บภาษาอื่นจากหน้าภาษาไทย (ดีไซน์/โลโก้/CSS ชุดเดียวกัน)
  en/*.html  ใช้คำแปลจาก src/build/en-strings.py
  my/*.html  (ภาษาพม่า) ใช้คำแปลจาก src/build/my-strings.py

รัน (หลังแก้หน้าไทย หรือหลังรัน programs-parts.py):
    python3 src/build/i18n-pages.py          # ทุกภาษา
    python3 src/build/i18n-pages.py my       # เฉพาะภาษาพม่า

- แปลข้อความทั้งท่อนตรงตัว ถ้ามีข้อความไทยที่ยังไม่มีคำแปล จะแสดงรายการและหยุด (ไม่เขียนไฟล์)
- เนื้อหาจากฐานข้อมูล (บทความ/โปรแกรม) Worker เติมตามภาษาให้เองตอนเปิดหน้า (คอลัมน์ en / my)
"""
import pathlib, re, sys, runpy

ROOT = pathlib.Path(__file__).resolve().parents[2]
NAV = runpy.run_path(str(ROOT / 'src/build/langnav.py'))
PAGES = ['index.html', 'programs.html', 'program.html', 'articles.html', 'article.html', 'privacy.html', 'cookies.html']
THAI = re.compile(r'[฀-๿][^<>"`\n]{0,400}')
TH_PATH = {'index.html': '/', 'programs.html': '/programs', 'program.html': '/programs', 'articles.html': '/articles',
           'article.html': '/articles', 'privacy.html': '/privacy', 'cookies.html': '/cookies'}
SITE = 'https://happiwellclinic.com'
LOCALE = {'en': 'en-GB', 'my': 'my-MM'}
ALL = ['th', 'en', 'my']
MY_HEAD = ('<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Myanmar:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
           '<style>html[lang="my"] body,html[lang="my"] h1,html[lang="my"] h2,html[lang="my"] h3,html[lang="my"] button,html[lang="my"] input,html[lang="my"] textarea,'
           'html[lang="my"] .btn,html[lang="my"] .brand-name,html[lang="my"] .price,html[lang="my"] .price-ask{font-family:"Anuphan","IBM Plex Sans Thai","Noto Sans Myanmar",sans-serif;}'
           'html[lang="my"] body{line-height:1.85;}html[lang="my"] h1,html[lang="my"] h2,html[lang="my"] h3{line-height:1.55;}</style>\n')


def must_replace(s, old, new, name, count=1):
    n = s.count(old)
    if n != count:
        sys.exit(f'{name}: expected {count}x {old[:60]!r}, found {n}')
    return s.replace(old, new)


def alternates(path):
    th = SITE + path
    out = [f'<link rel="alternate" hreflang="{l}" href="{SITE + NAV["prefixed"](path, l)}">' for l in ALL]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{th}">')
    return '\n'.join(out)


def build(name, lang, T):
    s = (ROOT / name).read_text(encoding='utf-8')
    pfx = '/' + lang

    # 1) เมนูภาษา: เก็บไว้ก่อน แล้วสร้างใหม่ตามภาษาของหน้า
    s, n = re.subn(re.escape(NAV['START']) + '.*?' + re.escape(NAV['END']), '@@LANGNAV@@', s, flags=re.S)
    if n != 1:
        sys.exit(f'{name}: language menu not found')

    # 2) JS ให้ใช้เนื้อหาตามภาษา (ภาษาพม่า: ถ้าไม่มี ใช้อังกฤษ)
    pickjs = (f"function LX(a){{ var e = (a.{lang} && a.{lang}.title) ? a.{lang} : " + ("((a.en && a.en.title) ? a.en : null)" if lang == 'my' else 'null') +
              "; return e ? Object.assign({}, a, { title: e.title, excerpt: e.excerpt || a.excerpt }) : a; }")
    if name == 'index.html':
        s = must_replace(s, '  loadNews();\n', "  if (document.querySelector('#news-grid .news-card')) buildNewsDots(); else loadNews();\n", name)
        s = must_replace(s, 'articles.push(result.data[0]);', 'articles.push(LX(result.data[0]));', name)
        s = must_replace(s, '  function cardHtml(a){', f'  {pickjs}\n  function cardHtml(a){{', name)
    if name == 'articles.html':
        s = must_replace(s, 'allArticles = data || [];', f'{pickjs}\n    allArticles = (data || []).map(LX);', name)
    s = s.replace("toLocaleDateString('th-TH'", f"toLocaleDateString('{LOCALE[lang]}'")
    s = s.replace("'/programs' : '/programs?cat='", f"'{pfx}/programs' : '{pfx}/programs?cat='")
    s = re.sub(r"(['\"`])/articles/", rf"\1{pfx}/articles/", s)

    # 3) ลิงก์ภายใน
    s = re.sub(r'href="/(programs|articles|privacy|cookies)(?=[/"?#])', rf'href="{pfx}/\1', s)
    s = re.sub(r'href="/(#[^"]*)?"', lambda m: f'href="{pfx}/{m.group(1) or ""}"', s)

    # 4) ภาษา + canonical/hreflang ของหน้าคงที่ + ฟอนต์พม่า
    s = must_replace(s, '<html lang="th"', f'<html lang="{lang}"', name)
    if name in ('privacy.html', 'cookies.html'):
        own = SITE + NAV['prefixed'](TH_PATH[name], lang)
        s = re.sub(r'\n<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', s)
        s, n = re.subn(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{own}">\n' + alternates(TH_PATH[name]), s)
        if n != 1:
            sys.exit(f'{name}: canonical not found')
    if lang == 'my':
        s = must_replace(s, '</head>', MY_HEAD + '</head>', name)

    # 5) แปลข้อความ
    missing = set()

    def sub(m):
        seg = m.group(0)
        key = seg.rstrip()
        if key in T:
            return T[key] + seg[len(key):]
        missing.add((name, key))
        return seg
    s = THAI.sub(sub, s)
    s = s.replace('@@LANGNAV@@', NAV['block'](lang, TH_PATH[name]))
    return s, missing


def thai_hreflang():
    """หน้าไทย privacy/cookies: hreflang ครบทุกภาษา"""
    for name in ('privacy.html', 'cookies.html'):
        p = ROOT / name
        s = p.read_text(encoding='utf-8')
        s = re.sub(r'\n<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', s)
        s, n = re.subn(r'(<link rel="canonical" href="[^"]*">)', lambda m: m.group(1) + '\n' + alternates(TH_PATH[name]), s, count=1)
        if n != 1:
            sys.exit(f'{name}: canonical not found')
        p.write_text(s, encoding='utf-8')


def main():
    langs = sys.argv[1:] or ['en', 'my']
    thai_hreflang()
    for lang in langs:
        T = runpy.run_path(str(ROOT / f'src/build/{lang}-strings.py'))['T']
        results, all_missing = {}, set()
        for name in PAGES:
            s, missing = build(name, lang, T)
            results[name] = s
            all_missing |= missing
        if all_missing:
            print(f'ข้อความที่ยังไม่มีคำแปลใน {lang}-strings.py:')
            for name, key in sorted(all_missing):
                print(f'  [{name}] {key}')
            sys.exit(1)
        out = ROOT / lang
        out.mkdir(exist_ok=True)
        for name, s in results.items():
            (out / name).write_text(s, encoding='utf-8')
        print('ok', ', '.join(f'{lang}/{n}' for n in results))


if __name__ == '__main__':
    main()

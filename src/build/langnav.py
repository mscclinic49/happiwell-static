# -*- coding: utf-8 -*-
"""เมนูเลือกภาษา (ไทย / English / မြန်မာ) ใช้ร่วมกันทุกหน้า
- หน้าคงที่: สร้างลิงก์ตาม path ของหน้านั้น
- หน้าที่ Worker render: Worker เปลี่ยน href ของ a.lang-th / a.lang-en / a.lang-my ให้ตรงหน้าอีกครั้ง
"""
LANGS = [('th', 'ไทย', 'ไทย'), ('en', 'EN', 'English'), ('my', 'မြန်မာ', 'မြန်မာ')]
GLOBE = '<svg viewBox="0 0 24 24" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>'
START = '<!--langnav-->'
END = '<!--/langnav-->'


def prefixed(path, lang):
    if lang == 'th':
        return path
    return f'/{lang}/' if path == '/' else f'/{lang}{path}'


def block(current, path):
    """current = ภาษาของหน้านี้, path = path ภาษาไทยของหน้านี้ เช่น '/programs'"""
    short = dict((c, s) for c, s, _ in LANGS)[current]
    links = ''.join(
        f'<a class="lang-{c}" href="{prefixed(path, c)}" hreflang="{c}" lang="{c}"{" aria-current=\"true\"" if c == current else ""}>{full}</a>'
        for c, _, full in LANGS)
    return (f'{START}<details class="lang-dd"><summary aria-label="Language / ภาษา / ဘာသာစကား">{GLOBE}<span lang="{current}">{short}</span></summary>'
            f'<div class="lang-menu">{links}</div></details>'
            '<script>document.addEventListener("click",function(e){document.querySelectorAll("details.lang-dd[open]").forEach(function(d){if(!d.contains(e.target))d.removeAttribute("open");});});</script>'
            f'{END}')


CSS = '''  .lang-dd{position:relative;margin-right:8px;}
  .lang-dd summary{list-style:none;display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:700;color:var(--mint-900);border:1.5px solid var(--mint-200);background:var(--surface);padding:7px 12px;border-radius:999px;cursor:pointer;white-space:nowrap;}
  .lang-dd summary::-webkit-details-marker{display:none;}
  .lang-dd summary::after{content:'▾';font-size:11px;opacity:.7;}
  .lang-dd summary svg{width:16px;height:16px;stroke:currentColor;fill:none;}
  .lang-dd[open] summary,.lang-dd summary:hover{border-color:var(--mint-600);}
  .lang-menu{position:absolute;right:0;top:calc(100% + 6px);background:var(--surface);border:1px solid var(--line);border-radius:12px;box-shadow:0 10px 28px rgba(16,40,60,.14);padding:6px;min-width:150px;z-index:80;display:flex;flex-direction:column;}
  .lang-menu a{padding:10px 12px;border-radius:8px;font-size:15px;font-weight:600;color:var(--ink);text-decoration:none;}
  .lang-menu a:hover,.lang-menu a[aria-current]{background:var(--mint-50);color:var(--mint-700);}
'''
MOBILE = '.lang-dd{margin-right:6px;} .lang-dd summary{padding:6px 10px;font-size:13.5px;} .lang-dd summary svg{display:none;}'

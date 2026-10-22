# -*- coding: utf-8 -*-
"""โพสต์: ใบรับรองแพทย์ใบขับขี่ (หน้าโปรแกรม + บทความ) ภาษาไทย + อังกฤษ + SEO
รัน: python3 supabase/seed/posts/driving_licence.py  → พิมพ์ SQL เป็นชิ้นเล็ก ๆ (รันทีละชิ้นได้)
"""
import json, sys

PROG_SLUG = 'driving-licence-medical-certificate'
ART_SLUG = 'driving-licence-medical-certificate-2569'

def doc(blocks):
    out = []
    for i, b in enumerate(blocks):
        t, v = b
        if t == 'P': out.append({'id': f'd{i}', 'type': 'paragraph', 'data': {'text': v}})
        elif t == 'H2': out.append({'id': f'd{i}', 'type': 'header', 'data': {'text': v, 'level': 2}})
        elif t == 'L': out.append({'id': f'd{i}', 'type': 'list', 'data': {'style': 'unordered', 'items': v}})
    return out

# ---------------- หน้าโปรแกรม (ราคา) ----------------
PROGRAM = dict(
  slug=PROG_SLUG, category='certificate', price=200, price_unit='ต่อฉบับ', sort_order=2, is_featured=True, is_published=True,
  related_article_slug=ART_SLUG,
  name='ใบรับรองแพทย์ ทำใบขับขี่',
  short_desc='ใบรับรองแพทย์สำหรับยื่นกรมการขนส่งทางบก ทำใบขับขี่ใหม่ 200 บาท ตรวจโดยแพทย์ ชาวต่างชาติก็ทำได้',
  description=doc([
    ('P', 'ใบรับรองแพทย์สำหรับยื่นทำใบอนุญาตขับรถที่กรมการขนส่งทางบก (ที่หลายคนเรียกว่า “ใบรับรองแพทย์ 5 โรค”) แพทย์ซักประวัติและตรวจร่างกายก่อนออกใบรับรองทุกครั้ง'),
    ('P', 'ใบรับรองแพทย์ต้องออกไม่เกิน 1 เดือนก่อนวันยื่นที่สำนักงานขนส่ง แนะนำให้มาตรวจก่อนวันนัดไม่กี่วัน ชาวต่างชาติทำได้ นำพาสปอร์ตตัวจริงมาด้วย'),
  ]),
  suitable_for=['ผู้ที่จะทำใบขับขี่รถยนต์หรือรถจักรยานยนต์ครั้งแรก', 'ชาวต่างชาติที่ต้องการทำใบขับขี่ไทย', 'ผู้ที่สำนักงานขนส่งแจ้งให้ยื่นใบรับรองแพทย์'],
  includes=['ซักประวัติและตรวจร่างกายโดยแพทย์', 'ใบรับรองแพทย์สำหรับยื่นทำใบขับขี่'],
  precautions=['ใบรับรองแพทย์ต้องออกไม่เกิน 1 เดือนก่อนวันยื่นที่ขนส่ง', 'คนไทยนำบัตรประชาชน ชาวต่างชาติต้องนำพาสปอร์ตตัวจริงมาด้วย', 'แจ้งแพทย์หากมีโรคประจำตัวหรือยาที่ใช้เป็นประจำ'],
  seo_title='ใบรับรองแพทย์ใบขับขี่ 200 บาท ทุ่งครุ ประชาอุทิศ | HappiWell',
  seo_description='ใบรับรองแพทย์ทำใบขับขี่ 200 บาท ตรวจโดยแพทย์ ชาวต่างชาติทำได้ ที่แฮปปี้เวลล์ คลินิกเวชกรรม ซ.ประชาอุทิศ 49 ทุ่งครุ เปิดทุกวัน จองผ่าน LINE',
)
PROGRAM_EN = dict(
  name='Medical certificate for a Thai driving licence',
  short_desc='Medical certificate for your driving licence application at the Department of Land Transport — 200 baht, examined by a doctor. Foreigners welcome.',
  description=json.dumps({'time': 1792700000000, 'version': '2.29.1', 'blocks': doc([
    ('P', 'A medical certificate for your driving licence application at Thailand’s Department of Land Transport (DLT), often called the “5-disease medical certificate”. A doctor takes your history and examines you before issuing every certificate.'),
    ('P', 'The certificate must be issued no more than 1 month before you submit it at the DLT office, so we recommend coming in a few days before your appointment. Foreigners are welcome — please bring your original passport.'),
  ])}, ensure_ascii=False),
  price_unit='per certificate',
  suitable_for=['Anyone applying for a car or motorcycle driving licence for the first time', 'Foreigners applying for a Thai driving licence', 'Anyone the DLT office has asked to submit a medical certificate'],
  includes=['History and physical examination by a doctor', 'Medical certificate for your driving licence application'],
  precautions=['The certificate must be issued no more than 1 month before you submit it at the DLT office', 'Thai citizens: bring your ID card. Foreigners: bring your original passport', 'Tell the doctor about any long-term conditions or regular medicines'],
  seo_title='Medical Certificate for Thai Driving Licence 200 THB, Bangkok | HappiWell',
  seo_description='Medical certificate for a Thai driving licence (DLT) for 200 baht, examined by a doctor. Foreigners welcome. HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok. Open daily.',
)
PROGRAM['description'] = json.dumps({'time': 1792700000000, 'version': '2.29.1', 'blocks': PROGRAM['description']}, ensure_ascii=False)

# ---------------- บทความ ----------------
BOOK_TH = 'สนใจรับบริการ ทักแชท LINE หรือโทรสอบถามได้ที่คลินิกแฮปปี้เวลล์ เปิดบริการทุกวัน จันทร์–ศุกร์ 08.00–18.00 น. เสาร์–อาทิตย์ 08.00–12.00 น.'
BOOK_EN = 'To book, message us on LINE or call HappiWell Clinic. We are open every day: Monday–Friday 08:00–18:00 and Saturday–Sunday 08:00–12:00.'
ARTICLE = dict(
  slug=ART_SLUG, category='article', is_published=True, published_at='2026-10-22T09:00:00+07:00',
  tags=['ใบรับรองแพทย์', 'ใบขับขี่', 'ชาวต่างชาติ'],
  title='ใบรับรองแพทย์ทำใบขับขี่ ต้องเตรียมอะไร ราคาเท่าไหร่ (อัปเดตปี 2569)',
  excerpt='ทำใบขับขี่ต้องใช้ใบรับรองแพทย์แบบไหน มีอายุกี่วัน ต้องเตรียมเอกสารอะไร ชาวต่างชาติทำได้ไหม พร้อมราคา 200 บาทที่คลินิกแฮปปี้เวลล์ ทุ่งครุ',
  seo_title='ใบรับรองแพทย์ใบขับขี่ ต้องเตรียมอะไร ราคา 200 บาท (2569) | HappiWell',
  seo_description='ใบรับรองแพทย์ทำใบขับขี่ใช้แบบไหน มีอายุกี่วัน เตรียมเอกสารอะไร ชาวต่างชาติทำได้ไหม ราคา 200 บาท ที่แฮปปี้เวลล์ คลินิก ซ.ประชาอุทิศ 49 ทุ่งครุ',
  blocks=[
    ('P', 'จะไปทำใบขับขี่ที่สำนักงานขนส่ง หนึ่งในเอกสารที่ต้องเตรียมคือ “ใบรับรองแพทย์” หลายคนไม่แน่ใจว่าต้องใช้แบบไหน มีอายุกี่วัน และต้องเตรียมอะไรไปบ้าง บทความนี้สรุปไว้ให้ครบในที่เดียว รวมถึงข้อมูลสำหรับชาวต่างชาติที่ต้องการทำใบขับขี่ไทย'),
    ('H2', 'ทำไมต้องใช้ใบรับรองแพทย์'),
    ('P', 'กรมการขนส่งทางบกกำหนดให้ผู้ขอใบอนุญาตขับรถยื่นใบรับรองแพทย์ เพื่อยืนยันว่าร่างกายพร้อมสำหรับการขับขี่ และไม่มีโรคหรือภาวะที่เป็นอุปสรรคต่อการขับรถ ใบรับรองนี้หลายคนเรียกกันว่า “ใบรับรองแพทย์ 5 โรค”'),
    ('H2', 'ใบรับรองแพทย์มีอายุกี่วัน'),
    ('P', 'ใบรับรองแพทย์ต้อง<b>ออกไม่เกิน 1 เดือน</b>ก่อนวันที่ยื่นที่สำนักงานขนส่ง จึงแนะนำให้มาตรวจก่อนวันนัดขนส่งเพียงไม่กี่วัน ไม่ควรตรวจไว้ล่วงหน้านานเกินไป'),
    ('H2', 'ต้องเตรียมอะไรมาที่คลินิก'),
    ('L', ['คนไทย: บัตรประชาชน', 'ชาวต่างชาติ: พาสปอร์ตตัวจริง', 'ข้อมูลโรคประจำตัวหรือยาที่ใช้เป็นประจำ (ถ้ามี) เพื่อแจ้งแพทย์']),
    ('H2', 'ที่คลินิกตรวจอะไรบ้าง'),
    ('P', 'แพทย์จะซักประวัติสุขภาพ ตรวจร่างกายทั่วไป และวัดความดันโลหิต เพื่อประเมินตามหัวข้อในแบบฟอร์มใบรับรองแพทย์ จากนั้นจึงออกใบรับรองให้นำไปยื่นที่สำนักงานขนส่ง'),
    ('H2', 'ชาวต่างชาติทำใบขับขี่ไทย ต้องใช้อะไรอีก'),
    ('P', 'นอกจากใบรับรองแพทย์ สำนักงานขนส่งมักขอเอกสารเพิ่มเติม เช่น พาสปอร์ตพร้อมสำเนาหน้าวีซ่าและตราประทับเข้าประเทศ และหนังสือรับรองถิ่นที่อยู่จากสำนักงานตรวจคนเข้าเมืองหรือสถานทูต ข้อกำหนดของแต่ละสำนักงานอาจแตกต่างกัน ควรสอบถามสำนักงานขนส่งก่อนไปยื่น'),
    ('H2', 'ทำใบรับรองแพทย์ใบขับขี่ที่คลินิกแฮปปี้เวลล์ ราคาเท่าไหร่'),
    ('P', 'ที่ <b>แฮปปี้เวลล์คลินิก (HappiWell Clinic)</b> ย่านทุ่งครุ ออกใบรับรองแพทย์สำหรับทำใบขับขี่ราคา <b>200 บาทต่อฉบับ</b> (ยังไม่รวมค่าบริการทางการแพทย์ 30 บาท) ตรวจโดยแพทย์ทุกครั้ง รับทั้งคนไทยและชาวต่างชาติ ดูรายละเอียดได้ที่ <a href="/programs/driving-licence-medical-certificate">หน้าใบรับรองแพทย์ทำใบขับขี่</a>'),
    ('P', BOOK_TH),
    ('H2', 'คำถามที่พบบ่อย'),
    ('P', '<b>ใบรับรองแพทย์ใบขับขี่ใช้ได้นานแค่ไหน</b><br>ต้องออกไม่เกิน 1 เดือนก่อนวันยื่นที่สำนักงานขนส่ง'),
    ('P', '<b>ชาวต่างชาติทำใบรับรองแพทย์ที่คลินิกได้ไหม</b><br>ได้ นำพาสปอร์ตตัวจริงมาด้วย แพทย์จะตรวจและออกใบรับรองให้เหมือนคนไทย'),
    ('P', '<b>ต้องงดอาหารก่อนมาตรวจไหม</b><br>ไม่ต้อง เป็นการตรวจร่างกายทั่วไป ไม่ต้องเจาะเลือด'),
    ('P', '<i>บทความนี้จัดทำเพื่อให้ข้อมูลทั่วไป ข้อกำหนดเอกสารอาจเปลี่ยนแปลงหรือแตกต่างกันในแต่ละสำนักงานขนส่ง ควรตรวจสอบกับสำนักงานขนส่งก่อนไปยื่น</i>'),
  ],
)
ARTICLE_EN = dict(
  title='Medical Certificate for a Thai Driving Licence: What You Need and How Much It Costs (2026 Update)',
  excerpt='Which medical certificate you need for a Thai driving licence, how long it is valid, what to bring, whether foreigners can get one, and the 200-baht price at HappiWell Clinic, Thung Khru, Bangkok.',
  seo_title='Medical Certificate for Thai Driving Licence: What to Bring & Price | HappiWell',
  seo_description='Medical certificate for a Thai driving licence: validity, documents, tips for foreigners, and the 200-baht price at HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok.',
  blocks=[
    ('P', 'When you go to the Department of Land Transport (DLT) for a driving licence, one of the documents you need is a medical certificate. Many people are unsure which type they need, how long it is valid and what to bring. This article covers everything in one place, including information for foreigners applying for a Thai driving licence.'),
    ('H2', 'Why do you need a medical certificate?'),
    ('P', 'Thailand’s Department of Land Transport requires driving licence applicants to submit a medical certificate confirming that they are physically fit to drive and have no condition that would prevent safe driving. It is often called the “5-disease medical certificate”.'),
    ('H2', 'How long is the medical certificate valid?'),
    ('P', 'The certificate must be <b>issued no more than 1 month</b> before you submit it at the DLT office, so we recommend getting it just a few days before your DLT appointment rather than too far in advance.'),
    ('H2', 'What to bring to the clinic'),
    ('L', ['Thai citizens: your ID card', 'Foreigners: your original passport', 'Details of any long-term conditions or regular medicines (if any) to tell the doctor']),
    ('H2', 'What does the clinic check?'),
    ('P', 'The doctor takes your health history, does a general physical examination and checks your blood pressure, assessing you against the items on the certificate form, then issues the certificate for you to submit at the DLT office.'),
    ('H2', 'Foreigners applying for a Thai driving licence: what else do you need?'),
    ('P', 'Besides the medical certificate, DLT offices usually ask for other documents, such as your passport with copies of your visa page and latest entry stamp, and a certificate of residence from the Immigration Bureau or your embassy. Requirements can differ between offices, so check with the DLT office before you go.'),
    ('H2', 'Driving licence medical certificate at HappiWell Clinic: how much does it cost?'),
    ('P', '<b>HappiWell Medical Clinic</b> in Thung Khru issues medical certificates for driving licences for <b>200 baht per certificate</b> (plus the 30 baht medical service fee), always examined by a doctor. Thai citizens and foreigners are both welcome. See details on <a href="/programs/driving-licence-medical-certificate">our driving licence medical certificate page</a>.'),
    ('P', BOOK_EN),
    ('H2', 'Frequently asked questions'),
    ('P', '<b>How long is a driving licence medical certificate valid?</b><br>It must be issued no more than 1 month before you submit it at the DLT office.'),
    ('P', '<b>Can foreigners get a medical certificate at the clinic?</b><br>Yes. Bring your original passport and the doctor will examine you and issue the certificate, just as for Thai citizens.'),
    ('P', '<b>Do I need to fast before the check?</b><br>No. It is a general physical examination with no blood test.'),
    ('P', '<i>This article is for general information. Document requirements may change or differ between DLT offices, so please check with the DLT office before you apply.</i>'),
  ],
)

def q(v): return '$j$' + json.dumps(v, ensure_ascii=False) + '$j$'

def chunks(lst, n): return [lst[i:i + n] for i in range(0, len(lst), n)]

def sql():
    out = []
    p = {k: v for k, v in PROGRAM.items() if k != 'description'}
    cols = ', '.join(p.keys())
    vals = ', '.join(f"array(select jsonb_array_elements_text({q(v)}::jsonb))" if isinstance(v, list) else ('true' if v is True else 'false' if v is False else (str(v) if isinstance(v, (int, float)) else f"$j${v}$j$")) for v in p.values())
    out.append(f"insert into public.hw_programs ({cols}) values ({vals}) on conflict (slug) do nothing;")
    out.append(f"update public.hw_programs set description = $j${PROGRAM['description']}$j$ where slug = '{PROG_SLUG}';")
    out.append(f"update public.hw_programs set en = {q(PROGRAM_EN)}::jsonb where slug = '{PROG_SLUG}';")
    # บทความ: แทรกแถวพร้อมเนื้อหาว่าง แล้วต่อบล็อกทีละชุด
    a = ARTICLE
    out.append("insert into public.hw_articles (slug, category, is_published, published_at, tags, title, excerpt, seo_title, seo_description, content) values "
               f"('{a['slug']}', '{a['category']}', true, '{a['published_at']}', array(select jsonb_array_elements_text({q(a['tags'])}::jsonb)), $j${a['title']}$j$, $j${a['excerpt']}$j$, $j${a['seo_title']}$j$, $j${a['seo_description']}$j$, "
               "'{\"time\":1792700000000,\"version\":\"2.29.1\",\"blocks\":[]}') on conflict (slug) do nothing;")
    for ch in chunks(doc(a['blocks']), 4):
        out.append(f"update public.hw_articles set content = jsonb_set(content::jsonb, '{{blocks}}', (content::jsonb->'blocks') || {q(ch)}::jsonb)::text where slug = '{a['slug']}';")
    e = ARTICLE_EN
    head = {k: e[k] for k in ('title', 'excerpt', 'seo_title', 'seo_description')}
    head['content'] = json.dumps({'time': 1792700000000, 'version': '2.29.1', 'blocks': []})
    out.append(f"update public.hw_articles set en = {q(head)}::jsonb where slug = '{a['slug']}';")
    for ch in chunks(doc(e['blocks']), 4):
        out.append(f"update public.hw_articles set en = jsonb_set(en, '{{content}}', to_jsonb(jsonb_set((en->>'content')::jsonb, '{{blocks}}', ((en->>'content')::jsonb->'blocks') || {q(ch)}::jsonb)::text)) where slug = '{a['slug']}';")
    return out

if __name__ == '__main__':
    for i, s in enumerate(sql()):
        print(f'-- [{i}] {len(s)} chars\n{s}\n')

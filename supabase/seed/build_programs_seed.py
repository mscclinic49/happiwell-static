"""สร้างไฟล์ SQL ข้อมูลโปรแกรมเริ่มต้น (ราคาอ้างอิงจากบทความบนเว็บ + ราคาที่คลินิกยืนยัน 21 ต.ค. 2569)

รัน: python3 supabase/seed/build_programs_seed.py
ได้: supabase/seed/programs_seed.sql (วางใน Supabase SQL Editor ต่อจาก migration)
     supabase/seed/programs_seed.json (ใช้ทดสอบในเครื่อง)
หลังจากนี้ให้แก้ข้อมูลผ่านหน้าแอดมิน /admin-programs.html แทนการแก้ไฟล์นี้
"""
import json, pathlib, time

VACCINE_INCLUDES = [
    'ซักประวัติและประเมินความเหมาะสมโดยแพทย์ก่อนฉีด',
    'ค่าวัคซีนและค่าฉีด',
    'สังเกตอาการหลังฉีดที่คลินิก',
]


def blocks(*paras):
    """ข้อความหลายย่อหน้า → Editor.js JSON"""
    out = []
    for i, p in enumerate(paras):
        if p.startswith('## '):
            out.append({'id': f'b{i}', 'type': 'header', 'data': {'text': p[3:], 'level': 2}})
        else:
            out.append({'id': f'b{i}', 'type': 'paragraph', 'data': {'text': p}})
    return json.dumps({'time': int(time.time() * 1000), 'blocks': out, 'version': '2.29.1'}, ensure_ascii=False)


P = []
def add(**kw):
    kw.setdefault('sort_order', len(P) + 1)
    kw.setdefault('is_published', True)
    P.append(kw)

# ---------------- วัคซีน ----------------
add(slug='flu-vaccine', category='vaccine', name='วัคซีนไข้หวัดใหญ่ 4 สายพันธุ์',
    short_desc='ฉีดปีละ 1 เข็ม สำหรับผู้ใหญ่และเด็กอายุ 9 ปีขึ้นไป แพทย์ประเมินก่อนฉีดทุกครั้ง',
    price=390, price_unit='ต่อเข็ม', is_featured=True, related_article_slug='flu-vaccine-2569',
    description=blocks(
        'วัคซีนไข้หวัดใหญ่ชนิด 4 สายพันธุ์ แนะนำให้ฉีดเป็นประจำทุกปี เพราะภูมิคุ้มกันจากวัคซีนจะค่อย ๆ ลดลง และสายพันธุ์ที่ระบาดเปลี่ยนไปทุกปี',
        'ผู้ใหญ่และเด็กอายุ 9 ปีขึ้นไปฉีดปีละ 1 เข็ม ส่วนเด็กอายุต่ำกว่า 9 ปีที่ฉีดครั้งแรก อาจต้องฉีด 2 เข็มห่างกันอย่างน้อย 4 สัปดาห์ตามดุลยพินิจของแพทย์'),
    suitable_for=['ทุกคนอายุ 6 เดือนขึ้นไป', 'ผู้สูงอายุ 65 ปีขึ้นไป', 'หญิงตั้งครรภ์ (ฉีดได้ทุกไตรมาส)', 'ผู้มีโรคประจำตัว เช่น เบาหวาน โรคหัวใจ โรคปอด'],
    includes=VACCINE_INCLUDES,
    precautions=['หากมีไข้หรือป่วยเฉียบพลัน แพทย์อาจแนะนำให้เลื่อนฉีด', 'แจ้งแพทย์หากเคยแพ้วัคซีนหรือส่วนประกอบของวัคซีน'],
    tags=['วัคซีน', 'ไข้หวัดใหญ่'])

add(slug='dengue-vaccine-qdenga', category='vaccine', name='วัคซีนไข้เลือดออก (Qdenga)',
    short_desc='ฉีด 2 เข็ม ห่างกัน 3 เดือน สำหรับผู้มีอายุ 4 ปีขึ้นไป แบ่งจ่ายรายเข็มได้',
    price=1800, price_unit='ต่อเข็ม', price_note='จองคอร์ส 2 เข็ม 3,450 บาท', is_featured=True,
    brand='Qdenga (TAK-003) — Takeda', related_article_slug='dengue-vaccine-2569',
    options=[{'label': 'วัคซีน 1 เข็ม (แบ่งจ่ายรายเข็ม)', 'price': 1800, 'note': 'ฉีดทั้งหมด 2 เข็ม ห่างกัน 3 เดือน'},
             {'label': 'คอร์ส 2 เข็ม', 'price': 3450, 'note': 'ชำระครั้งเดียวครบทั้งคอร์ส'}],
    description=blocks(
        'วัคซีน Qdenga (TAK-003) เป็นวัคซีนป้องกันโรคไข้เลือดออกที่ใช้กันแพร่หลายในไทย ขึ้นทะเบียนใช้ในผู้ที่มีอายุตั้งแต่ 4 ปีขึ้นไป',
        'ฉีดทั้งหมด 2 เข็ม ห่างกัน 3 เดือน หากเข็มที่สองล่าช้ากว่ากำหนดไม่จำเป็นต้องเริ่มนับหนึ่งใหม่ ฉีดต่อได้เลยเมื่อมีโอกาส'),
    suitable_for=['ผู้มีอายุ 4 ปีขึ้นไป', 'ผู้ที่อาศัยหรือทำงานในพื้นที่ที่มีการระบาด', 'ผู้ที่เคยเป็นไข้เลือดออกมาก่อน (ตามคำแนะนำแพทย์)'],
    includes=VACCINE_INCLUDES,
    precautions=['ผู้ที่ตั้งครรภ์ ให้นมบุตร หรือมีภูมิคุ้มกันบกพร่อง ควรปรึกษาแพทย์ก่อนฉีด', 'หากมีไข้สูงเฉียบพลันช่วงที่มีการระบาด ควรพบแพทย์ ไม่ควรซื้อยาแก้ปวดกลุ่ม NSAIDs กินเอง'],
    duration='2 เข็ม ห่างกัน 3 เดือน', tags=['วัคซีน', 'ไข้เลือดออก'])

add(slug='pneumococcal-vaccine-prevnar-20', category='vaccine', name='วัคซีนปอดอักเสบ (Prevnar 20)',
    short_desc='ผู้ใหญ่ที่ไม่เคยฉีดวัคซีนไอพีดีมาก่อน ฉีดเพียง 1 เข็ม',
    price=3000, price_unit='ต่อเข็ม', brand='Prevnar 20 (PCV20)', related_article_slug='pneumonia-vaccine-2569',
    description=blocks(
        'วัคซีน Prevnar 20 ป้องกันการติดเชื้อนิวโมคอคคัส (ไอพีดี) ซึ่งเป็นสาเหตุสำคัญของปอดอักเสบ ติดเชื้อในกระแสเลือด และเยื่อหุ้มสมองอักเสบ',
        'สำหรับผู้ใหญ่ทั่วไปที่ไม่เคยฉีดวัคซีนไอพีดีมาก่อน ฉีด Prevnar 20 เพียง 1 เข็ม'),
    suitable_for=['ผู้สูงอายุ 65 ปีขึ้นไป', 'ผู้มีโรคเรื้อรังหรือภูมิคุ้มกันบกพร่อง ไม่ว่าอายุเท่าไหร่', 'ผู้ใหญ่ทั่วไปที่ต้องการป้องกัน'],
    includes=VACCINE_INCLUDES,
    precautions=['แจ้งแพทย์หากเคยฉีดวัคซีนไอพีดีชนิดอื่นมาก่อน เพื่อวางแผนการฉีดให้เหมาะสม'],
    duration='1 เข็ม', tags=['วัคซีน', 'ปอดอักเสบ', 'ผู้สูงอายุ'])

add(slug='rsv-vaccine-abrysvo', category='vaccine', name='วัคซีน RSV (Abrysvo)',
    short_desc='ฉีด 1 เข็ม สำหรับผู้ใหญ่อายุ 60 ปีขึ้นไป และหญิงตั้งครรภ์อายุครรภ์ 24–36 สัปดาห์',
    price=7200, price_unit='ต่อเข็ม', brand='Abrysvo', related_article_slug='rsv-vaccine-2569',
    description=blocks(
        'RSV เป็นไวรัสทางเดินหายใจที่อาจทำให้เกิดอาการรุนแรงในผู้สูงอายุ ผู้มีโรคเรื้อรัง และทารก วัคซีน Abrysvo ครอบคลุมไวรัส RSV ทั้งสายพันธุ์ย่อย A และ B',
        'วัคซีน RSV ฉีดเพียง 1 เข็ม ไม่ต้องฉีดซ้ำทุกปีเหมือนวัคซีนไข้หวัดใหญ่'),
    suitable_for=['ผู้ใหญ่อายุ 60 ปีขึ้นไป', 'ผู้ใหญ่อายุ 50–59 ปีที่มีโรคปอด โรคหัวใจ หรือโรคเรื้อรัง', 'หญิงตั้งครรภ์อายุครรภ์ 24–36 สัปดาห์ เพื่อป้องกันทารกแรกเกิด'],
    includes=VACCINE_INCLUDES,
    precautions=['หญิงตั้งครรภ์ควรฉีดตามช่วงอายุครรภ์ที่แพทย์แนะนำ'],
    duration='1 เข็ม', tags=['วัคซีน', 'RSV', 'ผู้สูงอายุ'])

add(slug='hepatitis-a-b-vaccine', category='vaccine', name='วัคซีนรวมตับอักเสบเอและบี',
    short_desc='ป้องกันได้ทั้งไวรัสตับอักเสบเอและบีในเข็มเดียวกัน คอร์สครบ 3 เข็ม',
    price=1500, price_unit='คอร์ส 3 เข็ม', related_article_slug='hepatitis-ab-vaccine-2569',
    description=blocks(
        'วัคซีนรวมที่ป้องกันได้ทั้งไวรัสตับอักเสบเอและบีในเข็มเดียวกัน ฉีดตามตารางมาตรฐาน 3 เข็ม ที่ 0, 1 และ 6 เดือน',
        'สำหรับผู้ที่ต้องการภูมิคุ้มกันเร็วขึ้น เช่น ก่อนเดินทาง แพทย์อาจพิจารณาตารางฉีดแบบเร่งด่วนเป็นกรณีไป หากฉีดไม่ครบตามนัด ไม่ต้องเริ่มนับหนึ่งใหม่'),
    suitable_for=['ผู้ที่ยังไม่มีภูมิคุ้มกันต่อไวรัสตับอักเสบเอและบี', 'ผู้ที่วางแผนเดินทาง'],
    includes=['ซักประวัติและประเมินความเหมาะสมโดยแพทย์ก่อนฉีด', 'ค่าวัคซีนและค่าฉีดครบ 3 เข็ม', 'นัดหมายเข็มถัดไป'],
    precautions=['ผู้ที่ตั้งครรภ์ควรปรึกษาแพทย์ก่อนฉีด'],
    duration='3 เข็ม (เดือนที่ 0, 1, 6)', tags=['วัคซีน', 'ตับอักเสบ'])

add(slug='hpv-vaccine-gardasil-9', category='vaccine', name='วัคซีน HPV (Gardasil 9)',
    short_desc='วัคซีนป้องกันเชื้อไวรัส HPV 9 สายพันธุ์ จำนวนเข็มขึ้นกับอายุ แพทย์จะแนะนำตารางฉีดที่เหมาะสม',
    price=5500, price_unit='ต่อเข็ม', brand='Gardasil 9',
    description=blocks(
        'วัคซีน Gardasil 9 ป้องกันการติดเชื้อไวรัส HPV 9 สายพันธุ์ ซึ่งเกี่ยวข้องกับมะเร็งปากมดลูกและโรคอื่น ๆ ที่เกิดจากเชื้อ HPV',
        'จำนวนเข็มและระยะห่างขึ้นกับอายุที่เริ่มฉีด แพทย์จะประเมินและแนะนำตารางฉีดที่เหมาะสมกับแต่ละคน'),
    suitable_for=['ผู้หญิงและผู้ชายตามช่วงอายุที่แพทย์แนะนำ'],
    includes=VACCINE_INCLUDES,
    precautions=['ผู้ที่ตั้งครรภ์ควรปรึกษาแพทย์ก่อนฉีด'],
    tags=['วัคซีน', 'HPV'])

add(slug='rabies-vaccine', category='vaccine', name='วัคซีนพิษสุนัขบ้า',
    short_desc='โดนหมา/แมวกัดหรือข่วน แพทย์ประเมินแผลและฉีดวัคซีนตามตารางมาตรฐาน',
    price=390, price_unit='ต่อเข็ม', price_note='ค่าทำแผล/ล้างแผล 50 บาท และค่าเย็บแผล (กรณีจำเป็น) 50 บาทต่อเข็ม คิดแยก',
    related_article_slug='rabies-vaccine-2569',
    options=[{'label': 'วัคซีนพิษสุนัขบ้า', 'price': 390, 'note': 'ต่อเข็ม'},
             {'label': 'ทำแผล / ล้างแผล', 'price': 50, 'note': 'ต่อครั้ง'},
             {'label': 'เย็บแผล (กรณีจำเป็น)', 'price': 50, 'note': 'ต่อเข็ม'}],
    description=blocks(
        'หลังโดนสัตว์กัดหรือข่วน ให้ล้างแผลด้วยน้ำสะอาดและสบู่ทันทีอย่างน้อย 15 นาที แล้วรีบพบแพทย์เพื่อประเมินความเสี่ยงของแผล',
        'ผู้ที่ไม่เคยฉีดวัคซีนมาก่อน แพทย์จะฉีดตามตารางมาตรฐานวันที่ 0, 3, 7 และ 14 (บางกรณีอาจนัดเพิ่มวันที่ 28) ส่วนผู้ที่เคยฉีดป้องกันไว้แล้วมักฉีดกระตุ้นเพียง 2 เข็ม ต้องฉีดให้ครบตามนัด'),
    suitable_for=['ผู้ที่โดนหมา แมว หรือสัตว์เลี้ยงลูกด้วยนมกัด ข่วน หรือเลียแผล'],
    includes=['ประเมินแผลโดยแพทย์', 'ค่าวัคซีนและค่าฉีด', 'นัดหมายเข็มถัดไป'],
    precautions=['ห้ามหยุดฉีดกลางคันแม้แผลจะหายดีแล้ว', 'หญิงตั้งครรภ์ฉีดได้ เพราะโรคนี้อันตรายถึงชีวิต'],
    duration='4 เข็ม (วันที่ 0, 3, 7, 14) หรือตามแพทย์นัด', tags=['วัคซีน', 'พิษสุนัขบ้า', 'สัตว์กัด'])

# ---------------- ตรวจสุขภาพ ----------------
add(slug='annual-health-checkup', category='checkup', name='แพ็กเกจตรวจสุขภาพประจำปี',
    short_desc='เลือกได้ 3 ชุด ตรวจครบที่คลินิก พร้อมแพทย์อ่านผลและให้คำแนะนำ',
    price=999, price_unit='เริ่มต้น', is_featured=True,
    options=[{'label': 'ชุดเล็ก', 'price': 999, 'note': ''},
             {'label': 'ชุดใหญ่ (ผู้หญิง)', 'price': 1300, 'note': ''},
             {'label': 'ชุดใหญ่ (ผู้ชาย)', 'price': 1399, 'note': ''}],
    description=blocks(
        'แพ็กเกจตรวจสุขภาพประจำปีที่ HappiWell คลินิกเวชกรรม เลือกได้ตามช่วงอายุและความต้องการ พร้อมแพทย์อ่านผลและให้คำแนะนำการดูแลสุขภาพ',
        'สอบถามรายการตรวจในแต่ละชุดได้ทาง LINE @p49clinic'),
    includes=['แพทย์อ่านผลและให้คำแนะนำ'],
    precautions=['บางรายการต้องงดน้ำและอาหารก่อนตรวจ เจ้าหน้าที่จะแจ้งเมื่อนัดหมาย'],
    tags=['ตรวจสุขภาพ'])

add(slug='lab-test-single', category='checkup', name='ตรวจเลือด / ตรวจแล็บรายการเดี่ยว',
    short_desc='เลือกตรวจเฉพาะรายการที่ต้องการ เช่น น้ำตาล ไขมัน การทำงานของไต',
    price=100, price_unit='เริ่มต้นต่อรายการ', price_note='บางรายการราคามากกว่านี้ สอบถามราคาแต่ละรายการได้ทาง LINE',
    description=blocks('เลือกตรวจเลือดหรือตรวจแล็บเฉพาะรายการที่ต้องการ เหมาะกับผู้ที่ต้องการติดตามค่าบางตัว เช่น ผู้ป่วยโรคเรื้อรัง'),
    includes=['แพทย์อ่านผลและให้คำแนะนำ'],
    precautions=['บางรายการต้องงดน้ำและอาหารก่อนตรวจ'],
    tags=['ตรวจสุขภาพ', 'ตรวจเลือด'])

# ---------------- คุมกำเนิด ----------------
add(slug='contraceptive-injection-3-month', category='family-planning', name='ฉีดยาคุมกำเนิด 3 เดือน (DMPA)',
    short_desc='ฉีดครั้งเดียวคุมกำเนิดได้นาน 3 เดือน แพทย์ให้คำปรึกษาก่อนฉีดทุกครั้ง',
    price=100, price_unit='ต่อเข็ม', related_article_slug='contraception-injection-2569',
    description=blocks(
        'ยาฉีดคุมกำเนิด DMPA แบบ 3 เดือน ฉีดครั้งเดียวคุมกำเนิดได้นาน 3 เดือน เหมาะกับคนที่ไม่สะดวกกินยาคุมทุกวัน',
        'ข้อควรรู้คือประจำเดือนอาจมาไม่ปกติหรือหายไปช่วงที่ใช้ และหลังหยุดฉีดอาจต้องรอสักระยะกว่าจะกลับมามีบุตรได้ตามปกติ'),
    suitable_for=['คนที่ไม่สะดวกกินยาคุมทุกวัน', 'คนที่มีผลข้างเคียงจากยาคุมชนิดฮอร์โมนรวม'],
    includes=['คำปรึกษาจากแพทย์ก่อนฉีด', 'ค่ายาและค่าฉีด'],
    precautions=['ยาฉีดคุมกำเนิดไม่ป้องกันโรคติดต่อทางเพศสัมพันธ์'],
    duration='คุมกำเนิดได้ 3 เดือน', tags=['คุมกำเนิด'])

add(slug='contraceptive-injection-monthly', category='family-planning', name='ฉีดยาคุมกำเนิดรายเดือน',
    short_desc='ยาฉีดฮอร์โมนรวม ฉีดทุกเดือน รอบเดือนมาสม่ำเสมอกว่ายาฉีด 3 เดือน',
    price=250, price_unit='ต่อเข็ม', related_article_slug='monthly-contraceptive-injection-2569',
    description=blocks(
        'ยาฉีดคุมกำเนิดรายเดือนเป็นทางเลือกสำหรับคนที่เคยใช้ยาฉีด 3 เดือนแล้วมีปัญหาประจำเดือนมาไม่ปกติ',
        'ต้องมาฉีดที่คลินิกทุกเดือน หากไม่สะดวกมาบ่อย ยาฉีด 3 เดือนอาจเหมาะกว่า ปรึกษาแพทย์เพื่อเลือกวิธีที่เหมาะกับตัวเอง'),
    suitable_for=['คนที่ใช้ยาฉีด 3 เดือนแล้วประจำเดือนมาไม่ปกติ', 'คนที่ต้องการรอบเดือนสม่ำเสมอ', 'คนที่สะดวกมาคลินิกทุกเดือน'],
    includes=['คำปรึกษาจากแพทย์ก่อนฉีด', 'ค่ายาและค่าฉีด'],
    precautions=['ยาฉีดคุมกำเนิดไม่ป้องกันโรคติดต่อทางเพศสัมพันธ์'],
    duration='ฉีดทุกเดือน', tags=['คุมกำเนิด'])

# ---------------- หัตถการ ----------------
add(slug='nebulizer', category='procedure', name='พ่นยาขยายหลอดลม (Nebulizer)',
    short_desc='บรรเทาอาการหอบเหนื่อยจากหอบหืดหรือภูมิแพ้ทางเดินหายใจ',
    price=200, price_unit='ต่อครั้ง', price_note='ค่าหน้ากากพ่นยา 200 บาท ซื้อครั้งแรกครั้งเดียว ใช้ซ้ำได้ทุกครั้งถัดไป',
    related_article_slug='asthma-respiratory-allergy-2569',
    options=[{'label': 'พ่นยา', 'price': 200, 'note': 'ต่อครั้ง'},
             {'label': 'พ่นยา + หน้ากากพ่นยา (ครั้งแรก)', 'price': 400, 'note': 'หน้ากากใช้ซ้ำได้ทุกครั้งถัดไป'}],
    description=blocks('การพ่นยาด้วยเครื่องเนบูไลเซอร์เปลี่ยนยาน้ำให้เป็นละอองฝอยละเอียด เพื่อให้ยาเข้าสู่ทางเดินหายใจโดยตรง ช่วยขยายหลอดลมและบรรเทาอาการหอบเหนื่อย เหมาะกับเด็กเล็กหรือผู้ที่ไม่สะดวกใช้ยาพ่นชนิดสูดเอง'),
    includes=['ประเมินอาการโดยแพทย์', 'ค่ายาพ่น'],
    precautions=['หากหายใจลำบากมาก ริมฝีปากเขียว หรือพูดไม่เป็นประโยค ให้ไปโรงพยาบาลทันทีหรือโทร 1669'],
    tags=['หอบหืด', 'ภูมิแพ้'])

add(slug='wound-care', category='procedure', name='ทำแผล / เย็บแผล',
    short_desc='ล้างแผล ทำแผลสด แผลผ่าตัด และเย็บแผลโดยแพทย์',
    price=50, price_unit='เริ่มต้น',
    options=[{'label': 'ทำแผล / ล้างแผล', 'price': 50, 'note': 'ต่อครั้ง'},
             {'label': 'เย็บแผล', 'price': 50, 'note': 'ต่อเข็ม'}],
    description=blocks('ทำแผลสด แผลผ่าตัด และเย็บแผลโดยแพทย์ พร้อมติดตามอาการจนแผลหาย กรณีแผลเกินขีดความสามารถของคลินิก แพทย์จะส่งต่อโรงพยาบาล'),
    includes=['ประเมินแผลโดยแพทย์'],
    precautions=['แผลลึก เลือดออกไม่หยุด หรือมีสิ่งแปลกปลอมในแผล ควรไปโรงพยาบาล'],
    tags=['ทำแผล'])

# ---------------- ใบรับรองแพทย์ ----------------
add(slug='medical-certificate', category='certificate', name='ใบรับรองแพทย์ 5 โรค + ตรวจสารเสพติด',
    short_desc='สำหรับสมัครงาน ใบขับขี่ และเอกสารราชการ',
    price=250, price_unit='ต่อฉบับ',
    description=blocks('ออกใบรับรองแพทย์ 5 โรค พร้อมตรวจสารเสพติด สำหรับสมัครงาน ทำใบขับขี่ และเอกสารที่ต้องใช้ใบรับรองแพทย์'),
    includes=['ตรวจร่างกายโดยแพทย์', 'ตรวจสารเสพติด', 'ใบรับรองแพทย์'],
    precautions=['นำบัตรประชาชนมาด้วย'],
    tags=['ใบรับรองแพทย์'])

# ---------------- สุขภาพทางเพศ ----------------
add(slug='pep-prep', category='sexual-health', name='PEP / PrEP ยาป้องกันเอชไอวี',
    short_desc='ให้คำปรึกษาเป็นความลับ ต้องนัดหมายทาง LINE ก่อนเข้ารับบริการ',
    price=None, price_note='สอบถามค่ายาทาง LINE @p49clinic', related_article_slug='pep-prep-2569',
    description=blocks('บริการ PEP (ยาต้านไวรัสหลังสัมผัสเชื้อ) และ PrEP (ยาป้องกันก่อนสัมผัสเชื้อ) พร้อมคำปรึกษาเป็นความลับ กรุณาทัก LINE เพื่อนัดหมายก่อนเข้ารับบริการทุกครั้ง'),
    includes=['คำปรึกษาจากแพทย์เป็นความลับ'],
    precautions=['PEP ควรเริ่มยาโดยเร็วที่สุดหลังสัมผัสเชื้อ'],
    tags=['สุขภาพทางเพศ', 'HIV'])


def sql_str(v):
    if v is None:
        return 'null'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return 'array[' + ','.join(sql_str(x) for x in v) + ']::text[]' if v else "'{}'::text[]"
    return "'" + str(v).replace("'", "''") + "'"


COLS = ['slug', 'category', 'name', 'short_desc', 'description', 'price', 'price_unit', 'price_note', 'options',
        'suitable_for', 'includes', 'precautions', 'duration', 'brand', 'related_article_slug', 'tags',
        'sort_order', 'is_featured', 'is_published']
rows = []
for p in P:
    vals = []
    for c in COLS:
        v = p.get(c, [] if c in ('suitable_for', 'includes', 'precautions', 'tags') else (False if c == 'is_featured' else None))
        if c == 'options':
            vals.append(sql_str(json.dumps(p.get('options', []), ensure_ascii=False)) + '::jsonb')
        else:
            vals.append(sql_str(v))
    rows.append('(' + ', '.join(vals) + ')')

here = pathlib.Path(__file__).parent
(here / 'programs_seed.sql').write_text(
    '-- ข้อมูลโปรแกรมเริ่มต้น (สร้างจาก build_programs_seed.py) รันครั้งเดียวต่อจาก migration\n'
    f'insert into public.hw_programs ({", ".join(COLS)}) values\n' + ',\n'.join(rows) +
    '\non conflict (slug) do nothing;\n', encoding='utf-8')

# JSON สำหรับทดสอบในเครื่อง (รูปแบบเดียวกับที่ PostgREST ส่งกลับ)
now = '2026-10-21T00:00:00+00:00'
js = []
for i, p in enumerate(P):
    r = {c: p.get(c) for c in COLS}
    for c in ('suitable_for', 'includes', 'precautions', 'tags'):
        r[c] = r[c] or []
    r['options'] = p.get('options', [])
    r['is_featured'] = bool(p.get('is_featured'))
    r.update(id=f'00000000-0000-0000-0000-{i:012d}', fda_reg_no=None, cover_image=None, seo_title=None,
             seo_description=None, created_at=now, updated_at=now)
    js.append(r)
(here / 'programs_seed.json').write_text(json.dumps(js, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(P), 'programs')

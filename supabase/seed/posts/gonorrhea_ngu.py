# -*- coding: utf-8 -*-
"""บทความ: หนองในแท้ vs หนองในเทียม + หน้าราคาฉีดยา Ceftriaxone (Cef-3) 150 บาท
รัน: python3 supabase/seed/posts/gonorrhea_ngu.py → เขียน gonorrhea_ngu.json (article th/en + program th/en/my)
"""
import json, pathlib

SLUG = 'gonorrhea-vs-non-gonococcal-urethritis-2569'
PSLUG = 'ceftriaxone-injection'
LINE = 'https://line.me/R/ti/p/@p49clinic'
STD = '/programs/std-screening'
CEF = '/programs/' + PSLUG
REF = [
  '<a href="https://www.cdc.gov/std/treatment-guidelines/gonorrhea-adults.htm">CDC – STI Treatment Guidelines: Gonococcal Infections Among Adolescents and Adults</a>',
  '<a href="https://www.cdc.gov/std/treatment-guidelines/urethritis-and-cervicitis.htm">CDC – STI Treatment Guidelines: Urethritis and Cervicitis</a>',
  '<a href="https://www.who.int/news-room/fact-sheets/detail/gonorrhoea-(neisseria-gonorrhoeae-infection)">WHO – Gonorrhoea (Neisseria gonorrhoeae infection)</a>',
]


def blocks(items, pre, t=1793600000000):
    out = []
    for i, (kind, val) in enumerate(items):
        bid = f'{pre}{i}'
        if kind == 'p':
            out.append({'id': bid, 'type': 'paragraph', 'data': {'text': val}})
        elif kind in ('h2', 'h3'):
            out.append({'id': bid, 'type': 'header', 'data': {'text': val, 'level': int(kind[1])}})
        elif kind == 'ul':
            out.append({'id': bid, 'type': 'list', 'data': {'style': 'unordered', 'items': val}})
    return json.dumps({'time': t, 'version': '2.29.1', 'blocks': out}, ensure_ascii=False)


TH = dict(
  title='หนองในแท้ กับ หนองในเทียม ต่างกันยังไง อาการ การตรวจเชื้อ และการรักษา (อัปเดตปี 2569)',
  excerpt='หนองในแท้และหนองในเทียมมีอาการคล้ายกันมาก แยกด้วยตาเปล่าไม่ได้ ต้องตรวจเชื้อ รักษาได้ที่แฮปปี้เวลล์ คลินิก ทุ่งครุ มีบริการตรวจเชื้อและยาฉีด Ceftriaxone',
  seo_title='หนองในแท้ หนองในเทียม ต่างกันยังไง อาการ ตรวจเชื้อ รักษา ทุ่งครุ | HappiWell',
  seo_description='หนองในแท้ vs หนองในเทียม อาการเหมือนกันแต่เชื้อและการรักษาต่างกัน ตรวจเชื้อและรักษาเป็นความลับ มียาฉีด Ceftriaxone 150 บาท ที่แฮปปี้เวลล์ คลินิกเวชกรรม ทุ่งครุ',
  tags=['สุขภาพทางเพศ', 'หนองใน', 'โรคติดต่อทางเพศสัมพันธ์'],
  content=blocks([
    ('p', 'ปัสสาวะแสบ มีหนองหรือของเหลวไหลออกจากปลายท่อปัสสาวะ หลายคนเรียกว่า "หนองใน" แต่จริง ๆ แล้วมีทั้ง <b>หนองในแท้</b> และ <b>หนองในเทียม</b> ซึ่งเกิดจากเชื้อคนละชนิด และการรักษาก็ไม่เหมือนกัน บทความนี้อธิบายความต่างแบบเข้าใจง่าย'),
    ('h2', 'สรุปสั้น ๆ'),
    ('ul', ['<b>หนองในแท้</b> เกิดจากเชื้อแบคทีเรีย <i>Neisseria gonorrhoeae</i>',
            '<b>หนองในเทียม</b> (ท่อปัสสาวะอักเสบที่ไม่ใช่หนองในแท้) เกิดจากเชื้ออื่น เช่น คลามิเดีย (<i>Chlamydia trachomatis</i>) หรือ <i>Mycoplasma genitalium</i> พบบ่อยกว่าที่คนทั่วไปคิด',
            'อาการสองแบบ <b>คล้ายกันมาก แยกด้วยตาเปล่าไม่ได้</b> ต้องตรวจเชื้อจึงรู้แน่ชัด',
            'ทั้งสองแบบ <b>รักษาได้</b> แต่ต้องใช้ยาให้ตรงกับเชื้อ และอาจติดพร้อมกันได้']),
    ('h2', 'อาการที่พบบ่อย'),
    ('ul', ['ปัสสาวะแสบ ขัด หรือปวดเวลาปัสสาวะ',
            'มีหนองหรือของเหลวไหลออกจากปลายท่อปัสสาวะ หนองในแท้มักเป็นหนองข้นสีเหลืองหรือเขียว ส่วนหนองในเทียมมักเป็นสีขาวขุ่นหรือใส และอาการเบากว่า แต่ไม่ใช่กฎตายตัว',
            'อาการมักเริ่มภายใน 2–7 วันหลังสัมผัสเชื้อสำหรับหนองในแท้ และอาจช้ากว่านั้นสำหรับหนองในเทียม',
            'ผู้หญิงหลายคน <b>ไม่มีอาการเลย</b> หรือมีเพียงตกขาวผิดปกติ ปัสสาวะแสบ หรือปวดท้องน้อย',
            'การติดเชื้อที่คอหรือทวารหนักมักไม่มีอาการ แต่แพร่เชื้อให้คนอื่นได้']),
    ('p', 'บางคนไม่มีอาการเลยแต่ยังแพร่เชื้อได้ ถ้าเสี่ยงมา แม้ไม่มีอาการก็ควรตรวจ'),
    ('h2', 'ทำไมต้องตรวจเชื้อ ซื้อยากินเองได้ไหม'),
    ('ul', ['หนองในแท้และหนองในเทียมใช้ยาคนละกลุ่ม ถ้าเดาเอง ยาอาจไม่ตรงกับเชื้อ อาการดูเหมือนดีขึ้นแต่เชื้อยังอยู่',
            'เชื้อหนองในแท้ดื้อยาเพิ่มขึ้นทั่วโลก การกินยาเองในขนาดหรือระยะเวลาที่ไม่เหมาะสมทำให้ดื้อยามากขึ้น',
            'สองโรคนี้ติดพร้อมกันได้ แพทย์จึงมักวางแผนรักษาให้ครอบคลุมตามผลตรวจและประวัติเสี่ยง',
            'การตรวจเชื้อช่วยให้ทราบว่าควรตรวจโรคติดต่อทางเพศสัมพันธ์อื่นร่วมด้วยหรือไม่ เช่น เอชไอวี ซิฟิลิส']),
    ('h2', 'ที่แฮปปี้เวลล์ คลินิก ทำอะไรให้บ้าง'),
    ('ul', [f'<b>ตรวจเชื้อ</b>: แพทย์ซักประวัติ ตรวจร่างกาย และส่งตรวจเชื้อตามความเหมาะสม ดูรายละเอียดที่ <a href="{STD}">หน้าตรวจคัดกรองโรคติดต่อทางเพศสัมพันธ์</a>',
            f'<b>รักษา</b>: ถ้าแพทย์วินิจฉัยหนองในแท้ ยาหลักคือยาฉีดปฏิชีวนะ Ceftriaxone (Cef-3) ฉีดครั้งเดียว แพทย์อาจให้ยากินร่วมด้วยตามผลตรวจ ดูราคาที่ <a href="{CEF}">หน้าฉีดยา Ceftriaxone</a>',
            'หนองในเทียม แพทย์มักให้ยากินปฏิชีวนะตามชนิดเชื้อที่สงสัยหรือตรวจพบ',
            'ถุงยางอนามัยฟรี มีทุกขนาด']),
    ('p', '<b>ข้อมูลของคุณเป็นความลับ</b> การมารับบริการและผลตรวจเป็นความลับ ผู้ที่ตอบคำถามทั้งทาง LINE และที่คลินิกคือแพทย์และพยาบาลเท่านั้น'),
    ('h2', 'หลังรักษาต้องทำอะไรต่อ'),
    ('ul', ['กินยาให้ครบตามแพทย์สั่ง แม้อาการหายแล้ว',
            'งดมีเพศสัมพันธ์จนกว่าจะรักษาครบและอาการหาย โดยทั่วไปอย่างน้อย 7 วันหลังได้รับยา',
            '<b>คู่นอนควรมาตรวจและรักษาพร้อมกัน</b> ไม่เช่นนั้นจะติดกลับไปกลับมา',
            'ถ้าอาการไม่ดีขึ้นใน 3–5 วัน หรือกลับมาเป็นอีก ให้มาพบแพทย์อีกครั้ง',
            'แพทย์อาจแนะนำให้ตรวจ HIV ซิฟิลิส และโรคอื่นร่วมด้วย',
            'ใช้ถุงยางอนามัยทุกครั้งเพื่อป้องกันการติดเชื้อซ้ำ']),
    ('h2', 'ถ้าไม่รักษา จะเกิดอะไรขึ้น'),
    ('ul', ['ผู้ชาย: อัณฑะหรือท่อนเก็บอสุจิอักเสบ ต่อมลูกหมากอักเสบ ท่อปัสสาวะตีบ',
            'ผู้หญิง: การอักเสบในอุ้งเชิงกราน ท่อนำไข่ตัน เสี่ยงมีบุตรยากและท้องนอกมดลูก',
            'เชื้ออาจเข้ากระแสเลือดหรือข้อได้ในบางราย และการมีโรคติดต่อทางเพศสัมพันธ์เพิ่มโอกาสติดเอชไอวี',
            'หญิงตั้งครรภ์ที่ติดเชื้ออาจแพร่เชื้อสู่ทารกตอนคลอด']),
    ('h2', 'ราคาที่แฮปปี้เวลล์ คลินิก'),
    ('ul', [f'<a href="{CEF}">ฉีดยา Ceftriaxone (Cef-3)</a>: <b>150 บาทต่อครั้ง</b>',
            f'ตรวจเชื้อ: สอบถามรายการตรวจและราคาที่ <a href="{LINE}">LINE @p49clinic</a> หรือดู <a href="{STD}">หน้าตรวจคัดกรองโรคติดต่อทางเพศสัมพันธ์</a>']),
    ('p', 'ราคายังไม่รวมค่าบริการทางการแพทย์ แพทย์ซักประวัติและประเมินก่อนให้ยาทุกครั้ง'),
    ('p', f'ต้องการปรึกษาหรือนัดหมาย <a href="{LINE}">ทัก LINE @p49clinic</a> ได้เลย เปิดทุกวัน จันทร์–ศุกร์ 08:00–18:00 น. เสาร์–อาทิตย์ 08:00–12:00 น.'),
    ('h2', 'คำถามที่พบบ่อย'),
    ('p', '<b>หนองในแท้กับหนองในเทียมดูออกเองได้ไหม</b><br>ไม่ได้ อาการคล้ายกันมาก ต้องให้แพทย์ตรวจและส่งตรวจเชื้อ'),
    ('p', '<b>ฉีดยาเข็มเดียวหายเลยไหม</b><br>หนองในแท้มักตอบสนองดีต่อยาฉีด Ceftriaxone ครั้งเดียว แต่แพทย์จะประเมินว่าต้องให้ยาอื่นร่วมด้วยหรือไม่ และอาจนัดติดตามอาการ'),
    ('p', '<b>เป็นแล้วหายเองได้ไหม</b><br>ไม่ควรรอ แม้อาการเบาลงเชื้ออาจยังอยู่และแพร่ต่อหรือทำให้เกิดภาวะแทรกซ้อน'),
    ('p', '<b>ถ้าแพ้ยาปฏิชีวนะต้องบอกไหม</b><br>ต้องบอกแพทย์ทุกครั้ง โดยเฉพาะแพ้เพนิซิลลินหรือยากลุ่มเซฟาโลสปอริน'),
    ('h3', 'แหล่งอ้างอิง'),
    ('ul', REF),
    ('p', '<i>บทความนี้จัดทำเพื่อให้ข้อมูลทั่วไป ไม่ใช่คำแนะนำทางการแพทย์เฉพาะบุคคล หากมีอาการควรพบแพทย์เพื่อตรวจและรักษา</i>'),
  ], 'gn'))

EN = dict(
  title='Gonorrhoea vs Non-Gonococcal Urethritis ("True" vs "False" Gonorrhoea): Symptoms, Testing and Treatment (2026 Update)',
  excerpt='Gonorrhoea and non-gonococcal urethritis look almost the same and cannot be told apart by eye — you need a test. Testing and treatment are available at HappiWell Clinic, Thung Khru, including Ceftriaxone injections.',
  seo_title='Gonorrhoea vs Non-Gonococcal Urethritis: Symptoms, Testing & Treatment | HappiWell Bangkok',
  seo_description='Gonorrhoea and non-gonococcal urethritis have similar symptoms but different germs and treatment. Confidential testing and treatment, Ceftriaxone injection 150 baht, at HappiWell Medical Clinic, Thung Khru, Bangkok.',
  tags=['Sexual health', 'Gonorrhoea', 'STI'],
  content=blocks([
    ('p', 'Burning when you pass urine, or pus or discharge from the tip of the penis: in Thai this is often just called "gonorrhoea". In fact there are two conditions, <b>true gonorrhoea</b> and <b>non-gonococcal urethritis</b> (sometimes called "false gonorrhoea" in Thailand). They are caused by different germs and treated differently. This article explains the difference simply.'),
    ('h2', 'In short'),
    ('ul', ['<b>Gonorrhoea</b> is caused by the bacterium <i>Neisseria gonorrhoeae</i>.',
            '<b>Non-gonococcal urethritis</b> is caused by other germs, such as chlamydia (<i>Chlamydia trachomatis</i>) or <i>Mycoplasma genitalium</i>. It is more common than many people think.',
            'The symptoms are <b>very similar and cannot be told apart by eye</b>. A test is needed to know for sure.',
            'Both can be <b>treated</b>, but the medicine must match the germ, and you can have both at the same time.']),
    ('h2', 'Common symptoms'),
    ('ul', ['Burning, stinging or pain when passing urine',
            'Pus or discharge from the urethra. In gonorrhoea it is often thick and yellow or green; in non-gonococcal urethritis it is more often cloudy white or clear and milder — but this is not a reliable rule.',
            'Symptoms usually start 2–7 days after exposure for gonorrhoea, and may take longer for non-gonococcal urethritis.',
            'Many women have <b>no symptoms</b>, or only unusual discharge, burning when passing urine or lower abdominal pain.',
            'Infections in the throat or rectum often have no symptoms but can still be passed on.']),
    ('p', 'Some people have no symptoms but can still pass the infection on. If you have had a risk, get tested even if you feel fine.'),
    ('h2', 'Why test? Can I just buy antibiotics?'),
    ('ul', ['The two conditions need different medicines. Guessing can mean the wrong drug: symptoms may seem to ease while the germ is still there.',
            'Gonorrhoea is becoming more resistant to antibiotics worldwide. Taking the wrong dose or course makes this worse.',
            'You can have both infections at once, so doctors plan treatment from the test results and your risk history.',
            'A test also helps the doctor decide whether to check for other infections such as HIV and syphilis.']),
    ('h2', 'What HappiWell Clinic offers'),
    ('ul', [f'<b>Testing</b>: the doctor takes a history, examines you and sends tests as appropriate. See our <a href="{STD}">STI screening page</a>.',
            f'<b>Treatment</b>: for gonorrhoea the main treatment is a single injection of the antibiotic Ceftriaxone (Cef-3); the doctor may add tablets depending on your results. See the <a href="{CEF}">Ceftriaxone injection page</a> for the price.',
            'For non-gonococcal urethritis, the doctor usually prescribes antibiotic tablets matched to the germ suspected or found.',
            'Free condoms in all sizes.']),
    ('p', '<b>Your information is confidential.</b> Your visit and results are kept private, and questions — on LINE or at the clinic — are answered only by our doctors and nurses.'),
    ('h2', 'After treatment'),
    ('ul', ['Finish all the medicine as prescribed, even if you feel better.',
            'Avoid sex until treatment is finished and symptoms have gone — generally at least 7 days after you received the medicine.',
            '<b>Your partner(s) should be tested and treated at the same time</b>, or you can pass the infection back and forth.',
            'See the doctor again if symptoms do not improve within 3–5 days or come back.',
            'The doctor may advise tests for HIV, syphilis and other infections too.',
            'Use condoms every time to avoid re-infection.']),
    ('h2', 'What happens if it is not treated?'),
    ('ul', ['Men: inflammation of the testicle or epididymis, prostatitis, narrowing of the urethra.',
            'Women: pelvic inflammatory disease, blocked tubes, risk of infertility and ectopic pregnancy.',
            'Rarely the germ spreads to the blood or joints, and having an STI makes it easier to catch HIV.',
            'Pregnant women can pass the infection to the baby during birth.']),
    ('h2', 'Prices at HappiWell Clinic'),
    ('ul', [f'<a href="{CEF}">Ceftriaxone (Cef-3) injection</a>: <b>150 baht</b> per injection',
            f'Testing: ask about tests and prices on <a href="{LINE}">LINE @p49clinic</a> or see the <a href="{STD}">STI screening page</a>.']),
    ('p', 'Prices do not include the medical service fee. A doctor takes your history and assesses you before any medicine is given.'),
    ('p', f'To consult or book, <a href="{LINE}">message us on LINE @p49clinic</a>. We are open every day: Monday–Friday 08:00–18:00 and Saturday–Sunday 08:00–12:00.'),
    ('h2', 'Frequently asked questions'),
    ('p', '<b>Can I tell the two apart myself?</b><br>No. The symptoms are very similar. A doctor needs to examine you and test for the germ.'),
    ('p', '<b>Does one injection cure it?</b><br>Gonorrhoea usually responds well to a single Ceftriaxone injection, but the doctor will decide whether other medicine is needed and may ask you to come back for follow-up.'),
    ('p', '<b>Can it go away on its own?</b><br>Do not wait. Symptoms may ease while the germ stays, and you can still pass it on or develop complications.'),
    ('p', '<b>Should I tell the doctor about antibiotic allergies?</b><br>Always — especially allergy to penicillin or cephalosporin antibiotics.'),
    ('h3', 'References'),
    ('ul', REF),
    ('p', '<i>This article is for general information and is not personal medical advice. If you have symptoms, see a doctor for testing and treatment.</i>'),
  ], 'ge'))


def doc(paras, pre):
    return blocks([('p', x) for x in paras], pre, 1793600000001)


PROG = dict(
  slug=PSLUG, category='sexual-health', price=150, price_unit='ต่อครั้ง', sort_order=21,
  is_featured=False, is_published=True, brand='Ceftriaxone', related_article_slug=SLUG,
  th=dict(
    name='ฉีดยาปฏิชีวนะ Ceftriaxone (Cef-3)',
    short='ยาฉีดปฏิชีวนะที่ใช้รักษาหนองในแท้ แพทย์ประเมินก่อนฉีดทุกครั้ง เป็นความลับ',
    desc=doc(['Ceftriaxone (Cef-3) เป็นยาฉีดปฏิชีวนะกลุ่มเซฟาโลสปอริน ใช้รักษาหนองในแท้ และการติดเชื้อแบคทีเรียบางชนิดตามที่แพทย์เห็นสมควร',
              'แพทย์จะซักประวัติ ตรวจร่างกาย และพิจารณาส่งตรวจเชื้อก่อนให้ยา หนองในเทียมมักใช้ยากินคนละชนิด จึงไม่ควรฉีดยาเองโดยไม่ได้ตรวจ',
              'ข้อมูลของคุณเป็นความลับ ผู้ตอบคำถามทาง LINE และที่คลินิกคือแพทย์และพยาบาลเท่านั้น'], 'cf'),
    suit=['ผู้ที่แพทย์วินิจฉัยหรือสงสัยหนองในแท้', 'คู่นอนของผู้ติดเชื้อหนองในแท้ที่แพทย์แนะนำให้รักษา'],
    inc=['ซักประวัติและประเมินโดยแพทย์ก่อนฉีด', 'ค่ายาและค่าฉีด 1 ครั้ง', 'สังเกตอาการหลังฉีดที่คลินิก'],
    prec=['แจ้งแพทย์หากแพ้ยาปฏิชีวนะ โดยเฉพาะเพนิซิลลินหรือเซฟาโลสปอริน', 'งดมีเพศสัมพันธ์จนกว่าจะรักษาครบและอาการหาย และให้คู่นอนตรวจรักษาพร้อมกัน', 'หากอาการไม่ดีขึ้นใน 3–5 วัน ให้กลับมาพบแพทย์'],
    dur='ฉีด 1 ครั้ง (แพทย์อาจนัดติดตามอาการ)',
    seo_t='ฉีดยา Ceftriaxone (Cef-3) รักษาหนองใน 150 บาท ทุ่งครุ | HappiWell',
    seo_d='ฉีดยาปฏิชีวนะ Ceftriaxone (Cef-3) ครั้งละ 150 บาท แพทย์ประเมินก่อนฉีดทุกครั้ง เป็นความลับ ที่แฮปปี้เวลล์ คลินิกเวชกรรม ซ.ประชาอุทิศ 49 ทุ่งครุ'),
  en=dict(
    name='Ceftriaxone (Cef-3) antibiotic injection',
    short='Antibiotic injection used to treat gonorrhoea. A doctor assesses you before every injection. Confidential.',
    desc=doc(['Ceftriaxone (Cef-3) is an injectable cephalosporin antibiotic used to treat gonorrhoea and certain other bacterial infections as the doctor sees fit.',
              'The doctor takes a history, examines you and considers testing before giving the medicine. Non-gonococcal urethritis is usually treated with different tablets, so you should not have this injection without being assessed.',
              'Your information is kept confidential. Questions — on LINE or at the clinic — are answered only by our doctors and nurses.'], 'cf'),
    suit=['People diagnosed with, or suspected of having, gonorrhoea', 'Partners of someone with gonorrhoea when the doctor advises treatment'],
    inc=['Assessment by a doctor before the injection', 'Medicine and injection, 1 time', 'Observation after the injection at the clinic'],
    prec=['Tell the doctor about antibiotic allergies, especially penicillin or cephalosporins', 'Avoid sex until treatment is finished and symptoms have gone, and have your partner treated at the same time', 'If you are not better within 3–5 days, see the doctor again'],
    dur='1 injection (the doctor may ask you to come back for follow-up)',
    seo_t='Ceftriaxone (Cef-3) Injection for Gonorrhoea, 150 Baht | HappiWell Thung Khru',
    seo_d='Ceftriaxone (Cef-3) antibiotic injection at 150 baht per injection. Doctor assessment before every injection, confidential, at HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok.'),
  my=dict(
    name='Ceftriaxone (Cef-3) ပဋိဇီဝဆေးထိုးခြင်း',
    short='ကာလသားရောဂါ (ဂနိုရီးယား) ကုသရာတွင် သုံးသော ပဋိဇီဝဆေးထိုးခြင်း။ ထိုးမီ ဆရာဝန်က အကဲဖြတ်ပါသည်။ လျှို့ဝှက်ထားပါသည်။',
    desc=doc(['Ceftriaxone (Cef-3) သည် cephalosporin အမျိုးအစား ပဋိဇီဝဆေးထိုးဆေးဖြစ်ပြီး ဂနိုရီးယားနှင့် အခြားဘက်တီးရီးယားရောဂါများကို ဆရာဝန်သင့်လျော်သလို ကုသရာတွင် သုံးပါသည်။',
              'ဆေးမပေးမီ ဆရာဝန်က ရောဂါရာဇဝင်မေးမြန်း၊ စစ်ဆေးပြီး ပိုးစစ်ရန် စဉ်းစားပါမည်။ ဂနိုရီးယားမဟုတ်သော ဆီးလမ်းကြောင်းရောင်ရမ်းမှုကို ပုံမှန်အားဖြင့် ဆေးတောင့်ဖြင့် ကုသသဖြင့် စစ်ဆေးမှုမရှိဘဲ ထိုးမခံသင့်ပါ။',
              'သင့်အချက်အလက်များကို လျှို့ဝှက်ထားပါသည်။ LINE နှင့် ဆေးခန်းတွင် ဖြေကြားသူများမှာ ဆရာဝန်နှင့် သူနာပြုများသာ ဖြစ်ပါသည်။'], 'cf'),
    suit=['ဂနိုရီးယား ဖြစ်ကြောင်း ဆရာဝန်ရောဂါရှာဖွေတွေ့ရှိသူ သို့မဟုတ် သံသယရှိသူ', 'ဆရာဝန်က ကုသရန် အကြံပြုသော ဂနိုရီးယားရောဂါရှိသူ၏ လိင်ဖက်'],
    inc=['ထိုးမီ ဆရာဝန်၏ အကဲဖြတ်မှု', 'ဆေးနှင့် ဆေးထိုးခ ၁ ကြိမ်', 'ထိုးပြီးနောက် ဆေးခန်းတွင် လက္ခဏာများကို စောင့်ကြည့်ခြင်း'],
    prec=['ပဋိဇီဝဆေး မတည့်ပါက ဆရာဝန်ကို ပြောပါ (အထူးသဖြင့် penicillin သို့မဟုတ် cephalosporin)', 'ကုသမှုပြီးဆုံးပြီး လက္ခဏာပျောက်သည်အထိ လိင်ဆက်ဆံခြင်းကို ရှောင်ပါ၊ လိင်ဖက်ကိုလည်း တစ်ပြိုင်နက် ကုသပါ', '၃–၅ ရက်အတွင်း မသက်သာပါက ဆရာဝန်ထံ ပြန်လာပါ'],
    dur='၁ ကြိမ် ထိုးခြင်း (ဆရာဝန်က ပြန်လည်စစ်ဆေးရန် ချိန်းနိုင်ပါသည်)',
    seo_t='Ceftriaxone (Cef-3) ဆေးထိုးခြင်း ၁၅၀ ဘတ် | HappiWell Thung Khru',
    seo_d='Ceftriaxone (Cef-3) ပဋိဇီဝဆေးထိုးခြင်း တစ်ကြိမ် ၁၅၀ ဘတ်။ ထိုးမီ ဆရာဝန်အကဲဖြတ်၊ လျှို့ဝှက်၊ HappiWell ဆေးခန်း၊ Thung Khru ဘန်ကောက်။'),
)


def row(lang, p):
    return {'name': p['name'], 'short_desc': p['short'], 'description': p['desc'], 'suitable_for': p['suit'],
            'includes': p['inc'], 'precautions': p['prec'], 'duration': p['dur'], 'seo_title': p['seo_t'],
            'seo_description': p['seo_d']}


if __name__ == '__main__':
    pr = {k: PROG[k] for k in ('slug', 'category', 'price', 'price_unit', 'sort_order', 'is_featured', 'is_published', 'brand', 'related_article_slug')}
    th = row('th', PROG['th']); pr.update(th)
    pr['en'] = row('en', PROG['en']); pr['my'] = row('my', PROG['my'])
    pr['price_note'] = None
    out = {'slug': SLUG, 'th': TH, 'en': EN, 'program': pr}
    p = pathlib.Path(__file__).with_name('gonorrhea_ngu.json')
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print('ok', p)

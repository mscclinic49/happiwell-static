# -*- coding: utf-8 -*-
"""วัคซีนชุดใหม่ (พ.ย. 2569) — ไทย + อังกฤษ + พม่า + SEO
- เปลี่ยน Prevnar 20 (ไม่มีแล้ว) → Vaxneuvance (PCV15) 2,690 บาท (slug ใหม่, Worker redirect slug เก่า)
- เพิ่ม: Pneumovax 23 1,590 · Gardasil 4 2,790 · Varivax 1,490 · VAQTA 1,190 · MMR II 650 · ProQuad 2,590
- แก้บทความ pneumonia-vaccine-2569 ให้เป็น PCV15 + PPSV23 (ไทย/อังกฤษ)
ราคาที่เจ้าของคลินิกยืนยันแล้ว ไม่รวมค่าบริการทางการแพทย์ (หน้าเว็บแสดงข้อความนี้เอง)
รัน: python3 supabase/seed/posts/vaccines_2569.py → เขียน vaccines_2569.json (นำเข้าฐานข้อมูลด้วย SQL)
"""
import json, pathlib

def desc(*paras, kind='paragraph'):
    return json.dumps({'time': 1793500000000, 'version': '2.29.1', 'blocks': [
        {'id': f'v{i}', 'type': 'paragraph', 'data': {'text': t}} for i, t in enumerate(paras)]}, ensure_ascii=False)

ASSESS = ('ซักประวัติและประเมินความเหมาะสมโดยแพทย์ก่อนฉีด', "Doctor's history check and assessment before the injection", 'ကာကွယ်ဆေးမထိုးမီ ဆရာဝန်က ရောဂါရာဇဝင်မေးပြီး စစ်ဆေးအကဲဖြတ်ခြင်း')
VFEE = ('ค่าวัคซีนและค่าฉีด', 'Vaccine and injection fee', 'ကာကွယ်ဆေးဖိုးနှင့် ဆေးထိုးခ')
OBS = ('สังเกตอาการหลังฉีดที่คลินิก', 'Observation at the clinic after the injection', 'ဆေးထိုးပြီးနောက် ဆေးခန်းတွင် ခဏစောင့်ကြည့်ခြင်း')
STD_INC = [ASSESS, VFEE, OBS]
UNIT = ('ต่อเข็ม', 'per dose', 'တစ်လုံးလျှင်')
CL_TH = 'แฮปปี้เวลล์ คลินิกเวชกรรม ซ.ประชาอุทิศ 49 ทุ่งครุ'
CL_EN = 'HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok'
CL_MY = 'HappiWell ဆေးခန်း၊ Soi Pracha Uthit 49၊ Thung Khru၊ ဘန်ကောက်'


def prog(slug, sort, price, brand, related, th, en, my, featured=False, inc=STD_INC):
    """th/en/my = dict(name, short, desc(list), suit(list), prec(list), dur, seo_t, seo_d)"""
    def lang(d, i):
        out = dict(name=d['name'], short_desc=d['short'], description=desc(*d['desc']),
                   suitable_for=d['suit'], includes=[x[i] for x in inc], precautions=d['prec'],
                   price_unit=UNIT[i], seo_title=d['seo_t'], seo_description=d['seo_d'])
        if d.get('dur'):
            out['duration'] = d['dur']
        return out
    row = lang(th, 0)
    row.update(slug=slug, category='vaccine', price=price, sort_order=sort, is_featured=featured,
               is_published=True, brand=brand, related_article_slug=related)
    row['en'] = lang(en, 1)
    row['my'] = lang(my, 2)
    return row


P = []

# ---------------- Vaxneuvance (PCV15) — แทน Prevnar 20 ----------------
P.append(prog('pneumococcal-vaccine-vaxneuvance', 3, 2690, 'Vaxneuvance (PCV15)', 'pneumonia-vaccine-2569',
  dict(name='วัคซีนปอดอักเสบ 15 สายพันธุ์ (Vaxneuvance)',
       short='วัคซีนป้องกันโรคไอพีดี (ปอดอักเสบจากเชื้อนิวโมคอคคัส) ชนิดคอนจูเกต 15 สายพันธุ์ แพทย์ประเมินก่อนฉีดทุกครั้ง',
       desc=['วัคซีน Vaxneuvance (PCV15) เป็นวัคซีนชนิดคอนจูเกต ป้องกันการติดเชื้อนิวโมคอคคัส 15 สายพันธุ์ ซึ่งเป็นสาเหตุสำคัญของปอดอักเสบ ติดเชื้อในกระแสเลือด และเยื่อหุ้มสมองอักเสบ (โรคไอพีดี)',
             'ผู้ใหญ่ที่ไม่เคยฉีดวัคซีนไอพีดีมาก่อน มักได้รับคำแนะนำให้ฉีด PCV15 แล้วตามด้วยวัคซีน Pneumovax 23 (PPSV23) อีก 1 เข็ม โดยทั่วไปห่างกันอย่างน้อย 1 ปี แพทย์จะประเมินและวางแผนการฉีดตามอายุ โรคประจำตัว และประวัติวัคซีนเดิม'],
       suit=['ผู้สูงอายุ 65 ปีขึ้นไป', 'ผู้ใหญ่ที่มีโรคเรื้อรัง เช่น เบาหวาน โรคหัวใจ โรคปอด โรคไต หรือภูมิคุ้มกันบกพร่อง', 'ผู้ใหญ่ทั่วไปที่ต้องการป้องกัน'],
       prec=['แจ้งแพทย์หากเคยฉีดวัคซีนไอพีดีชนิดอื่นมาก่อน เพื่อวางแผนการฉีดให้เหมาะสม', 'หากมีไข้หรือเจ็บป่วยเฉียบพลัน แพทย์อาจแนะนำให้เลื่อนการฉีด'],
       dur='1 เข็ม (ผู้ใหญ่ส่วนใหญ่ฉีด PPSV23 ต่ออีก 1 เข็มตามที่แพทย์แนะนำ)',
       seo_t='วัคซีนปอดอักเสบ 15 สายพันธุ์ Vaxneuvance ราคา 2,690 บาท ทุ่งครุ | HappiWell',
       seo_d=f'วัคซีนปอดอักเสบ (ไอพีดี) Vaxneuvance PCV15 เข็มละ 2,690 บาท แพทย์ประเมินและวางแผนฉีดร่วมกับ PPSV23 ที่{CL_TH}'),
  dict(name='Pneumococcal vaccine, 15-valent (Vaxneuvance)',
       short='A 15-valent conjugate vaccine against invasive pneumococcal disease (IPD). A doctor assesses you before every injection.',
       desc=['Vaxneuvance (PCV15) is a conjugate vaccine that protects against 15 types of pneumococcus, a major cause of pneumonia, bloodstream infection and meningitis (invasive pneumococcal disease, IPD).',
             'Adults who have never had a pneumococcal vaccine are usually advised to have PCV15 followed by one dose of Pneumovax 23 (PPSV23), generally at least 1 year apart. The doctor will plan your schedule based on your age, health conditions and vaccination history.'],
       suit=['Adults aged 65 and over', 'Adults with long-term conditions such as diabetes, heart, lung or kidney disease, or a weakened immune system', 'Any adult who wants protection'],
       prec=['Tell the doctor if you have had another pneumococcal vaccine before, so the right schedule can be planned', 'If you have a fever or acute illness, the doctor may advise postponing the injection'],
       dur='1 dose (most adults then have 1 dose of PPSV23 as advised by the doctor)',
       seo_t='Vaxneuvance PCV15 Pneumococcal Vaccine 2,690 THB, Bangkok | HappiWell',
       seo_d=f'Vaxneuvance (PCV15) pneumococcal vaccine for 2,690 baht per dose, with a doctor planning your schedule with PPSV23. {CL_EN}.'),
  dict(name='နျူမိုကိုကပ်စ် ကာကွယ်ဆေး ၁၅ မျိုးခံ (Vaxneuvance)',
       short='နျူမိုကိုကပ်စ် ပိုးဝင်ခြင်း (IPD) ကို ကာကွယ်သော ၁၅ မျိုးခံ ကွန်ဂျူဂိတ် ကာကွယ်ဆေး။ ဆေးမထိုးမီ ဆရာဝန်က အကဲဖြတ်ပေးပါသည်။',
       desc=['Vaxneuvance (PCV15) သည် အဆုတ်ရောင်ခြင်း၊ သွေးထဲပိုးဝင်ခြင်းနှင့် ဦးနှောက်အမြှေးရောင်ခြင်း (IPD) ၏ အဓိကအကြောင်းရင်း ဖြစ်သော နျူမိုကိုကပ်စ် ၁၅ မျိုးကို ကာကွယ်ပေးသော ကွန်ဂျူဂိတ် ကာကွယ်ဆေး ဖြစ်ပါသည်။',
             'နျူမိုကိုကပ်စ် ကာကွယ်ဆေး မထိုးဖူးသော အရွယ်ရောက်သူများကို PCV15 ထိုးပြီးနောက် Pneumovax 23 (PPSV23) ၁ လုံး ထပ်ထိုးရန် များသောအားဖြင့် အကြံပြုပါသည်၊ ယေဘုယျအားဖြင့် အနည်းဆုံး ၁ နှစ်ခြားပါသည်။ ဆရာဝန်က အသက်၊ ရောဂါနှင့် ယခင်ထိုးဖူးမှုအပေါ် မူတည်၍ အချိန်ဇယား စီစဉ်ပေးပါမည်။'],
       suit=['အသက် ၆၅ နှစ် နှင့်အထက် လူကြီးများ', 'ဆီးချို၊ နှလုံး၊ အဆုတ်၊ ကျောက်ကပ်ရောဂါ (သို့) ခုခံအားကျနေသော အရွယ်ရောက်သူများ', 'ကာကွယ်လိုသော အရွယ်ရောက်သူ မည်သူမဆို'],
       prec=['အခြား နျူမိုကိုကပ်စ် ကာကွယ်ဆေး ထိုးဖူးပါက ဆရာဝန်ကို ပြောပြပါ', 'ဖျားနေခြင်း (သို့) ရုတ်တရက် နေမကောင်းဖြစ်နေပါက ဆရာဝန်က ဆေးထိုးချိန်ကို ရွှေ့ရန် အကြံပေးနိုင်ပါသည်'],
       dur='၁ လုံး (အရွယ်ရောက်သူ အများစုသည် ဆရာဝန်အကြံပြုချက်အတိုင်း PPSV23 ၁ လုံး ထပ်ထိုးသည်)',
       seo_t='Vaxneuvance PCV15 နျူမိုကိုကပ်စ် ကာကွယ်ဆေး 2,690 ဘတ် | HappiWell',
       seo_d=f'Vaxneuvance (PCV15) နျူမိုကိုကပ်စ် ကာကွယ်ဆေး တစ်လုံး 2,690 ဘတ်၊ ဆရာဝန်က PPSV23 နှင့်အတူ အချိန်ဇယား စီစဉ်ပေးသည်။ {CL_MY}။')))

# ---------------- Pneumovax 23 ----------------
P.append(prog('pneumococcal-vaccine-pneumovax-23', 3, 1590, 'Pneumovax 23 (PPSV23)', 'pneumonia-vaccine-2569',
  dict(name='วัคซีนปอดอักเสบ 23 สายพันธุ์ (Pneumovax 23)',
       short='วัคซีนป้องกันโรคไอพีดี ชนิดโพลีแซคคาไรด์ 23 สายพันธุ์ มักฉีดต่อจากวัคซีน PCV15 ตามที่แพทย์แนะนำ',
       desc=['วัคซีน Pneumovax 23 (PPSV23) ป้องกันการติดเชื้อนิวโมคอคคัส 23 สายพันธุ์ ช่วยขยายความครอบคลุมสายพันธุ์ของการป้องกันโรคไอพีดี',
             'ในผู้ใหญ่ มักฉีดต่อจากวัคซีนชนิดคอนจูเกต เช่น PCV15 (Vaxneuvance) โดยทั่วไปห่างกันอย่างน้อย 1 ปี แพทย์จะดูประวัติวัคซีนเดิมและแนะนำเวลาที่เหมาะสม'],
       suit=['ผู้ที่ฉีด PCV15 แล้ว และถึงกำหนดฉีดเข็มต่อไป', 'ผู้สูงอายุ 65 ปีขึ้นไป และผู้ที่มีโรคเรื้อรังตามที่แพทย์แนะนำ'],
       prec=['แจ้งแพทย์หากเคยฉีดวัคซีนไอพีดีชนิดใดมาก่อน และฉีดเมื่อไร', 'หากมีไข้หรือเจ็บป่วยเฉียบพลัน แพทย์อาจแนะนำให้เลื่อนการฉีด'],
       dur='1 เข็ม ตามกำหนดที่แพทย์แนะนำ',
       seo_t='วัคซีนปอดอักเสบ 23 สายพันธุ์ Pneumovax 23 ราคา 1,590 บาท | HappiWell',
       seo_d=f'วัคซีนปอดอักเสบ Pneumovax 23 (PPSV23) เข็มละ 1,590 บาท ฉีดต่อจาก PCV15 ตามที่แพทย์แนะนำ ที่{CL_TH}'),
  dict(name='Pneumococcal vaccine, 23-valent (Pneumovax 23)',
       short='A 23-valent polysaccharide vaccine against invasive pneumococcal disease, usually given after PCV15 as advised by the doctor.',
       desc=['Pneumovax 23 (PPSV23) protects against 23 types of pneumococcus, broadening your protection against invasive pneumococcal disease.',
             'In adults it is usually given after a conjugate vaccine such as PCV15 (Vaxneuvance), generally at least 1 year apart. The doctor will review your vaccination history and advise the right timing.'],
       suit=['People who have had PCV15 and are due for the next dose', 'Adults aged 65 and over, and people with long-term conditions, as advised by the doctor'],
       prec=['Tell the doctor which pneumococcal vaccines you have had before, and when', 'If you have a fever or acute illness, the doctor may advise postponing the injection'],
       dur='1 dose, timed as advised by the doctor',
       seo_t='Pneumovax 23 (PPSV23) Pneumococcal Vaccine 1,590 THB, Bangkok | HappiWell',
       seo_d=f'Pneumovax 23 (PPSV23) pneumococcal vaccine for 1,590 baht per dose, usually given after PCV15 as advised by the doctor. {CL_EN}.'),
  dict(name='နျူမိုကိုကပ်စ် ကာကွယ်ဆေး ၂၃ မျိုးခံ (Pneumovax 23)',
       short='နျူမိုကိုကပ်စ် ၂၃ မျိုးကို ကာကွယ်သော ကာကွယ်ဆေး၊ ဆရာဝန်အကြံပြုချက်အတိုင်း PCV15 ပြီးမှ ထိုးလေ့ရှိသည်။',
       desc=['Pneumovax 23 (PPSV23) သည် နျူမိုကိုကပ်စ် ၂၃ မျိုးကို ကာကွယ်ပြီး IPD ကာကွယ်မှုကို ပိုမိုကျယ်ပြန့်စေပါသည်။',
             'အရွယ်ရောက်သူများတွင် PCV15 (Vaxneuvance) ကဲ့သို့ ကွန်ဂျူဂိတ် ကာကွယ်ဆေး ပြီးမှ ယေဘုယျအားဖြင့် အနည်းဆုံး ၁ နှစ်ခြား၍ ထိုးလေ့ရှိပါသည်။ ဆရာဝန်က ယခင်ထိုးဖူးမှုကို ကြည့်ပြီး သင့်တော်သောအချိန်ကို အကြံပေးပါမည်။'],
       suit=['PCV15 ထိုးပြီး နောက်တစ်လုံး ထိုးရန် အချိန်ရောက်သူများ', 'ဆရာဝန်အကြံပြုချက်အတိုင်း အသက် ၆၅ နှစ်အထက်နှင့် နာတာရှည်ရောဂါရှိသူများ'],
       prec=['ယခင် ထိုးဖူးသော နျူမိုကိုကပ်စ် ကာကွယ်ဆေးနှင့် ထိုးခဲ့သည့်အချိန်ကို ဆရာဝန်ကို ပြောပြပါ', 'ဖျားနေခြင်း (သို့) ရုတ်တရက် နေမကောင်းဖြစ်နေပါက ဆရာဝန်က ဆေးထိုးချိန်ကို ရွှေ့ရန် အကြံပေးနိုင်ပါသည်'],
       dur='ဆရာဝန် အကြံပြုသည့်အချိန်တွင် ၁ လုံး',
       seo_t='Pneumovax 23 (PPSV23) နျူမိုကိုကပ်စ် ကာကွယ်ဆေး 1,590 ဘတ် | HappiWell',
       seo_d=f'Pneumovax 23 (PPSV23) နျူမိုကိုကပ်စ် ကာကွယ်ဆေး တစ်လုံး 1,590 ဘတ်၊ ဆရာဝန်အကြံပြုချက်အတိုင်း PCV15 ပြီးမှ ထိုးသည်။ {CL_MY}။')))

# ---------------- Gardasil 4 ----------------
P.append(prog('hpv-vaccine-gardasil-4', 6, 2790, 'Gardasil (4-valent)', None,
  dict(name='วัคซีน HPV 4 สายพันธุ์ (Gardasil)',
       short='วัคซีนป้องกันเชื้อไวรัส HPV 4 สายพันธุ์ (6, 11, 16, 18) จำนวนเข็มขึ้นกับอายุ แพทย์จะแนะนำตารางฉีดที่เหมาะสม',
       desc=['วัคซีน Gardasil 4 สายพันธุ์ ป้องกันการติดเชื้อไวรัส HPV สายพันธุ์ 16 และ 18 ซึ่งเกี่ยวข้องกับมะเร็งปากมดลูก และสายพันธุ์ 6 และ 11 ซึ่งเป็นสาเหตุของหูดหงอนไก่',
             'จำนวนเข็มและระยะห่างขึ้นกับอายุที่เริ่มฉีด แพทย์จะประเมินและแนะนำตารางฉีดที่เหมาะสมกับแต่ละคน หากต้องการการป้องกันที่ครอบคลุมสายพันธุ์มากกว่า มีวัคซีน Gardasil 9 ให้เลือกด้วย'],
       suit=['ผู้หญิงและผู้ชายตามช่วงอายุที่แพทย์แนะนำ'],
       prec=['ผู้ที่ตั้งครรภ์ควรปรึกษาแพทย์ก่อนฉีด', 'วัคซีนไม่ได้ทดแทนการตรวจคัดกรองมะเร็งปากมดลูก ผู้หญิงควรตรวจคัดกรองตามกำหนดต่อไป'],
       seo_t='วัคซีน HPV 4 สายพันธุ์ Gardasil ราคา 2,790 บาท ทุ่งครุ | HappiWell',
       seo_d=f'ฉีดวัคซีน HPV 4 สายพันธุ์ (Gardasil) เข็มละ 2,790 บาท แพทย์แนะนำตารางฉีดตามอายุ ที่{CL_TH}'),
  dict(name='HPV vaccine, 4-valent (Gardasil)',
       short='Protects against 4 types of HPV (6, 11, 16, 18). The number of doses depends on your age — the doctor will advise the right schedule.',
       desc=['The 4-valent Gardasil vaccine protects against HPV types 16 and 18, which are linked to cervical cancer, and types 6 and 11, which cause genital warts.',
             'The number of doses and the interval depend on your age when you start. The doctor will assess you and recommend the right schedule. For broader protection, Gardasil 9 is also available.'],
       suit=['Women and men in the age ranges recommended by the doctor'],
       prec=['If you are pregnant, talk to the doctor before the injection', 'The vaccine does not replace cervical screening — women should continue regular screening'],
       seo_t='Gardasil 4-valent HPV Vaccine 2,790 THB in Bangkok | HappiWell Clinic',
       seo_d=f'4-valent HPV vaccine (Gardasil) for 2,790 baht per dose, with a schedule advised by the doctor for your age. {CL_EN}.'),
  dict(name='HPV ကာကွယ်ဆေး ၄ မျိုးခံ (Gardasil)',
       short='HPV ၄ မျိုး (6, 11, 16, 18) ကို ကာကွယ်သည်။ ထိုးရမည့်အရေအတွက်သည် အသက်ပေါ် မူတည်ပြီး ဆရာဝန်က အကြံပေးပါမည်။',
       desc=['Gardasil ၄ မျိုးခံ ကာကွယ်ဆေးသည် သားအိမ်ခေါင်းကင်ဆာနှင့် ဆက်စပ်သော HPV 16 နှင့် 18၊ လိင်အင်္ဂါကြွက်နို့ ဖြစ်စေသော HPV 6 နှင့် 11 ကို ကာကွယ်ပေးပါသည်။',
             'ထိုးရမည့် အရေအတွက်နှင့် ကြားကာလသည် စတင်ထိုးချိန် အသက်ပေါ် မူတည်ပါသည်။ ဆရာဝန်က အကဲဖြတ်ပြီး သင့်တော်သော အချိန်ဇယားကို အကြံပေးပါမည်။ ပိုမိုကျယ်ပြန့်သော ကာကွယ်မှုအတွက် Gardasil 9 လည်း ရနိုင်ပါသည်။'],
       suit=['ဆရာဝန် အကြံပြုသော အသက်အရွယ်ရှိ အမျိုးသမီးနှင့် အမျိုးသားများ'],
       prec=['ကိုယ်ဝန်ဆောင်ပါက ဆေးမထိုးမီ ဆရာဝန်နှင့် တိုင်ပင်ပါ', 'ကာကွယ်ဆေးသည် သားအိမ်ခေါင်းကင်ဆာ စစ်ဆေးမှုကို အစားမထိုးပါ၊ အမျိုးသမီးများ ပုံမှန်စစ်ဆေးမှုကို ဆက်လုပ်သင့်ပါသည်'],
       seo_t='HPV ကာကွယ်ဆေး ၄ မျိုးခံ Gardasil 2,790 ဘတ် ဘန်ကောက် | HappiWell',
       seo_d=f'HPV ၄ မျိုးခံ ကာကွယ်ဆေး (Gardasil) တစ်လုံး 2,790 ဘတ်၊ အသက်အလိုက် ဆရာဝန်က အချိန်ဇယား အကြံပေးသည်။ {CL_MY}။')))

# ---------------- Varivax ----------------
P.append(prog('chickenpox-vaccine-varivax', 10, 1490, 'Varivax', None,
  dict(name='วัคซีนอีสุกอีใส (Varivax)',
       short='วัคซีนป้องกันโรคอีสุกอีใส สำหรับเด็กอายุ 1 ปีขึ้นไปและผู้ใหญ่ที่ยังไม่มีภูมิคุ้มกัน ฉีด 2 เข็ม',
       desc=['วัคซีน Varivax ป้องกันโรคอีสุกอีใส เป็นวัคซีนชนิดเชื้อเป็นอ่อนฤทธิ์ ใช้ได้ในเด็กอายุ 1 ปีขึ้นไป วัยรุ่น และผู้ใหญ่ที่ไม่เคยเป็นอีสุกอีใสหรือไม่เคยได้รับวัคซีน',
             'ฉีดทั้งหมด 2 เข็ม ระยะห่างระหว่างเข็มขึ้นกับอายุ แพทย์จะแนะนำตารางฉีดที่เหมาะสม'],
       suit=['เด็กอายุ 1 ปีขึ้นไป ตามตารางวัคซีน', 'วัยรุ่นและผู้ใหญ่ที่ไม่เคยเป็นอีสุกอีใสและไม่เคยได้รับวัคซีน'],
       prec=['ผู้ที่ตั้งครรภ์ หรือมีภูมิคุ้มกันบกพร่อง ห้ามฉีด', 'ผู้หญิงควรหลีกเลี่ยงการตั้งครรภ์หลังฉีดตามระยะเวลาที่แพทย์แนะนำ', 'แจ้งแพทย์หากเพิ่งได้รับเลือด ผลิตภัณฑ์จากเลือด หรือวัคซีนเชื้อเป็นชนิดอื่น'],
       dur='2 เข็ม',
       seo_t='วัคซีนอีสุกอีใส Varivax ราคา 1,490 บาท ทุ่งครุ | HappiWell',
       seo_d=f'วัคซีนอีสุกอีใส Varivax เข็มละ 1,490 บาท สำหรับเด็กอายุ 1 ปีขึ้นไปและผู้ใหญ่ที่ยังไม่มีภูมิ แพทย์ประเมินก่อนฉีด ที่{CL_TH}'),
  dict(name='Chickenpox vaccine (Varivax)',
       short='Protects against chickenpox, for children from 1 year and adults without immunity. 2 doses.',
       desc=['Varivax is a live attenuated vaccine against chickenpox (varicella). It can be given to children from 1 year of age, teenagers and adults who have never had chickenpox or the vaccine.',
             'The course is 2 doses. The interval depends on your age — the doctor will advise the right schedule.'],
       suit=['Children aged 1 year and over, following the vaccination schedule', 'Teenagers and adults who have never had chickenpox or the vaccine'],
       prec=['Not for pregnant women or people with a weakened immune system', 'Women should avoid pregnancy after vaccination for the period advised by the doctor', 'Tell the doctor if you have recently had blood, blood products or another live vaccine'],
       dur='2 doses',
       seo_t='Varivax Chickenpox Vaccine 1,490 THB in Bangkok | HappiWell Clinic',
       seo_d=f'Varivax chickenpox vaccine for 1,490 baht per dose, for children from 1 year and adults without immunity. Doctor assessment before every shot. {CL_EN}.'),
  dict(name='ရေကျောက် ကာကွယ်ဆေး (Varivax)',
       short='ရေကျောက်ရောဂါကို ကာကွယ်သည်၊ အသက် ၁ နှစ်အထက် ကလေးများနှင့် ခုခံအားမရှိသေးသော အရွယ်ရောက်သူများအတွက် ၂ လုံး။',
       desc=['Varivax သည် ရေကျောက်ကို ကာကွယ်သော အားလျော့ထားသည့် ပိုးရှင် ကာကွယ်ဆေး ဖြစ်ပြီး အသက် ၁ နှစ်အထက် ကလေးများ၊ ဆယ်ကျော်သက်များနှင့် ရေကျောက် မဖြစ်ဖူး/ကာကွယ်ဆေး မထိုးဖူးသော အရွယ်ရောက်သူများ ထိုးနိုင်ပါသည်။',
             'စုစုပေါင်း ၂ လုံး ထိုးရပါမည်။ ကြားကာလသည် အသက်ပေါ် မူတည်ပြီး ဆရာဝန်က အချိန်ဇယား အကြံပေးပါမည်။'],
       suit=['ကာကွယ်ဆေးအချိန်ဇယားအတိုင်း အသက် ၁ နှစ်အထက် ကလေးများ', 'ရေကျောက် မဖြစ်ဖူးပြီး ကာကွယ်ဆေး မထိုးဖူးသော ဆယ်ကျော်သက်နှင့် အရွယ်ရောက်သူများ'],
       prec=['ကိုယ်ဝန်ဆောင်များနှင့် ခုခံအားကျနေသူများ မထိုးရပါ', 'ဆေးထိုးပြီးနောက် ဆရာဝန်အကြံပြုသည့် ကာလအတွင်း ကိုယ်ဝန်ရှောင်ပါ', 'မကြာမီက သွေး၊ သွေးထုတ်ကုန် (သို့) အခြား ပိုးရှင်ကာကွယ်ဆေး ရရှိခဲ့ပါက ဆရာဝန်ကို ပြောပြပါ'],
       dur='၂ လုံး',
       seo_t='ရေကျောက် ကာကွယ်ဆေး Varivax 1,490 ဘတ် ဘန်ကောက် | HappiWell',
       seo_d=f'Varivax ရေကျောက် ကာကွယ်ဆေး တစ်လုံး 1,490 ဘတ်၊ အသက် ၁ နှစ်အထက် ကလေးများနှင့် အရွယ်ရောက်သူများအတွက်။ {CL_MY}။')))

# ---------------- VAQTA (Hep A) ----------------
P.append(prog('hepatitis-a-vaccine-vaqta', 11, 1190, 'VAQTA', None,
  dict(name='วัคซีนไวรัสตับอักเสบเอ (VAQTA)',
       short='วัคซีนป้องกันไวรัสตับอักเสบเอ ฉีด 2 เข็ม ห่างกัน 6–18 เดือน สำหรับเด็กอายุ 1 ปีขึ้นไปและผู้ใหญ่',
       desc=['วัคซีน VAQTA เป็นวัคซีนชนิดเชื้อตาย ป้องกันโรคไวรัสตับอักเสบเอ ซึ่งติดต่อทางอาหารและน้ำดื่มที่ปนเปื้อน',
             'ฉีด 2 เข็ม ห่างกัน 6–18 เดือน ใช้ได้ในเด็กอายุ 1 ปีขึ้นไปและผู้ใหญ่ แพทย์จะประเมินว่าควรตรวจภูมิคุ้มกันก่อนฉีดหรือไม่'],
       suit=['เด็กอายุ 1 ปีขึ้นไป', 'ผู้ใหญ่ที่ยังไม่มีภูมิคุ้มกันต่อไวรัสตับอักเสบเอ', 'ผู้ที่ทำงานเกี่ยวกับอาหาร หรือจะเดินทางไปพื้นที่ที่มีโรคชุกชุม', 'ผู้ที่มีโรคตับเรื้อรัง ตามที่แพทย์แนะนำ'],
       prec=['ผู้ที่ตั้งครรภ์ควรปรึกษาแพทย์ก่อนฉีด', 'หากมีไข้หรือเจ็บป่วยเฉียบพลัน แพทย์อาจแนะนำให้เลื่อนการฉีด'],
       dur='2 เข็ม ห่างกัน 6–18 เดือน',
       seo_t='วัคซีนไวรัสตับอักเสบเอ VAQTA ราคา 1,190 บาท ทุ่งครุ | HappiWell',
       seo_d=f'วัคซีนไวรัสตับอักเสบเอ (VAQTA) เข็มละ 1,190 บาท ฉีด 2 เข็ม สำหรับเด็กอายุ 1 ปีขึ้นไปและผู้ใหญ่ ที่{CL_TH}'),
  dict(name='Hepatitis A vaccine (VAQTA)',
       short='Protects against hepatitis A. 2 doses, 6–18 months apart, for children from 1 year and adults.',
       desc=['VAQTA is an inactivated vaccine against hepatitis A, a liver infection spread through contaminated food and water.',
             'The course is 2 doses given 6–18 months apart, for children from 1 year of age and adults. The doctor will advise whether an immunity test is worthwhile before vaccination.'],
       suit=['Children aged 1 year and over', 'Adults who are not yet immune to hepatitis A', 'Food handlers and travellers to areas where hepatitis A is common', 'People with long-term liver disease, as advised by the doctor'],
       prec=['If you are pregnant, talk to the doctor before the injection', 'If you have a fever or acute illness, the doctor may advise postponing the injection'],
       dur='2 doses, 6–18 months apart',
       seo_t='VAQTA Hepatitis A Vaccine 1,190 THB in Bangkok | HappiWell Clinic',
       seo_d=f'Hepatitis A vaccine (VAQTA) for 1,190 baht per dose, 2-dose course for children from 1 year and adults. {CL_EN}.'),
  dict(name='အသည်းရောင် အေ ကာကွယ်ဆေး (VAQTA)',
       short='အသည်းရောင် အေ ကို ကာကွယ်သည်။ ၆–၁၈ လခြား၍ ၂ လုံး၊ အသက် ၁ နှစ်အထက် ကလေးများနှင့် အရွယ်ရောက်သူများအတွက်။',
       desc=['VAQTA သည် ညစ်ညမ်းသော အစားအစာနှင့် သောက်ရေမှတစ်ဆင့် ကူးစက်သော အသည်းရောင် အေ ကို ကာကွယ်သည့် ပိုးသေ ကာကွယ်ဆေး ဖြစ်ပါသည်။',
             '၆–၁၈ လခြား၍ ၂ လုံး ထိုးရပြီး အသက် ၁ နှစ်အထက် ကလေးများနှင့် အရွယ်ရောက်သူများ ထိုးနိုင်ပါသည်။ ဆေးမထိုးမီ ခုခံအား စစ်ဆေးသင့်မသင့်ကို ဆရာဝန်က အကြံပေးပါမည်။'],
       suit=['အသက် ၁ နှစ်အထက် ကလေးများ', 'အသည်းရောင် အေ ခုခံအား မရှိသေးသော အရွယ်ရောက်သူများ', 'အစားအစာနှင့်ပတ်သက်သော အလုပ်လုပ်သူများနှင့် ရောဂါများသော ဒေသသို့ ခရီးသွားမည့်သူများ', 'ဆရာဝန်အကြံပြုချက်အတိုင်း နာတာရှည် အသည်းရောဂါရှိသူများ'],
       prec=['ကိုယ်ဝန်ဆောင်ပါက ဆေးမထိုးမီ ဆရာဝန်နှင့် တိုင်ပင်ပါ', 'ဖျားနေခြင်း (သို့) ရုတ်တရက် နေမကောင်းဖြစ်နေပါက ဆရာဝန်က ဆေးထိုးချိန်ကို ရွှေ့ရန် အကြံပေးနိုင်ပါသည်'],
       dur='၆–၁၈ လခြား၍ ၂ လုံး',
       seo_t='အသည်းရောင် အေ ကာကွယ်ဆေး VAQTA 1,190 ဘတ် ဘန်ကောက် | HappiWell',
       seo_d=f'အသည်းရောင် အေ ကာကွယ်ဆေး (VAQTA) တစ်လုံး 1,190 ဘတ်၊ ကလေးနှင့် အရွယ်ရောက်သူများအတွက် ၂ လုံး။ {CL_MY}။')))

# ---------------- MMR II ----------------
P.append(prog('mmr-vaccine', 12, 650, 'M-M-R II', None,
  dict(name='วัคซีนหัด คางทูม หัดเยอรมัน (MMR)',
       short='วัคซีนรวมป้องกันโรคหัด คางทูม และหัดเยอรมัน สำหรับเด็กตามตารางวัคซีน และผู้ใหญ่ที่ยังไม่มีภูมิคุ้มกัน',
       desc=['วัคซีน M-M-R II เป็นวัคซีนรวมชนิดเชื้อเป็นอ่อนฤทธิ์ ป้องกันโรคหัด คางทูม และหัดเยอรมันในเข็มเดียว',
             'เด็กฉีดตามตารางวัคซีน ส่วนผู้ใหญ่ที่ไม่เคยได้รับวัคซีนหรือไม่แน่ใจ เช่น ผู้หญิงที่วางแผนจะตั้งครรภ์ แพทย์จะประเมินประวัติวัคซีนและแนะนำจำนวนเข็มที่ต้องฉีด'],
       suit=['เด็กตามตารางวัคซีน', 'ผู้ใหญ่ที่ไม่เคยได้รับวัคซีนหรือไม่แน่ใจประวัติวัคซีน', 'ผู้หญิงที่วางแผนจะตั้งครรภ์ (ฉีดก่อนตั้งครรภ์)'],
       prec=['ผู้ที่ตั้งครรภ์ หรือมีภูมิคุ้มกันบกพร่อง ห้ามฉีด', 'ผู้หญิงควรหลีกเลี่ยงการตั้งครรภ์หลังฉีดตามระยะเวลาที่แพทย์แนะนำ', 'แจ้งแพทย์หากเพิ่งได้รับเลือด ผลิตภัณฑ์จากเลือด หรือวัคซีนเชื้อเป็นชนิดอื่น'],
       seo_t='วัคซีน MMR หัด คางทูม หัดเยอรมัน ราคา 650 บาท ทุ่งครุ | HappiWell',
       seo_d=f'วัคซีนหัด คางทูม หัดเยอรมัน (MMR) เข็มละ 650 บาท สำหรับเด็กและผู้ใหญ่ที่ยังไม่มีภูมิ แพทย์ประเมินก่อนฉีด ที่{CL_TH}'),
  dict(name='Measles, mumps and rubella vaccine (MMR)',
       short='A combined vaccine against measles, mumps and rubella, for children on the vaccination schedule and adults without immunity.',
       desc=['M-M-R II is a live attenuated combined vaccine that protects against measles, mumps and rubella in a single injection.',
             'Children receive it on the vaccination schedule. For adults who have never been vaccinated or are unsure — for example women planning a pregnancy — the doctor will review your history and advise how many doses you need.'],
       suit=['Children, following the vaccination schedule', 'Adults who have never been vaccinated or are unsure of their vaccination history', 'Women planning a pregnancy (vaccinate before pregnancy)'],
       prec=['Not for pregnant women or people with a weakened immune system', 'Women should avoid pregnancy after vaccination for the period advised by the doctor', 'Tell the doctor if you have recently had blood, blood products or another live vaccine'],
       seo_t='MMR Vaccine (Measles, Mumps, Rubella) 650 THB, Bangkok | HappiWell',
       seo_d=f'MMR vaccine against measles, mumps and rubella for 650 baht per dose, for children and adults without immunity. {CL_EN}.'),
  dict(name='ဝက်သက်၊ ပါးချိတ်ရောင်၊ ဂျိုက်သိုး ကာကွယ်ဆေး (MMR)',
       short='ဝက်သက်၊ ပါးချိတ်ရောင်နှင့် ဂျိုက်သိုး (Rubella) ကို ကာကွယ်သော ပေါင်းစပ်ကာကွယ်ဆေး၊ ကလေးများနှင့် ခုခံအားမရှိသေးသော အရွယ်ရောက်သူများအတွက်။',
       desc=['M-M-R II သည် ဝက်သက်၊ ပါးချိတ်ရောင်နှင့် ဂျိုက်သိုးကို တစ်လုံးတည်းဖြင့် ကာကွယ်ပေးသော အားလျော့ထားသည့် ပိုးရှင် ပေါင်းစပ်ကာကွယ်ဆေး ဖြစ်ပါသည်။',
             'ကလေးများသည် ကာကွယ်ဆေးအချိန်ဇယားအတိုင်း ထိုးရပါမည်။ မထိုးဖူးသော (သို့) မသေချာသော အရွယ်ရောက်သူများ — ဥပမာ ကိုယ်ဝန်ယူရန် စီစဉ်နေသော အမျိုးသမီးများ — အတွက် ဆရာဝန်က ရာဇဝင်ကို ကြည့်ပြီး ထိုးရမည့်အရေအတွက်ကို အကြံပေးပါမည်။'],
       suit=['ကာကွယ်ဆေးအချိန်ဇယားအတိုင်း ကလေးများ', 'မထိုးဖူးသော (သို့) ထိုးဖူးမှု မသေချာသော အရွယ်ရောက်သူများ', 'ကိုယ်ဝန်ယူရန် စီစဉ်နေသော အမျိုးသမီးများ (ကိုယ်ဝန်မရှိမီ ထိုးရန်)'],
       prec=['ကိုယ်ဝန်ဆောင်များနှင့် ခုခံအားကျနေသူများ မထိုးရပါ', 'ဆေးထိုးပြီးနောက် ဆရာဝန်အကြံပြုသည့် ကာလအတွင်း ကိုယ်ဝန်ရှောင်ပါ', 'မကြာမီက သွေး၊ သွေးထုတ်ကုန် (သို့) အခြား ပိုးရှင်ကာကွယ်ဆေး ရရှိခဲ့ပါက ဆရာဝန်ကို ပြောပြပါ'],
       seo_t='MMR ကာကွယ်ဆေး (ဝက်သက်၊ ပါးချိတ်ရောင်၊ ဂျိုက်သိုး) 650 ဘတ် | HappiWell',
       seo_d=f'MMR ကာကွယ်ဆေး တစ်လုံး 650 ဘတ်၊ ကလေးများနှင့် ခုခံအားမရှိသေးသော အရွယ်ရောက်သူများအတွက်။ {CL_MY}။')))

# ---------------- ProQuad (MMRV) ----------------
P.append(prog('mmrv-vaccine-proquad', 13, 2590, 'ProQuad (MMRV)', None,
  dict(name='วัคซีนหัด คางทูม หัดเยอรมัน อีสุกอีใส (ProQuad)',
       short='วัคซีนรวม 4 โรค (MMR + อีสุกอีใส) ในเข็มเดียว สำหรับเด็กอายุ 1–12 ปี ช่วยลดจำนวนครั้งที่ต้องฉีด',
       desc=['วัคซีน ProQuad (MMRV) รวมการป้องกันโรคหัด คางทูม หัดเยอรมัน และอีสุกอีใสไว้ในเข็มเดียว ใช้ในเด็กอายุ 1–12 ปี',
             'แพทย์จะดูประวัติวัคซีนของเด็กและแนะนำว่าควรใช้ ProQuad หรือฉีด MMR กับวัคซีนอีสุกอีใสแยกกัน ให้เหมาะกับเด็กแต่ละคน'],
       suit=['เด็กอายุ 1–12 ปี ตามตารางวัคซีน'],
       prec=['แจ้งแพทย์หากเด็กหรือคนในครอบครัวมีประวัติชัก', 'เด็กที่มีภูมิคุ้มกันบกพร่อง ห้ามฉีด', 'แจ้งแพทย์หากเด็กเพิ่งได้รับเลือด ผลิตภัณฑ์จากเลือด หรือวัคซีนเชื้อเป็นชนิดอื่น'],
       seo_t='วัคซีน MMRV ProQuad หัด คางทูม หัดเยอรมัน อีสุกอีใส 2,590 บาท | HappiWell',
       seo_d=f'วัคซีนรวม 4 โรค ProQuad (MMRV) เข็มละ 2,590 บาท สำหรับเด็กอายุ 1–12 ปี แพทย์ประเมินก่อนฉีด ที่{CL_TH}'),
  dict(name='Measles, mumps, rubella and chickenpox vaccine (ProQuad)',
       short='A 4-in-1 vaccine (MMR + chickenpox) in a single injection for children aged 1–12, meaning fewer injections.',
       desc=['ProQuad (MMRV) combines protection against measles, mumps, rubella and chickenpox in one injection, for children aged 1–12 years.',
             "The doctor will review your child's vaccination history and advise whether ProQuad or separate MMR and chickenpox vaccines suit your child best."],
       suit=['Children aged 1–12, following the vaccination schedule'],
       prec=['Tell the doctor if your child or a family member has a history of seizures', 'Not for children with a weakened immune system', 'Tell the doctor if your child has recently had blood, blood products or another live vaccine'],
       seo_t='ProQuad MMRV Vaccine 2,590 THB for Children, Bangkok | HappiWell',
       seo_d=f'ProQuad (MMRV) 4-in-1 vaccine against measles, mumps, rubella and chickenpox for 2,590 baht per dose, for children aged 1–12. {CL_EN}.'),
  dict(name='ဝက်သက်၊ ပါးချိတ်ရောင်၊ ဂျိုက်သိုး၊ ရေကျောက် ကာကွယ်ဆေး (ProQuad)',
       short='ရောဂါ ၄ မျိုး (MMR + ရေကျောက်) ကို တစ်လုံးတည်းဖြင့် ကာကွယ်သည်၊ အသက် ၁–၁၂ နှစ် ကလေးများအတွက်။',
       desc=['ProQuad (MMRV) သည် ဝက်သက်၊ ပါးချိတ်ရောင်၊ ဂျိုက်သိုးနှင့် ရေကျောက်ကို တစ်လုံးတည်းဖြင့် ကာကွယ်ပေးပြီး အသက် ၁–၁၂ နှစ် ကလေးများ ထိုးနိုင်ပါသည်။',
             'ဆရာဝန်က ကလေး၏ ကာကွယ်ဆေးရာဇဝင်ကို ကြည့်ပြီး ProQuad (သို့) MMR နှင့် ရေကျောက်ကာကွယ်ဆေးကို သီးခြားထိုးခြင်း မည်သည်က ပိုသင့်တော်ကြောင်း အကြံပေးပါမည်။'],
       suit=['ကာကွယ်ဆေးအချိန်ဇယားအတိုင်း အသက် ၁–၁၂ နှစ် ကလေးများ'],
       prec=['ကလေး (သို့) မိသားစုဝင်တွင် တက်ခြင်းရာဇဝင် ရှိပါက ဆရာဝန်ကို ပြောပြပါ', 'ခုခံအားကျနေသော ကလေးများ မထိုးရပါ', 'ကလေးသည် မကြာမီက သွေး၊ သွေးထုတ်ကုန် (သို့) အခြား ပိုးရှင်ကာကွယ်ဆေး ရရှိခဲ့ပါက ဆရာဝန်ကို ပြောပြပါ'],
       seo_t='ProQuad MMRV ကာကွယ်ဆေး ကလေးများအတွက် 2,590 ဘတ် | HappiWell',
       seo_d=f'ProQuad (MMRV) ရောဂါ ၄ မျိုး ကာကွယ်ဆေး တစ်လုံး 2,590 ဘတ်၊ အသက် ၁–၁၂ နှစ် ကလေးများအတွက်။ {CL_MY}။')))


# ---------------- Article: pneumonia-vaccine-2569 ----------------
def blocks(items):
    out = []
    for i, it in enumerate(items):
        kind, val = it
        bid = f'pv{i}'
        if kind == 'p':
            out.append({'id': bid, 'type': 'paragraph', 'data': {'text': val}})
        elif kind == 'h2':
            out.append({'id': bid, 'type': 'header', 'data': {'text': val, 'level': 2}})
        elif kind == 'h3':
            out.append({'id': bid, 'type': 'header', 'data': {'text': val, 'level': 3}})
        elif kind == 'ul':
            out.append({'id': bid, 'type': 'list', 'data': {'style': 'unordered', 'items': val}})
    return json.dumps({'time': 1793500000000, 'version': '2.29.1', 'blocks': out}, ensure_ascii=False)

ART_TH = dict(
  title='วัคซีนปอดอักเสบ (ไอพีดี) PCV15 และ PPSV23 จำเป็นแค่ไหน ฉีดกี่เข็ม ราคาเท่าไหร่ (อัปเดตปี 2569)',
  excerpt='วัคซีนปอดอักเสบ (ไอพีดี) Vaxneuvance PCV15 และ Pneumovax 23 ป้องกันอะไร ใครควรฉีด ฉีดกี่เข็ม พร้อมราคาที่แฮปปี้เวลล์ คลินิก ทุ่งครุ',
  seo_title='วัคซีนปอดอักเสบ PCV15 + PPSV23 จำเป็นไหม ฉีดกี่เข็ม ราคาเท่าไหร่ (2569)',
  seo_description='วัคซีนปอดอักเสบ (ไอพีดี) Vaxneuvance PCV15 และ Pneumovax 23 ป้องกันอะไร ใครควรฉีด ฉีดกี่เข็ม พร้อมราคาที่แฮปปี้เวลล์ คลินิกเวชกรรม ทุ่งครุ',
  content=blocks([
    ('p', 'ปอดอักเสบเป็นโรคที่หลายคนคิดว่าเป็นแค่ภาวะแทรกซ้อนของไข้หวัด แต่เชื้อแบคทีเรียนิวโมคอคคัสที่เป็นสาเหตุหลักสามารถก่อโรครุนแรงได้หลายแบบ ตั้งแต่หูชั้นกลางอักเสบไปจนถึงเยื่อหุ้มสมองอักเสบและติดเชื้อในกระแสเลือด บทความนี้จะพาไปดูว่าวัคซีนปอดอักเสบช่วยป้องกันได้อย่างไร และใครควรฉีดเป็นพิเศษ'),
    ('h2', 'เชื้อนิวโมคอคคัสอันตรายแค่ไหน'),
    ('p', 'เชื้อแบคทีเรียนิวโมคอคคัส (Pneumococcus) เป็นสาเหตุของกลุ่มโรคที่เรียกว่าไอพีดี (IPD - Invasive Pneumococcal Disease) ซึ่งครอบคลุมตั้งแต่ปอดอักเสบ เยื่อหุ้มสมองอักเสบ ติดเชื้อในกระแสเลือด ไปจนถึงหูชั้นกลางอักเสบและไซนัสอักเสบ เชื้อตัวนี้ยังชอบแทรกซ้อนร่วมกับการติดเชื้อไวรัสอย่างไข้หวัดใหญ่หรือโควิด-19 ทำให้อาการรุนแรงขึ้น'),
    ('h2', 'ใครเสี่ยงอาการรุนแรงเป็นพิเศษ'),
    ('ul', ['เด็กอายุต่ำกว่า 2 ปี', 'ผู้สูงอายุ 65 ปีขึ้นไป', 'ผู้ที่ได้รับยาหรือการรักษาที่กระทบภูมิคุ้มกัน เช่น เคมีบำบัด หรือใช้สเตียรอยด์ระยะยาว', 'ผู้มีโรคประจำตัวเรื้อรัง เช่น โรคไต โรคปอด โรคหัวใจ เบาหวาน มะเร็งเม็ดเลือด และผู้ติดเชื้อ HIV']),
    ('h2', 'วัคซีนปอดอักเสบมีกี่ชนิด'),
    ('p', '<b>PCV15 (Vaxneuvance)</b> เป็นวัคซีนชนิดคอนจูเกต ป้องกันเชื้อนิวโมคอคคัส 15 สายพันธุ์ กระตุ้นภูมิคุ้มกันได้ดีและเป็นเข็มแรกของการฉีดในผู้ใหญ่'),
    ('p', '<b>PPSV23 (Pneumovax 23)</b> เป็นวัคซีนชนิดโพลีแซคคาไรด์ ป้องกัน 23 สายพันธุ์ ใช้ฉีดต่อจาก PCV15 เพื่อขยายความครอบคลุมสายพันธุ์ให้กว้างขึ้น'),
    ('h2', 'ใครควรฉีด ฉีดกี่เข็ม'),
    ('p', 'สำหรับผู้ใหญ่ที่ไม่เคยฉีดวัคซีนไอพีดีมาก่อน คำแนะนำทั่วไปคือฉีด <b>PCV15 1 เข็ม แล้วตามด้วย PPSV23 อีก 1 เข็ม</b> โดยทั่วไปห่างกันอย่างน้อย 1 ปี ในบางกลุ่ม เช่น ผู้มีภูมิคุ้มกันบกพร่อง แพทย์อาจพิจารณาให้ห่างกันน้อยกว่านั้น กลุ่มที่แนะนำให้ฉีดเป็นพิเศษคือ'),
    ('ul', ['ผู้สูงอายุ 65 ปีขึ้นไปทุกคน', 'ผู้มีโรคเรื้อรังหรือภูมิคุ้มกันบกพร่องตามที่กล่าวมาข้างต้น ไม่ว่าอายุเท่าไหร่']),
    ('p', 'ผู้ที่เคยฉีดวัคซีนไอพีดีมาแล้ว ควรนำประวัติวัคซีนมาให้แพทย์ดู เพื่อวางแผนว่าต้องฉีดเข็มไหนต่อและเมื่อไร'),
    ('h2', 'ราคาที่แฮปปี้เวลล์ คลินิก'),
    ('p', 'ที่ <b>แฮปปี้เวลล์ คลินิกเวชกรรม</b> ย่านทุ่งครุ วัคซีน <b>Vaxneuvance (PCV15) ราคา 2,690 บาทต่อเข็ม</b> และ <b>Pneumovax 23 (PPSV23) ราคา 1,590 บาทต่อเข็ม</b> แพทย์ให้คำปรึกษาก่อนฉีดทุกครั้งว่าเหมาะกับสุขภาพและประวัติการฉีดวัคซีนเดิมหรือไม่'),
    ('p', 'สนใจนัดฉีดวัคซีนปอดอักเสบ ทักแชทหรือโทรสอบถามคิวได้ที่คลินิกแฮปปี้เวลล์ เปิดบริการทุกวัน จันทร์–ศุกร์ 08.00–18.00 น. เสาร์–อาทิตย์ 08.00–12.00 น.'),
    ('h2', 'คำถามที่พบบ่อย'),
    ('p', '<b>ฉีดวัคซีนไข้หวัดใหญ่กับวัคซีนปอดอักเสบพร้อมกันได้ไหม</b><br>โดยทั่วไปฉีดพร้อมกันได้ในคนละตำแหน่งแขน และยังช่วยลดความเสี่ยงภาวะแทรกซ้อนที่เชื้อนิวโมคอคคัสมักมาซ้ำเติมตอนเป็นไข้หวัดใหญ่ ควรให้แพทย์ประเมินก่อนเสมอ'),
    ('p', '<b>ต้องฉีดทั้ง PCV15 และ PPSV23 ไหม</b><br>ผู้ใหญ่ส่วนใหญ่ที่เริ่มด้วย PCV15 จะได้รับคำแนะนำให้ฉีด PPSV23 ต่ออีก 1 เข็ม เพื่อให้ครอบคลุมสายพันธุ์มากขึ้น แพทย์จะแนะนำตามอายุและโรคประจำตัว'),
    ('p', '<b>เคยฉีด PCV13 มาแล้ว ต้องทำอย่างไรต่อ</b><br>ขึ้นอยู่กับว่าเคยฉีด PPSV23 แล้วหรือยัง และฉีดเมื่อไร ควรนำประวัติวัคซีนมาให้แพทย์ประเมิน'),
    ('p', '<b>อายุยังไม่ถึง 65 ปี และไม่มีโรคประจำตัว ยังฉีดได้ไหม</b><br>ฉีดได้ หากต้องการป้องกันไว้ก่อนสามารถปรึกษาแพทย์ได้'),
    ('h2', 'สรุป'),
    ('p', 'เชื้อนิวโมคอคคัสก่อโรคได้ตั้งแต่ไม่รุนแรงไปจนถึงอันตรายถึงชีวิต โดยเฉพาะในผู้สูงอายุและผู้มีโรคเรื้อรัง การฉีด PCV15 ตามด้วย PPSV23 ช่วยให้ป้องกันได้ครอบคลุม หากอายุ 65 ปีขึ้นไปหรือมีโรคประจำตัวที่เพิ่มความเสี่ยง แนะนำให้ปรึกษาแพทย์เพื่อวางแผนการฉีด'),
    ('h3', 'แหล่งอ้างอิง'),
    ('ul', ['<a href="https://www.cdc.gov/mmwr/volumes/71/wr/mm7104a1.htm">CDC MMWR – Use of PCV15 and PCV20 among U.S. adults (ACIP)</a>', '<a href="https://ddc.moph.go.th/">กรมควบคุมโรค กระทรวงสาธารณสุข</a>']),
    ('p', '<i>บทความนี้จัดทำเพื่อให้ข้อมูลทั่วไป ไม่ใช่คำแนะนำทางการแพทย์เฉพาะบุคคล ควรปรึกษาแพทย์ก่อนตัดสินใจฉีดวัคซีนทุกครั้ง</i>'),
  ]))

ART_EN = dict(
  title='Pneumococcal Vaccines (PCV15 and PPSV23): Do You Need Them, How Many Doses and How Much? (2026 Update)',
  excerpt='What the Vaxneuvance (PCV15) and Pneumovax 23 pneumococcal vaccines protect against, who should get them, how many doses, and the price at HappiWell Clinic, Thung Khru.',
  seo_title='PCV15 + PPSV23 Pneumococcal Vaccines: Who Needs Them & Price (2026) | HappiWell',
  seo_description='What Vaxneuvance (PCV15) and Pneumovax 23 protect against, who should get them, how many doses, and the price at HappiWell Medical Clinic, Thung Khru, Bangkok.',
  content=blocks([
    ('p', 'Many people think pneumonia is just a complication of a cold, but pneumococcus — the main bacterial cause — can cause many serious illnesses, from middle ear infections to meningitis and bloodstream infection. This article explains how pneumococcal vaccines protect you and who should especially get them.'),
    ('h2', 'How dangerous is pneumococcus?'),
    ('p', 'Pneumococcus bacteria cause a group of illnesses called invasive pneumococcal disease (IPD), which includes pneumonia, meningitis and bloodstream infection, as well as middle ear infections and sinusitis. It often strikes on top of viral infections such as flu or COVID-19, making them more severe.'),
    ('h2', 'Who is at higher risk of severe illness?'),
    ('ul', ['Children under 2', 'Adults aged 65 and over', 'People receiving medicines or treatments that weaken immunity, such as chemotherapy or long-term steroids', 'People with long-term conditions such as kidney disease, lung disease, heart disease, diabetes, blood cancers, or HIV']),
    ('h2', 'What types of pneumococcal vaccine are there?'),
    ('p', '<b>PCV15 (Vaxneuvance)</b> is a conjugate vaccine covering 15 pneumococcal types. It produces a strong immune response and is the first dose of the adult schedule.'),
    ('p', '<b>PPSV23 (Pneumovax 23)</b> is a polysaccharide vaccine covering 23 types. It is given after PCV15 to broaden the range of types covered.'),
    ('h2', 'Who should get it, and how many doses?'),
    ('p', 'For adults who have never had a pneumococcal vaccine, the usual recommendation is <b>1 dose of PCV15 followed by 1 dose of PPSV23</b>, generally at least 1 year apart. For some groups, such as people with weakened immunity, the doctor may use a shorter interval. It is especially recommended for:'),
    ('ul', ['All adults aged 65 and over', 'People of any age with the long-term conditions or weakened immunity listed above']),
    ('p', 'If you have had a pneumococcal vaccine before, bring your vaccination record so the doctor can plan which dose you need next, and when.'),
    ('h2', 'Price at HappiWell Clinic'),
    ('p', 'At <b>HappiWell Medical Clinic</b> in Thung Khru, <b>Vaxneuvance (PCV15) costs 2,690 baht per dose</b> and <b>Pneumovax 23 (PPSV23) costs 1,590 baht per dose</b>, with a doctor’s consultation before every injection to check it suits your health and vaccination history.'),
    ('p', 'To book your pneumococcal vaccine, message us on LINE or call HappiWell Clinic. We are open every day: Monday–Friday 08:00–18:00 and Saturday–Sunday 08:00–12:00.'),
    ('h2', 'Frequently asked questions'),
    ('p', '<b>Can I have the flu vaccine and the pneumococcal vaccine at the same time?</b><br>Usually yes, in different arms. It also helps reduce the risk of pneumococcal complications that often follow flu. Always let a doctor assess you first.'),
    ('p', '<b>Do I need both PCV15 and PPSV23?</b><br>Most adults who start with PCV15 are advised to have one dose of PPSV23 afterwards for broader coverage. The doctor will advise based on your age and health conditions.'),
    ('p', '<b>I have already had PCV13. What should I do next?</b><br>It depends on whether — and when — you have had PPSV23. Bring your vaccination record for the doctor to review.'),
    ('p', '<b>I am under 65 with no long-term conditions. Can I still have it?</b><br>Yes. If you want to be protected, talk to a doctor.'),
    ('h2', 'Summary'),
    ('p', 'Pneumococcus causes illnesses ranging from mild to life-threatening, especially in older adults and people with long-term conditions. PCV15 followed by PPSV23 gives broad protection. If you are 65 or over, or have a condition that raises your risk, talk to a doctor about planning your vaccination.'),
    ('h3', 'References'),
    ('ul', ['<a href="https://www.cdc.gov/mmwr/volumes/71/wr/mm7104a1.htm">CDC MMWR – Use of PCV15 and PCV20 among U.S. adults (ACIP)</a>', '<a href="https://ddc.moph.go.th/">Department of Disease Control, Ministry of Public Health (Thai)</a>']),
    ('p', '<i>This article is for general information and is not personal medical advice. Always talk to a doctor before deciding on any vaccination.</i>'),
  ]))

if __name__ == '__main__':
    out = {'programs': P, 'article': {'slug': 'pneumonia-vaccine-2569', 'th': ART_TH, 'en': ART_EN}}
    path = pathlib.Path(__file__).with_name('vaccines_2569.json')
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print('ok', path, len(P), 'programs')

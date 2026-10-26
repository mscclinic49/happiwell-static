# -*- coding: utf-8 -*-
"""หน้าโปรแกรม: ตรวจสุขภาพแรงงานต่างด้าว (ทำใบอนุญาตทำงาน) — ไทย + อังกฤษ + พม่า + SEO
ราคา: สอบถามทาง LINE (ยังไม่ใส่ราคา)
รัน: python3 supabase/seed/posts/work_permit.py → พิมพ์ SQL เป็นชิ้นเล็ก ๆ
"""
import json

SLUG = 'work-permit-health-check'

def desc(*paras):
    return json.dumps({'time': 1793000000000, 'version': '2.29.1', 'blocks': [
        {'id': f'w{i}', 'type': 'paragraph', 'data': {'text': t}} for i, t in enumerate(paras)]}, ensure_ascii=False)

TH = dict(
  slug=SLUG, category='certificate', price=None, sort_order=1, is_featured=True, is_published=True,
  name='ตรวจสุขภาพแรงงานต่างด้าว (ทำใบอนุญาตทำงาน)',
  short_desc='ตรวจสุขภาพและออกใบรับรองแพทย์สำหรับแรงงานต่างด้าวที่ยื่นขอหรือต่อใบอนุญาตทำงาน สอบถามราคาทาง LINE',
  price_note='สอบถามราคาและรายการตรวจทาง LINE @p49clinic',
  description=desc('ตรวจสุขภาพโดยแพทย์และออกใบรับรองแพทย์สำหรับแรงงานต่างด้าวที่ต้องยื่นขอหรือต่ออายุใบอนุญาตทำงาน (Work Permit) รายการตรวจเป็นไปตามแบบฟอร์มที่ทางราชการกำหนด',
                   'ทัก LINE แจ้งชื่อเอกสารที่ต้องใช้และจำนวนคน เพื่อสอบถามราคาและนัดวันตรวจ นายจ้างที่ต้องพาแรงงานมาตรวจหลายคนก็ทักมาสอบถามได้'),
  suitable_for=['แรงงานต่างด้าวที่ยื่นขอหรือต่ออายุใบอนุญาตทำงาน', 'นายจ้างที่ต้องพาแรงงานมาตรวจสุขภาพ'],
  includes=['ตรวจร่างกายโดยแพทย์', 'ใบรับรองแพทย์สำหรับยื่นขอใบอนุญาตทำงาน'],
  precautions=['นำพาสปอร์ตหรือเอกสารประจำตัวแรงงานตัวจริงมาด้วย', 'ทัก LINE สอบถามราคาและรายการตรวจก่อนเข้ารับบริการ'],
  seo_title='ตรวจสุขภาพแรงงานต่างด้าว ใบอนุญาตทำงาน ทุ่งครุ | HappiWell',
  seo_description='ตรวจสุขภาพและใบรับรองแพทย์สำหรับแรงงานต่างด้าว ยื่นขอหรือต่อใบอนุญาตทำงาน ที่แฮปปี้เวลล์ คลินิกเวชกรรม ซ.ประชาอุทิศ 49 ทุ่งครุ สอบถามราคาทาง LINE',
)
EN = dict(
  name='Work permit health check for migrant workers',
  short_desc='Health check and medical certificate for migrant workers applying for or renewing a Thai work permit. Ask us on LINE for the price.',
  price_note='Ask about the price and tests on LINE @p49clinic',
  description=desc('A health check by a doctor and a medical certificate for migrant workers applying for or renewing a work permit in Thailand. The checks follow the official government form.',
                   'Message us on LINE with the document you need and the number of people to ask about the price and book a date. Employers bringing several workers are welcome to ask too.'),
  suitable_for=['Migrant workers applying for or renewing a work permit', 'Employers who need to bring workers for a health check'],
  includes=['Physical examination by a doctor', 'Medical certificate for your work permit application'],
  precautions=['Bring your original passport or worker identity document', 'Ask about the price and tests on LINE before your visit'],
  seo_title='Work Permit Health Check for Migrant Workers, Bangkok | HappiWell',
  seo_description='Health check and medical certificate for migrant workers applying for or renewing a Thai work permit. HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok. Ask on LINE.',
)
MY = dict(
  name='အလုပ်လုပ်ခွင့် (Work Permit) ကျန်းမာရေးစစ်ဆေးမှု',
  short_desc='ရွှေ့ပြောင်းအလုပ်သမားများ အလုပ်လုပ်ခွင့် လျှောက်ရန် (သို့) သက်တမ်းတိုးရန် ကျန်းမာရေးစစ်ဆေးပြီး ဆေးလက်မှတ် ထုတ်ပေးပါသည်။ ဈေးနှုန်းကို LINE တွင် မေးပါ။',
  price_note='ဈေးနှုန်းနှင့် စစ်ဆေးမှုများကို LINE @p49clinic တွင် မေးပါ',
  description=desc('ထိုင်းနိုင်ငံတွင် အလုပ်လုပ်ခွင့် (Work Permit) လျှောက်ရန် (သို့) သက်တမ်းတိုးရန် လိုအပ်သော ရွှေ့ပြောင်းအလုပ်သမားများအတွက် ဆရာဝန်က ကျန်းမာရေးစစ်ဆေးပြီး ဆေးလက်မှတ် ထုတ်ပေးပါသည်။ စစ်ဆေးမှုများသည် အစိုးရ သတ်မှတ်ထားသော ပုံစံအတိုင်း ဖြစ်ပါသည်။',
                   'ဈေးနှုန်းမေးရန်နှင့် ရက်ချိန်းယူရန် လိုအပ်သော စာရွက်စာတမ်းအမည်နှင့် လူဦးရေကို LINE တွင် ပို့ပါ။ အလုပ်သမားအများအပြား ခေါ်လာမည့် အလုပ်ရှင်များလည်း မေးမြန်းနိုင်ပါသည်။'),
  suitable_for=['အလုပ်လုပ်ခွင့် လျှောက်မည် (သို့) သက်တမ်းတိုးမည့် ရွှေ့ပြောင်းအလုပ်သမားများ', 'အလုပ်သမားများကို ကျန်းမာရေးစစ်ဆေးရန် ခေါ်လာမည့် အလုပ်ရှင်များ'],
  includes=['ဆရာဝန်က ကိုယ်ခန္ဓာစစ်ဆေးခြင်း', 'အလုပ်လုပ်ခွင့် လျှောက်ရန် ဆေးလက်မှတ်'],
  precautions=['ပတ်စ်ပို့ (သို့) အလုပ်သမား သက်သေခံကတ် မူရင်းကို ယူလာပါ', 'မလာမီ ဈေးနှုန်းနှင့် စစ်ဆေးမှုများကို LINE တွင် မေးပါ'],
  seo_title='အလုပ်လုပ်ခွင့် ကျန်းမာရေးစစ်ဆေးမှု ဘန်ကောက် | HappiWell ဆေးခန်း',
  seo_description='ရွှေ့ပြောင်းအလုပ်သမားများ ထိုင်းအလုပ်လုပ်ခွင့် လျှောက်ရန် ကျန်းမာရေးစစ်ဆေးမှုနှင့် ဆေးလက်မှတ်။ HappiWell ဆေးခန်း၊ Soi Pracha Uthit 49၊ Thung Khru၊ ဘန်ကောက်။ LINE တွင် မေးပါ။',
)

def q(v): return '$j$' + (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)) + '$j$'
def arr(v): return f"array(select jsonb_array_elements_text({q(v)}::jsonb))"

def sql():
    t = TH
    out = [f"insert into public.hw_programs (slug, category, price, sort_order, is_featured, is_published, name, short_desc, price_note, suitable_for, includes, precautions, seo_title, seo_description) values "
           f"('{SLUG}', 'certificate', null, 1, true, true, {q(t['name'])}, {q(t['short_desc'])}, {q(t['price_note'])}, {arr(t['suitable_for'])}, {arr(t['includes'])}, {arr(t['precautions'])}, {q(t['seo_title'])}, {q(t['seo_description'])}) on conflict (slug) do nothing;",
           f"update public.hw_programs set description = {q(t['description'])} where slug = '{SLUG}';"]
    for col, d in (('en', EN), ('my', MY)):
        keys = list(d)
        for i in range(0, len(keys), 3):
            part = {k: d[k] for k in keys[i:i + 3]}
            out.append(f"update public.hw_programs set {col} = {col} || {q(part)}::jsonb where slug = '{SLUG}';")
    return out

if __name__ == '__main__':
    for s in sql():
        print(f'-- {len(s.encode())} bytes\n{s}\n')

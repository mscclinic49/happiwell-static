"""คำแปลภาษาอังกฤษของหมวดหมู่และโปรแกรม → programs_en.sql (อัปเดตคอลัมน์ en)
รัน: python3 supabase/seed/programs_en.py
หมายเหตุ: options เรียงตามลำดับเดียวกับภาษาไทย (ราคาใช้จากภาษาไทย)
"""
import json, pathlib

def desc(*paras):
    return json.dumps({"time": 1792600000000, "blocks": [
        {"id": f"e{i}", "type": "paragraph", "data": {"text": p}} for i, p in enumerate(paras)], "version": "2.29.1"}, ensure_ascii=False)

CATS = {
    'vaccine': {'name': 'Vaccines', 'description': 'Vaccines for adults and children, given by a doctor with an assessment before every injection'},
    'checkup': {'name': 'Health check-ups', 'description': 'Annual health check-up packages and individual blood tests'},
    'chronic-care': {'name': 'Chronic & elderly care', 'description': 'Ongoing care for chronic conditions and older adults, close to home'},
    'family-planning': {'name': 'Contraception', 'description': 'Contraceptive injections and family planning advice'},
    'procedure': {'name': 'Procedures', 'description': 'Wound care, stitches, nebuliser treatment and other procedures'},
    'certificate': {'name': 'Medical certificates', 'description': 'Medical certificates for jobs, driving licences and more'},
    'sexual-health': {'name': 'Sexual health', 'description': 'Confidential screening and counselling'},
}

VAX_INCL = ['Doctor’s history check and assessment before the injection', 'Vaccine and injection fee', 'Observation at the clinic after the injection']
FAST = 'Fast for 8–10 hours before the blood test; plain water is fine (morning visits recommended)'
BASE = [
    'Blood sugar (FBS) — diabetes screening',
    'Blood fats, 4 values — total cholesterol, triglycerides, “good” cholesterol (HDL), “bad” cholesterol (LDL)',
    'Kidney function, 3 values — BUN, creatinine, kidney filtration rate (eGFR)',
    'Uric acid — gout risk',
]
CBC = 'Complete blood count (CBC) — anaemia and infection'
HEPB = 'Hepatitis B, 2 values — infection (HBsAg) and immunity (HBsAb)'
VDRL = 'Syphilis (VDRL)'
UA = 'Urine test (UA)'
BMI = 'Weight, height and body mass index (BMI)'
READ = 'Results explained by a doctor, with advice'
BIG_EXTRA = ['Blood group (ABO and Rh)', 'Blood calcium', 'Liver cancer marker (AFP)', 'Digestive tract cancer marker (CEA)']

P = {
  'flu-vaccine': dict(
    name='Quadrivalent flu vaccine',
    short_desc='One dose a year for adults and children aged 9 and over. A doctor assesses you before every injection.',
    description=desc('The quadrivalent (4-strain) flu vaccine is recommended every year, because protection fades over time and the circulating strains change each year.',
                     'Adults and children aged 9 and over need one dose a year. Children under 9 having their first flu vaccine may need 2 doses at least 4 weeks apart, as advised by the doctor.'),
    price_unit='per dose',
    suitable_for=['Everyone aged 6 months and over', 'Adults aged 65 and over', 'Pregnant women (any trimester)', 'People with long-term conditions such as diabetes, heart or lung disease'],
    includes=VAX_INCL,
    precautions=['If you have a fever or acute illness, the doctor may advise postponing the injection', 'Tell the doctor if you have ever been allergic to a vaccine or its ingredients'],
    seo_title='Flu Vaccine 390 THB in Thung Khru, Bangkok | HappiWell Clinic',
    seo_description='Quadrivalent flu vaccine for 390 baht per dose at HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok. Doctor assessment before every shot. Open daily, book via LINE.'),
  'dengue-vaccine-qdenga': dict(
    name='Dengue vaccine (Qdenga)',
    short_desc='2 doses, 3 months apart, for anyone aged 4 and over. You can pay per dose.',
    description=desc('Qdenga (TAK-003) is a dengue vaccine widely used in Thailand. It is registered for people aged 4 years and over.',
                     'The course is 2 doses given 3 months apart. If the second dose is late, you do not need to restart — simply get it as soon as you can.'),
    price_unit='per dose', price_note='Full 2-dose course: 3,450 baht',
    options=[{'label': '1 dose (pay per dose)', 'note': 'The full course is 2 doses, 3 months apart'}, {'label': '2-dose course', 'note': 'Pay once for the full course'}],
    suitable_for=['Anyone aged 4 and over', 'People who live or work in areas with dengue outbreaks', 'People who have had dengue before (as advised by the doctor)'],
    includes=VAX_INCL,
    precautions=['If you are pregnant, breastfeeding or have a weakened immune system, talk to the doctor first',
                 'If you develop a sudden high fever during a dengue outbreak, see a doctor and do not take NSAID painkillers on your own'],
    duration='2 doses, 3 months apart',
    seo_title='Dengue Vaccine Qdenga 1,800 THB in Bangkok | HappiWell Clinic',
    seo_description='Qdenga dengue vaccine for 1,800 baht per dose or 3,450 baht for the 2-dose course, for ages 4+. HappiWell Medical Clinic, Pracha Uthit 49, Thung Khru, Bangkok. Book via LINE.'),
  'pneumococcal-vaccine-prevnar-20': dict(
    name='Pneumococcal vaccine (Prevnar 20)',
    short_desc='Adults who have never had a pneumococcal vaccine need just 1 dose.',
    description=desc('Prevnar 20 protects against pneumococcal infection (IPD), a major cause of pneumonia, bloodstream infection and meningitis.',
                     'Adults who have never had a pneumococcal vaccine need only 1 dose of Prevnar 20.'),
    price_unit='per dose',
    suitable_for=['Adults aged 65 and over', 'People of any age with a long-term condition or weakened immune system', 'Any adult who wants protection'],
    includes=VAX_INCL,
    precautions=['Tell the doctor if you have had another pneumococcal vaccine before, so the right schedule can be planned'],
    duration='1 dose',
    seo_title='Prevnar 20 Pneumococcal Vaccine 3,000 THB, Bangkok | HappiWell',
    seo_description='Prevnar 20 (PCV20) pneumococcal vaccine for 3,000 baht. Adults need just 1 dose; recommended for 65+. HappiWell Medical Clinic, Pracha Uthit 49, Thung Khru, Bangkok.'),
  'rsv-vaccine-abrysvo': dict(
    name='RSV vaccine (Abrysvo)',
    short_desc='One dose for adults aged 60 and over, and for pregnant women at 24–36 weeks.',
    description=desc('RSV is a respiratory virus that can cause serious illness in older adults, people with long-term conditions and babies. Abrysvo covers both RSV subtypes A and B.',
                     'The RSV vaccine is a single dose — it does not need to be repeated every year like the flu vaccine.'),
    price_unit='per dose',
    suitable_for=['Adults aged 60 and over', 'Adults aged 50–59 with lung disease, heart disease or another long-term condition', 'Pregnant women at 24–36 weeks, to protect the newborn'],
    includes=VAX_INCL,
    precautions=['Pregnant women should be vaccinated within the weeks of pregnancy recommended by the doctor'],
    duration='1 dose',
    seo_title='RSV Vaccine Abrysvo 7,200 THB in Bangkok | HappiWell Clinic',
    seo_description='Abrysvo RSV vaccine for 7,200 baht, single dose, for adults 60+ and pregnant women at 24–36 weeks. HappiWell Medical Clinic, Thung Khru, Bangkok. Book via LINE.'),
  'hepatitis-b-vaccine': dict(
    name='Hepatitis B vaccine',
    short_desc='3-dose course: 500 baht per dose if you pay for the full course, or 600 baht if you pay per dose.',
    description=desc('The hepatitis B vaccine is given on the standard 3-dose schedule at 0, 1 and 6 months.',
                     'Pay for the full course in advance at 500 baht per dose, or pay as you go at 600 baht per dose. If you miss an appointment, you do not need to restart the course.'),
    price_unit='per dose',
    options=[{'label': 'Pay for the full 3-dose course', 'note': 'Works out to 500 baht per dose'}, {'label': 'Pay per dose', 'note': 'per dose'}],
    suitable_for=['Anyone not yet immune to hepatitis B'],
    includes=['Doctor’s history check and assessment before the injection', 'Vaccine fee', 'Appointment for your next dose'],
    precautions=['If you are pregnant, talk to the doctor before the injection'],
    duration='3 doses (months 0, 1 and 6)',
    seo_title='Hepatitis B Vaccine from 500 THB per Dose, Bangkok | HappiWell',
    seo_description='3-dose hepatitis B vaccine: 500 baht per dose for the full course or 600 baht per dose pay-as-you-go. HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok.'),
  'hpv-vaccine-gardasil-9': dict(
    name='HPV vaccine (Gardasil 9)',
    short_desc='Protects against 9 types of HPV. The number of doses depends on your age — the doctor will advise the right schedule.',
    description=desc('Gardasil 9 protects against 9 types of HPV, which are linked to cervical cancer and other HPV-related diseases.',
                     'The number of doses and the interval depend on your age when you start. The doctor will assess you and recommend the right schedule.'),
    price_unit='per dose',
    suitable_for=['Women and men in the age ranges recommended by the doctor'],
    includes=VAX_INCL,
    precautions=['If you are pregnant, talk to the doctor before the injection'],
    seo_title='HPV Vaccine Gardasil 9 5,500 THB in Bangkok | HappiWell Clinic',
    seo_description='Gardasil 9 HPV vaccine (9 strains) for 5,500 baht per dose, with a schedule advised by the doctor for your age. HappiWell Medical Clinic, Pracha Uthit 49, Thung Khru, Bangkok.'),
  'rabies-vaccine': dict(
    name='Rabies vaccine',
    short_desc='Bitten or scratched by a dog or cat? The doctor assesses the wound and vaccinates on the standard schedule.',
    description=desc('After an animal bite or scratch, wash the wound immediately with clean water and soap for at least 15 minutes, then see a doctor quickly to assess the risk.',
                     'If you have never been vaccinated, the doctor will follow the standard schedule on days 0, 3, 7 and 14 (sometimes with an extra dose on day 28). People who were vaccinated before usually need only 2 booster doses. Complete every dose on schedule.'),
    price_unit='per dose', price_note='Wound cleaning/dressing (50 baht) and stitches if needed (50 baht per stitch) are charged separately',
    options=[{'label': 'Rabies vaccine', 'note': 'per dose'}, {'label': 'Wound cleaning / dressing', 'note': 'per visit'}, {'label': 'Stitches (if needed)', 'note': 'per stitch'}],
    suitable_for=['Anyone bitten, scratched or licked on a wound by a dog, cat or other mammal'],
    includes=['Wound assessment by a doctor', 'Vaccine and injection fee', 'Appointment for your next dose'],
    precautions=['Do not stop the course early, even if the wound has healed', 'Pregnant women can be vaccinated, because rabies is fatal'],
    duration='4 doses (days 0, 3, 7 and 14) or as scheduled by the doctor',
    seo_title='Dog or Cat Bite? Rabies Vaccine 390 THB, Bangkok | HappiWell',
    seo_description='Bitten or scratched by a dog or cat? Rabies vaccine 390 baht per dose, wound care 50 baht, every wound assessed by a doctor. Open daily. HappiWell Medical Clinic, Pracha Uthit 49, Thung Khru.'),
  'tetanus-vaccine': dict(
    name='Tetanus vaccine',
    short_desc='Tetanus protection after a wound, or as a scheduled booster. A doctor assesses you before every injection.',
    description=desc('The tetanus vaccine is used as a scheduled booster, or after a wound with a risk of tetanus — for example a dirty wound, a cut from a sharp object or stepping on a nail.',
                     'The number of doses depends on your vaccination history. The doctor will ask about it and advise how many doses you need.'),
    price_unit='per dose',
    suitable_for=['People with a wound who are unsure whether their tetanus vaccinations are up to date', 'Adults due for a booster'],
    includes=VAX_INCL,
    precautions=['Tell the doctor if you have ever been allergic to a vaccine', 'Deep or very dirty wounds should also be assessed by the doctor'],
    seo_title='Tetanus Vaccine 100 THB per Dose in Bangkok | HappiWell Clinic',
    seo_description='Tetanus vaccine for 100 baht per dose — after a wound, a nail injury, or as a booster. Doctor assessment before every shot. HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru.'),
  'health-checkup-basic': dict(
    name='Health Check-up Package (Basic)',
    short_desc='16 checks — blood sugar, cholesterol, liver, kidneys and hepatitis B — for 999 baht, with results explained by a doctor.',
    description=desc('One blood draw gives you 16 key health values, including blood sugar, cholesterol, liver, kidneys and hepatitis B. The doctor explains your results in plain language — what is normal and what needs attention.'),
    price_unit='per package',
    suitable_for=['Working adults who want a basic yearly check', 'Anyone who has never had a health check-up', 'Anyone who wants to know their blood sugar, cholesterol, liver and kidney values'],
    includes=BASE + ['Liver function test', CBC, HEPB, VDRL, UA, BMI, READ],
    precautions=[FAST],
    seo_title='Basic Health Check-up 999 THB in Bangkok | HappiWell Clinic',
    seo_description='Basic health check-up, 16 checks for 999 baht: blood sugar, cholesterol, liver, kidneys, hepatitis B and urine, with a doctor explaining your results. HappiWell Medical Clinic, Thung Khru, Bangkok.'),
  'health-checkup-female': dict(
    name='Health Check-up Package (Comprehensive, Women)',
    short_desc='23 checks including detailed liver tests, blood group, calcium, and liver and digestive tract cancer markers.',
    description=desc('More detailed than the basic package: 3 liver values, your blood group, calcium level, and liver and digestive tract cancer markers. One blood draw, and the doctor explains every result in plain language.'),
    price_unit='per package',
    suitable_for=['Women who want a more detailed check than the basic package', 'People with a family history of liver disease, diabetes or high cholesterol', 'Anyone who does not know their blood group'],
    includes=BASE + ['Liver function, 3 values — SGOT, SGPT, ALP', CBC, HEPB, VDRL, UA] + BIG_EXTRA + [BMI, READ],
    precautions=[FAST, 'Cancer markers (AFP, CEA) are for screening only and do not diagnose cancer. The doctor interprets them together with your symptoms and history.'],
    seo_title='Women’s Comprehensive Health Check-up 1,300 THB, Bangkok | HappiWell',
    seo_description='Comprehensive women’s health check-up, 23 checks for 1,300 baht: blood sugar, cholesterol, liver, kidneys, blood group, calcium and AFP/CEA markers. HappiWell Medical Clinic, Thung Khru, Bangkok.'),
  'health-checkup-male': dict(
    name='Health Check-up Package (Comprehensive, Men)',
    short_desc='23 checks including detailed liver tests, prostate PSA, and liver and digestive tract cancer markers.',
    description=desc('More detailed than the basic package: 3 liver values, your blood group, calcium level, prostate PSA, and liver and digestive tract cancer markers. One blood draw, and the doctor explains every result in plain language.'),
    price_unit='per package',
    suitable_for=['Men who want a more detailed check than the basic package', 'Middle-aged and older men who want to know their prostate PSA', 'People with a family history of liver disease, diabetes or high cholesterol'],
    includes=BASE + ['Liver function, 3 values — SGOT, SGPT, ALP', CBC, HEPB, VDRL, UA] + BIG_EXTRA + ['PSA — prostate marker', READ],
    precautions=[FAST, 'Cancer markers (AFP, CEA, PSA) are for screening only and do not diagnose cancer. The doctor interprets them together with your symptoms and history.'],
    seo_title='Men’s Comprehensive Health Check-up 1,399 THB, Bangkok | HappiWell',
    seo_description='Comprehensive men’s health check-up, 23 checks for 1,399 baht: blood sugar, cholesterol, liver, kidneys, blood group, PSA and AFP/CEA markers. HappiWell Medical Clinic, Thung Khru, Bangkok.'),
  'contraceptive-injection-3-month': dict(
    name='3-month contraceptive injection (DMPA)',
    short_desc='One injection gives 3 months of contraception. The doctor advises you before every injection.',
    description=desc('The 3-month DMPA contraceptive injection protects against pregnancy for 3 months with a single injection — a good option if taking a daily pill is inconvenient.',
                     'Good to know: your periods may become irregular or stop while using it, and after stopping it may take some time before fertility returns to normal.'),
    price_unit='per injection',
    suitable_for=['People who find a daily pill inconvenient', 'People who had side effects from combined hormonal pills'],
    includes=['Advice from a doctor before the injection', 'Medicine and injection fee'],
    precautions=['Contraceptive injections do not protect against sexually transmitted infections'],
    duration='3 months of contraception',
    seo_title='3-Month Contraceptive Injection 100 THB, Bangkok | HappiWell',
    seo_description='3-month contraceptive injection (DMPA) for 100 baht, with doctor advice before every injection. HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok. Book via LINE.'),
  'ekg': dict(
    name='Electrocardiogram (EKG)',
    short_desc='A quick, painless heart test — useful for check-ups and for symptoms like palpitations or chest discomfort.',
    description=desc('An electrocardiogram (EKG or ECG) records the heart’s electrical signals through stickers placed on the chest, arms and legs. It is quick and painless, and shows your heart rhythm and some abnormalities.',
                     'It is often done with an annual check-up, or when the doctor suspects symptoms may be heart-related.'),
    price_unit='per test',
    suitable_for=['Annual check-ups, especially from age 40', 'People with high blood pressure, diabetes or high cholesterol', 'Anyone who needs a heart test result for a job application or document'],
    includes=['Electrocardiogram at the clinic'],
    precautions=['If you have severe chest pain, cannot breathe or are sweating heavily, call 1669 or go to a hospital immediately', 'Wear a top that is easy to remove or open at the chest'],
    seo_title='EKG Heart Test 200 THB in Bangkok | HappiWell Clinic',
    seo_description='Electrocardiogram (EKG) for 200 baht — quick and painless, ideal with an annual check-up. HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok. Book via LINE.'),
  'contraceptive-injection-monthly': dict(
    name='Monthly contraceptive injection',
    short_desc='A combined hormonal injection given every month, with more regular periods than the 3-month injection.',
    description=desc('The monthly contraceptive injection is an option for people who had irregular periods on the 3-month injection.',
                     'You need to come to the clinic every month. If that is difficult, the 3-month injection may suit you better — talk to the doctor to choose the right method.'),
    price_unit='per injection',
    suitable_for=['People who had irregular periods on the 3-month injection', 'People who want regular periods', 'People who can visit the clinic every month'],
    includes=['Advice from a doctor before the injection', 'Medicine and injection fee'],
    precautions=['Contraceptive injections do not protect against sexually transmitted infections'],
    duration='Every month',
    seo_title='Monthly Contraceptive Injection 250 THB, Bangkok | HappiWell',
    seo_description='Monthly contraceptive injection for 250 baht, with more regular periods than the 3-month injection. Doctor advice before every injection. HappiWell Medical Clinic, Thung Khru, Bangkok.'),
  'lab-test-single': dict(
    name='Individual blood / lab tests',
    short_desc='Choose only the tests you need, such as blood sugar, cholesterol or kidney function.',
    description=desc('Choose individual blood or lab tests — ideal if you need to monitor certain values, for example for a long-term condition.'),
    price_unit='per test', price_note='Some tests cost more. Ask us on LINE for the price of each test.',
    includes=[READ],
    precautions=['Some tests require fasting beforehand'],
    seo_title='Blood Tests from 100 THB in Thung Khru, Bangkok | HappiWell',
    seo_description='Individual blood tests such as blood sugar, cholesterol and kidney function from 100 baht per test, with results read by a doctor. HappiWell Medical Clinic, Pracha Uthit 49, Thung Khru.'),
  'employee-health-checkup': dict(
    name='Employee / corporate health check-ups',
    short_desc='Annual check-up packages for companies and factories, customised to your needs. Request a quote on LINE.',
    description=desc('Annual health check-ups for company and factory employees in Thung Khru and nearby areas. Choose tests to suit the type of work and your company’s budget.',
                     'Individual packages start at 999 baht. For group check-ups, message us on LINE with the number of employees and the tests you need to get a quote.'),
    price_note='Price per person depends on the number of employees and tests. Request a quote on LINE @p49clinic',
    suitable_for=['HR teams arranging annual check-ups for staff', 'Companies and factories in Thung Khru and nearby', 'Pre-employment health checks'],
    includes=['Tests customised to your company’s needs', READ],
    seo_title='Employee Health Check-ups for Companies, Thung Khru | HappiWell',
    seo_description='Annual employee health check-ups for companies and factories around Thung Khru, Bang Mod and Pracha Uthit. Customisable tests, packages from 999 baht. Request a quote on LINE.'),
  'nebulizer': dict(
    name='Nebuliser treatment',
    short_desc='Relief for wheezing and shortness of breath from asthma or respiratory allergies.',
    description=desc('A nebuliser turns liquid medicine into a fine mist that goes straight into the airways, opening them up and easing breathlessness. It is ideal for young children or anyone who finds inhalers difficult to use.'),
    price_unit='per treatment', price_note='The nebuliser mask costs 200 baht, bought once on your first visit and reused every time after',
    options=[{'label': 'Nebuliser treatment', 'note': 'per treatment'}, {'label': 'Treatment + nebuliser mask (first visit)', 'note': 'The mask can be reused on later visits'}],
    includes=['Assessment by a doctor', 'Nebuliser medicine'],
    precautions=['If breathing is very difficult, your lips turn blue or you cannot speak in full sentences, go to a hospital immediately or call 1669'],
    seo_title='Nebuliser Treatment 200 THB in Bangkok | HappiWell Clinic',
    seo_description='Nebuliser treatment for 200 baht to relieve asthma and respiratory allergy symptoms, with a doctor’s assessment. HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok.'),
  'wound-care': dict(
    name='Wound care / stitches',
    short_desc='Wound cleaning, dressing of fresh and surgical wounds, and stitches by a doctor.',
    description=desc('Care for fresh and surgical wounds and stitches by a doctor, with follow-up until healed. If a wound is beyond what the clinic can treat, the doctor will refer you to a hospital.'),
    price_unit='',
    options=[{'label': 'Wound cleaning / dressing', 'note': 'per visit'}, {'label': 'Stitches', 'note': 'per stitch'}],
    includes=['Wound assessment by a doctor'],
    precautions=['Deep wounds, bleeding that will not stop, or objects stuck in the wound should be treated at a hospital'],
    seo_title='Wound Care & Stitches from 50 THB, Thung Khru | HappiWell',
    seo_description='Wound cleaning, dressing and stitches by a doctor from 50 baht, close to home in Thung Khru, Bang Mod and Pracha Uthit. Open daily at HappiWell Medical Clinic.'),
  'medical-certificate': dict(
    name='Medical certificate',
    short_desc='Medical certificates for jobs, driving licences and official documents, from 200 baht.',
    description=desc('We issue the standard “5-disease” medical certificate and certificates for job applications, driving licences and other documents. All types start at 200 baht.',
                     'If a drug test is also required, the price is 300 baht.'),
    price_unit='per certificate',
    options=[{'label': 'Medical certificate (5-disease / job / driving licence / general)', 'note': 'per certificate'}, {'label': 'Medical certificate + drug test', 'note': 'per certificate'}],
    includes=['Physical examination by a doctor', 'Medical certificate'],
    precautions=['Bring your ID card or passport'],
    seo_title='Medical Certificate 200 THB in Thung Khru, Bangkok | HappiWell',
    seo_description='Medical certificates for jobs, driving licences and official documents for 200 baht, or 300 baht with a drug test. HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok.'),
  'pep-prep': dict(
    name='PEP / PrEP HIV prevention',
    short_desc='Confidential counselling. Please book on LINE before your visit.',
    description=desc('PEP (post-exposure prophylaxis) and PrEP (pre-exposure prophylaxis) with confidential counselling. Please message us on LINE to book before every visit.'),
    price_note='Ask about medicine prices on LINE @p49clinic',
    includes=['Confidential consultation with a doctor'],
    precautions=['PEP should be started as soon as possible after exposure'],
    seo_title='PEP & PrEP HIV Prevention in Thung Khru, Bangkok | HappiWell',
    seo_description='PEP and PrEP HIV prevention with confidential doctor counselling. Book on LINE before your visit. HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok.'),
  'std-screening': dict(
    name='STI screening',
    short_desc='Confidential screening and counselling. Ask us on LINE about tests and prices.',
    description=desc('Screening for sexually transmitted infections with confidential counselling by a doctor. If anything abnormal is found, the doctor will advise treatment or refer you as appropriate.',
                     'Free condoms in all sizes are available at the clinic.'),
    price_note='Ask about tests and prices on LINE @p49clinic',
    includes=['Confidential consultation with a doctor'],
    precautions=['Some tests can only detect infection after a certain time since the risk. The doctor will advise the right timing.'],
    seo_title='STI Testing in Thung Khru, Bangkok | HappiWell Clinic',
    seo_description='Confidential STI screening with doctor counselling and free condoms at HappiWell Medical Clinic, Soi Pracha Uthit 49, Thung Khru, Bangkok. Ask us on LINE.'),
}

def q(v):
    return '$j$' + json.dumps(v, ensure_ascii=False) + '$j$::jsonb'

lines = ['-- English translations (column en). Generated by programs_en.py']
for slug, v in CATS.items():
    lines.append(f"update public.hw_program_categories set en = {q(v)} where slug = '{slug}';")
for slug, v in P.items():
    lines.append(f"update public.hw_programs set en = {q(v)} where slug = '{slug}';")
out = pathlib.Path(__file__).with_name('programs_en.sql')
out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(out, len(P), 'programs', len(CATS), 'categories')

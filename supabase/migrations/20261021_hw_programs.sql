-- HappiWell: โปรแกรมและราคา (หน้า /programs) + คำขอจองคิว
-- รันใน Supabase project happiwell-ai → SQL Editor → Run
-- สร้างตารางใหม่ 3 ตาราง ไม่แตะตารางเดิม / ใช้ is_admin() แบบเดียวกับ hw_articles

create table if not exists public.hw_program_categories (
  slug        text primary key check (slug ~ '^[a-z0-9-]{2,40}$'),
  name        text not null,
  description text,
  sort_order  int not null default 0,
  is_active   boolean not null default true,
  created_at  timestamptz not null default now()
);

create table if not exists public.hw_programs (
  id                   uuid primary key default gen_random_uuid(),
  slug                 text not null unique check (slug ~ '^[a-z0-9-]{2,80}$'),
  category             text not null references public.hw_program_categories(slug) on update cascade,
  name                 text not null,
  short_desc           text,
  description          text,                 -- Editor.js JSON (แบบเดียวกับ hw_articles.content)
  price                numeric(10,2),        -- null = แสดง "สอบถามราคา"
  price_unit           text,                 -- เช่น "ต่อเข็ม", "ต่อครั้ง", "คอร์ส 3 เข็ม"
  price_note           text,
  options              jsonb not null default '[]'::jsonb, -- [{label, price, note}]
  suitable_for         text[] not null default '{}',
  includes             text[] not null default '{}',
  precautions          text[] not null default '{}',
  duration             text,
  brand                text,
  fda_reg_no           text,
  cover_image          text,
  related_article_slug text,
  tags                 text[] not null default '{}',
  sort_order           int not null default 0,
  is_featured          boolean not null default false,
  is_published         boolean not null default false,
  seo_title            text,
  seo_description      text,
  created_at           timestamptz not null default now(),
  updated_at           timestamptz not null default now(),
  constraint options_is_array check (jsonb_typeof(options) = 'array')
);
create index if not exists hw_programs_public_idx on public.hw_programs (is_published, category, sort_order);

create table if not exists public.hw_program_bookings (
  id             uuid primary key default gen_random_uuid(),
  program_id     uuid references public.hw_programs(id) on delete set null,
  program_name   text not null check (char_length(program_name) <= 200),
  option_label   text check (char_length(option_label) <= 200),
  price          numeric(10,2),
  customer_name  text not null check (char_length(customer_name) between 1 and 120),
  phone          text not null check (phone ~ '^[0-9+() -]{9,20}$'),
  line_id        text check (char_length(line_id) <= 60),
  preferred_date date,
  preferred_time text check (preferred_time in ('morning','afternoon','evening')),
  note           text check (char_length(note) <= 1000),
  pdpa_consent   boolean not null default false,
  status         text not null default 'new' check (status in ('new','contacted','confirmed','done','cancelled')),
  admin_note     text,
  created_at     timestamptz not null default now()
);
create index if not exists hw_program_bookings_status_idx on public.hw_program_bookings (status, created_at desc);

create or replace function public.hw_programs_touch() returns trigger
language plpgsql set search_path = public as $$
begin new.updated_at = now(); return new; end $$;
drop trigger if exists hw_programs_touch on public.hw_programs;
create trigger hw_programs_touch before update on public.hw_programs
for each row execute function public.hw_programs_touch();

alter table public.hw_program_categories enable row level security;
alter table public.hw_programs           enable row level security;
alter table public.hw_program_bookings   enable row level security;

drop policy if exists public_read_program_categories on public.hw_program_categories;
create policy public_read_program_categories on public.hw_program_categories
  for select using (is_active = true);
drop policy if exists admin_all_program_categories on public.hw_program_categories;
create policy admin_all_program_categories on public.hw_program_categories
  for all to authenticated using (is_admin()) with check (is_admin());

drop policy if exists public_read_published_programs on public.hw_programs;
create policy public_read_published_programs on public.hw_programs
  for select using (is_published = true);
drop policy if exists admin_all_programs on public.hw_programs;
create policy admin_all_programs on public.hw_programs
  for all to authenticated using (is_admin()) with check (is_admin());

-- คนทั่วไปส่งคำขอจองได้อย่างเดียว อ่าน/แก้ไม่ได้
drop policy if exists public_insert_program_bookings on public.hw_program_bookings;
create policy public_insert_program_bookings on public.hw_program_bookings
  for insert to anon, authenticated
  with check (pdpa_consent = true and status = 'new' and admin_note is null);
drop policy if exists admin_all_program_bookings on public.hw_program_bookings;
create policy admin_all_program_bookings on public.hw_program_bookings
  for all to authenticated using (is_admin()) with check (is_admin());

insert into public.hw_program_categories (slug, name, description, sort_order) values
  ('vaccine',         'วัคซีน',        'วัคซีนสำหรับผู้ใหญ่และเด็ก ฉีดโดยแพทย์ พร้อมประเมินก่อนฉีดทุกครั้ง', 1),
  ('checkup',         'ตรวจสุขภาพ',    'แพ็กเกจตรวจสุขภาพประจำปีและตรวจเลือดรายการเดี่ยว', 2),
  ('family-planning', 'คุมกำเนิด',     'ยาฉีดคุมกำเนิดและคำปรึกษาวางแผนครอบครัว', 3),
  ('procedure',       'หัตถการ',       'ทำแผล เย็บแผล พ่นยา และบริการหัตถการทั่วไป', 4),
  ('certificate',     'ใบรับรองแพทย์', 'ใบรับรองแพทย์สำหรับสมัครงาน ใบขับขี่ และอื่น ๆ', 5),
  ('sexual-health',   'สุขภาพทางเพศ',  'ตรวจคัดกรองและให้คำปรึกษาเป็นความลับ', 6)
on conflict (slug) do nothing;

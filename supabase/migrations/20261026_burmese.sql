-- HappiWell: เนื้อหาภาษาพม่า (/my/...) เก็บเป็น jsonb เหมือนคอลัมน์ en ว่าง = ใช้อังกฤษ/ไทยแทน
alter table public.hw_programs           add column if not exists my jsonb not null default '{}'::jsonb;
alter table public.hw_program_categories add column if not exists my jsonb not null default '{}'::jsonb;
alter table public.hw_articles           add column if not exists my jsonb not null default '{}'::jsonb;

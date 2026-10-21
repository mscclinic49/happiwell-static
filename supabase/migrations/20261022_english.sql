-- HappiWell: เนื้อหาภาษาอังกฤษ (/en/...) เก็บเป็น jsonb คอลัมน์เดียว ว่าง = ใช้ภาษาไทยแทน
-- programs:   {name, short_desc, description, price_unit, price_note, options:[{label,note}], suitable_for[], includes[], precautions[], duration, seo_title, seo_description}
-- categories: {name, description}
-- articles:   {title, excerpt, content, category, seo_title, seo_description}
alter table public.hw_programs           add column if not exists en jsonb not null default '{}'::jsonb;
alter table public.hw_program_categories add column if not exists en jsonb not null default '{}'::jsonb;
alter table public.hw_articles           add column if not exists en jsonb not null default '{}'::jsonb;

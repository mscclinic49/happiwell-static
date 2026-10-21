-- ช่อง SEO ของบทความ (รันแล้ว 21 ต.ค. 2569)
alter table public.hw_articles add column if not exists seo_title text, add column if not exists seo_description text;

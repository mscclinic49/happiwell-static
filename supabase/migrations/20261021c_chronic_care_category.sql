-- หมวดใหม่: โรคเรื้อรังและผู้สูงอายุ (รันแล้ว 21 ต.ค. 2569)
insert into public.hw_program_categories (slug, name, description, sort_order) values
  ('chronic-care', 'โรคเรื้อรังและผู้สูงอายุ', 'ดูแลโรคเรื้อรัง ผู้สูงอายุ และข้อเข่า อย่างต่อเนื่องใกล้บ้าน', 3)
on conflict (slug) do nothing;
update public.hw_program_categories set sort_order = sort_order + 1 where slug in ('family-planning','procedure','certificate','sexual-health');

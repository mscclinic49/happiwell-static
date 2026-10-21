-- ปิดการรับคำขอจองผ่านเว็บ (เปลี่ยนไปจองผ่าน LINE แทน) ตารางและข้อมูลเดิมยังอยู่
-- เปิดกลับ: รันคำสั่ง create policy public_insert_program_bookings ใน 20261021_hw_programs.sql อีกครั้ง
drop policy if exists public_insert_program_bookings on public.hw_program_bookings;

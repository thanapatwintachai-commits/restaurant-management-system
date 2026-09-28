# Restaurant Management System

ระบบจัดการร้านอาหารด้วย Flask สำหรับโปรเจกต์นักเรียน/นักศึกษา

## ฟีเจอร์หลัก
- Login และ Role: admin / staff / customer
- จัดการเมนู เพิ่ม แก้ไข ลบ และเปลี่ยนสถานะพร้อมขาย/หมด
- ค้นหา Filter และจัดการเมนู
- จัดการโต๊ะ 1-10
- สร้างออเดอร์และ Kitchen Display
- Billing พร้อมภาษีและ Service Charge
- รายงานยอดขายและเมนูขายดี
- Activity Log
- **QR Ordering:** ลูกค้าสแกน QR ของแต่ละโต๊ะเพื่อเปิดหน้าสั่งอาหารโดยไม่ต้อง Login
- หน้า Tables แสดง QR ของโต๊ะแต่ละโต๊ะ และมีลิงก์ทดสอบหน้าสั่งอาหาร
- มีเมนูตัวอย่าง 18 รายการ พร้อมรูปภาพแบบ local ใน `static/food/`

## บัญชีทดสอบ
- admin / 1234
- staff / 1234
- customer / 1234

## QR Ordering
แต่ละโต๊ะใช้ URL รูปแบบ `/customer/order/<table_id>` และ QR ถูกสร้างอัตโนมัติที่ `/qr/table/<table_id>`

ตัวอย่าง:
- โต๊ะ 1: `/customer/order/1`
- QR โต๊ะ 1: `/qr/table/1`

## Deploy บน Vercel
ติดตั้ง dependency จาก `requirements.txt` แล้ว deploy ได้ด้วย Flask configuration ของ Vercel

หมายเหตุ: การเขียน `restaurant_data.json` บน serverless deployment ของ Vercel ไม่ใช่ persistent storage ถาวร หากต้องการให้ข้อมูลออเดอร์/เมนูคงอยู่หลัง deployment แบบ production ควรเชื่อมฐานข้อมูลหรือ storage ภายนอก

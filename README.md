# Restaurant Management

โปรเจกต์ระบบจัดการร้านอาหารแบบ Console ด้วย Python Standard Library

## ไฟล์
- `main.py` - โปรแกรมหลัก
- `menu.py` - จัดการเมนูอาหาร
- `table.py` - จัดการโต๊ะ
- `order.py` - รับออเดอร์
- `billing.py` - คำนวณบิล
- `report.py` - รายงานยอดขาย
- `file_manager.py` - อ่าน/เขียน JSON และจัดการ error log
- `utils.py` - รับข้อมูลและตรวจสอบ input
- `restaurant_data.json` - จะถูกสร้างอัตโนมัติหลังบันทึกข้อมูล
- `error.log` - จะถูกสร้างเมื่อเกิดข้อผิดพลาด

## วิธีรัน
เปิด Terminal ในโฟลเดอร์นี้ แล้วใช้

```bash
python main.py
```

## ความสามารถตามโจทย์
- ตัวแปร `int`, `float`, `str`, `bool`
- `if / elif / else`
- `for` และ `while`
- ฟังก์ชันมากกว่า 6 ฟังก์ชัน พร้อม parameter และ return
- ใช้ `list` และ `dict`
- แยกโปรแกรมเป็นหลาย module
- บันทึกข้อมูลลง JSON
- `try / except` และ traceback ลง `error.log`
- เพิ่ม/แก้ไข/ลบ/ค้นหาเมนู
- จัดการโต๊ะ
- รับออเดอร์
- เช็กบิล ส่วนลด ภาษี และค่าบริการ
- รายงานยอดขายและเมนูขายดี

## Web / Vercel
The project includes a Flask web interface in `app.py`, `templates/`, `requirements.txt`, and `vercel.json`.

Demo accounts: `admin/1234`, `staff/1234`, `customer/1234`.

Roles:
- Admin: dashboard, menu CRUD, orders, kitchen, billing, reports, activity log.
- Staff: orders, kitchen, billing, reports, menu status.
- Customer: dashboard, menu, tables, orders, create order.

Web orders include server-side search, status filter, sorting, and pagination.

For Vercel, `restaurant_data.json` is suitable for local/classroom demonstration. Serverless runtime storage should not be treated as permanent database storage; use an external database/storage if persistent web edits are required.

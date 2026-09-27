from datetime import datetime


class OrderManager:

    def __init__(self, orders=None):
        self.orders = orders if orders is not None else []

    # ==================================================
    # สร้างออเดอร์
    # ==================================================

    def create_order(self, menu_manager, table_manager):

        from utils import input_int

        # =========================
        # เลือกโต๊ะ
        # =========================

        table_id = input_int("เลขโต๊ะ: ")

        table = table_manager.get(table_id)

        if table is None:
            print("ไม่พบโต๊ะ")
            return

        # =========================
        # เช็กสถานะโต๊ะ
        # =========================

        if table["status"] == "ว่าง":

            customer = input("ชื่อลูกค้า: ").strip()

            ok, message = table_manager.check_in(
                table_id,
                customer
            )

            print(message)

            if not ok:
                return

        # =========================
        # หาออเดอร์เดิม
        # =========================

        order = self.get_open_order(table_id)

        # =========================
        # สร้างออเดอร์ใหม่
        # =========================

        if order is None:

            order = {
                "id": self._next_id(),
                "table_id": table_id,
                "customer": table.get("customer", ""),
                "created_at": datetime.now().isoformat(
                    timespec="seconds"
                ),
                "status": "open",
                "items": []
            }

            self.orders.append(order)

        # =========================
        # เมนูจัดการออเดอร์
        # =========================

        while True:

            print("\n========== ORDER MENU ==========")

            print("1. เพิ่มรายการอาหาร")
            print("2. ลดจำนวนอาหาร")
            print("3. ยกเลิกรายการอาหาร")
            print("4. แสดงออเดอร์")
            print("0. จบการสั่งอาหาร")

            choice = input("เลือก: ").strip()

            # =========================
            # เพิ่มอาหาร
            # =========================

            if choice == "1":

                self.add_order_item(
                    order,
                    menu_manager
                )

            # =========================
            # ลดจำนวนอาหาร
            # =========================

            elif choice == "2":

                self.reduce_order_item(
                    order,
                    menu_manager
                )

            # =========================
            # ยกเลิกรายการ
            # =========================

            elif choice == "3":

                self.cancel_order_item(
                    order,
                    menu_manager
                )

            # =========================
            # แสดงออเดอร์
            # =========================

            elif choice == "4":

                self.show_order(
                    order,
                    menu_manager
                )

            # =========================
            # จบ
            # =========================

            elif choice == "0":

                break

            else:

                print("กรุณาเลือกเมนูที่มีในระบบ")

        # =========================
        # แสดงออเดอร์สุดท้าย
        # =========================

        print("\n========== ORDER SUMMARY ==========")

        self.show_order(
            order,
            menu_manager
        )

        print("\nบันทึกออเดอร์เรียบร้อย")

    # ==================================================
    # เพิ่มรายการอาหาร
    # ==================================================

    def add_order_item(self, order, menu_manager):

        from utils import input_int

        print("\n========== MENU ==========")

        menu_manager.show_all()

        item_id = input_int(
            "รหัสเมนู: "
        )

        if item_id == 0:
            return

        item = menu_manager.find(item_id)

        if item is None:

            print("ไม่พบเมนู")
            return

        # ตรวจสอบสถานะเมนู

        if item["status"] == "หมด":

            print("เมนูนี้หมดแล้ว")
            return

        quantity = input_int(
            "จำนวน: "
        )

        if quantity <= 0:

            print("จำนวนต้องมากกว่า 0")
            return

        # =========================
        # ถ้ามีเมนูนี้อยู่แล้ว
        # ให้เพิ่มจำนวนแทนการสร้างรายการใหม่
        # =========================

        existing_item = None

        for order_item in order["items"]:

            if order_item["menu_id"] == item_id:

                existing_item = order_item
                break

        if existing_item is not None:

            existing_item["quantity"] += quantity

        else:

            order["items"].append({
                "menu_id": item_id,
                "quantity": quantity
            })

        print(
            f"เพิ่ม {item['name']} x{quantity} แล้ว"
        )

    # ==================================================
    # ลดจำนวนอาหาร
    # ==================================================

    def reduce_order_item(self, order, menu_manager):

        from utils import input_int

        if not order["items"]:

            print("ยังไม่มีรายการอาหาร")
            return

        self.show_order(
            order,
            menu_manager
        )

        item_id = input_int(
            "รหัสเมนูที่ต้องการลดจำนวน: "
        )

        order_item = self.find_order_item(
            order,
            item_id
        )

        if order_item is None:

            print("ไม่พบรายการอาหารในออเดอร์")
            return

        quantity = input_int(
            "ต้องการลดจำนวนกี่รายการ: "
        )

        if quantity <= 0:

            print("จำนวนต้องมากกว่า 0")
            return

        # =========================
        # ลดจำนวน
        # =========================

        order_item["quantity"] -= quantity

        # ถ้าจำนวนเหลือ 0 หรือติดลบ
        # ให้ลบรายการออก

        if order_item["quantity"] <= 0:

            order["items"].remove(
                order_item
            )

            print("รายการอาหารถูกลบออกจากออเดอร์แล้ว")

        else:

            print(
                f"ลดจำนวนเหลือ "
                f"{order_item['quantity']} รายการ"
            )

    # ==================================================
    # ยกเลิกรายการอาหาร
    # ==================================================

    def cancel_order_item(self, order, menu_manager):

        from utils import input_int

        if not order["items"]:

            print("ยังไม่มีรายการอาหาร")
            return

        self.show_order(
            order,
            menu_manager
        )

        item_id = input_int(
            "รหัสเมนูที่ต้องการยกเลิก: "
        )

        order_item = self.find_order_item(
            order,
            item_id
        )

        if order_item is None:

            print("ไม่พบรายการอาหารในออเดอร์")
            return

        item = menu_manager.find(
            item_id
        )

        if item is not None:

            confirm = input(
                f"ยืนยันยกเลิก "
                f"{item['name']} หรือไม่ (y/n): "
            ).lower()

        else:

            confirm = input(
                "ยืนยันยกเลิกรายการหรือไม่ (y/n): "
            ).lower()

        if confirm == "y":

            order["items"].remove(
                order_item
            )

            print("ยกเลิกรายการอาหารแล้ว")

        else:

            print("ยกเลิกการทำรายการ")

    # ==================================================
    # ค้นหารายการอาหารในออเดอร์
    # ==================================================

    def find_order_item(self, order, item_id):

        for order_item in order["items"]:

            if order_item["menu_id"] == item_id:

                return order_item

        return None

    # ==================================================
    # แสดงออเดอร์
    # ==================================================

    def show_order(self, order, menu_manager):

        print("\n========== CURRENT ORDER ==========")

        print(
            f"ออเดอร์: #{order['id']}"
        )

        print(
            f"โต๊ะ: {order['table_id']}"
        )

        print(
            f"ลูกค้า: {order.get('customer', '-')}"
        )

        print(
            f"เวลา: {order.get('created_at', '-')}"
        )

        print("-----------------------------------")

        if not order["items"]:

            print("ยังไม่มีรายการอาหาร")
            return

        total = 0

        for order_item in order["items"]:

            item = menu_manager.find(
                order_item["menu_id"]
            )

            if item is None:
                continue

            quantity = order_item["quantity"]

            line_total = (
                item["price"] * quantity
            )

            total += line_total

            print(
                f"รหัส {item['id']} | "
                f"{item['name']} | "
                f"x{quantity} | "
                f"{line_total:.2f} บาท"
            )

        print("-----------------------------------")

        print(
            f"รวมก่อนคิดภาษี: "
            f"{total:.2f} บาท"
        )

    # ==================================================
    # สร้าง ID ออเดอร์
    # ==================================================

    def _next_id(self):

        if not self.orders:

            return 1

        return max(
            order["id"]
            for order in self.orders
        ) + 1

    # ==================================================
    # หาออเดอร์ที่ยังไม่จ่าย
    # ==================================================

    def get_open_order(self, table_id):

        for order in self.orders:

            if (
                order["table_id"] == table_id
                and order["status"] == "open"
            ):

                return order

        return None

    # ==================================================
    # บันทึกการชำระเงิน
    # ==================================================

    def save_payment(self, order, bill):

        order["bill"] = bill

        order["paid_at"] = datetime.now().isoformat(
            timespec="seconds"
        )

    # ==================================================
    # คำนวณยอดขายทั้งหมด
    # ==================================================

    def total_sales(self):

        total = 0

        for order in self.orders:

            if order["status"] == "paid":

                total += order.get(
                    "bill",
                    {}
                ).get(
                    "total",
                    0
                )

        return total
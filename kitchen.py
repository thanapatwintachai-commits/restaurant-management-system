from datetime import datetime


class KitchenManager:

    # ==================================================
    # แสดง Kitchen Display
    # ==================================================

    def show_kitchen(self, order_manager, menu_manager):

        open_orders = []

        # หาเฉพาะออเดอร์ที่ยังไม่ชำระเงิน
        for order in order_manager.orders:

            if order["status"] == "open":

                # ถ้ายังไม่มีสถานะครัว
                # ให้เริ่มต้นเป็น "รอทำ"
                if "kitchen_status" not in order:

                    order["kitchen_status"] = "รอทำ"

                open_orders.append(order)

        # เรียงตามเวลาที่สร้างออเดอร์
        open_orders.sort(
            key=lambda order: order.get(
                "created_at",
                ""
            )
        )

        print("\n")
        print("==========================================")
        print("           KITCHEN DISPLAY")
        print("==========================================")

        if not open_orders:

            print("ไม่มีออเดอร์ที่กำลังรอ")
            return

        # แสดงออเดอร์
        for order in open_orders:

            print("\n------------------------------------------")

            print(
                f"ออเดอร์ #{order['id']} "
                f"| โต๊ะ {order['table_id']}"
            )

            print(
                f"ลูกค้า: "
                f"{order.get('customer', '-')}"
            )

            print(
                f"เวลา: "
                f"{order.get('created_at', '-')}"
            )

            print(
                f"สถานะ: "
                f"{order.get('kitchen_status', 'รอทำ')}"
            )

            print("------------------------------------------")

            for order_item in order["items"]:

                item = menu_manager.find(
                    order_item["menu_id"]
                )

                if item is not None:

                    print(
                        f"- {item['name']} "
                        f"x{order_item['quantity']}"
                    )

        print("\n==========================================")

    # ==================================================
    # เปลี่ยนสถานะออเดอร์
    # ==================================================

    def update_status(
        self,
        order_manager,
        order_id
    ):

        order = None

        # ค้นหาออเดอร์
        for current_order in order_manager.orders:

            if current_order["id"] == order_id:

                order = current_order
                break

        if order is None:

            print("ไม่พบออเดอร์")
            return

        # ออเดอร์ที่จ่ายเงินแล้ว
        # ไม่สามารถเปลี่ยนสถานะครัวได้
        if order["status"] != "open":

            print("ออเดอร์นี้ชำระเงินแล้ว")
            return

        current_status = order.get(
            "kitchen_status",
            "รอทำ"
        )

        print("\n========== เปลี่ยนสถานะ ==========")

        print(
            f"ออเดอร์ #{order['id']}"
        )

        print(
            f"สถานะปัจจุบัน: {current_status}"
        )

        print("\n1. รอทำ")
        print("2. กำลังทำ")
        print("3. เสร็จแล้ว")

        choice = input(
            "เลือกสถานะใหม่: "
        ).strip()

        status_map = {
            "1": "รอทำ",
            "2": "กำลังทำ",
            "3": "เสร็จแล้ว"
        }

        if choice not in status_map:

            print("เลือกสถานะไม่ถูกต้อง")
            return

        new_status = status_map[choice]

        order["kitchen_status"] = new_status

        # เก็บเวลาที่เปลี่ยนสถานะ
        order["kitchen_updated_at"] = (
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

        print(
            f"เปลี่ยนสถานะเป็น "
            f"'{new_status}' แล้ว"
        )

    # ==================================================
    # เมนู Kitchen Display
    # ==================================================

    def menu(
        self,
        order_manager,
        menu_manager
    ):

        while True:

            print("\n")
            print("========== KITCHEN ==========")

            print("1. ดูออเดอร์ในครัว")
            print("2. เปลี่ยนสถานะออเดอร์")
            print("0. กลับ")

            choice = input(
                "เลือก: "
            ).strip()

            # ------------------------------------------
            # ดูออเดอร์
            # ------------------------------------------

            if choice == "1":

                self.show_kitchen(
                    order_manager,
                    menu_manager
                )

            # ------------------------------------------
            # เปลี่ยนสถานะ
            # ------------------------------------------

            elif choice == "2":

                from utils import input_int

                order_id = input_int(
                    "เลขออเดอร์: "
                )

                self.update_status(
                    order_manager,
                    order_id
                )

            # ------------------------------------------
            # กลับ
            # ------------------------------------------

            elif choice == "0":

                break

            else:

                print(
                    "กรุณาเลือกเมนูที่มีในระบบ"
                )
class MenuManager:

    def __init__(self, items=None):
        self.items = items if items is not None else []

    # ==================================================
    # เพิ่มเมนู
    # ==================================================

    def add_item(
        self,
        name,
        price,
        category,
        image
    ):

        item = {
            "id": self._next_id(),
            "name": name,
            "price": float(price),
            "category": category,
            "image": image,
            "status": "พร้อมขาย"
        }

        self.items.append(item)

    # ==================================================
    # สร้าง ID ใหม่
    # ==================================================

    def _next_id(self):

        if not self.items:
            return 1

        return max(
            item["id"]
            for item in self.items
        ) + 1

    # ==================================================
    # ค้นหาเมนูจาก ID
    # ==================================================

    def find(self, item_id):

        for item in self.items:

            if item["id"] == item_id:
                return item

        return None

    # ==================================================
    # ค้นหาแบบ Keyword
    # ==================================================

    def search(self, keyword=""):

        keyword = keyword.lower().strip()

        return [
            item
            for item in self.items
            if keyword in item["name"].lower()
            or keyword in item["category"].lower()
        ]

    # ==================================================
    # ลบเมนู
    # ==================================================

    def delete_item(self, item_id):

        item = self.find(item_id)

        if item:

            self.items.remove(item)

            return True

        return False

    # ==================================================
    # แก้ไขสถานะเมนู
    # ==================================================

    def change_status(self, item_id, status):

        item = self.find(item_id)

        if item is None:
            return False

        if status not in ["พร้อมขาย", "หมด"]:
            return False

        item["status"] = status

        return True

    # ==================================================
    # SEARCH / FILTER / SORT / PAGINATION
    # ==================================================

    def advanced_search(
        self,
        keyword="",
        category="",
        status="",
        sort_by="",
        ascending=True,
        page=1,
        per_page=5
    ):

        # ----------------------------------------------
        # เริ่มจากข้อมูลทั้งหมด
        # ----------------------------------------------

        results = self.items.copy()

        # ----------------------------------------------
        # SEARCH
        # ----------------------------------------------

        keyword = keyword.lower().strip()

        if keyword:

            results = [
                item
                for item in results
                if keyword in item["name"].lower()
                or keyword in item["category"].lower()
            ]

        # ----------------------------------------------
        # FILTER CATEGORY
        # ----------------------------------------------

        category = category.lower().strip()

        if category:

            results = [
                item
                for item in results
                if item["category"].lower()
                == category
            ]

        # ----------------------------------------------
        # FILTER STATUS
        # ----------------------------------------------

        status = status.strip()

        if status:

            results = [
                item
                for item in results
                if item["status"] == status
            ]

        # ----------------------------------------------
        # SORT
        # ----------------------------------------------

        if sort_by == "name":

            results.sort(
                key=lambda item: item["name"].lower(),
                reverse=not ascending
            )

        elif sort_by == "price":

            results.sort(
                key=lambda item: item["price"],
                reverse=not ascending
            )

        elif sort_by == "id":

            results.sort(
                key=lambda item: item["id"],
                reverse=not ascending
            )

        # ----------------------------------------------
        # PAGINATION
        # ----------------------------------------------

        total_items = len(results)

        if per_page <= 0:
            per_page = 5

        total_pages = max(
            1,
            (total_items + per_page - 1)
            // per_page
        )

        if page < 1:
            page = 1

        if page > total_pages:
            page = total_pages

        start = (
            page - 1
        ) * per_page

        end = start + per_page

        page_items = results[start:end]

        return {
            "items": page_items,
            "total_items": total_items,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        }

    # ==================================================
    # แสดงผล Search / Filter / Sort / Pagination
    # ==================================================

    def advanced_menu(self):

        from utils import input_int

        print("\n========== SEARCH / FILTER ==========")

        keyword = input(
            "ค้นหาเมนูหรือหมวดหมู่ (Enter = ทั้งหมด): "
        ).strip()

        category = input(
            "กรองหมวดหมู่ (Enter = ทั้งหมด): "
        ).strip()

        print("\nสถานะ")

        print("1. ทั้งหมด")
        print("2. พร้อมขาย")
        print("3. หมด")

        status_choice = input(
            "เลือกสถานะ: "
        ).strip()

        status_map = {
            "1": "",
            "2": "พร้อมขาย",
            "3": "หมด"
        }

        status = status_map.get(
            status_choice,
            ""
        )

        print("\n========== SORT ==========")

        print("1. ไม่เรียง")
        print("2. ชื่อ A-Z")
        print("3. ชื่อ Z-A")
        print("4. ราคา น้อย → มาก")
        print("5. ราคา มาก → น้อย")
        print("6. ID น้อย → มาก")
        print("7. ID มาก → น้อย")

        sort_choice = input(
            "เลือกการเรียง: "
        ).strip()

        sort_by = ""
        ascending = True

        if sort_choice == "2":

            sort_by = "name"
            ascending = True

        elif sort_choice == "3":

            sort_by = "name"
            ascending = False

        elif sort_choice == "4":

            sort_by = "price"
            ascending = True

        elif sort_choice == "5":

            sort_by = "price"
            ascending = False

        elif sort_choice == "6":

            sort_by = "id"
            ascending = True

        elif sort_choice == "7":

            sort_by = "id"
            ascending = False

        # ----------------------------------------------
        # จำนวนข้อมูลต่อหน้า
        # ----------------------------------------------

        per_page = input_int(
            "\nจำนวนรายการต่อหน้า: "
        )

        if per_page <= 0:

            per_page = 5

        page = 1

        # ----------------------------------------------
        # แสดงแต่ละหน้า
        # ----------------------------------------------

        while True:

            result = self.advanced_search(
                keyword=keyword,
                category=category,
                status=status,
                sort_by=sort_by,
                ascending=ascending,
                page=page,
                per_page=per_page
            )

            print("\n")
            print(
                "========== MENU RESULT =========="
            )

            print(
                f"พบทั้งหมด "
                f"{result['total_items']} รายการ"
            )

            print(
                f"หน้า "
                f"{result['page']}"
                f"/"
                f"{result['total_pages']}"
            )

            print("------------------------------------------")

            self.show_all(
                result["items"]
            )

            print("------------------------------------------")

            if result["total_pages"] <= 1:

                break

            print("\n1. หน้าถัดไป")
            print("2. หน้าก่อนหน้า")
            print("0. กลับ")

            page_choice = input(
                "เลือก: "
            ).strip()

            if page_choice == "1":

                if page < result["total_pages"]:

                    page += 1

                else:

                    print("อยู่หน้าสุดท้ายแล้ว")

            elif page_choice == "2":

                if page > 1:

                    page -= 1

                else:

                    print("อยู่หน้าแรกแล้ว")

            elif page_choice == "0":

                break

            else:

                print("เลือกไม่ถูกต้อง")

    # ==================================================
    # เมนูจัดการ
    # ==================================================

    def menu(self):

        from utils import input_float, input_int

        while True:

            print("\n--- จัดการเมนู ---")

            print("1. แสดงเมนู")
            print("2. เพิ่มเมนู")
            print("3. แก้ไขราคา")
            print("4. ลบเมนู")
            print("5. ค้นหา / กรอง / เรียง / แบ่งหน้า")
            print("6. เปลี่ยนสถานะเมนู")
            print("0. กลับ")

            choice = input(
                "เลือก: "
            ).strip()

            # ------------------------------------------
            # แสดงเมนู
            # ------------------------------------------

            if choice == "1":

                self.show_all()

            # ------------------------------------------
            # เพิ่ม
            # ------------------------------------------

            elif choice == "2":

                name = input(
                    "ชื่อเมนู: "
                ).strip()

                price = input_float(
                    "ราคา: "
                )

                category = input(
                    "หมวดหมู่: "
                ).strip()

                image = input(
                    "URL รูปภาพ: "
                ).strip()

                self.add_item(
                    name,
                    price,
                    category,
                    image
                )

                print("เพิ่มเมนูแล้ว")

            # ------------------------------------------
            # แก้ไขราคา
            # ------------------------------------------

            elif choice == "3":

                item_id = input_int(
                    "รหัสเมนู: "
                )

                item = self.find(
                    item_id
                )

                if item:

                    item["price"] = input_float(
                        "ราคาใหม่: "
                    )

                    print("แก้ไขแล้ว")

                else:

                    print("ไม่พบเมนู")

            # ------------------------------------------
            # ลบ
            # ------------------------------------------

            elif choice == "4":

                item_id = input_int(
                    "รหัสเมนู: "
                )

                if self.delete_item(
                    item_id
                ):

                    print("ลบแล้ว")

                else:

                    print("ไม่พบเมนู")

            # ------------------------------------------
            # Search / Filter / Sort / Pagination
            # ------------------------------------------

            elif choice == "5":

                self.advanced_menu()

            # ------------------------------------------
            # เปลี่ยนสถานะ
            # ------------------------------------------

            elif choice == "6":

                item_id = input_int(
                    "รหัสเมนู: "
                )

                item = self.find(
                    item_id
                )

                if item is None:

                    print("ไม่พบเมนู")

                    continue

                print("\nสถานะปัจจุบัน:")
                print(
                    item["status"]
                )

                print("\n1. พร้อมขาย")
                print("2. หมด")

                status_choice = input(
                    "เลือกสถานะใหม่: "
                ).strip()

                if status_choice == "1":

                    status = "พร้อมขาย"

                elif status_choice == "2":

                    status = "หมด"

                else:

                    print("เลือกไม่ถูกต้อง")

                    continue

                if self.change_status(
                    item_id,
                    status
                ):

                    print(
                        f"เปลี่ยนสถานะเป็น "
                        f"{status} แล้ว"
                    )

            # ------------------------------------------
            # กลับ
            # ------------------------------------------

            elif choice == "0":

                break

            else:

                print("เลือกไม่ถูกต้อง")

    # ==================================================
    # แสดงรายการเมนู
    # ==================================================

    def show_all(self, items=None):

        items = (
            self.items
            if items is None
            else items
        )

        if not items:

            print("ไม่มีข้อมูลเมนู")
            return

        print(
            f"{'ID':<4}"
            f"{'เมนู':<20}"
            f"{'ราคา':>10}"
            f"  {'หมวดหมู่':<18}"
            f"สถานะ"
        )

        print("-" * 75)

        for item in items:

            print(
                f"{item['id']:<4}"
                f"{item['name']:<20}"
                f"{item['price']:>10.2f}"
                f"  {item['category']:<18}"
                f"{item['status']}"
            )
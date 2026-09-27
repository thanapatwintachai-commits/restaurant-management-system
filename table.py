class TableManager:
    def __init__(self, tables=None):
        self.tables = tables if tables is not None else []

    def add_table(self, table_id):
        self.tables.append({
            "id": table_id,
            "status": "ว่าง",
            "customer": ""
        })

    def get(self, table_id):
        for table in self.tables:
            if table["id"] == table_id:
                return table
        return None

    def check_in(self, table_id, customer=""):
        table = self.get(table_id)
        if table is None:
            return False, "ไม่พบโต๊ะ"
        if table["status"] != "ว่าง":
            return False, "โต๊ะนี้ไม่ว่าง"
        table["status"] = "มีลูกค้า"
        table["customer"] = customer
        return True, "เช็กอินสำเร็จ"

    def checkout(self, table_id):
        table = self.get(table_id)
        if table:
            table["status"] = "ว่าง"
            table["customer"] = ""

    def menu(self):
        from utils import input_int

        while True:
            print("\n--- จัดการโต๊ะ ---")
            print("1. ดูสถานะโต๊ะ")
            print("2. เช็กอินลูกค้า")
            print("3. เช็กเอาต์")
            print("0. กลับ")

            choice = input("เลือก: ").strip()

            if choice == "1":
                self.show()
            elif choice == "2":
                table_id = input_int("เลขโต๊ะ: ")
                customer = input("ชื่อลูกค้า: ").strip()
                ok, message = self.check_in(table_id, customer)
                print(message)
            elif choice == "3":
                table_id = input_int("เลขโต๊ะ: ")
                self.checkout(table_id)
                print("เช็กเอาต์แล้ว")
            elif choice == "0":
                break
            else:
                print("เลือกไม่ถูกต้อง")

    def show(self):
        print("\n--- สถานะโต๊ะ ---")
        for table in self.tables:
            print(
                f"โต๊ะ {table['id']}: {table['status']}"
                + (f" ({table['customer']})" if table["customer"] else "")
            )

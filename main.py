from auth import AuthManager

from menu import MenuManager
from table import TableManager
from order import OrderManager
from kitchen import KitchenManager
from billing import calculate_bill, show_receipt
from report import show_daily_report
from file_manager import save_data, load_data
from activity_logger import log_activity, show_activity_log
from utils import input_int, pause


def seed_data(menu_manager, table_manager):

    if not menu_manager.items:

        menu_manager.add_item(
            "ข้าวกะเพราไก่",
            55,
            "อาหารจานเดียว",
            "https://example.com/padkra-pao.jpg"
        )

        menu_manager.add_item(
            "ผัดไทย",
            60,
            "อาหารจานเดียว",
            "https://example.com/padthai.jpg"
        )

        menu_manager.add_item(
            "ชาไทย",
            35,
            "เครื่องดื่ม",
            "https://example.com/thai-tea.jpg"
        )

    if not table_manager.tables:

        for table_id in range(1, 11):

            table_manager.add_table(
                table_id
            )


def main():

    auth = AuthManager()

    print("\n========== LOGIN ==========")

    username = input("Username: ")
    password = input("Password: ")

    user = auth.login(
        username,
        password
    )

    if user is None:

        print(
            "Username หรือ Password ไม่ถูกต้อง"
        )

        return

    print("\nเข้าสู่ระบบสำเร็จ")

    print(
        f"ผู้ใช้: {user['username']}"
    )

    print(
        f"Role: {user['role']}"
    )

    log_activity(
        user["username"],
        "เข้าสู่ระบบ"
    )

    role = user["role"]

    data = load_data()

    menu_manager = MenuManager(
        data.get("menu", [])
    )

    table_manager = TableManager(
        data.get("tables", [])
    )

    order_manager = OrderManager(
        data.get("orders", [])
    )

    kitchen_manager = KitchenManager()

    seed_data(
        menu_manager,
        table_manager
    )

    while True:

        print(
            "\n========== RESTAURANT MANAGEMENT =========="
        )

        # ==================================================
        # ADMIN
        # ==================================================

        if role == "admin":

            print("1. จัดการเมนู")
            print("2. จัดการโต๊ะ")
            print("3. รับออเดอร์")
            print("4. Kitchen Display")
            print("5. เช็กบิล")
            print("6. Dashboard / รายงาน")
            print("7. Activity Log")
            print("8. บันทึกข้อมูล")
            print("0. ออกจากโปรแกรม")

        # ==================================================
        # STAFF
        # ==================================================

        elif role == "staff":

            print("1. ดูเมนู")
            print("2. จัดการโต๊ะ")
            print("3. รับออเดอร์")
            print("4. Kitchen Display")
            print("5. เช็กบิล")
            print("6. Dashboard / รายงาน")
            print("7. บันทึกข้อมูล")
            print("0. ออกจากโปรแกรม")

        # ==================================================
        # CUSTOMER
        # ==================================================

        elif role == "customer":

            print("1. ดูเมนู")
            print("2. สั่งอาหาร")
            print("0. ออกจากโปรแกรม")

        choice = input(
            "เลือกเมนู: "
        ).strip()

        # ==================================================
        # ADMIN
        # ==================================================

        if role == "admin":

            if choice == "1":

                menu_manager.menu()

                log_activity(
                    user["username"],
                    "จัดการเมนู"
                )

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

            elif choice == "2":

                table_manager.menu()

                log_activity(
                    user["username"],
                    "จัดการโต๊ะ"
                )

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

            elif choice == "3":

                order_manager.create_order(
                    menu_manager,
                    table_manager
                )

                log_activity(
                    user["username"],
                    "สร้างหรือแก้ไขออเดอร์"
                )

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

                print(
                    "บันทึกออเดอร์แล้ว"
                )

            elif choice == "4":

                kitchen_manager.menu(
                    order_manager,
                    menu_manager
                )

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

            elif choice == "5":

                table_id = input_int(
                    "เลขโต๊ะ: "
                )

                order = (
                    order_manager
                    .get_open_order(table_id)
                )

                if order is None:

                    print(
                        "ไม่พบออเดอร์ของโต๊ะนี้"
                    )

                else:

                    bill = calculate_bill(
                        order,
                        menu_manager
                    )

                    show_receipt(
                        order,
                        bill
                    )

                    confirm = input(
                        "\nชำระเงินและปิดโต๊ะหรือไม่ (y/n): "
                    ).lower()

                    if confirm == "y":

                        order["status"] = "paid"

                        table_manager.checkout(
                            table_id
                        )

                        order_manager.save_payment(
                            order,
                            bill
                        )

                        log_activity(
                            user["username"],
                            f"ชำระเงินออเดอร์ #{order['id']}"
                        )

                        save_data(
                            menu_manager,
                            table_manager,
                            order_manager
                        )

                        print(
                            "ชำระเงินเรียบร้อย"
                        )

            elif choice == "6":

                show_daily_report(
                    order_manager,
                    menu_manager
                )

            elif choice == "7":

                show_activity_log()

            elif choice == "8":

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

                print(
                    "บันทึกข้อมูลแล้ว"
                )

            elif choice == "0":

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

                log_activity(
                    user["username"],
                    "ออกจากระบบ"
                )

                print(
                    "ปิดโปรแกรมและบันทึกข้อมูลแล้ว"
                )

                break

            else:

                print(
                    "กรุณาเลือกเมนูที่มีในระบบ"
                )

        # ==================================================
        # STAFF
        # ==================================================

        elif role == "staff":

            if choice == "1":

                menu_manager.show_all()

            elif choice == "2":

                table_manager.menu()

                log_activity(
                    user["username"],
                    "จัดการโต๊ะ"
                )

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

            elif choice == "3":

                order_manager.create_order(
                    menu_manager,
                    table_manager
                )

                log_activity(
                    user["username"],
                    "สร้างหรือแก้ไขออเดอร์"
                )

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

                print(
                    "บันทึกออเดอร์แล้ว"
                )

            elif choice == "4":

                kitchen_manager.menu(
                    order_manager,
                    menu_manager
                )

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

            elif choice == "5":

                table_id = input_int(
                    "เลขโต๊ะ: "
                )

                order = (
                    order_manager
                    .get_open_order(table_id)
                )

                if order is None:

                    print(
                        "ไม่พบออเดอร์ของโต๊ะนี้"
                    )

                else:

                    bill = calculate_bill(
                        order,
                        menu_manager
                    )

                    show_receipt(
                        order,
                        bill
                    )

                    confirm = input(
                        "\nชำระเงินและปิดโต๊ะหรือไม่ (y/n): "
                    ).lower()

                    if confirm == "y":

                        order["status"] = "paid"

                        table_manager.checkout(
                            table_id
                        )

                        order_manager.save_payment(
                            order,
                            bill
                        )

                        log_activity(
                            user["username"],
                            f"ชำระเงินออเดอร์ #{order['id']}"
                        )

                        save_data(
                            menu_manager,
                            table_manager,
                            order_manager
                        )

                        print(
                            "ชำระเงินเรียบร้อย"
                        )

            elif choice == "6":

                show_daily_report(
                    order_manager,
                    menu_manager
                )

            elif choice == "7":

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

                print(
                    "บันทึกข้อมูลแล้ว"
                )

            elif choice == "0":

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

                log_activity(
                    user["username"],
                    "ออกจากระบบ"
                )

                print(
                    "ปิดโปรแกรมและบันทึกข้อมูลแล้ว"
                )

                break

            else:

                print(
                    "กรุณาเลือกเมนูที่มีในระบบ"
                )

        # ==================================================
        # CUSTOMER
        # ==================================================

        elif role == "customer":

            if choice == "1":

                menu_manager.show_all()

            elif choice == "2":

                order_manager.create_order(
                    menu_manager,
                    table_manager
                )

                log_activity(
                    user["username"],
                    "สร้างหรือแก้ไขออเดอร์"
                )

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

                print(
                    "บันทึกออเดอร์แล้ว"
                )

            elif choice == "0":

                save_data(
                    menu_manager,
                    table_manager,
                    order_manager
                )

                log_activity(
                    user["username"],
                    "ออกจากระบบ"
                )

                print(
                    "ออกจากระบบแล้ว"
                )

                break

            else:

                print(
                    "กรุณาเลือกเมนูที่มีในระบบ"
                )

        pause()


if __name__ == "__main__":
    main()
import json
import traceback

DATA_FILE = "restaurant_data.json"
LOG_FILE = "error.log"


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            traceback.print_exc(file=log)
        print("เกิดข้อผิดพลาดในการอ่านข้อมูล")
        return {}


def save_data(menu_manager, table_manager, order_manager):
    data = {
        "menu": menu_manager.items,
        "tables": table_manager.tables,
        "orders": order_manager.orders
    }

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            traceback.print_exc(file=log)
        print("เกิดข้อผิดพลาดในการบันทึกข้อมูล")

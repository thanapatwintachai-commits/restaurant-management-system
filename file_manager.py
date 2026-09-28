import json
import os
import tempfile
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUNDLED_DATA_FILE = os.path.join(BASE_DIR, "restaurant_data.json")
IS_VERCEL = bool(os.environ.get("VERCEL"))
RUNTIME_DIR = tempfile.gettempdir()
DATA_FILE = os.path.join(RUNTIME_DIR, "restaurant_data_runtime.json") if IS_VERCEL else BUNDLED_DATA_FILE
LOG_FILE = os.path.join(RUNTIME_DIR, "restaurant_error.log") if IS_VERCEL else os.path.join(BASE_DIR, "error.log")


def _load_path():
    if IS_VERCEL and os.path.exists(DATA_FILE):
        return DATA_FILE
    return BUNDLED_DATA_FILE


def load_data():
    try:
        with open(_load_path(), "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                traceback.print_exc(file=log)
        except Exception:
            pass
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
        return True
    except Exception:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                traceback.print_exc(file=log)
        except Exception:
            pass
        print("เกิดข้อผิดพลาดในการบันทึกข้อมูล")
        return False

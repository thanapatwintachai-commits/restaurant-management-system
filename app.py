from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash

from menu import MenuManager
from table import TableManager
from order import OrderManager
from kitchen import KitchenManager
from billing import calculate_bill
from auth import AuthManager
from file_manager import load_data, save_data
from activity_logger import log_activity

app = Flask(__name__)
app.secret_key = "restaurant-management-secret-key"


def build_managers():
    data = load_data()
    return (
        MenuManager(data.get("menu", [])),
        TableManager(data.get("tables", [])),
        OrderManager(data.get("orders", [])),
        KitchenManager(),
        AuthManager(),
    )


menu_manager, table_manager, order_manager, kitchen_manager, auth = build_managers()


def current_user():
    return session.get("user")


def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = current_user()
            if user is None:
                return redirect(url_for("login"))
            if user.get("role") not in roles:
                flash("คุณไม่มีสิทธิ์เข้าถึงหน้านี้", "error")
                return redirect(url_for("index"))
            return view(*args, **kwargs)
        return wrapped
    return decorator


def save_all():
    save_data(menu_manager, table_manager, order_manager)


@app.route("/")
def index():
    if not current_user():
        return redirect(url_for("login"))

    paid_orders = [o for o in order_manager.orders if o.get("status") == "paid"]
    open_orders = [o for o in order_manager.orders if o.get("status") == "open"]
    available_tables = [t for t in table_manager.tables if t.get("status") == "ว่าง"]
    occupied_tables = [t for t in table_manager.tables if t.get("status") == "มีลูกค้า"]

    best_selling = {}
    for order in paid_orders:
        for item in order.get("items", []):
            best_selling[item["menu_id"]] = best_selling.get(item["menu_id"], 0) + item["quantity"]
    best_selling_list = []
    for menu_id, quantity in best_selling.items():
        item = menu_manager.find(menu_id)
        if item:
            best_selling_list.append({"name": item["name"], "quantity": quantity})
    best_selling_list.sort(key=lambda x: x["quantity"], reverse=True)

    return render_template(
        "index.html",
        user=current_user(), menu=menu_manager.items, tables=table_manager.tables,
        orders=order_manager.orders, total_sales=order_manager.total_sales(),
        paid_orders=paid_orders, open_orders=open_orders,
        available_tables=available_tables, occupied_tables=occupied_tables,
        best_selling=best_selling_list[:5]
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = auth.login(username, password)
        if user:
            session["user"] = user
            log_activity(username, f"เข้าสู่ระบบสำเร็จ (role={user['role']})")
            return redirect(url_for("index"))
        return render_template("login.html", error="Username หรือ Password ไม่ถูกต้อง")
    return render_template("login.html", error="")


@app.route("/logout")
def logout():
    user = current_user()
    if user:
        log_activity(user["username"], "ออกจากระบบ")
    session.clear()
    return redirect(url_for("login"))


@app.route("/menu")
def menu():
    if not current_user():
        return redirect(url_for("login"))
    keyword = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "all")
    status = request.args.get("status", "all")
    items = menu_manager.items
    if keyword:
        items = [x for x in items if keyword in x.get("name", "").lower() or keyword in x.get("category", "").lower()]
    if category != "all":
        items = [x for x in items if x.get("category") == category]
    if status != "all":
        items = [x for x in items if x.get("status") == status]
    categories = sorted({x.get("category", "") for x in menu_manager.items if x.get("category")})
    return render_template("menu.html", user=current_user(), menu=items, categories=categories, q=keyword, category=category, status=status)


@app.route("/menu/add", methods=["GET", "POST"])
@roles_required("admin")
def menu_add():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            category = request.form.get("category", "").strip()
            price = float(request.form.get("price", "0"))
            image = request.form.get("image", "").strip()
            status = request.form.get("status", "พร้อมขาย")
            if not name or not category or price <= 0:
                raise ValueError("กรุณากรอกข้อมูลให้ครบและราคาต้องมากกว่า 0")
            menu_manager.add_item(name, price, category, image)
            new_item = menu_manager.find(menu_manager._next_id() - 1)
            if new_item is not None:
                new_item["status"] = status
            save_all()
            log_activity(current_user()["username"], f"เพิ่มเมนู {name}")
            flash("เพิ่มเมนูสำเร็จ", "success")
            return redirect(url_for("menu"))
        except Exception as e:
            return render_template("menu_form.html", user=current_user(), title="เพิ่มเมนู", item=None, error=str(e))
    return render_template("menu_form.html", user=current_user(), title="เพิ่มเมนู", item=None, error="")


@app.route("/menu/edit/<int:item_id>", methods=["GET", "POST"])
@roles_required("admin")
def menu_edit(item_id):
    item = menu_manager.find(item_id)
    if item is None:
        flash("ไม่พบเมนู", "error")
        return redirect(url_for("menu"))
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            category = request.form.get("category", "").strip()
            price = float(request.form.get("price", "0"))
            image = request.form.get("image", "").strip()
            status = request.form.get("status", "พร้อมขาย")
            if not name or not category or price <= 0:
                raise ValueError("กรุณากรอกข้อมูลให้ครบและราคาต้องมากกว่า 0")
            item.update({"name": name, "price": price, "category": category, "image": image, "status": status})
            save_all()
            log_activity(current_user()["username"], f"แก้ไขเมนู #{item_id} {name}")
            flash("แก้ไขเมนูสำเร็จ", "success")
            return redirect(url_for("menu"))
        except Exception as e:
            return render_template("menu_form.html", user=current_user(), title="แก้ไขเมนู", item=item, error=str(e))
    return render_template("menu_form.html", user=current_user(), title="แก้ไขเมนู", item=item, error="")


@app.post("/menu/delete/<int:item_id>")
@roles_required("admin")
def menu_delete(item_id):
    item = menu_manager.find(item_id)
    if item is None:
        flash("ไม่พบเมนู", "error")
        return redirect(url_for("menu"))
    name = item["name"]
    result = menu_manager.delete_item(item_id)
    if result is False:
        flash("ไม่สามารถลบเมนูได้", "error")
    else:
        save_all()
        log_activity(current_user()["username"], f"ลบเมนู #{item_id} {name}")
        flash("ลบเมนูสำเร็จ", "success")
    return redirect(url_for("menu"))


@app.post("/menu/toggle/<int:item_id>")
@roles_required("admin", "staff")
def menu_toggle(item_id):
    item = menu_manager.find(item_id)
    if not item:
        flash("ไม่พบเมนู", "error")
        return redirect(url_for("menu"))
    new_status = "หมด" if item.get("status") != "หมด" else "พร้อมขาย"
    menu_manager.change_status(item_id, new_status)
    save_all()
    log_activity(current_user()["username"], f"เปลี่ยนสถานะเมนู #{item_id} เป็น {new_status}")
    return redirect(url_for("menu"))


@app.route("/tables")
@roles_required("admin", "staff", "customer")
def tables():
    return render_template("tables.html", user=current_user(), tables=table_manager.tables)


@app.route("/orders")
@roles_required("admin", "staff", "customer")
def orders():
    # Search / filter / sort / pagination are server-side here.
    q = request.args.get("q", "").strip().lower()
    status = request.args.get("status", "all")
    sort = request.args.get("sort", "newest")
    try:
        page = max(1, int(request.args.get("page", "1")))
    except ValueError:
        page = 1
    per_page = 5
    items = list(order_manager.orders)
    if q:
        items = [o for o in items if q in str(o.get("id", "")).lower() or q in str(o.get("table_id", "")).lower() or q in o.get("customer", "").lower()]
    if status in {"open", "paid"}:
        items = [o for o in items if o.get("status") == status]
    items.sort(key=lambda o: o.get("created_at", ""), reverse=(sort == "newest"))
    total = len(items)
    pages = max(1, (total + per_page - 1) // per_page)
    page = min(page, pages)
    shown = items[(page - 1) * per_page: page * per_page]
    return render_template("orders.html", user=current_user(), orders=shown, menu=menu_manager.items,
                           q=q, status=status, sort=sort, page=page, pages=pages, total=total)


@app.route("/order/create", methods=["GET", "POST"])
@roles_required("admin", "staff", "customer")
def create_order():
    if request.method == "POST":
        try:
            table_id = int(request.form.get("table_id", ""))
            customer = request.form.get("customer", "").strip() or current_user()["username"]
        except ValueError:
            return render_template("order_create.html", user=current_user(), tables=table_manager.tables, menu=menu_manager.items, error="เลขโต๊ะไม่ถูกต้อง")
        table = table_manager.get(table_id)
        if table is None:
            return render_template("order_create.html", user=current_user(), tables=table_manager.tables, menu=menu_manager.items, error="ไม่พบโต๊ะ")
        if table["status"] == "ว่าง":
            ok, message = table_manager.check_in(table_id, customer)
            if not ok:
                return render_template("order_create.html", user=current_user(), tables=table_manager.tables, menu=menu_manager.items, error=message)
        order = order_manager.get_open_order(table_id)
        if order is None:
            order = {"id": order_manager._next_id(), "table_id": table_id, "customer": customer,
                     "created_at": datetime.now().isoformat(timespec="seconds"), "status": "open", "items": []}
            order_manager.orders.append(order)
        added = 0
        for item in menu_manager.items:
            try:
                quantity = int(request.form.get(f"quantity_{item['id']}", "0"))
            except ValueError:
                quantity = 0
            if quantity <= 0 or item.get("status") == "หมด":
                continue
            existing = next((x for x in order["items"] if x["menu_id"] == item["id"]), None)
            if existing:
                existing["quantity"] += quantity
            else:
                order["items"].append({"menu_id": item["id"], "quantity": quantity})
            added += quantity
        if added == 0:
            return render_template("order_create.html", user=current_user(), tables=table_manager.tables, menu=menu_manager.items, error="กรุณาเลือกอาหารอย่างน้อย 1 รายการ")
        save_all()
        log_activity(current_user()["username"], f"สร้าง/เพิ่มออเดอร์ #{order['id']} โต๊ะ {table_id}")
        flash("บันทึกออเดอร์สำเร็จ", "success")
        return redirect(url_for("orders"))
    return render_template("order_create.html", user=current_user(), tables=table_manager.tables, menu=menu_manager.items, error="")


@app.route("/kitchen")
@roles_required("admin", "staff")
def kitchen():
    open_orders = [o for o in order_manager.orders if o.get("status") == "open"]
    open_orders.sort(key=lambda o: o.get("created_at", ""))
    return render_template("kitchen.html", user=current_user(), orders=open_orders, menu=menu_manager.items)


@app.route("/billing")
@roles_required("admin", "staff")
def billing():
    return render_template("billing.html", user=current_user(), tables=table_manager.tables)


@app.route("/bill/<int:table_id>")
@roles_required("admin", "staff")
def bill(table_id):
    order = order_manager.get_open_order(table_id)
    bill_data = calculate_bill(order, menu_manager) if order else None
    return render_template("bill.html", user=current_user(), order=order, bill=bill_data, menu=menu_manager.items)


@app.post("/pay/<int:table_id>")
@roles_required("admin", "staff")
def pay_bill(table_id):
    order = order_manager.get_open_order(table_id)
    if order is None:
        flash("ไม่พบออเดอร์ที่ยังไม่ชำระ", "error")
        return redirect(url_for("billing"))
    bill_data = calculate_bill(order, menu_manager)
    order_manager.save_payment(order, bill_data)
    order["status"] = "paid"
    table_manager.checkout(table_id)
    save_all()
    log_activity(current_user()["username"], f"ชำระเงินออเดอร์ #{order['id']} โต๊ะ {table_id} จำนวน {bill_data['total']:.2f} บาท")
    flash("ชำระเงินสำเร็จ", "success")
    return redirect(url_for("tables"))


@app.route("/report")
@roles_required("admin", "staff")
def report():
    paid = [o for o in order_manager.orders if o.get("status") == "paid"]
    sales = order_manager.total_sales()
    counts = {}
    for order in paid:
        for item in order.get("items", []):
            counts[item["menu_id"]] = counts.get(item["menu_id"], 0) + item["quantity"]
    best = []
    for menu_id, qty in counts.items():
        item = menu_manager.find(menu_id)
        if item:
            best.append({"name": item["name"], "quantity": qty})
    best.sort(key=lambda x: x["quantity"], reverse=True)
    return render_template("report.html", user=current_user(), sales=sales, paid_count=len(paid), best=best)


@app.route("/logs")
@roles_required("admin")
def logs():
    try:
        with open("activity.log", "r", encoding="utf-8") as f:
            entries = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        entries = []
    return render_template("logs.html", user=current_user(), logs=list(reversed(entries)))


if __name__ == "__main__":
    app.run(debug=True)

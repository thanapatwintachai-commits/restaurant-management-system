def show_daily_report(order_manager, menu_manager):

    paid_orders = [
        order
        for order in order_manager.orders
        if order["status"] == "paid"
    ]

    total_sales = order_manager.total_sales()

    total_items_sold = 0

    sales_by_menu = {}

    for order in paid_orders:

        bill = order.get(
            "bill",
            {}
        )

        for line in bill.get(
            "lines",
            []
        ):

            quantity = line["quantity"]

            total_items_sold += quantity

            name = line["name"]

            sales_by_menu[name] = (
                sales_by_menu.get(name, 0)
                + quantity
            )

    # ==========================================
    # DASHBOARD
    # ==========================================

    print("\n")
    print("==================================================")
    print("              RESTAURANT DASHBOARD")
    print("==================================================")

    print(
        f"จำนวนบิลที่ชำระแล้ว : "
        f"{len(paid_orders)} บิล"
    )

    print(
        f"ยอดขายรวม           : "
        f"{total_sales:.2f} บาท"
    )

    print(
        f"จำนวนอาหารที่ขายได้ : "
        f"{total_items_sold} รายการ"
    )

    print(
        f"จำนวนเมนูในระบบ     : "
        f"{len(menu_manager.items)} เมนู"
    )

    print("==================================================")

    # ==========================================
    # MENU STATUS
    # ==========================================

    ready_count = 0
    sold_out_count = 0

    for item in menu_manager.items:

        if item["status"] == "พร้อมขาย":

            ready_count += 1

        elif item["status"] == "หมด":

            sold_out_count += 1

    print("\n========== สถานะเมนู ==========")

    print(
        f"พร้อมขาย : {ready_count} เมนู"
    )

    print(
        f"หมด      : {sold_out_count} เมนู"
    )

    # ==========================================
    # TOP SELLING MENU
    # ==========================================

    print("\n========== เมนูขายดี ==========")

    if not sales_by_menu:

        print(
            "ยังไม่มีข้อมูลการขาย"
        )

    else:

        ranked = sorted(
            sales_by_menu.items(),
            key=lambda item: item[1],
            reverse=True
        )

        for rank, (
            name,
            quantity
        ) in enumerate(
            ranked[:5],
            start=1
        ):

            print(
                f"{rank}. {name} "
                f"- ขายได้ {quantity} รายการ"
            )

    # ==========================================
    # RECENT ORDERS
    # ==========================================

    print("\n========== ออเดอร์ล่าสุด ==========")

    if not paid_orders:

        print(
            "ยังไม่มีออเดอร์ที่ชำระเงินแล้ว"
        )

    else:

        recent_orders = paid_orders[-5:]

        for order in reversed(
            recent_orders
        ):

            bill = order.get(
                "bill",
                {}
            )

            print(
                f"Order #{order['id']} "
                f"| โต๊ะ {order['table_id']} "
                f"| {bill.get('total', 0):.2f} บาท"
            )

    print("\n==================================================")
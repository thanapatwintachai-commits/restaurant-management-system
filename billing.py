def calculate_bill(order, menu_manager):

    subtotal = 0
    lines = []

    # =========================
    # คำนวณรายการอาหาร
    # =========================

    for order_item in order["items"]:

        menu_item = menu_manager.find(
            order_item["menu_id"]
        )

        if menu_item is None:
            continue

        quantity = order_item["quantity"]

        line_total = (
            menu_item["price"] * quantity
        )

        subtotal += line_total

        lines.append({
            "name": menu_item["name"],
            "quantity": quantity,
            "price": menu_item["price"],
            "total": line_total
        })

    # =========================
    # ส่วนลด
    # =========================

    if subtotal >= 500:
        discount = subtotal * 0.05
    else:
        discount = 0

    # =========================
    # คำนวณภาษี
    # =========================

    taxable = subtotal - discount

    tax = taxable * 0.07

    # =========================
    # ค่าบริการ
    # =========================

    service_charge = taxable * 0.10

    # =========================
    # ยอดสุทธิ
    # =========================

    total = (
        taxable
        + tax
        + service_charge
    )

    return {
        "lines": lines,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "service_charge": service_charge,
        "total": total
    }


def show_receipt(order, bill):

    print("\n")
    print("========================================")
    print("              RECEIPT")
    print("           RESTAURANT")
    print("========================================")

    print(f"โต๊ะ: {order['table_id']}")

    print(
        f"ลูกค้า: "
        f"{order.get('customer', '-')}"
    )

    print(
        f"เวลา: "
        f"{order.get('created_at', '-')}"
    )

    print("----------------------------------------")

    print(
        f"{'รายการ':<18}"
        f"{'จำนวน':>6}"
        f"{'ราคา':>10}"
    )

    print("----------------------------------------")

    for line in bill["lines"]:

        print(
            f"{line['name']:<18}"
            f"{line['quantity']:>6}"
            f"{line['total']:>10.2f}"
        )

    print("----------------------------------------")

    print(
        f"{'ยอดรวม':<25}"
        f"{bill['subtotal']:>10.2f}"
    )

    print(
        f"{'ส่วนลด':<25}"
        f"{bill['discount']:>10.2f}"
    )

    print(
        f"{'ภาษี 7%':<25}"
        f"{bill['tax']:>10.2f}"
    )

    print(
        f"{'ค่าบริการ 10%':<25}"
        f"{bill['service_charge']:>10.2f}"
    )

    print("----------------------------------------")

    print(
        f"{'ยอดสุทธิ':<25}"
        f"{bill['total']:>10.2f}"
    )

    print("========================================")
    print("        ขอบคุณที่ใช้บริการ")
    print("========================================")
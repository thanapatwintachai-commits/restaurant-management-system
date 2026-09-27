def input_int(message):
    while True:
        try:
            value = int(input(message))
            return value
        except ValueError:
            print("กรุณากรอกเป็นตัวเลขจำนวนเต็ม")


def input_float(message):
    while True:
        try:
            value = float(input(message))
            if value < 0:
                print("ค่าต้องไม่ติดลบ")
            else:
                return value
        except ValueError:
            print("กรุณากรอกเป็นตัวเลข")


def pause():
    input("\nกด Enter เพื่อดำเนินการต่อ...")

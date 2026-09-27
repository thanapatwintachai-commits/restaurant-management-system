from datetime import datetime


LOG_FILE = "activity.log"


def log_activity(username, action):

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    message = (
        f"[{now}] "
        f"{username} "
        f"{action}"
    )

    try:

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                message + "\n"
            )

    except Exception as error:

        print(
            f"ไม่สามารถบันทึก Activity Log: {error}"
        )


def show_activity_log():

    try:

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            logs = file.readlines()

    except FileNotFoundError:

        print(
            "\nยังไม่มี Activity Log"
        )

        return

    except Exception as error:

        print(
            f"ไม่สามารถอ่าน Activity Log: {error}"
        )

        return

    print("\n")
    print("==========================================")
    print("             ACTIVITY LOG")
    print("==========================================")

    if not logs:

        print("ยังไม่มีข้อมูล")

        return

    for log in logs:

        print(
            log.strip()
        )

    print("==========================================")
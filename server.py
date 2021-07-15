from draw_image import DrawImage
from gmail import Gmail
from spreadsheet import SpreadSheet
from time import sleep
import re
from db import EmailDB

SENDER_EMAIL = "yoongi@yoongi.kim"


def check_email_address(email):
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    if (re.search(regex, email)):
        return True
    else:
        return False


def main():
    gmail = Gmail()
    spreadsheet = SpreadSheet()
    drawimage = DrawImage()
    email_db = EmailDB()  # Prevent sending email twice

    data = spreadsheet.get_data()
    for row in data:
        print(row)

    while True:
        try:
            data = spreadsheet.get_data()

            for i, row in enumerate(data):
                if i == 0:
                    continue

                # add email to database that is already recorded at spreadsheet but not in db
                if len(row) == 3 and row[2] == '1' and not email_db.is_sent(row[3]):
                    print(f"[{row[3]}] db: NOT SENT: spreadsheet: SENT")
                    email_db.add(row[3])

                if len(row) == 3 and row[2] != '1':
                    print(f"Send to {row}")
                    sender = SENDER_EMAIL
                    to = row[1]
                    name = row[0]

                    if email_db.is_sent(to):
                        print(f"[{to}] db: SENT, spreadsheet: NOT SENT")
                        continue

                    if not name:
                        print(f"Invalid name: {name}")
                        continue
                    image1_path = drawimage.draw_image_1(name)
                    image2_path = drawimage.draw_image_2(name)

                    if not check_email_address(to):
                        print(f"Invalid email: {to}")
                        continue

                    is_sent = gmail.send_email(sender, to, image1_path, image2_path)
                    if not is_sent:
                        print(f"Email send failed: {to}")
                    if is_sent:
                        email_db.add(to)
                        sheet_result = spreadsheet.write_value(f"C{i + 1}:C{i + 1}", values=[[1]])
                        if not sheet_result:
                            print(f"Write to spreadsheet failed: {to}")
                            raise Exception("SpreadSheet Error")

        except Exception as e:
            print(f"Error: {e}")
        sleep(60)


if __name__ == '__main__':
    main()

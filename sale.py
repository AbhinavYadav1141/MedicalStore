from mysql.connector import connect
import actions

conn = connect(host='localhost', user='root', password='1234')
cur = conn.cursor()


def create_record(receipt_no, name, count, date, price, table="Sale"):
    query = f"insert into {table} values({receipt_no}, '{name}', {count}, '{date}', {price})"
    cur.execute(query)
    conn.commit()


def create_record_from_list(lst, table="Sale"):
    create_record(lst[0], lst[1], lst[2], lst[3], lst[5], table)


def create_records(records, table="Sale"):
    for i in records:
        create_record_from_list(i, table)


def create_table(receipt_no, count):
    cur.execute("use Sales")
    table = 't' + str(receipt_no)

    l = []

    for i in range(count):
        bar = input("Enter medicine barcode: ")
        while not bar.isdigit():
            bar = input("Barcode should be an integer. Please enter again: ")

        qty = input("Enter no. of tablets(or bottles) sold: ")
        while not qty.isdigit():
            qty = input("No. of tablets should be an integer. Please enter again: ")

        price = input("Enter price of medicine: ")
        while not price.isdigit():
            price = input("Price should be an integer. Please enter again: ")

        l.append((bar, qty, price))

    create_records(l)
    cur.execute("use MedicalStore")


def init():
    pass

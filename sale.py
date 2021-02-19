from mysql.connector import connect
import actions

conn = connect(host='localhost', user='root', password='abhinav1')
cur = conn.cursor()
cur.execute("use MedicalStore")


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

    lst = []

    for i in range(count):
        print(f"\nRecord{i+1}")
        bar = input("Enter medicine barcode: ")
        while not bar.isdigit():
            bar = input("Barcode should be an integer. Please enter again: ")

        qty = input("Enter no. of tablets(or bottles) sold: ")
        while not qty.isdigit():
            qty = input("No. of tablets should be an integer. Please enter again: ")

        price = input("Enter price of medicine: ")
        while not price.isdigit():
            price = input("Price should be an integer. Please enter again: ")

        lst.append((bar, qty, price))

    create_records(lst, table)
    cur.execute("use MedicalStore")


def view():
    print()
    print("How many columns do you want to view:")
    print("2: All columns, All records")
    print("3: All columns, Some records")
    print("4: Some columns, All records")
    print("5: Some columns, Some records")
    print("0: Go to home")
    print("1: Go to Medicine Information")
    ch = input()

    while ch not in '012345' or len(ch) != 1:
        ch = input("Invalid choice. Enter again: ")

    if ch == '0':
        return '0'

    elif ch == '1':
        return '1'

    elif ch == '2':
        actions.format_print(actions.get_columns("Sale"), actions.show_all("Sale"))

    elif ch == '3':
        column = input("Which column do you want to use for record matching").lower()
        columns = actions.get_columns("Sale")
        while column not in columns:
            print(f"Valid Columns: {columns}")
            column = input("Column you entered is not in table. Please enter again: ").lower()
        records = input_rows()
        actions.format_print(columns, actions.search_multiple("Sale", column, records))

    elif ch == '4':
        clm = input_cols()
        actions.format_print(clm, actions.show_columns("Sale", clm))

    elif ch == '5':
        columns = input_cols()
        column = input("Which column do you want to use for record matching")
        columns_all = actions.get_columns("Sale")
        while column not in columns_all:
            column = input("Column you entered is not in table. Please enter again: ")
        records = input_rows()
        actions.format_print(columns, actions.search_multiple("Sale", column, records, columns))


def input_cols():
    num = input("Enter no. of columns you want: ")
    while not num.isdigit():
        num = input("Enter integer value only: ")

    columns = actions.get_columns("Sale")
    clm = []
    print(columns)
    for i in range(int(num)):
        column = input(f"Enter name of column{i + 1}: ").lower()
        while column not in columns:
            column = input("The column you entered is not in table. Please enter again: ").lower()
        clm.append(column)
    return clm


def input_rows():
    num = input("Enter no. of records you want to view: ")
    while not num.isdigit():
        num = input("Enter integer value only: ")
    records = []
    for i in range(int(num)):
        record = input(f'Enter record{i + 1}: ')
        records.append(record)
    return records


def insert():
    pass


def delete():
    pass


def update():
    pass


def search():
    pass


def init():
    print('\n')
    print("=" * 10 + "     Sale Information     " + "=" * 10)
    while True:
        try:
            ch = input(msg)
            code = 1

            while ch not in '012345' or len(ch) != 1:
                ch = input("Invalid choice. Enter again: ")

            if ch == '0':
                break

            elif ch == '1':
                code = view()

            elif ch == '2':
                code = insert()

            elif ch == '3':
                code = delete()

            elif ch == '4':
                code = update()

            elif ch == '5':
                code = search()

            if code == '0':
                break

        except Exception as e:
            print("An Error Occurred!!")
            print(e)


msg = """

    Enter Your Choice:
    0: Home
    1: View Sale Information
    2: Insert records
    3: Delete records
    4: Update record
    5: Search records
    """

if __name__ == '__main__':
    actions.conn = conn
    actions.cur = cur
    init()

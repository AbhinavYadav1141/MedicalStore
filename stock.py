from mysql.connector import connect
import actions


conn = connect(host='localhost', user='root', password='1234')
cur = conn.cursor()
cur.execute("use MedicalStore")


def create_record(batch, bar, cost, date, qty_left, mfg, exp):
    query = f"insert into Stock values('{batch}', '{bar}', '{cost}', '{date}', {qty_left}, '{mfg}'. '{exp}')"
    cur.execute(query)
    conn.commit()


def create_record_from_list(lst):
    create_record(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6])


def create_records(records):
    for i in records:
        create_record_from_list(i)


def view():
    print()
    print("How many columns do you want to view:")
    print("2: All columns, All records")
    print("3: All columns, Some records")
    print("4: Some columns, All records")
    print("5: Some columns, Some records")
    print("6: Expired Medicines")
    print("0: Go to home")
    print("1: Go to Stock Information")
    ch = input()

    while ch not in '0123456' or len(ch) != 1:
        ch = input("Invalid choice. Enter again: ")

    if ch == '0':
        return '0'

    elif ch == '1':
        return '1'

    elif ch == '2':
        actions.format_print(actions.get_columns("Stock"), actions.show_all("Stock"))

    elif ch == '3':
        column = input("Which column do you want to use for record matching").lower()
        columns = actions.get_columns("Stock")
        while column not in columns:
            column = input("Column you entered is not in table. Please enter again: ").lower()
        records = actions.input_rows()
        actions.format_print(columns, actions.search_multiple("Stock", column, records))

    elif ch == '4':
        clm = actions.input_cols("Stock")
        actions.format_print(clm, actions.show_columns("Stock", clm))

    elif ch == '5':
        columns = actions.input_cols("Stock")
        column = input("Which column do you want to use for record matching").lower()
        columns_all = actions.get_columns("Stock")
        while column not in columns_all:
            column = input("Column you entered is not in table. Please enter again: ").lower()
        records = actions.input_rows()
        actions.format_print(columns, actions.search_multiple("Stock", column, records, columns))

    elif ch == '6':
        cur.execute("select * from Stock where Exp<(select sysdate())")
        actions.format_print(actions.get_columns("Stock"),  cur.fetchall())


def insert():
    print()
    print("Insert Options:")
    print("2. Enter values separately")
    print("3. Enter many records at once")
    print("0. Home")
    print("1. Stock Information")

    ch = input("Enter your choice: ")
    while ch not in '0123' or len(ch) != 1:
        ch = input("Invalid choice! Please Enter again: ")

    if ch == '0':
        return '0'

    elif ch == '1':
        return '1'

    elif ch == '2':
        print("Enter Records")
        batch = input("Batch No.: ")
        while not batch.isdigit():
            batch = input("Batch No. should be an integer only. Please enter again: ")

        bar = input("Barcode of medicine: ")
        while not bar.isdigit():
            bar = input("Barcode should be an integer only! Please enter again: ")

        cp = input("Enter Cost per packet (Rs): ")
        while not cp.isdigit():
            cp = "Cost should be an integer! Please enter again: "

        p_date = input("Purchase date (yyyy-mm-dd): ")

        qty = input("Quantity left (no. of packets): ")
        while not qty.isdigit():
            qty = input("Quantity should be an integer only! Please enter again: ")

        mfg = input("Manufacturing date: ")

        exp = input("Expiry date: ")

        try:
            create_record(batch, bar, cp, p_date, qty, mfg, exp)
        except Exception as e:
            print("An Error Occurred!!")
            print(e)

    elif ch == '3':
        num = input("How many records do you want to create: ")
        while not num.isdigit():
            num = input("No. of records should be an integer only! Enter again: ")

        records = []
        for i in range(int(num)):
            record = input("Enter values separated with semicolon(;): ").split(';')

            while len(record) != actions.column_count("Stock"):
                record = input("No. of records you entered is not equal to no. of columns! Enter again: ").split(';')

            records.append(record)
        try:
            create_records(records)
        except Exception as e:
            print("An Error Occurred: ")
            print(e)


def delete():
    print()
    print("Delete Options")
    print("2. Delete using batch no.")
    print("3. Delete using condition")
    print("0. Home")
    print("1. Stock Information")
    ch = input("Enter your choice: ")

    while ch not in '0123' or len(ch) != 1:
        ch = input("Invalid choice! Please enter again: ")

    if ch == '0':
        return 0

    elif ch == '1':
        return '1'

    elif ch == '2':
        batch = input("Enter batch no. of stock to be deleted: ")
        while not batch.isdigit():
            batch = input("Barcode should be an integer only! Please enter again: ")

        actions.delete_record("Stock", "BatchNo", batch)

    elif ch == '3':
        condition = input("Enter condition for deletion: ")
        try:
            actions.delete_by_condition("Stock", condition)
        except Exception as e:
            print(e)
            print("Your condition had the above error!")


def update():
    print("Update options:")
    print("2. Update using batch no.")
    print("3. Update using condition")
    print("0. Home")
    print("1. Medicine Information")
    ch = input("Enter your choice: ")

    while ch not in '0123' or len(ch) != 1:
        ch = input("Invalid choice! Please enter again: ")

    if ch == '0':
        return 0

    elif ch == '1':
        return '1'

    elif ch == '2':
        batch = input("Enter batch no. of stock: ")
        while not batch.isdigit():
            batch = input("Batch no. should be an integer only! Please enter again: ")

        condition = f"BatchNo='{batch}'"

    elif ch == '3':
        condition = input("Enter condition: ")

    if ch in '23' and len(ch) == 1:
        column = input("Which column do you want to update: ").lower()
        columns = actions.get_columns("Stock")
        while column not in columns:
            column = input("Column you entered is not in table! Enter again: ").lower()
        val = input("Enter value: ")
        try:
            actions.update("Stock", column, val, condition)
        except Exception as e:
            print("An error occurred!")
            print(e)


def search():
    print()
    print("Search Options:")
    print("2: Search using barcode")
    print("3: Search using many fields")
    print("4: Search using condition")
    print("0: Home")
    print("1: Medicine information")
    ch = input("Enter your choice: ")

    while ch not in '01234' or len(ch) != 1:
        ch = input("Invalid choice. Enter again: ")

    if ch == '0':
        return '0'

    elif ch == '1':
        return '1'

    elif ch == '2':
        batch = input("Enter batch no.: ")
        while not batch.isdigit():
            batch = input("Batch no. should only be integer. Enter again: ")
        actions.format_print(actions.get_columns("Stock"),
                             actions.search_by_condition("Stock", f"BatchNo={batch}"))

    elif ch == '3':
        num = input("Enter no. of columns you want to use: ")
        while not num.isdigit():
            num = input("Enter integer value only: ")

        columns = actions.get_columns("Stock")
        condition = ''
        for i in range(int(num)):
            col = input(f"Enter name of column{i + 1}: ")
            while col not in columns:
                col = input("The column you entered is not in table. Please enter again: ")
            val = input(f"Enter value for column{i + 1}: ")
            op = input("Enter condition (<, =, >, >=, <=): ")
            while op not in ['<', '>', '=', '<=', '>=']:
                op = input("Wrong operator! Please enter again: ")
            condition += col + op + "'" + val + "'"
            if i != int(num) - 1:
                condition += '&&'
        print(condition)
        actions.format_print(columns, actions.search_by_condition("Stock", condition))

    elif ch == '4':

        try:
            condition = input("Enter condition: ")
            actions.format_print(actions.get_columns("Stock"),
                                 actions.search_by_condition("Stock", condition))
        except Exception as e:
            print(e)
            print("There was an error!!")


def init():
    print('\n')
    print("=" * 10 + "     Stock Information     " + "=" * 10)
    while True:
        try:
            ch = input(msg)
            code = 1

            while ch not in '012345' or len(ch) != 1:
                ch = input("Invalid choice. Enter again: ")

            if ch == '0':
                code = 0
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
    1: View Stock Information
    2: Insert records
    3: Delete records
    4: Update record
    5: Search records
    """

if __name__ == '__main__':
    actions.conn = conn
    actions.cur = cur
    init()

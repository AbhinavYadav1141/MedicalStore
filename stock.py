from mysql.connector import connect
import actions


def create_record(batch, bar, cost, date, qty_left, mfg, exp):
    date, mfg, exp = actions.date_format(date, mfg, exp)
    query = f"insert into Stock values('{batch}', '{bar}', '{cost}', '{date}', {qty_left}, '{mfg}', '{exp}')"
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
    columns_all = actions.get_columns("Stock")
    col_dict = {i+1: columns_all[i] for i in range(len(columns_all))}

    while ch not in '0123456' or len(ch) != 1:
        ch = input("Invalid choice. Enter again: ")

    if ch == '0':
        return '0'

    elif ch == '1':
        return '1'

    elif ch == '2':
        actions.format_print(columns_all, actions.show_all("Stock"))

    elif ch == '3':
        print("The columns are:")
        print(str(col_dict).lstrip('{').rstrip('}'))
        column = input("Which column no. do you want to use for record matching: ").lower()
        while not column.isdigit() or int(column) not in col_dict:
            column = input("Column no. you entered is not in option. Please enter again: ").lower()
        records = actions.input_rows()
        actions.format_print(columns_all, actions.search_multiple("Stock", col_dict[int(column)], records))

    elif ch == '4':
        clm = actions.input_cols("Stock")
        actions.format_print(clm, actions.show_columns("Stock", clm))

    elif ch == '5':
        columns = actions.input_cols("Stock")
        column = input("Which column no. do you want to use for record matching").lower()
        while not column.isdigit() or int(column) not in col_dict:
            column = input("Column no. you entered is not in option. Please enter again: ").lower()
        records = actions.input_rows()
        actions.format_print(columns, actions.search_multiple("Stock", col_dict[int(column)], records, columns))

    elif ch == '6':
        cur.execute("select * from Stock where Exp<(select sysdate())")
        actions.format_print(actions.get_columns("Stock"),  cur.fetchall())


def insert():
    print()
    print("Enter Records")

    batch = input("Batch No.: ")
    batch_nos = actions.get_values("Stock", "BatchNo")
    while not batch.isdigit() or batch in batch_nos:
        if not batch.isdigit():
            batch = input("Batch No. should be an integer only. Please enter again: ")
        else:
            batch = input("This batch no. is already there! Enter another: ")

    bar = input("Barcode of medicine: ")
    while not bar.isdigit():
        bar = input("Barcode should be an integer only! Please enter again: ")

    cp = input("Enter Cost per packet (Rs): ")
    while not cp.isdigit():
        cp = "Cost should be an integer! Please enter again: "

    p_date = input("Purchase date (yyyy-mm-dd): ")
    while not actions.check_date(p_date):
        p_date = input("Your date format is nor correct! Enter again(yyyy-mm-dd): ")

    qty = input("Quantity left (no. of packets): ")
    while not qty.isdigit():
        qty = input("Quantity should be an integer only! Please enter again: ")

    mfg = input("Manufacturing date: ")
    while not actions.check_date(mfg):
        mfg = input("Your date format is nor correct! Enter again(yyyy-mm-dd): ")

    exp = input("Expiry date: ")
    while not actions.check_date(exp):
        exp = input("Your date format is nor correct! Enter again(yyyy-mm-dd): ")

    create_record(batch, bar, cp, p_date, qty, mfg, exp)
    print("Created record successfully...")


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
        print("Deleted successfully...")

    elif ch == '3':
        condition = input("Enter condition for deletion: ")
        try:
            actions.delete_by_condition("Stock", condition)
            print("Deleted successfully...")
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

    condition = '1=1'

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
        condition = input('Enter condition(<column_name><operator>"<value>"): ')
        while True:
            try:
                cur.execute(f"select 1+2 where {condition}")
                cur.fetchall()
                break
            except Exception as e:
                print(e)
                condition = input('Your condition had above error! Enter again(<column_name><operator>"<value>"): ')

    if ch in '23' and len(ch) == 1:
        columns_all = actions.get_columns("Stock")
        col_dict = {i + 1: columns_all[i] for i in range(len(columns_all))}
        print(col_dict)
        column = input("Which column no. do you want to update: ").lower()
        while column not in col_dict:
            column = input("Column you entered is not in table! Enter again: ").lower()
        column = col_dict[int(column)]
        val = input("Enter value: ")
        try:
            actions.update("Stock", column, val, condition)
            print("Updated successfully...")
        except Exception as e:
            print("An error occurred!!  Error code: 021" if ch == '2' else "Your condition had an error!!")
            print(e)


def search():
    print()
    print("Search Options:")
    print("2: Search using batch no.")
    print("3: Search using many fields")
    print("4: Search using condition")
    print("0: Home")
    print("1: Medicine information")
    ch = input("Enter your choice: ")

    columns_all = actions.get_columns("Stock")
    col_dict = {i+1: columns_all[i] for i in range(len(columns_all))}

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
        actions.format_print(columns_all,
                             actions.search_by_condition("Stock", f"BatchNo={batch}"))

    elif ch == '3':
        num = input("Enter no. of columns you want to use: ")
        while not num.isdigit():
            num = input("Enter integer value only: ")

        print("The columns are:")
        print(str(col_dict).lstrip('{').rstrip('}'))
        condition = ''
        for i in range(int(num)):
            col = input(f"Enter code for column{i + 1}: ")
            while not col.isdigit() or int(col) not in col_dict:
                col = input("The column no. you entered is not in option. Please enter again: ")
            col = col_dict[int(col)]
            val = input(f"Enter value for column{i + 1}: ")
            op = input("Enter operator (<, =, >, >=, <=): ")
            while op not in ['<', '>', '=', '<=', '>=']:
                op = input("Wrong operator! Please enter again: ")
            condition += col + op + "'" + val + "'"
            if i != int(num) - 1:
                condition += '&&'
        actions.format_print(columns_all, actions.search_by_condition("Stock", condition))

    elif ch == '4':

        try:
            condition = input('Enter condition(<column_name><operator>"<value>": ')
            while True:
                try:
                    cur.execute(f"select 1+2 where {condition}")
                    cur.fetchall()
                    break
                except Exception as e:
                    print(e)
                    condition = input("Your condition had above error! Enter again: ")
            actions.format_print(actions.get_columns("Stock"),
                                 actions.search_by_condition("Stock", condition))
        except Exception as e:
            print(e)
            print("There was an error!!  Error code: 022")


def init():
    print("=" * 10 + "     Stock Information     " + "=" * 10)
    while True:
        where = 0
        try:
            ch = input(msg)
            code = 1

            while ch not in '012345' or len(ch) != 1:
                ch = input("Invalid choice. Enter again: ")

            where = 1

            if ch == '0':
                break

            elif ch == '1':
                code = view()

            elif ch == '2':
                insert()

            elif ch == '3':
                code = delete()

            elif ch == '4':
                code = update()

            elif ch == '5':
                code = search()

            if code == '0':
                break

        except KeyboardInterrupt:
            if where == 0:
                break

        except Exception as e:
            print("An Error Occurred!!  Error code: 02")
            print(e)


msg = """

0: Home
1: View Stock Information
2: Insert records
3: Delete records
4: Update record
5: Search records

Enter Your Choice: """

if __name__ == '__main__':
    conn = connect(host='localhost', user='root', password='abhinav1')
    cur = conn.cursor()
    cur.execute("use MedicalStore")
    actions.conn = conn
    actions.cur = cur
    init()

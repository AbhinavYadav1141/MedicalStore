from mysql.connector import connect
import actions
import traceback


def create_record(barcode, name, m_type, composition):
    if composition == "NULL":
        query = f"insert into MedicineInfo values({barcode}, '{name}', '{m_type}', {composition})"
    else:
        query = f"insert into MedicineInfo values({barcode}, '{name}', '{m_type}', '{composition}')"

    cur.execute(query)
    conn.commit()


def create_record_from_list(lst):
    create_record(lst[0], lst[1], lst[2], lst[3])


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
    print("0: Go to home")
    print("1: Go to Medicine Information")
    ch = input()
    columns_all = actions.get_columns("MedicineInfo")
    col_dict = {i+1: columns_all[i] for i in range(len(columns_all))}

    while ch not in '012345' or len(ch) != 1:
        ch = input("Invalid choice. Enter again: ")

    if ch == '0':
        return '0'

    elif ch == '1':
        return '1'

    elif ch == '2':
        actions.format_print(actions.get_columns("MedicineInfo"), actions.show_all("MedicineInfo"))

    elif ch == '3':
        print("All columns are:")
        print(str(col_dict).lstrip('{').rstrip('}'))
        column = input("Which column no. do you want to use for record matching: ").lower()
        while not column.isdigit() or int(column) not in col_dict:
            column = input("Column no. you entered is not in option. Please enter again: ").lower()
        records = actions.input_rows()
        column = col_dict[int(column)]
        if column.lower() == "composition":
            q = f"select * from MedicineInfo where {column} like '%{records[0]}%' "
            for i in range(1, len(records)):
                q += f"or {column} like '%{records[i]}%' "
            cur.execute(q)
            actions.format_print(columns_all, cur.fetchall())
        else:
            actions.format_print(columns_all, actions.search_multiple("MedicineInfo", column, records))

    elif ch == '4':
        clm = actions.input_cols("MedicineInfo")
        actions.format_print(clm, actions.show_columns("MedicineInfo", clm))

    elif ch == '5':
        columns = actions.input_cols("MedicineInfo")
        column = input("Which column no. do you want to use for record matching: ").lower()
        while not column.isdigit() or int(column) not in col_dict:
            column = input("Column no. you entered is not in option. Please enter again: ").lower()
        column = col_dict[int(column)]
        records = tuple(actions.input_rows())
        cols = str(columns).lstrip('[').rstrip(']').replace("'", '')
        if column.lower() == "composition":
            q = f"select {cols} from MedicineInfo where {column} like '%{records[0]}%' "
            for i in range(1, len(records)):
                q += f"or {column} like '%{records[i]}%' "
            cur.execute(q)
            actions.format_print(columns, cur.fetchall())
        else:
            actions.format_print(columns, actions.search_multiple("MedicineInfo", column, records))


def insert(bar=None):
    print()
    if bar is None:
        bar = input("Enter barcode of medicine: ")
        bars = actions.get_values("MedicineInfo", "Barcode")

        while not bar.isdigit() or bar in bars:
            if not bar.isdigit():
                bar = input(" Barcode should be an integer only! Enter again: ")
            else:
                bar = input("This  barcode is already taken! Enter another: ")

    name = input("Enter name of medicine: ")
    while name == '':
        name = input("Please enter a name: ")

    m_type = input("Enter type  (eg: antipyretic, analgesic etc.): ")
    while m_type == "":
        m_type = input("Please enter a medicine type: ")

    composition = input("Enter composition: ")
    if composition == '':
        composition = "NULL"

    create_record(bar, name, m_type, composition)
    print("Inserted record successfully...")


def delete():
    print()
    print("Delete Options")
    print("2. Delete using barcode")
    print("3. Delete using name")
    print("4. Delete using condition")
    print("0. Home")
    print("1. Medicine Information")
    ch = input("Enter your choice: ")

    while ch not in '01234' or len(ch) != 1:
        ch = input("Invalid choice! Please enter again: ")

    if ch == '0':
        return 0

    elif ch == '1':
        return '1'

    elif ch == '2':
        bar = input("Enter barcode of medicine to be deleted: ")
        while not bar.isdigit():
            bar = input("Barcode should be an integer only! Please enter again: ")

        actions.delete_record("MedicineInfo", "Barcode", bar)
        print("Deleted record successfully...")

    elif ch == '3':
        name = input("Enter name of medicine: ")
        actions.delete_record("MedicineInfo", "Name", name)
        print("Deleted record successfully...")

    elif ch == '4':
        print("All columns are")
        print(actions. get_columns("MedicineInfo"))
        condition = input('Enter condition for deletion(<column_name><operator>"<value>"): ')
        try:
            actions.delete_by_condition("MedicineInfo", condition)
            print("Deleted record(s) successfully...")
        except Exception as e:
            print(e)
            print("Your condition had the above error!")


def update():
    print("Update options:")
    print("2. Update using barcode")
    print("3. Update using name")
    print("4. Update using condition")
    print("0. Home")
    print("1. Medicine Information")
    ch = input("Enter your choice: ")
    condition = '1=1'

    while ch not in '01234' or len(ch) != 1:
        ch = input("Invalid choice! Please enter again: ")

    if ch == '0':
        return 0

    elif ch == '1':
        return '1'

    elif ch == '2':
        bar = input("Enter barcode of medicine: ")
        while not bar.isdigit():
            bar = input("Barcode should be an integer only! Please enter again: ")

        condition = f"Barcode='{bar}'"

    elif ch == '3':
        name = input("Enter name of medicine: ")
        condition = f"Name='{name}'"

    elif ch == '4':
        print("All columns are")
        print(actions. get_columns("MedicineInfo"))
        condition = input('Enter condition(<column_name><operator>"<value>"): ')
        while True:
            try:
                cur.execute(f"select 1+2 from MedicineInfo where {condition}")
                cur.fetchall()
                break
            except Exception as e:
                print(e)
                condition = input('Your condition had above error! \nEnter again(<column_name><operator>"<value>"): ')

    if ch in '234' and len(ch) == 1:
        columns_all = actions.get_columns("MedicineInfo")
        col_dict = {i + 1: columns_all[i] for i in range(len(columns_all))}
        print(col_dict)
        column = input("Which column no. do you want to update: ").lower()
        while not column.isdigit() or int(column) not in col_dict:
            column = input("Column no. you entered is not in option! Enter again: ").lower()
        column = col_dict[int(column)]
        val = input("Enter value: ")
        try:
            actions.update("MedicineInfo", column, val, condition)
            print("Updated records successfully...")
        except Exception as e:
            print("Your condition had below error!")
            print(e)


def search():
    print()
    print("Search Options:")
    print("2: Search using barcode")
    print("3: Search using name")
    print("4: Search using many fields")
    print("5: Search using condition")
    print("0: Home")
    print("1: Medicine information")
    ch = input("Enter your choice: ")

    columns_all = actions.get_columns("MedicineInfo")
    col_dict = {i + 1: columns_all[i] for i in range(len(columns_all))}

    while ch not in '012345' or len(ch) != 1:
        ch = input("Invalid choice. Enter again: ")

    if ch == '0':
        return '0'

    elif ch == '1':
        return '1'

    elif ch == '2':
        barcode = input("Enter barcode: ")
        while not barcode.isdigit():
            barcode = input("Barcode should only be integer. Enter again: ")
        actions.format_print(actions.get_columns("MedicineInfo"),
                             actions.search_by_condition("MedicineInfo", f"barcode={barcode}"))

    elif ch == '3':
        name = input("Enter name of medicine: ")
        actions.format_print(actions.get_columns("MedicineInfo"),
                             actions.search_by_condition("MedicineInfo", f"name='{name}'"))

    elif ch == '4':
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
                condition += ' && '

        actions.format_print(columns_all, actions.search_by_condition("MedicineInfo", condition))

    elif ch == '5':

        try:
            print("All columns are:")
            print(columns_all)
            condition = input('Enter condition(<column_name><operator>"<value>": ')
            while True:
                try:
                    cur.execute(f"select 1+2 from MedicineInfo where {condition}")
                    cur.fetchall()
                    break
                except Exception as e:
                    print(e)
                    condition = input("Your condition had above error! Enter again: ")
            actions.format_print(columns_all,
                                 actions.search_by_condition("MedicineInfo", condition))
        except Exception as e:
            print(e)
            print("There was an error!!  Error code: 022")


def init():
    print("=" * 10 + "     Medicine Information     " + "=" * 10)
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
            cur.execute("use MedicalStore")
            if where == 0:
                break

        except Exception as e:
            print("An Error occurred!! Error code: 04")
            print(e)
            traceback.print_exc()


msg = """

0: Home
1: View records
2: Insert records
3: Delete records
4: Update records
5: Search records

Enter Your Choice: """

if __name__ == '__main__':
    conn = connect(host='localhost', user='root', password='abhinav1')
    cur = conn.cursor()
    cur.execute("use MedicalStore")
    actions.conn = conn
    actions.cur = cur
    init()

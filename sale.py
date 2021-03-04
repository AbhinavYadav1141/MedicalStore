import traceback

from mysql.connector import connect
import actions
import medicine_info
import management

months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
          7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}


def create_record(receipt_no, name, count, date, time):
    barcodes = actions.get_values("MedicineInfo", "Barcode")
    cur.execute("use Sales")
    print("\nNow enter record for each medicine.")
    cp, sp = create_table(receipt_no, count, barcodes)
    query = f"insert into Sale values('{receipt_no}', '{name}', '{count}', '{date}', '{time}', '{cp}', '{sp}')"
    cur.execute("use MedicalStore")
    cur.execute(query)

    management.update_record(months[int(date.split('-')[1])], date.split('-')[0], cp, sp)
    conn.commit()


def create_record_from_list(lst):
    create_record(*lst)


def create_records(records):
    for i in records:
        create_record_from_list(i)


def create_rec(table, sno, barcode, cp, sp):
    cur.execute(f"insert into {table} values('{sno}', '{barcode}', '{cp}', '{sp}', '{int(sp) - int(cp)}')")
    conn.commit()


def create_table(receipt_no, count, barcodes):
    table = "t" + str(receipt_no)
    cur.execute(f"""create table if not exists {table} 
    (SNo int, barcode int, CostPrice int, SellingPrice int, Profit int)""")

    total_cp = total_sp = 0

    for i in range(int(count)):
        print()
        print(f"Enter record{i + 1}")

        sno = i + 1

        barcode = input("Barcode: ")

        while barcode not in barcodes or not barcode.isdigit():
            if not barcode.isdigit():
                barcode = input("Barcode should be an integer only! Enter again: ")
            else:
                ch = input("""This barcode is not in the database!
                Enter 'y' to add it in database, any other to continue: """).lower()
                if ch == 'y':
                    cur.execute("use MedicalStore")
                    medicine_info.insert(barcode)
                    print()
                    cur.execute("use Sales")
                break

        cur.execute(f"select CostPrice from MedicalStore.Stock where Barcode={barcode}")
        cps = cur.fetchall()
        if len(cps) == 0:
            cp = input("Cost Price: ")
            while not cp.isdigit():
                cp = input("Cost Price should be an integer! Enter again: ")
        else:
            cp = cps[0][0]

        sp = input(f"Selling Price(Cost: Rs {cp}): ")
        while not sp.isdigit():
            sp = input("Selling Price should be an integer! Enter Again: ")

        create_rec(table, sno, barcode, cp, sp)
        total_cp += int(cp)
        total_sp += int(sp)
    return total_cp, total_sp


def print_format(receipt_no):
    print()
    print(f"ReceiptNo.: {receipt_no}")
    cur.execute(f"select * from Sale where ReceiptNo={receipt_no}")
    _, name, count, date, time, cp, sp = cur.fetchall()[0]
    print(f"Customer Name: {name}")
    print(f"No. of medicines: {count}")
    print(f"Date: {date}")
    print(f"Time: {time}")
    print(f"Cost Price: {cp}")
    print(f"Selling Price: {sp}")
    print("Other info:")

    query = f"Select * from Sales.t{receipt_no}"
    columns = actions.get_columns(f"Sales.t{receipt_no}")
    a = 1

    bm = actions.get_values("MedicineInfo", "Barcode")

    for i in actions.get_values(f"Sales.t{receipt_no}", "Barcode"):
        if i not in bm:
            a = 0

    if a:
        query = f"""select t.SNo, t.Barcode, m.Name, m.Type, m.Composition, t.CostPrice, t.SellingPrice, t.Profit
        from t{receipt_no} as t, MedicalStore.MedicineInfo as m where t.Barcode=m.barcode"""
        columns = ("SNo", "Barcode", "Name", "Type", "Composition", "CostPrice", "SellingPrice", "Profit")

    cur.execute("use Sales")
    cur.execute(query)
    actions.format_print(columns, cur.fetchall())
    cur.execute("Use MedicalStore")


def view():
    print()
    print("Viewing Options:")
    print("2: All data")
    print("3: One record using Receipt No.")
    print("4: many records using Receipt No.")
    print("5: All Receipt Numbers")
    print("6: Receipt numbers by condition")
    print("0: Go to home")
    print("1: Go to Medicine Information")
    ch = input()

    while ch not in '0123456' or len(ch) != 1:
        ch = input("Invalid choice. Enter again: ")

    num = 0

    if ch == '0':
        return '0'

    elif ch == '1':
        return '1'

    elif ch == '2':
        values = actions.get_values("Sale", "ReceiptNo")
        for i in values:
            print_format(i)
        if len(values) == 0:
            print("No records!!")

    elif ch == '3':
        num = 1

    elif ch == '4':
        num = input("How many records do tou want to view: ")
        while not num.isdigit():
            num = input("No. of records should be integer only! Enter again: ")

    elif ch == '5':
        cur.execute("select ReceiptNo from Sale")
        actions.format_print(["ReceiptNo", ], cur.fetchall())

    elif ch == '6':
        print("All columns are")
        print(actions.get_columns("Sale"))
        condition = input('Enter condition(<column_name><operator>"<value>"): ')
        while True:
            try:
                cur.execute(f"select 1+2 from Sale where {condition}")
                cur.fetchall()
                break
            except Exception as e:
                print(e)
                condition = input('Your condition had above error! Enter again(<column_name><operator>"<value>"): ')
        try:
            cur.execute(f"select ReceiptNo from Sale where {condition}")
            actions.format_print(["ReceiptNo"], cur.fetchall())
        except Exception as e:
            print("Your condition had an error!!")
            print(e)
            traceback.print_exc()

    records = []
    receipts = actions.get_values("Sale", "ReceiptNo")
    for i in range(int(num)):
        rec = input(f"Enter record{i + 1} Receipt No.: ")
        while rec not in receipts or not rec.isdigit():
            if not rec.isdigit():
                rec = input("Receipt No. should be an integer! Enter again: ")
            else:
                rec = input(f"Receipt No.: {rec} is not there! Enter again: ")
        records.append(rec)
    for i in records:
        print_format(i)


def insert():
    print("Enter records")
    receipt_no = input("Receipt no.: ")
    receipt_nos = actions.get_values("Sale", "ReceiptNo")

    while not receipt_no.isdigit() or receipt_no in receipt_nos:
        if not receipt_no.isdigit():
            receipt_no = input("Receipt no. should be an integer only! Enter again: ")
        else:
            receipt_no = input("This receipt no. is already taken! Enter another: ")

    cust = input("Customer Name: ")
    while cust == '':
        cust = input("Customer name cannot be empty! Enter a name: ")

    count = input("No. of medicines sold: ")
    while not count.isdigit():
        count = input("No. of medicines should be integer! Enter again: ")

    date = actions.date()
    time = actions.time()

    create_record(receipt_no, cust, count, date, time)
    print("Created record successfully...")


def delete():
    receipt = input("Enter receipt no. of record to be deleted: ")
    while not receipt.isdigit():
        receipt = input("Receipt no. should be an integer! Enter Again: ")

    receipts = actions.get_values("Sale", "ReceiptNo")
    if receipt not in receipts:
        print(f"Receipt No. {receipt} is not there! Skipping delete.")

    else:
        cur.execute(f"select SellingPrice, CostPrice, SaleDate from Sale where ReceiptNo={receipt}")
        sp, cp, date = cur.fetchall()[0]
        date = str(date.isoformat())
        month = months[int(date.split('-')[1])]
        year = date.split("-")[0]

        management.update_record(month, year, -int(cp), -int(sp))
        cur.execute(f"delete from Sale where ReceiptNo='{receipt}'")
        cur.execute("use Sales")
        cur.execute(f"drop table t{receipt}")
        cur.execute("use MedicalStore")
        conn.commit()
        print("Deleted record successfully...")


def update():
    rec = input("Enter receipt no. of record to be updated: ")
    receipts = actions.get_values("Sale", "ReceiptNo")
    while rec not in receipts:
        rec = input("Receipt no. you entered is not in table! Enter again: ")
    print("Enter new records. Leave blank to not update")
    receipt = input("Receipt No.: ")
    while receipt != '' and not receipt.isdigit():
        receipt = input("Receipt no. should be an integer! Enter again: ")

    if receipt != '':
        cur.execute(f"update Sale set ReceiptNo={receipt} where ReceiptNo = {rec}")
        cur.execute(f"alter table Sales.t{rec} rename Sales.t{receipt}")
        print("Updated successfully...")
        rec = receipt

    name = input("Customer Name: ")
    if name != '':
        cur.execute(f"update Sale set CustomerName={name} where ReceiptNo = {rec}")
        print("Updated successfully...")

    count = input("No. of medicines sold: ")
    while count != '' and not count.isdigit():
        count = input("No. of medicines should be an integer! Enter again: ")

    if count != '':
        cur.execute(f"update Sale set TypeCount={count} where ReceiptNo = {rec}")
        print("Updated successfully...")

    date = input("Date (yyyy-mm-dd): ")
    cur.execute(f"select SaleDate from Sale where ReceiptNo={rec}")
    old_date = cur.fetchall()[0][0]
    dt = actions.check_date(date)
    while not dt and date != '':
        date = input("Date you entered is not of correct format! Enter again: ")
        dt = actions.check_date(date)

    if date != '':
        print(f"Date: {dt}")
        cur.execute(f"update Sale set SaleDate={dt} where ReceiptNo = {rec}")
        print("Updated successfully...")

    time = input("Time (hh:mm:ss)")
    while not actions.check_time(time) and time != '':
        time = input("Time you entered is not of correct format! Enter again: ")

    if time != '':
        cur.execute(f"update Sale set SaleTime={time} where ReceiptNo = {rec}")
        print("Updated successfully...")
    conn.commit()

    ch = input("Enter 'y' if you want to change other info: ").lower()
    receipt = rec

    if ch == 'y':
        total_cp = total_sp = 0
        while True:
            bar = input("Enter barcode of medicine you want to update. Leave empty to quit: ").lower()
            cur.execute("use Sales")
            barcodes = actions.get_values(f"t{rec}", "Barcode")
            while bar not in barcodes and bar != '':
                bar = input("Barcode you entered is not in table! Enter again: ")
            if bar == '':
                break

            print("\nEnter new records. Leave empty to not update.")
            barcode = input("Barcode: ")
            while not barcode.isdigit() and barcode != '':
                barcode = input("Barcode should be an integer! Enter again: ")
            if barcode != '':
                cur.execute(f"update Sales.t{rec} set Barcode={barcode} where Barcode={bar}")
                print("Updated successfully...")
            if barcode == '':
                barcode = bar

            cp = input("Cost Price: ")
            while not cp.isdigit() and cp != '':
                cp = input("Cost Price should be an integer! Enter again: ")

            if cp != '':
                cur.execute(f"select CostPrice from t{rec} where Barcode={barcode}")
                old_cp = cur.fetchall()[0][0]
                cur.execute(f"update t{rec} set CostPrice={cp} where Barcode={barcode}")
                print("Updated successfully...")
                total_cp += int(cp) - int(old_cp)

            sp = input("Selling Price: ")
            while not sp.isdigit() and sp != '':
                sp = input("Selling Price should be an integer! Enter again: ")

            if sp != '':
                cur.execute(f"select SellingPrice from t{rec} where Barcode={barcode}")
                old_sp = cur.fetchall()[0][0]
                cur.execute(f"update t{receipt} set SellingPrice={sp} where Barcode={barcode}")
                
                print("Updated successfully...")
                total_sp += int(sp) - int(old_sp)
            print("Record Updated...")
        cur.execute("use MedicalStore")
        month = months[int(str(old_date).split('-')[1])]
        year = str(old_date).split('-')[0]
        management.update_record(month, year, total_cp, total_sp)


def search():
    print("Search options:")
    print("2: Using Receipt No.")
    print("3: Using Customer Name")
    print("4: Using Date range")
    print("5: Using Time range")
    print("6: Using date and time ranges")
    print("0: Home")
    print("1: Sale Information")

    ch = input("Enter your choice: ")

    while ch not in '0123456' or len(ch) != 1:
        ch = input("Invalid choice! Enter again: ")

    if ch == '0':
        return '0'

    elif ch == '1':
        return '1'

    elif ch == '2':
        receipt = input("Enter Receipt No.: ")
        while not receipt.isdigit():
            receipt = input("Receipt No. should be an integer! Enter again: ")
        
        cur.execute(f"select * from Sale where ReceiptNo like '%{receipt}%'")
        data = cur.fetchall()
        actions.format_print(actions.get_columns("Sale"), data)

    elif ch == '3':
        name = input("Enter Customer Name: ")
        actions.format_print(actions.get_columns("Sale"), actions.search("Sale", "CustomerName", "%"+name+"%", " like "))

    elif ch == '4':
        start = input("Enter starting date(yyyy-mm-dd): ")
        start = actions.check_date(start)
        while not start:
            start = input("Date you entered is not of correct format! Enter again(yyyy-mm-dd): ")
            start = actions.check_date(start)
        print(f"Starting Date: {start}")

        end = input("Enter ending date(yyyy-mm-dd): ")
        end = actions.check_date(end)
        while not end:
            end = input("Date you entered is not of correct format! Enter again(yyyy-mm-dd): ")
            end = actions.check_date(end)
        print(f"Ending Date: {end}")

        actions.format_print(actions.get_columns("Sale"),
                             actions.search_by_condition("Sale", f"'{end}'>=SaleDate and SaleDate>='{start}'"))

    elif ch == '5':
        start = input("Enter starting time(hh:mm:ss): ")
        while not actions.check_time(start):
            start = input("Time you entered is not of correct format! Enter again(hh:mm:ss): ")

        end = input("Enter ending time(hh:mm:ss): ")
        while not actions.check_time(end):
            end = input("Time you entered is not of correct format! Enter again(hh:mm:ss): ")

        actions.format_print(actions.get_columns("Sale"),
                             actions.search_by_condition("Sale", f"'{end}'>=SaleTime and SaleTime>='{start}'"))

    elif ch == '6':
        start1 = input("Enter starting date(yyyy-mm-dd): ")
        start1 = actions.check_date(start1)
        while not start1:
            start1 = input("Date you entered is not of correct format! Enter again(yyyy-mm-dd): ")
            start1 = actions.check_date(start1)
        print(f"Starting date: {start1}")

        end1 = input("Enter ending date(yyyy-mm-dd): ")
        end1 = actions.check_date(end1)
        while not end1:
            end1 = input("Date you entered is not of correct format! Enter again(yyyy-mm-dd): ")
            end1 = actions.check_date(end1)
        print(f"Ending Date: {end1}")

        start2 = input("Enter starting time(hh:mm:ss): ")
        while not actions.check_time(start2):
            start2 = input("Time you entered is not of correct format! Enter again(hh:mm:ss): ")

        end2 = input("Enter ending time(hh:mm:ss): ")
        while not actions.check_time(end2):
            end2 = input("Time you entered is not of correct format! Enter again(hh:mm:ss): ")

        actions.format_print(actions.get_columns("Sale"),
                             actions.search_by_condition("Sale", f"""'{end2}'>=SaleTime and SaleTime>='{start2}' and 
                             '{end1}'>=SaleDate and SaleDate>='{start1}'"""))


def init():
    print("=" * 10 + "     Sale Information     " + "=" * 10)
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
                delete()

            elif ch == '4':
                update()

            elif ch == '5':
                code = search()

            if code == '0':
                break

        except KeyboardInterrupt:
            cur.execute("use MedicalStore")
            if where == 0:
                break

        except Exception as e:
            print("An Error Occurred!! Error code: 01")
            print(e)
            traceback.print_exc()


msg = """

0: Home
1: View Sale Information
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

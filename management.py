from mysql.connector import connect, errors
import actions
import sale
import traceback


def create_record(month, year, cost, sell):
    query = f"""insert into Management values(
    '{month}', '{year}', {cost}, {sell}, SellingPrice-CostPrice, NetGain*100/CostPrice)"""
    cur.execute(query)
    conn.commit()


def create_record_from_list(lst):
    create_record(lst[0], lst[1], lst[2], lst[3])


def create_records(records):
    for i in records:
        create_record_from_list(i)


def update_record(month, year, cost, sell):
    cur.execute("select Month, Year from Management")
    values = cur.fetchall()
    if (month, int(year)) in values:
        cur.execute(f"""update Management set CostPrice=CostPrice+{int(cost)},
        SellingPrice=SellingPrice+{int(sell)}, NetGain=SellingPrice-CostPrice, NetPercent=NetGain/CostPrice*100""")
        conn.commit()
    else:
        create_record(month, year, cost, sell)


def view():
    print()
    print("View Options: ")
    print("2: All data")
    print("3: Year wise data")
    print("0: Home")
    print("1: Management Information")

    ch = input("Enter your choice: ")
    while ch not in '0123' or len(ch) != 1:
        ch = input("Invalid choice! Enter again: ")

    if ch == '0':
        return '0'

    elif ch == '1':
        return '1'

    elif ch == '2':
        actions.format_print(actions.get_columns("Management"), actions.show_all("Management"))

    elif ch == '3':
        years = input("Enter year range(yyyy-yyyy) Leave empty to include all years: ")
        while years != '' and (len(years) != 9 or years.count('-') != 1
                               or not (len(years.split('-')[0]) == len(years.split('-')[1]) == 4) or
                               not years.replace('-', '0').isdigit()):
            years = input("Year range you entered is not correct! enter again: ")

        if years == '':
            cur.execute("""select Year, sum(CostPrice), sum(SellingPrice), sum(NetGain), 
                        sum(NetGain)/sum(CostPrice)*100 from Management group by Year""")
            columns = ("Year", "CostPrice", "SellingPrice", "NetGain", "NetPercent")
            values = cur.fetchall()

        else:
            query = f"""select Year, sum(CostPrice), sum(SellingPrice), sum(NetGain), 
                        sum(NetGain)/sum(CostPrice)*100 from Management group by Year
                        having year<= '{years.split('-')[1]}' and year>='{years.split('-')[0]}'"""

            cur.execute(query)
            values = cur.fetchall()
            columns = ("Year", "CostPrice", "SellingPrice", "NetGain", "NetPercent")

        actions.format_print(columns, values)


def insert():
    print()
    cur.execute("select Month, Year from Management")
    my = cur.fetchall()
    while True:
        month = input(f"{sale.months}\nEnter month number: ")
        while not month.isdigit() or 1 >= int(month) >= 12:
            month = input("Month no. you entered is not valid! Enter again: ")
        month = sale.months[int(month)]

        year = input("Enter year(yyyy): ")
        while not year.isdigit() or len(year) != 4:
            year = input("Year should be of form yyyy! Enter again: ")

        if (month, int(year)) not in my:
            break
        else:
            print("This month-year pair is already in table. Enter again")

    cp = input("Enter cost price: ")
    while not cp.isdigit():
        cp = input("Cost Price should be an integer! Enter again: ")

    sp = input("Enter Selling Price: ")
    while not sp.isdigit():
        sp = input("Selling Price should be an integer! Enter again: ")

    create_record(month, year, cp, sp)
    print("Created record successfully...")


def delete():
    year = input('Enter year to be deleted(yyyy). Enter "y" to delete everything: ')
    while (not year.isdigit() or len(year) != 4) and year != 'y':
        year = input("Year you entered is not correct! Enter again: ")

    if year == 'y':
        cur.execute("delete from management")

    else:
        print(sale.months)
        month = input('Enter month no. Enter "m" to delete whole year: ')

        while (not month.isdigit() or len(month) != 2) and month != 'm':
            month = input("Month you entered is not of correct format! Enter again: ")

        if month == 'm':
            cur.execute(f"delete from Management where Year={year}")

        else:
            cur.execute(f"delete from Management where Year={year} and Month={month}")

    conn.commit()
    print("Deleted successfully...")


def update():
    print()
    print("Enter Month and Year of record to be updated")
    cur.execute("select month, year from Management")
    month_year = cur.fetchall()
    print(sale.months)
    while True:
        year = input("Year: ")

        while not year.isdigit() or len(year) != 4:
            year = input("Year you entered is not of correct format! Enter again: ")

        month = input("Month No. : ")

        while not month.isdigit() or int(month) not in sale.months:
            month = input("Month no. you entered is not correct! Enter again: ")
        month = sale.months[int(month)]
        if (month, int(year),) not in month_year:
            print("Month-year you entered is not in table! Enter again. ")
        else:
            break

    print()
    print("Enter new records. Leave empty to not update.")
    m = input("Month no.: ")
    while m != '' and (not m.isdigit() or int(m) not in sale.months):
        m = input("Month no. you entered is not valid! Enter again: ")

    if m != '':
        try:
            m = sale.months[int(m)]
            cur.execute(f"update Management set Month='{m}' where Month='{month}' and Year={year}")
        except errors.IntegrityError:
            print("This month-year already exists!!")
            m = month

    else:
        m = month

    y = input("Year: ")
    while y != '' and (not y.isdigit() or len(y) != 4):
        y = input("Year you entered is not valid! Enter again: ")

    if y != '':
        try:
            cur.execute(f"update Management set Year={y} where Month='{m}' and Year={year}")
        except errors.IntegrityError:
            print("This month-year already exists!!")
            y = year
    else:
        y = year

    cp = input("Cost Price: ")

    while not cp.isdigit() and cp != '':
        cp = input("Cost price should be an integer! Enter again: ")
    cur.execute(f"""update Management set CostPrice={cp}, NetGain=SellingPrice-CostPrice,
                NetPercent=NetGain/CostPrice*100 where Month='{m}' and Year={y}""")

    sp = input("Selling Price: ")

    while not sp.isdigit() and sp != '':
        sp = input("Selling price should be an integer! Enter again: ")
    cur.execute(f"""update Management set SellingPrice={sp}, NetGain=SellingPrice-CostPrice,
                    NetPercent=NetGain/CostPrice*100 where Month='{m}' and Year={y}""")
    print("Updated successfully...")


def init():
    print("=" * 10 + "     Management Information     " + "=" * 10)

    a = 1
    while True:
        where = 0
        try:
            print(msg)
            ch = input()

            while ch not in '01234' or len(ch) != 1:
                ch = input("Invalid Choice! Enter again: ")

            where = 1

            if ch == '0':
                break

            elif ch == '1':
                a = view()

            elif ch == '2':
                insert()

            elif ch == '3':
                delete()

            elif ch == '4':
                update()

        except KeyboardInterrupt:
            if where == 0:
                break

        except Exception as e:
            print("An Error Occurred!!  Error code: 04")
            print(e)
            traceback.print_exc()

        if a == '0':
            break


msg = """

0: Home
1: View Management Information
2: Insert record
3: Delete record
4: Update record

Enter Your Choice: """

if __name__ == "__main__":
    conn = connect(host='localhost', user='root', password='abhinav1')
    cur = conn.cursor()
    init()

import mysql.connector as connector

conn = connector.connect(user='root', password='1234', host='localhost')
cur = conn.cursor()

cur.execute("create database if not exists RecordManagement")
cur.execute("use RecordManagement")
cur.execute("""create table if not exists Employees (
                                                    ID char(5), 
                                                    Name varchar(30), 
                                                    Age int, 
                                                    Gender char(1),
                                                    Department char(15),
                                                    Salary int
                                                    )
                                                    """)


def insert():
    ID = input("Enter Employee ID: ")
    name = input("Enter Employee Name: ")
    age = input("Enter Employee Age: ")
    gender = input("Enter Employee Gender: ")
    depart = input("Enter Employee Department: ")
    sal = input("Enter Employee Salary: ")
    code = "insert into Employees values('" + ID + "', '" + name + "', " + age + ", '" + gender + "', '" + depart + "', " + sal + ")"

    print(code)
    cur.execute(code)


def delete_record():
    table = input("Enter table name: ")
    ID = input("Enter Employee ID to be removed: ")
    cur.execute("delete from Employees where ID=" + ID)


def show_tables():
    cur.execute("show tables")
    print("The tables in this database are:")
    for i in cur.fetchall():
        print(i)


def show_records():
    table = input("Enter table name")
    cur.execute("select * from " + table)
    print("The records in table '" + table + "' are:")
    for i in cur.fetchall():
        print(i)


def create_table():
    table = input("Enter table name: ")
    num = int(input("Enter no. of column to be created: "))

    columns = []
    for i in range(num):
        column = input("Enter column" + str(i + 1) + " name: ")
        dtype = input("Enter column" + str(i + 1) + " datatype: ")
        length = input("Enter column" + str(i + 1) + " length: ")
        columns.append((column, dtype, length))

    code = 'create table ' + table + ' ('
    for i in columns:
        code += i[0] + ' ' + i[1] + '(' + i[2] + '), '

    code += ')'
    cur.execute(code)


def delete_table():
    table = input("Enter table name")
    cur.execute("drop table " + table)


msg = """

Employee record management system:
0. quit
1. show records
2. Add record
3. Delete record"""

while True:
    try:
        print(msg)
        ch = input("Enter Choice: ")

        if ch == '0':
            print("Bye bye ...")
            break

        elif ch == '1':
            show_records()

        elif ch == '2':
            insert()

        elif ch == '3':
            delete_record()

        else:
            print("Wrong choice")

    except connector.ProgrammingError:
        print("Please enter correct values!!")
        print("TRY AGAIN")

    except Exception as e:
        print(e)
        print("TRY AGAIN")

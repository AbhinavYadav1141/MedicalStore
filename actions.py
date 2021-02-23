from mysql.connector import connect

conn = cur = None


def delete_record(table, column, value):
    cur.execute(f"delete from {table} where {column}={value}")
    conn.commit()


def delete_multiple(table, column, values):
    for i in values:
        delete_record(table, column, i)


def delete_by_condition(table, condition):
    cur.execute(f"delete from {table} where {condition}")
    conn.commit()


def search_by_condition(table, condition, sel_col='*'):
    cur.execute(f"select {sel_col} from {table} where {condition}")
    result = cur.fetchall()
    return result


def search(table, column, value, operator):
    if isinstance(value, int):
        return search_by_condition(table, f"{column} {operator} {value}")
    return search_by_condition(table, f"{column} {operator} '{value}'")


def search_multiple(table, column, values: list, sel_col='*', operator='='):
    if len(values) == 1:
        query = f"select {sel_col} from {table} where {column} = '{values[0]}'"
    else:
        query = f"select {sel_col} from {table} where {column} in {tuple(values)}"
    print(query)
    cur.execute(query)
    result = cur.fetchall()
    return result


def sysdate():
    cur.execute("select sysdate()")
    date = cur.fetchall()
    return str(date[0][0].isoformat()).split('T')


def date():
    return sysdate()[0]


def time():
    return sysdate()[1]


def show_all(table):
    cur.execute(f"select * from {table}")
    return cur.fetchall()


def show_columns(table, columns):
    query = "select "
    for i in range(len(columns)-1):
        query += columns[i]+', '
    query += columns[-1] + f' from {table}'
    # print(query)
    cur.execute(query)
    return cur.fetchall()


def format_print(columns, values):
    sizes = {i: len(i) for i in columns}
    if len(values) > 0:
        for i in range(len(columns)):
            longest = sizes[columns[i]]
            for j in values:
                j = j[i]
                if len(str(j)) > longest:
                    longest = len(str(j))
            sizes[columns[i]] = longest

        for i in sizes:
            print("+", end='')
            print("-" * (sizes[i] + 2), end='')
        print("+")

        for i in columns:
            print("|", i.upper(), " "*(sizes[i] - len(str(i))), end='  ', sep='')
        print("|")

        for i in sizes:
            print("+", end='')
            print("-" * (sizes[i] + 2), end='')
        print("+")

        for i in values:
            for j in range(len(i)):
                print("|", i[j], " "*(sizes[columns[j]] - len(str(i[j]))), end='  ', sep='')
            print("|")

        for i in sizes:
            print("+", end='')
            print("-" * (sizes[i] + 2), end='')
        print("+")

    else:
        print("No records!")


def update(table, column, value, condition):
    if isinstance(value, int):
        cur.execute(f"update {table} set {column}={value} where {condition}")
    else:
        cur.execute(f"update {table} set {column}='{value}' where {condition}")


def get_columns(table):
    cur.execute(f"desc {table}")
    columns = []
    for i in cur.fetchall():
        columns.append(i[0].lower())

    return columns
    
    
def get_values(table, column):
    cur.execute(f"select {column} from {table}")
    val = cur.fetchall()
    values=[]
    for i in val:
        values.append(str(i[0]))
    return values


def column_count(table):
    num = len(get_columns(table))
    return num


def input_cols(table):
    num = input("Enter no. of columns you want: ")
    while not num.isdigit():
        num = input("Enter integer value only: ")

    columns = get_columns(table)
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

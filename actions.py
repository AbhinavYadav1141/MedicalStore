from mysql.connector import connect


conn = connect(host='localhost', user='root', password='1234')
cur = conn.cursor()


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
    for i in columns:
        print(i.upper(), end='     ')
    print()

    for i in values:
        for j in i:
            print(j, end='     ')
        print()


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

from mysql.connector import connect
import actions


conn = connect(host='localhost', user='root', password='1234')
cur = conn.cursor()


def create_record(batch, bar, date, qty_bought, qty_left, mfg, exp):
    query = f"insert into Stock values({batch}, {bar}, '{date}', {qty_bought}, {qty_left}, '{mfg}'. '{exp}')"
    cur.execute(query)
    conn.commit()


def create_record_from_list(l):
    create_record(l[0], l[1], l[2], l[3], l[4], l[5], l[6])


def create_records(records):
    for i in records:
        create_record_from_list(i)


def init():
    pass

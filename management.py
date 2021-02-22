from mysql.connector import connect
import actions


conn = connect(host='localhost', user='root', password='abhinav1')
cur = conn.cursor()


def create_record(month, year, cost, sell, net=None):
    if net is None:
        net = sell - cost
    net_percent = net / cost * 100
    query = f"insert into Management values('{month}', '{year}', {cost}, {sell}, {net}, {net_percent})"
    cur.execute(query)
    conn.commit()


def create_record_from_list(l):
    create_record(l[0], l[1], l[2], l[3], l[4])


def create_records(records):
    for i in records:
        create_record_from_list(i)


def init():
    pass

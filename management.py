from mysql.connector import connect
import actions


def create_record(month, year, cost, sell):
    query = f"""insert into Management values(
    '{month}', '{year}', {cost}, {sell}, SellingPrice-CostPrice, NetGain*100/CoStPrice)"""
    cur.execute(query)
    conn.commit()


def create_record_from_list(lst):
    create_record(lst[0], lst[1], lst[2], lst[3])


def create_records(records):
    for i in records:
        create_record_from_list(i)


def update_record(month, year, cost, sell):
    cur.execute("select Month, Year from Management")
    if (month, year) in cur.fetchall():
        cur.execute(f"""update Management set CostPrice=CostPrice+{int(cost)},
        SellingPrice=SellingPrice+{int(sell)}, NetGain=SellingPrice-CostPrice, NetPercent=NetGain/CostPrice*100""")
        conn.commit()
    else:
        create_record(month, year, cost, sell)


def init():
    pass


if __name__ == "__main__":
    conn = connect(host='localhost', user='root', password='abhinav1')
    cur = conn.cursor()
    init()

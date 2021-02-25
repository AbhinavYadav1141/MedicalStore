from mysql.connector import connect


def init():
    
    queries = [
        "create database if not exists MedicalStore",
        "create database if not exists Sales",
        "use MedicalStore",
        """create table if not exists MedicineInfo (Barcode int PRIMARY KEY, Name varchar(40),
         Type varchar(20), Composition varchar(200))""",
        """create table if not exists Sale (ReceiptNo int PRIMARY KEY, CustomerName varchar(30),
         TypeCount int, SaleDate date, SaleTime char(8), SellingPrice int)""",
        """create table if not exists Stock (BatchNo int PRIMARY KEY, Barcode int UNIQUE, CostPrice int,
         PurchaseDate date, QuantityLeft int, Mfg date, Exp date)""",
        """create table if not exists Management (Month varchar(20), Year int,
         CostPrice int, SellingPrice int, NetGain int, NetPercent int)"""
    ]

    for i in queries:
        cur.execute(i)

    conn.commit()


if __name__ == '__main__':
    conn = connect(host='localhost', user='root', password='abhinav1')
    cur = conn.cursor()
    init()

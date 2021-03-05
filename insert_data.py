"""
This file is just to add some data in the database for testing...
"""

from mysql.connector import connect
import medicine_info
import stock

conn = connect(user='root', passwd='1234', db="MedicalStore")
cur = conn.cursor()


medicine_info_l = [
    [
        "465343", "Calpol", "analgesic, antipyretic", "Paracetamol, Acetaminophen"
    ],
    [
        "562327", "Avil", "anti-allergic", "Pheniramine"
    ],
    [
        "464367", "Voveran SR", "analgesic", "Diclofenac"
    ],
    [
        "436474", "Acyclovir 400 DT", "antiviral", "Acyclovir"
    ]
]

stock_l = [
    [
        "5373", "465343", "10", "2021-03-05", "65", "2021-03-01", "2023-03-01"
    ],
    [
        "3564", "562327", "5", "2021-03-05", "108", "2021-03-01", "2023-03-01"
    ],
    [
        "7846", "464367", "120", "2021-03-05", "46", "2021-03-01", "2023-03-01"
    ],
    [
        "9784", "436474", "34", "2021-03-05", "74", "2021-03-01", "2023-03-01"
    ]
]

medicine_info.cur = stock.cur = cur
medicine_info.conn = stock.conn = conn
medicine_info.create_records(medicine_info_l)
stock.create_records(stock_l)

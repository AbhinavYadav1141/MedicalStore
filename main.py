from mysql.connector import connect
import actions
import initialize
import management
import medicine_info
import sale
import stock

conn = connect(user='root', passwd='abhinav1')
cur = conn.cursor()

medicine_info.conn = sale.conn = stock.conn = management.conn = initialize.conn = actions.conn = conn
medicine_info.cur = sale.cur = stock.cur = management.cur = initialize.cur = actions.cur = cur

initialize.init()
cur.execute("use MedicalStore")

msg = """
0: quit
1: Sales
2: Stock
3: Medicine Information
4: Management
"""


while True:
    try:
        print(msg)
        ch = input("Enter your choice: ")
        
        while ch not in '01234' or len(ch) > 1:
            ch = input("Invalid choice! Enter again")
            
        if ch == '0':
            print("Bye bye...")
            break
            
        elif ch == '1':
            sale.init()
            
        elif ch == '2':
            stock.init()
            
        elif ch == '3':
            medicine_info.init()
            
        elif ch == '4':
            management.init()

    except KeyboardInterrupt:
        print("\nBye Bye...")
        break

    except Exception as e:
        print("An Error Occurred")
        print(e)

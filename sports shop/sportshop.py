import mysql.connector

try:
    
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="3007",
        database="sportshop"
    )
    
    def inventery_add_items(inventery_name, items):
        mycursor = mydb.cursor()
        sql = f"""
            INSERT INTO {inventery_name} (
                item_name,
                quantity,
                cost
            ) 
            VALUES (%s, %s, %s)
        """
        for item in items:
            value = (
                item['item_name'], 
                int(item['item_quantity']),
                float(item['item_cost'])
            )
            mycursor.execute(sql, value)
        mydb.commit()
        mycursor.close()
        
    def add_cart_items(inventery_name, inventory_items, column_name):
        mycursor = mydb.cursor()
        for cartitem in inventory_items:
            sql = f"SELECT {column_name}, cost FROM {inventery_name} WHERE item_name = %s"
            mycursor.execute(sql, (cartitem['item_name'],))
            result = mycursor.fetchone()
            if result:
                quantity, cost = result
                if cartitem['item_quantity'] <= quantity:
                    insert_sql = """
                        INSERT INTO cart_items (
                            item_name,
                            quantity,
                            cost
                        ) 
                        VALUES (%s, %s, %s)
                    """
                    value = (
                        cartitem['item_name'], 
                        int(cartitem['item_quantity']),
                        cost
                    )
                    mycursor.execute(insert_sql, value)
                    mydb.commit()
                else:
                    print('Less quantity in the shop')
            else:
                print(f"Item {cartitem['item_name']} not found in inventory")
        mycursor.close()

    def display_cart_items():
        mycursor = mydb.cursor()
        sql = "SELECT * FROM cart_items"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for i in result:
            print(i)
        mycursor.close()
        
    def display_inventory_items(inventery_name):
        mycursor = mydb.cursor()
        sql = f"SELECT * FROM {inventery_name}"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for data in myresult:
            print(data)
        mycursor.close()
        
    
    print('\t\t\t Welcome to Sport shop\n\t\t\t')
    username = input('Enter UserName: ')
    user_password = input('Enter Password: ')
    admin = 'shanmu'
    password = 'shanmu'
    
    
    if username == admin and user_password == password:
        while True:
            print('1. Add items\n2. Display Inventory Items\n3. Exit')
            choice = int(input('Enter Choice: '))
            if choice == 1:
                inventery_name = input('Enter Inventory name: ')
                items = []
                while True:
                    item_name = input('Enter Item name (or "done" to finish): ')
                    if item_name.lower() == "done":
                        break
                    item_quantity = int(input('Enter Item quantity: '))
                    item_cost = float(input('Enter Item cost: '))
                    items.append({'item_name': item_name, 'item_quantity': item_quantity, 'item_cost': item_cost})
                inventery_add_items(inventery_name, items)
            elif choice == 2:
                inventery_name = input('Enter Inventory name: ')
                display_inventory_items(inventery_name)
            elif choice == 3:
                break
            else:
                print('Invalid choice')
                
    else:
        while True:
            print('1. Add Cart items\n2. Display Cart Items\n3. Exit')
            choice = int(input('Enter Choice: '))
            if choice == 1:
                items = []
                inventery_name = input('Enter Inventory name: ')
                column_name = "quantity" 
                while True:
                    item_name = input('Enter Item name (or "done" to finish): ')
                    if item_name.lower() == "done":
                        break
                    item_quantity = int(input('Enter Item quantity: '))
                    items.append({'item_name': item_name, 'item_quantity': item_quantity})
                add_cart_items(inventery_name, items, column_name)
            elif choice == 2:
                display_cart_items()
            elif choice == 3:
                break
            else:
                print('Invalid choice')
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'mydb' in locals() or 'mydb' in globals():
        mydb.close()

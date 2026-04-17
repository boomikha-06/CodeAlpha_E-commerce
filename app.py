import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="ecommerce_db"
)

print("Connected successfully!")

cursor = db.cursor()

# MENU
print("1. Show Users")
print("2. Show Products")
print("3. Add User")
print("4. Login")
print("5. Add to Cart")
print("6. Place Order")
print("7. View Orders")

choice = input("Enter your choice: ")

# 1. SHOW USERS
if choice == "1":
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(row)

# 2. SHOW PRODUCTS
elif choice == "2":
    cursor.execute("SELECT * FROM products")
    for row in cursor.fetchall():
        print(row)

# 3. ADD USER
elif choice == "3":
    name = input("Enter name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    phone = input("Enter phone: ")
    address = input("Enter address: ")

    cursor.execute("""
    INSERT INTO users (name, email, password, phone, address)
    VALUES (%s, %s, %s, %s, %s)
    """, (name, email, password, phone, address))

    db.commit()
    print("User added successfully!")

# 4. LOGIN
elif choice == "4":
    email = input("Enter email: ")
    password = input("Enter password: ")

    cursor.execute("""
    SELECT * FROM users WHERE email=%s AND password=%s
    """, (email, password))

    user = cursor.fetchone()

    if user:
        print("Login successful!")
        print("Welcome,", user[1])
    else:
        print("Invalid email or password")

# 5. ADD TO CART
elif choice == "5":
    user_id = input("Enter user ID: ")
    product_id = input("Enter product ID: ")
    quantity = input("Enter quantity: ")

    cursor.execute("INSERT INTO cart (user_id) VALUES (%s)", (user_id,))
    db.commit()

    cart_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO cart_items (cart_id, product_id, quantity)
    VALUES (%s, %s, %s)
    """, (cart_id, product_id, quantity))

    db.commit()
    print("Product added to cart!")

# 6. PLACE ORDER
elif choice == "6":
    user_id = input("Enter user ID: ")

    cursor.execute("""
    INSERT INTO orders (user_id, total_amount, order_status)
    VALUES (%s, %s, %s)
    """, (user_id, 0, "Pending"))

    db.commit()

    order_id = cursor.lastrowid

    cursor.execute("""
    SELECT cart_items.product_id, cart_items.quantity, products.price
    FROM cart
    JOIN cart_items ON cart.cart_id = cart_items.cart_id
    JOIN products ON cart_items.product_id = products.product_id
    WHERE cart.user_id = %s
    """, (user_id,))

    items = cursor.fetchall()

    total = 0

    for item in items:
        product_id, quantity, price = item
        total += quantity * price

        cursor.execute("""
        INSERT INTO order_items (order_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s)
        """, (order_id, product_id, quantity, price))

    cursor.execute("""
    UPDATE orders SET total_amount=%s WHERE order_id=%s
    """, (total, order_id))

    db.commit()

    print("Order placed successfully!")
    print("Total amount:", total)

# 7. VIEW ORDERS
elif choice == "7":
    cursor.execute("""
    SELECT orders.order_id, users.name, orders.total_amount, orders.order_status
    FROM orders
    JOIN users ON orders.user_id = users.user_id
    """)

    for row in cursor.fetchall():
        print(row)

# INVALID
else:
    print("Invalid choice")
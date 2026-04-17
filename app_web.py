from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="ecommerce_db"
)

cursor = db.cursor()

# HOME
@app.route('/')
def home():
    return render_template("index.html")

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
            (name, email, password)
        )
        db.commit()
        return redirect('/login')

    return render_template("register.html")

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            return redirect('/products')
        else:
            return "Invalid Login"

    return render_template("login.html")

# PRODUCTS
@app.route('/products')
def products():
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    return render_template("products.html", products=data)

# ADD TO CART (simple)
@app.route('/add_to_cart/<int:pid>')
def add_to_cart(pid):
    user_id = 1   # simple (fixed user)

    cursor.execute("INSERT INTO cart (user_id) VALUES (%s)", (user_id,))
    db.commit()

    cart_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s,%s,%s)",
        (cart_id, pid, 1)
    )
    db.commit()

    return "Added to Cart!"

app.run(debug=True)
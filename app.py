from flask import Flask, request
import psycopg2
from redis import Redis
from flask_cors import CORS

app = Flask(__name__)       #Initalize flask app
redis_client = Redis(host='redis', port=6379)  # connect to redis 
app = Flask(__name__)
CORS(app)

#connect to postgres
conn = psycopg2.connect(
    host='postgres',
    database='ordersdb',
    user='postgres',
    password='postgres123'
)

cur = conn.cursor() #cursor to execute sql commands

cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name TEXT,
        price DECIMAL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES products(id),
        customer_name TEXT,
        status TEXT
    )
''')

conn.commit() #save the changes

@app.route('/products', methods=['POST'])   # Endpoint: POST /products → adds a new product to the database
def add_product():
    data = request.get_json()
    cur.execute(
        "INSERT INTO products (name, price) VALUES (%s, %s)",
        (data['name'], data['price'])
    )
    conn.commit()
    return {'message': 'Product added'}, 201

@app.route('/products', methods=['GET'])   # Endpoint: GET /products → returns list of all products
def get_products():
    cur.execute("SELECT id, name, price FROM products")
    rows = cur.fetchall()
    products = [{'id': r[0], 'name': r[1], 'price': float(r[2])} for r in rows]
    return {'products': products}

@app.route('/orders', methods=['POST'])   # Endpoint: POST /orders → places a new order (status starts as 'pending')
def place_order():
    data = request.get_json()
    cur.execute(
        "INSERT INTO orders (product_id, customer_name, status) VALUES (%s, %s, %s)",
        (data['product_id'], data['customer_name'], 'pending')
    )
    conn.commit()
    return {'message': 'Order placed'}, 201

@app.route('/orders', methods=['GET'])    # Endpoint: GET /orders → returns list of all orders
def get_orders():
    cur.execute("SELECT id, product_id, customer_name, status FROM orders")
    rows = cur.fetchall()
    orders = [{'id': r[0], 'product_id': r[1], 'customer_name': r[2], 'status': r[3]} for r in rows]
    return {'orders': orders}

# Run the Flask app, accessible from outside the container on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
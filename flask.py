from flask import Flask, render_template, request, redirect, url_for
from dataclasses import dataclass, field
from typing import List

# Flask app initialization
app = Flask(__name__)

# Dataclasses for Product, ProductStock, Shop, and Customer
@dataclass
class Product:
    name: str
    price: float = 0.0

@dataclass
class ProductStock:
    product: Product
    quantity: int

@dataclass
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)
    
the_shop = Shop() 

# creating the routes for shop 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('setup_shop', methods =['GET', 'POST'])
def setup_shop():
    global the_shop 
    if request.method == "POST":
        cash = float(request.form['cash'])
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        
        product = Product(name, price)
        product_stock = ProductStock(product, quantity)
        the_shop.stock.append(product_stock)
        
        return redirect(url_for('add_products'))

    return render_template('add_products.html', stock=the_shop.stock)

@app.route('/shop_overview')
def shop_overview():
    global the_shop
    return render_template('shop_overview.html', shop=the_shop)


@app.route('/live_order', methods=['GET', 'POST'])
def live_order():
    global the_shop
    if request.method == "POST":
        customer_name = request.form[customer_name]
        customer_budget = float(request.form['customer_budget'])
        customer = Customer(name=customer_name, budget=customer_budget)
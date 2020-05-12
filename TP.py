from flask import Flask, jsonify,request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/python_database'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Brands(db.Model):
    brand_id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Brands %r>' % self.brand_name

class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(40), nullable=True)

    def __repr__(self):
        return '<Categories %r>' % self.category_id

class Customers(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(40))
    street = db.Column(db.String(50))
    city = db.Column(db.String(60))
    state = db.Column(db.String(40))
    zip_code = db.Column(db.String(20))

    def __repr__(self):
        return '<Customers %r>' % self.customer_id

class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    order_status = db.Column(db.String(40), nullable=True)
    order_date = db.Column(db.DateTime, nullable=True)
    required_date = db.Column(db.DateTime, nullable=True)
    shipped_date = db.Column(db.DateTime, nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.staff_id'), nullable=False)

    def __repr__(self):
        return '<Orders %r>' % self.order_id

class Order_items(db.Model): 
    item_id = db.Column(db.Integer, primary_key=True, unique=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    list_price = db.Column(db.Float, nullable=True)
    discount = db.Column (db.Float, nullable=True)

    def __repr__(self):
        return '<Order_items %r>' % self.item_id

class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.brand_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    model_year = db.Column(db.Integer, nullable=True)
    list_price = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return '<Products %r>' % self.product_id

class Staffs(db.Model):
    staff_id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(40), nullable=True)
    phone = db.Column(db.String(40), nullable=True)
    active = db.Column(db.Integer, nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=False)
    manager_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Staff %r>' % self.staff_id

stock = db.Table('Stocks',
    db.Column('store_id', db.Integer, db.ForeignKey('stores.store_id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.product_id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False)
)

class Stores(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(40), nullable=True)
    phone = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(40), nullable=True)
    street = db.Column(db.String(40), nullable=True)
    city = db.Column(db.String(40), nullable=True)
    state = db.Column(db.String(40), nullable=True)
    zip_code = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Stores %r>' % self.store_id

@app.route("/")
def index():
    products = Products.query.all()
    return render_template('index.html', products=products)

@app.route("/brands", methods=['GET'])
def brands_show():
    brands = Brands.query.all() 
    return render_template('brands.html', brands=brands)

@app.route("/commandes")
def Orders_show():
    orders = Orders.query.all()
    return render_template('orders.html', orders=orders)

@app.route("/clients")
def Clients_show():
    customers = Customers.query.all()
    return render_template('customers.html', customers=customers)

@app.route("/historique")
def Historique_show():
    order_items = Order_items.query.all()
    return render_template('historiques.html', order_items=order_items)

@app.route("/magasins")
def Magasins_show():
    stores = Stores.query.all()
    return render_template('stores.html', stores=stores)

@app.route("/add_brands",methods = ['POST', 'GET'])
def AddStore():
    if request.method == "POST":
        name = request.form['name']
        add = Brands(brand_name=name)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("brands"))


    return render_template('add_brands.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=8080)  
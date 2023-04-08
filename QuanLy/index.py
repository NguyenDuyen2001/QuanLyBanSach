from flask import render_template, request, redirect, session
from QuanLy import app, dao
from QuanLy import admin
from QuanLy import login
from flask_login import login_user, logout_user
import cloudinary.uploader


@app.route("/")
def index():
    categories = dao.get_categories()
    kw = request.args.get('kw')
    category_id = request.args.get('category_id')
    products = dao.get_products(kw=kw, category_id=category_id)

    return render_template("index.html", categories=categories, products=products)


@app.route("/products/<int:product_id>")
def details(product_id):
    categories = dao.get_categories()
    # product = {
    #     "id": 1,
    #     "name": "Khó Mà Tìm Được Một Người Tốt",
    #     "description": "Nhà cung cấp:Phanbook, Tác giả:Flannery O’Connor, Nhà xuất bản:NXB Hội Nhà Văn, Hình thức bìa:Bìa Mềm",
    #     "price": 198000,
    #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
    #     "category_id": 1
    # }
    product = dao.get_product_by_id(product_id)

    return render_template("details.html",categoties=categories, product=product)

# Buổi 3 - video 4:18s
# @app.context_processor
# def common_attr():
#     return {
#         'çategories': dao.get_categories()
#     }


@app.route('/login')
def my_login():
    return render_template('login.html')


@app.route("/login", methods=['post'])
def my_login_process():
    username = request.form['username']
    password = request.form['password']
    u = dao.auth_user(username, password)
    if u:
        login_user(user=u)
        return redirect('/')

    return render_template('login.html')


@app.route("/logout")
def my_logout():
    logout_user()
    return redirect("/login")



@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/order/<int:product_id>')
def order_item(product_id):
    p = dao.get_product_by_id(product_id)

    cart = {}
    if 'cart' in session:
        cart = session['çart']

    product_id = str(product_id)
    if product_id in cart:
        cart[product_id]['quantity'] = cart[product_id]['quantity'] + 1
    else:
        cart[product_id] = {
            "ïd": p.id,
            "name": p.name,
            "price": p.price,
            "quantity": 1
        }
    session['çart'] = cart

    return redirect('/çart')



@app.route("/cart")
def cart():
    # session['cart'] = {
    #     "1": {
    #         "ïd": 1,
    #         "name": "Sách giáo dục",
    #         "price": 18000,
    #         "quantity": 2
    #     }, "2": {
    #         "ïd": 2,
    #         "name": "Sách toán",
    #         "price": 25000,
    #         "quantity": 1
    #     }
    # }
    return render_template('cart.html')



if __name__ == '__main__':
    app.run(debug=True)

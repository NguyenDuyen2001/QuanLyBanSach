from flask import render_template, request, redirect, session
from QuanLy import app, dao
from QuanLy.models import User
# from QuanLy import admin
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

    product = dao.get_product_by_id(product_id)

    return render_template("details.html",categoties=categories, product=product)


@app.route('/order/<int:product_id>')
def order_item(product_id):
    p = dao.get_product_by_id(product_id)

    cart = {}
    if 'cart' in session:
        cart = session['cart']

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
    session['cart'] = cart

    return redirect('/cart')


@app.route("/cart")
def cart():

    return render_template('cart.html')

# begin for admin

#### admin login to system
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
        return redirect('/admin/home')

    return render_template('login.html')


@app.route("/admin/logout")
def my_logout():
    logout_user()
    return redirect("/login")


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/admin/home")
def admin_home():
    getProduct = dao.get_product_all()

    return render_template('home_admin.html', getProduct=getProduct)

@app.route("/admin/home", methods=['post'])
def admin_home_process():
    getProduct = dao.get_product_all()

    return render_template('home_admin.html', getProduct=getProduct)

@app.route("/admin/home/register")
def register():
    # getRole = dao.get_roles()
    return render_template('register.html')

@app.route("/admin/home/register", methods=["POST"])
def register_process():

    # getRole = dao.get_roles()

    if request.form['username'] != User.query.filter(User.username == request.form['username']):

        name = request.form["name"]
        username = request.form["username"]
        pwd = request.form["password"]
        phone = request.form["phone"]
        user_role = request.form["user_role"]

        try:
            dao.add_users(name=name, username=username, password=pwd, phone=phone, user_role=user_role)
            msg = 'Tạo tài khoản thành công'
        except Exception as ex:
            msg = 'Tài khoản đăng nhập đã tồn tại' + str(ex)
    else:
        msg = 'Tạo tài khoản thành công'

    return render_template('register.html', msg=msg)


@app.route("/admin/home/regulations")
def regulations():
    tableReg = dao.get_regulations()

    return render_template('regulations.html', tableReg=tableReg)

@app.route("/admin/home/regulations/create", methods=['POST'])
def regCreate():
    name = request.form['namelogic']

    try:

        dao.add_regulations(name=name)
        msg = 'Lưu thành công'
    except Exception as ex:
        msg = 'Lưu thất bại' + str(ex)

    return render_template('create_regulation.html', msg=msg)






@app.route("/admin/home/logics")
def logics():
    tableLogic = dao.get_logic()

    return render_template('logics.html', tableLogic=tableLogic)

@app.route("/admin/home/logics/create")
def logicCreate():
    getReg = dao.get_regulations()

    return render_template('create_logic.html', getReg=getReg)

@app.route("/admin/home/logics/create", methods=['POST'])
def logicCreate_process():
    getReg = dao.get_regulations()

    regID = request.form['regulation']
    type = request.form['type']
    value = int(request.form['value'])
    unit = int(request.form['unit'])

    try:

        dao.add_logic(regID=regID, type=type, value=value, unit=unit)
        msg = 'Lưu thành công'
    except Exception as ex:
        msg = 'Lưu thất bại' + str(ex)

    return render_template('create_logic.html', msg=msg, getReg=getReg)





@app.route("/admin/home/categories")
def categories():
    tableCat = dao.get_categories()

    return render_template('categories.html', tableCat=tableCat)

@app.route("/admin/home/categories/create", methods=["POST"])
def cateCreate():

    name = request.form['nameCate']

    try:

        dao.add_category(name=name)
        msg = 'Lưu thành công'
    except Exception as ex:
        msg = 'Lưu thất bại' + str(ex)

    return render_template('create_category.html', msg=msg)





@app.route("/admin/home/products")
def products():
    tableProduct = dao.get_product_all()

    return render_template('products.html', tableProduct=tableProduct)

@app.route("/admin/home/products/create")
def productCreate():
    getCate = dao.get_categories()
    return render_template('create_product.html', getCate=getCate)

@app.route("/admin/home/products/create", methods=["POST"])
def productCreate_process():
    getCate = dao.get_categories()

    name = request.form['productName']
    cate = request.form['category']
    price = int(request.form['price'])
    qty = int(request.form['qty'])
    if request.form['isFull'] == 'Thiếu':
        is_full = 1
    else:
        is_full = 0
    desc = request.form['desciption']
    img = request.form['image']

    try:
        dao.add_product(name=name, desc=desc, price=price, image=img, category_id=cate, qty=qty, is_full=is_full)
        msg = 'Lưu thành công'
    except Exception as ex:
        msg = 'Lưu thất bại' + str(ex)

    return render_template('create_product.html', msg=msg, getCate=getCate)





# end for admin

if __name__ == '__main__':
    app.run(debug=True)

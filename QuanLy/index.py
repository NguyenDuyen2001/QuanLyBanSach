from flask import render_template, request, redirect, session
from QuanLy import app, dao
from QuanLy.models import User
# from QuanLy import admin
from QuanLy import login
from flask_login import login_user, logout_user, login_required
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


@app.route("/admin/home/regulations/create")
def regCreate():
    return render_template('create_regulation.html')

@app.route("/admin/home/regulations/create", methods=['POST'])
def regCreate_process():
    name = request.form['namelogic']

    try:

        dao.add_regulations(name=name)
        msg = 'Lưu thành công'
    except Exception as ex:
        msg = 'Lưu thất bại' + str(ex)

    return render_template('create_regulation.html', msg=msg)

@app.route("/admin/home/regulations/update")
def regUpdate():
    getReg = dao.get_regulations()
    return render_template('update_regulation.html', getReg=getReg)

@app.route("/admin/home/regulations/update", methods=['POST'])
def regUpdate_process():
    getReg = dao.get_regulations()

    id = request.form['regulation']
    name = request.form['newName']

    try:

        dao.update_regulations(id=id, name=name)
        msg = 'Cập nhật thành công'
    except Exception as ex:
        msg = 'Cập nhật thất bại' + str(ex)

    return render_template('update_regulation.html', msg=msg, getReg=getReg)


@app.route("/admin/home/regulations/delete")
def regDel():
    tableReg = dao.get_regulations()
    return render_template('delete_regulation.html', tableReg=tableReg)

@app.route("/admin/home/regulations/delete/<id>", methods=['POST'])
def regDel_process(id):
    try:

        dao.delete_regulations(id=id)
    except Exception as ex:
        return str(ex)

    return redirect('/admin/home/regulations/delete')


@app.route("/admin/home/logics")
def logics():
    tableLogic = dao.get_logic()

    return render_template('logics.html', tableLogic=tableLogic)

@app.route("/admin/home/logics/create")
def logicCreate():
    tableLogic = dao.get_logic()

    return render_template('create_logic.html', tableLogic=tableLogic)

@app.route("/admin/home/logics/create", methods=['POST'])
def logicCreate_process():
    getReg = dao.get_regulations()

    regID = request.form['regulation']
    type = request.form['type']
    value = int(request.form['value'])
    unit = request.form['unit']

    try:

        dao.add_logic(regID=regID, type=type, value=value, unit=unit)
        msg = 'Lưu thành công'
    except Exception as ex:
        msg = 'Lưu thất bại' + str(ex)

    return render_template('create_logic.html', msg=msg, getReg=getReg)


@app.route("/admin/home/logics/delete")
def logicDel():
    tableLogic = dao.get_logic()
    return render_template('delete_logic.html', tableLogic=tableLogic)

@app.route("/admin/home/logics/delete/<id>", methods=['POST'])
def logicDel_process(id):
    try:

        dao.delete_logic(id)
    except Exception as ex:
        return str(ex)

    return redirect('/admin/home/logics/delete')


@app.route("/admin/home/categories")
def categories():
    tableCate = dao.get_categories()

    return render_template('categories.html', tableCate=tableCate)

@app.route("/admin/home/categories/create")
def cateCreate():
    return render_template('create_category.html')

@app.route("/admin/home/categories/create", methods=["POST"])
def cateCreate_process():

    name = request.form['nameCate']

    try:

        dao.add_category(name=name)
        msg = 'Lưu thành công'
    except Exception as ex:
        msg = 'Lưu thất bại' + str(ex)

    return render_template('create_category.html', msg=msg)

@app.route("/admin/home/categories/update")
def cateUpdate():
    getCate = dao.get_categories()
    return render_template('update_category.html', getCate=getCate)

@app.route("/admin/home/categories/update", methods=['POST'])
def cateUpdate_process():
    getCate = dao.get_categories()

    id = request.form['cate_id']
    name = request.form['newName']

    try:

        dao.update_category(id=id, name=name)
        msg = 'Cập nhật thành công'
    except Exception as ex:
        msg = 'Cập nhật thất bại' + str(ex)

    return render_template('update_category.html', msg=msg, getCate=getCate)


@app.route("/admin/home/categories/delete")
def cateDel():
    tableCate = dao.get_categories()

    return render_template('delete_category.html', tableCate=tableCate)

@app.route("/admin/home/categories/delete/<id>", methods=['POST'])
def cateDel_process(id):

    try:

        dao.delete_category(id=id)
    except Exception as ex:
        return str(ex)

    return redirect('/admin/home/categories/delete')



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

@app.route("/admin/home/products/update")
def productUpdate():
    getProductName = dao.get_product_all()


    return render_template('update_product.html', getProductName=getProductName)

@app.route("/admin/home/products/update", methods=['POST'])
def productUpdate_process():
    getProduct = dao.get_product_all()

    product_id = request.form['productName']

    getProductByID = dao.get_product_by_id(product_id=product_id)

    return render_template('update_product.html', getProduct=getProduct, getProductByID=getProductByID)


@app.route("/admin/home/products/delete")
def productDel():
    tableProduct = dao.get_product_all()
    return render_template('delete_product.html', tableProduct=tableProduct)

@app.route("/admin/home/products/delete/<id>", methods=['POST'])
def productDel_process(id):
    try:

        dao.delete_product(id=id)
    except Exception as ex:
        return str(ex)

    return redirect('/admin/home/products/delete')


# end for admin




if __name__ == '__main__':
    app.run(debug=True)

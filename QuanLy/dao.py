from QuanLy.models import Category, Product, User, Regulations, Logic
from QuanLy import db, app
import hashlib
from sqlalchemy import or_, and_

def get_categories():
    query = Category.query.filter(Category.is_active == 1).all()

    return query


def get_products(kw=None, category_id=None):
    query = Product.query.join(Category,
                               Product.category_id == Category.id) \
                .filter(and_(Product.is_active == 1, Category.is_active == 1))

    if kw:
        query = query.filter(Product.name.contains(kw))

    if category_id:
        query = query.filter(Product.category_id.__eq__(category_id))

    return query.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def auth_user(username, password):
   password=str(hashlib.md5(password.encode('utf-8')).hexdigest())
   return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()

def get_users():
    return User.query.all()


# def auth_user(username):
#     return User.query.filter(User.username==username)

def get_regulations():
    query = Regulations.query.filter(Regulations.is_active == 1).all()
    return query

def add_regulations(name):
    regulation = Regulations(name=name)
    db.session.add(regulation)
    db.session.commit()

def update_regulations(id, name):
    reg = Regulations.query.get(id)
    reg.name = name
    db.session.add(reg)
    db.session.commit()

def delete_regulations(id):
    reg = Regulations.query.get(id)
    reg.is_active = 0
    db.session.add(reg)
    db.session.commit()


def get_logic():
    query = Logic.query.filter(Logic.is_active == 1).all()
    return query

def add_logic(regID, type, value, unit):
    logic = Logic(regID=regID, type=type, value=value, unit=unit)
    db.session.add(logic)
    db.session.commit()

def delete_logic(id):
    logic = Logic.query.get(id)
    logic.is_active = 0
    db.session.add(logic)
    db.session.commit()


def add_users(name, phone, username, password, user_role):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User(name=name, phone=phone, username=username, password=password, user_role=user_role)
    db.session.add(user)
    db.session.commit()


def get_product_all():
    query = Product.query.join(Category,
                               Product.category_id == Category.id) \
                .filter(and_(Product.is_active == 1, Category.is_active == 1)) \
                .all()
    return query

def add_product(name, desc, price, image, category_id, qty, is_full):
    product = Product(name=name, description=desc, price=price, image=image, category_id=category_id, qty=qty, is_full=is_full)
    db.session.add(product)
    db.session.commit()

def update_product(id, name, desc, price, img, qty, is_full):
    p = Product.query.get(id)
    p.name = name
    p.description = desc
    p.price = price
    p.image = img
    p.qty = qty
    p.is_full = is_full
    db.session.add(p)
    db.session.commit()

def delete_product(id):
    product = Product.query.get(id)
    product.is_active = 0
    db.session.add(product)
    db.session.commit()

def add_category(name):
    cate = Category(name=name)
    db.session.add(cate)
    db.session.commit()

def update_category(id, name):
    cate = Category.query.get(id)
    cate.name = name
    db.session.add(cate)
    db.session.commit()

def delete_category(id):
    cate = Category.query.get(id)
    cate.is_active = 0
    db.session.add(cate)
    db.session.commit()


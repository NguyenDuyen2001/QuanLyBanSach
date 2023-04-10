from QuanLy.models import Category, Product, User, Regulations, Logic
from QuanLy import db, app
import hashlib

def get_categories():
    return Category.query.all()


def get_products(kw=None, category_id=None):
    query = Product.query

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


def auth_user(username):
    return User.query.filter(User.username==username)

def get_regulations():
    return Regulations.query.all()

def add_regulations(name):
    regulation = Regulations(name=name)
    db.session.add(regulation)
    db.session.commit()

def add_logic(regID, type, value, unit):
    logic = Logic(regID=regID, type=type, value=value, unit=unit)
    db.session.add(logic)
    db.session.commit()

def add_users(name, phone, username, password, user_role):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User(name=name, phone=phone, username=username, password=password, user_role=user_role)
    db.session.add(user)
    db.session.commit()


def get_product_all():
    return Product.query.all()

def add_product(name, desc, price, image, category_id, qty, is_full):
    product = Product(name=name, description=desc, price=price, image=image, category_id=category_id, qty=qty, is_full=is_full)
    db.session.add(product)
    db.session.commit()

def get_category():
    return Category.query.all()

def add_category(name):
    cate = Category(name=name)
    db.session.add(cate)
    db.session.commit()

def get_logic():
    return Logic.query.all()
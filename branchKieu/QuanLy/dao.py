from QuanLy.models import Users, Roles, Regulations, Logic
from QuanLy import db, app
from sqlalchemy import func
import hashlib

def add_roles(name_role):
    role = Roles(name_role=name_role)
    db.session.add(role)
    db.session.commit()


def add_users(name, phone, username, password, role_id):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = Users(name=name, phone=phone, username=username, password=password, role_id=role_id)
    db.session.add(user)
    db.session.commit()


def get_roles():
    return Roles.query.all()

def get_users():
    return Users.query.all()

def auth_user(username):
    return Users.query.filter(Users.username==username)

def get_regulations():
    return Regulations.query.all()

def add_logic(regID, type, value, unit):
    logic = Logic(regID=regID, type=type, value=value, unit=unit)
    db.session.add(logic)
    db.session.commit()

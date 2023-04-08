from sqlalchemy import ForeignKey, Column, String, Text, DateTime, Integer, Float
from sqlalchemy.orm import relationship
from QuanLy import db, app
from flask_login import UserMixin



class Users(db.Model, UserMixin):
    # __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))


    def __str__(self):
        return self.name_emp


class Roles(db.Model):
    # __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_role = Column(String(100), nullable=False)

    users = relationship("Users", backref="roles", lazy=True)

    def __str__(self):
        return self.name_role


class Regulations(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    logic = relationship('Logic', backref='regulations', lazy=True)


class Logic(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    regID = Column(Integer, ForeignKey("regulations.id"))
    type = Column(String(50), nullable=False)
    value = Column(Integer)
    unit = Column(String(50))


def AddRoles():
    role1 = Roles(name_role='Admin')
    role2 = Roles(name_role='Nhân viên kho')
    role3 = Roles(name_role='Thu ngân')
    db.session.add(role1)
    db.session.add(role2)
    db.session.add(role3)
    db.session.commit()

def AddRegulations():
    reg1 = Regulations(name='Số lượng nhập sách')
    reg2 = Regulations(name='Số lượng tồn trước khi nhập sách')
    reg3 = Regulations(name='Thời gian hủy đơn nếu người dùng không nhận')
    reg4 = Regulations(name='Thời gian hủy đơn nếu người dùng không thanh toán online')
    db.session.add(reg1)
    db.session.add(reg2)
    db.session.add(reg3)
    db.session.add(reg4)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        AddRoles()
        AddRegulations()



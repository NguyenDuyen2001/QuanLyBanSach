from sqlalchemy import Column, String, Integer, Text, Float, ForeignKey, Boolean
from QuanLy import db, app
from sqlalchemy.orm import relationship
from flask_login import UserMixin



class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    avatar = Column(String(100))
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    user_role = Column(String(100), default='Admin')



class Regulations(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    logic = relationship('Logic', backref='regulations', lazy=False)
    is_active = Column(Boolean, default=1)


class Logic(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    regID = Column(Integer, ForeignKey("regulations.id"))
    type = Column(String(50), nullable=False)
    value = Column(Integer)
    unit = Column(String(50))
    is_active = Column(Boolean, default=1)

class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)
    is_active = Column(Boolean, default=1)


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    category_id = Column(Integer, ForeignKey(Category.id))
    qty = Column(Integer, nullable=False)
    is_full = Column(Boolean, nullable=False)
    is_active = Column(Boolean, default=1)



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


def Example_Account():
    import hashlib

    u = User(username='demo', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
             name='ABC DEF',
             avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg', phone='0374727547')
    db.session.add(u)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()

        Example_Account()
        AddRegulations()





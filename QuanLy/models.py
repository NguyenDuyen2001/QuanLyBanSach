from sqlalchemy import Column, String, Integer, Text, Float, ForeignKey
from QuanLy import db, app
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    avatar = Column(String(100))
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(String(100), default='USER')


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    category_id = Column(Integer, ForeignKey(Category.id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()


        import hashlib

        u = User(username='demo', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 name='ABC DEF',
                 avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg')
        db.session.add(u)
        db.session.commit()

        # c1 = Category(name='Khó Mà Tìm Được Một Người Tốt')
        # c2 = Category(name='Chiếc Xe Đạp Mất Cắp')
        # db.session.add_all([c1, c2])
        # db.session.commit()
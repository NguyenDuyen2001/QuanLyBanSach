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


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()


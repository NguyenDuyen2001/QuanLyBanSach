from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from QuanLy import app, db
from QuanLy.models import Category, Product

admin = Admin(app, name='QUẢN LÝ SÁCH', template_mode='bootstrap4')
admin.add_view(ModelView(Category, db.session, name='Danh mục'))
admin.add_view(ModelView(Product, db.session, name='Sản phẩm'))
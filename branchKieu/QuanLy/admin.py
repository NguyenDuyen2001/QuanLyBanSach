from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from QuanLy.models import Users, Roles
from QuanLy import app, db


admin = Admin(app, name='QUẢN LÝ SÁCH', template_mode='bootstrap4')
admin.add_view(ModelView(Users, db.session, name='Users'))
admin.add_view(ModelView(Roles, db.session, name='Roles'))
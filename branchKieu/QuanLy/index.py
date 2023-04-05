from QuanLy import db, app, dao
from flask import render_template, request, redirect, flash, url_for
from QuanLy.models import Users, Roles


@app.route("/")
def home():
    return render_template("base_manage.html")

@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route("/admin/login", methods=["GET", "POST"])
def login():
    return render_template('login.html')


@app.route("/admin/register")
def register():
    getRole = dao.get_roles()
    return render_template('register.html', getRole=getRole)

@app.route("/admin/register", methods=["POST"])
def register_process():

    getRole = dao.get_roles()

    if request.form['username'] != Users.query.filter(Users.username == request.form['username']):

        name = request.form["name"]
        username = request.form["username"]
        pwd = request.form["password"]
        phone = request.form["phone"]
        role_id = int(request.form["idRole"])

        try:
            dao.add_users(name=name, username=username, password=pwd, phone=phone, role_id=role_id)
            msg = 'Tạo thành công'
        except Exception as ex:
            msg = 'Tài khoản đăng nhập đã tồn tại' + str(ex)
    else:
        msg = 'Tạo thành công'

    return render_template('register.html', msg=msg, getRole=getRole)

if __name__ == '__main__':
    app.run(debug=True)



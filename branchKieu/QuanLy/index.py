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

@app.route("/arlets")
def arlets():
    return render_template('arlets.html')

# @app.route("/admin/register")
# def register():
#
#     return render_template('register.html', getRole=getRole)

@app.route("/admin/register", methods=["GET", "POST"])
def register():

    getRole = dao.get_roles()
    error = None

    if request.method == 'post':
        try:
            if request.form['username'] != Users.query.filter(Users.username==request.form['username']):
                name = request.form["name"]
                username = request.form["username"]
                pwd = request.form["password"]
                phone = request.form["phone"]
                role_id = int(request.form["idRole"])

                dao.add_users(name=name, username=username, password=pwd, phone=phone, role_id=role_id)
                return redirect(url_for('admin'))

            else:
                error = 'Tài khoản đăng nhập đã tồn tại'

        except Exception as ex:
            error = str(ex)

    return render_template('register.html', error=error, getRole=getRole)





if __name__ == '__main__':
    app.run(debug=True)



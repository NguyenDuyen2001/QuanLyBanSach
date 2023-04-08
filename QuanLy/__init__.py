from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '249ru3trrgt4567%#32l83beligut*^^%$'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/quanlynhasach?charset=utf8mb4"% quote('12345678')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
login = LoginManager(app)

cloudinary.config(cloud_name='dkyr4znvv', api_key='212769388125549', api_secret='K4OF9_dgoYn-w1FBPibqnhBPPqI')
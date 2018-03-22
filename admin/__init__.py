#! coding: utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask.ext import restful


app = Flask(__name__)
# api = restful.Api(app)


# 加载配置文件内容
app.config.from_object('admin.setting')     # 模块下的setting文件名，不用加py后缀
app.config.from_envvar('FLASKR_SETTINGS')   # 环境变量，指向配置文件setting的路径

# 创建数据库对象
db = SQLAlchemy(app)

# 导入 Model 注意：只有db创建后才可以导入
from admin.model import User

# 创建表
db.create_all()

# 导入Controller文件
from admin.controller import admin_controller
from admin.controller import Admin


# Login 登陆管理
# 声明login对象
login_manager = LoginManager()

# 初始化绑定到应用
login_manager.init_app(app)

# 声明默认视图函数为login，当我们进行@require_login时，如果没登陆会自动跳到该视图函数处理
login_manager.login_view = "login"


# 当登陆成功后，该函数会自动从会话中存储的用户 ID 重新加载用户对象。它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。
@login_manager.user_loader
def load_user(userid):
    return User.User.query.get(userid)


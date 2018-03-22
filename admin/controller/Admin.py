#! coding: utf8

from flask_admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from admin import app, db
from admin.model.User import User, Operation, Role, Blog


admin_obj = Admin(app, name=u"后台管理系统")
admin_obj.add_view(ModelView(User, db.session))
admin_obj.add_view(ModelView(Role, db.session))
admin_obj.add_view(ModelView(Operation, db.session))

# 功能模块-博客
admin_obj.add_view(ModelView(Blog, db.session))


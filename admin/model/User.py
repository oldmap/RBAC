#! coding: utf8

from admin import db
from flask_login import UserMixin


user_role = db.Table(
        'user_role',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    )


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Integer, default=0, nullable=False)  # 是否管理员 0 不是 1 是
    status = db.Column(db.Integer, default=1, nullable=False)  # 是否有效 0 无效 1有效

    roles = db.relationship(
        "Role",
        secondary=user_role,
        lazy='subquery',
        backref=db.backref('users', lazy=True),
    )

    # 功能模块-用户关联部分
    # 定义一对多关系
    # blogs: 一个用户有多个博客，字段：复数
    # author：一篇博客只能属于一个用户，字段：单数
    blogs = db.relationship(
        'Blog',
        backref='author',
    )

    def __repr__(self):
        return self.username


role_operation = db.Table(
    'role_operation',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('operation_id', db.Integer, db.ForeignKey('operation.id'), primary_key=True),
    )


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    status = db.Column(db.Integer, default=1, nullable=False)  # 是否有效 0 无效 1有效

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Operation(db.Model):
    """
        可以把此看作权限表，但我将其定义为 操作某种资源(资源的定义参考 restfull api设计理念)的一系列动作，
        如 查看  某个 资源， 如 新增 一个资源
        而把 某动作  授予  某个角色，即完成了权限的管理(绑定)
    """
    __tablename__ = 'operation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    method = db.Column(db.String(32), default='GET', )
    uri = db.Column(db.String(256), default='/', nullable=False)

    roles = db.relationship(
        "Role",
        secondary=role_operation,
        lazy='subquery',
        backref=db.backref('operations', lazy=True),
    )

    description = db.Column(db.Text, comment=u'描述信息')

    def __repr__(self):
        return self.name


# 功能模块表
class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    content = db.Column(db.Text, )
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment=u'作者')

    def __repr__(self):
        return self.title


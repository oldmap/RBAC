#! coding: utf8

# 调试模式是否开启
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

# session必须要设置key
SECRET_KEY = 'asdgasdgsagljasdg'

# mysql数据库连接信息,这里改为自己的账号
SQLALCHEMY_DATABASE_URI = "mysql://rbac_user:rbac_password@10.104.19.9:3306/rbac"


# -*- coding:utf-8 -*-

# 默认配置
CSRF_ENABLED = True
SECRET_KEY = 'lian yun'

# 路径
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# SQL配置
SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(os.path.join(basedir, "app.db"))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_respository")

# mail 配置
MAIL_SERVER = "smtp.163.com"
MAIL_PORT = 25
MAIL_USERNAME = "bjliany@163.com"
MAIL_PASSWORD = "1990O0916cloud"
MAIL_USER_TLS = False
MAIL_USER_SSL = False

USERS_EMAIL = ['lianyun08@126.com']

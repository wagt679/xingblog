# -*- coding:utf-8 -*-

# 设定blog的编码的格式
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 导入扩展模块
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from flask.ext.mail import Mail

# 初始化blog应用，并从config中设定配置
blog = Flask(__name__)
blog.config.from_object('config')

# 初始化数据库
db = SQLAlchemy(blog)

# 设定登录管理
lm = LoginManager()
lm.setup_app(blog)

# 设定markdown
pagedown = PageDown()
pagedown.init_app(blog)

# 使用邮件服务器发送邮件
mail = Mail()
mail.init_app(blog)

# 导入模型Models和视图Views
from app import views, models

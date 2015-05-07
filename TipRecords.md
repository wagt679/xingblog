
### 编写原则

使用的模块说明：包括document地址，简单说明，在博客中的使用方案

### Flask 关键问题
#### 应用上下文与响应上下文
Flask将一些用于request的object设定为Thread Local的，提供了类似与全局变量的访问模式。
如在很多View function中，差不多以全局的方式访问request
Table：flask Context globals


|变量名|上下文对象|描述|
|-----|------------|--|
|current_app | 应用上下文| 活动应用的实例|
|g | 应用上下文| 一个可以用于存储上下文临时数据的对象|
|request|响应上下文|收到来自client的HTTP request的包装|
|session|响应上下文|一个dict，记录使得一些数据能够在request之间保存|

当一个request被分配时，Flask会创建application context和request context。
当这个request结束后，则将其pop。


### 使用的模块

#### Flask-Login
[document](https://flask-login.readthedocs.org/en/latest/)
[github](https://github.com/maxcountryman/flask-login/)

#### Flask-SQLAlchemy
[document](http://pythonhosted.org/Flask-SQLAlchemy/index.html)
数据迁移非常方便，还可以构建数据库的降级和升级。并且维护数据库中各个表之间的依赖关系。
过程比较复杂，可以参考Flask Web Development第五章的相关内容。

#### Flask-Migrate
创建、升级、迁移、降级数据库

#### Flask-Script
未使用

#### Flask-Bootstrap
[document](http://www.pythonhosted.org/Flask-Bootstrap/index.html)
```python
pip install flask-bootstrap

from flask.ext.bootstrap import Bootstrap
bootstrap = Bootstrap(app)
```
然后就可以在html模板中使用bootstrap相关的形式了。
在编写中也可以使用通常的形式来应用bootstrap。

#### Flask-Moment 本地化
继承了`moment.js`的falsk模块。
```python
pip install flask-moment

from flask.ext.moment import Moment
moment = Moment(app)
```

```html
{% block scripts %}
{{ super() }}
{{ moment.include_moment() }}
{% endblock %}
```

使用：
```python
from datetime import datetime
@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())
```
当前时间显示:
```html
<p>The local date and time is {{ moment(current_time).format('LLL') }}.</p>
<p>That was {{ moment(current_time).fromNow(refresh=True) }}</p>
```

#### Flask-WTF
详细参见Flask Web Development第三章。

#### Flask-Misaka
[document](http://pythonhosted.org//Flask-Misaka/)
Markdown解释器。

#### Flask-Markdown
[document](https://pythonhosted.org/Flask-Markdown/)
使得博客文章可以支持Markdown编辑。
未使用

#### MDMagick 网页上的markdown编辑器
[例子](http://fguillen.github.io/MDMagick/)
[github](https://github.com/fguillen/MDMagick)

#### Flask-Mail
[document](https://pythonhosted.org/Flask-Mail/)

这个插件将会连接到SMTP服务器上，将邮件发送给接收者。

|Key|Default|描述|
|---|--------|---|
|MAIL_HOSTNAME|localhost|邮件服务器的IP地址和主机名|
|MAIL_PORT|25 |邮件服务器的端口|
|MAIL_USER_TLS|False|是否使用Transport Layout Security(TLS) security|
|MAIL_USER_SSL|False|是否使用Secure Sockets Layer (SSL) security|
|MAIL_USERNAME|None|邮件账号用户名
|MAIL_PASSWORD|None|邮件账号密码
```python
from app import blog, mail
from flask_mail import Message

msg = Message('test subject', sender='you@example.com',recipients=['you@example.com'])
msg.body = """欢迎您来到行××××"""
with blog.app_context():
    mail.send(msg)
```

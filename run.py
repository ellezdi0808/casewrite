from flask import Flask, render_template, redirect, session, make_response, request, flash, url_for,jsonify,g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from datetime import datetime, timedelta
from makedb import db

# datetime 描述当前日期时间，   timedelta 描述时间片段
import sqlite3,json,time

app = Flask(__name__, static_url_path='')  # 网站核心对象
app.debug = True
# app这个对象非常重要，一些 配置，获取，什么的都要找app
# __name__站点根目录以这个文件的目录为界限


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/getcase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

app.secret_key = "alisa.com"
# session 是靠cookie实现的，cookie是存在本地硬盘的一小段文本信息，存在本地硬盘就会有可能被人篡改
# 加了 app.secret_key安全码 就相当于加密解密有了秘钥，这个猜不到，别人就没有办法篡改你的cookie

DATABASE_URL = r'./db/case.db'

# db = SQLAlchemy(app)  # 数据库核心对象
db.init_app(app)  # 把app 和db关联起来

from account import account
from case import case
from project import project
from module import module


app.register_blueprint(account,url_prefix="/account")
app.register_blueprint(case,url_prefix='/case')
app.register_blueprint(project,url_prefix='/project')
app.register_blueprint(module,url_prefix='/module')



# migrate = Migrate(app, db)
#
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)


# from case.views import LoginUser,RegUser

# 为导入的基于类的视图添加分配URL规则
#
# app.add_url_rule('/reg/reg/',view_func=LoginUser.as_view("reg_user"))  #reg_user终结点
# app.add_url_rule('/reg/login/',view_func=RegUser.as_view("login_user"))



# 缺少用例池，执行过的用例也可以复用
# 用户权限，不同的权限可以查看不同的目录
# 批量添加功能可以优化，现在是进来显示所有的项目和模块，没有像单独添加case那样可以获取当前的项目和对应的模块
# 现在是登录上来的用户就能看见所有用例，这里需要根据不同用户登录，查看不同的数据
# 删除功能优化，现在是删除项目，项目对应的模块和case还在
# 缺少批量删除功能




if __name__ == '__main__':
    # manager.run()
    app.run()

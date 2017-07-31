from flask import Flask, render_template, redirect, session, make_response, request, flash, url_for,jsonify,g
from flask.views import View,MethodView  #view 是基类
from flask import Blueprint
# from account import account
from case.models import *
from datetime import datetime, timedelta
import time,flask



#基于类的视图
# class RegUser(View):# 集成基类 view    py2 是集成object
#     def dispatch_request(self): #调度请求
#         return render_template('reg.html')
#
# class MyRegUser(MethodView):
#     def get(self):
#         return render_template('reg.html')
#
#     def post(self):
#         return None
#
#
# class UserLogin(View):
#     def dispatch_request(self):
#         pass
#
#
# @account.route('/articles/')
# def arcicle_list():
#     return render_template('admin/login.html')
#
# @account.route('/reg/<id>/')
# def article_detail(id=None):
#     item = {"id":id}
#     return render_template('info/reg.html',item=item)

class AccountLogin(MethodView):
    def get(self):
        name = request.cookies.get("username")
        if name:
            return redirect(url_for("case.case_list"))
        return render_template('admin/login.html')

    def post(self):
        # name = request.cookies.get("username")

        username = request.form.get('username',None)
        password = request.form.get('password',None)
        rememberMe = request.form.get('rememberMe',None)

        from case.models import User

        user = db.session.query(User).filter(User.username == '{}'.format(username)).all()
        pwd = db.session.query(User).filter(User.username=='{}'.format(username),User.password=='{}'.format(password)).all()

        lenAccount = len(pwd)

        if lenAccount > 0:
            session['admin'] = username
            if rememberMe == 'on':
                resp = make_response(redirect(url_for('case.case_list')))
                resp.set_cookie('username',username,path='/',expires=datetime.now() + timedelta(days=7))
                return resp
            # 创建session，session 是某一个用户请求的不同页面之  间共享的一些信息

            return redirect(url_for('case.case_list'))

        elif len(user) == 0:

            flash('用户名不存在')
            return redirect(url_for('account.login'))
        elif username is None:
            flash('请输入用户名')
            return redirect(url_for('account.login'))

        elif password is None:
            flash("请输入密码")
            return redirect(url_for('account.login'))

        else:
            flash('密码输入错误')
            return redirect(url_for('account.login'))


class AccountLogout(MethodView):
    def get(self):

            # session.pop('admin', None)
            # return redirect(url_for('case_list'))

            name = request.cookies.get("username")

            if name:
                resp = make_response(redirect(url_for('account.login')))
                resp.set_cookie('username', '', expires=datetime.now() + timedelta(minutes=-1))

                session.pop('admin', None)  # 清空session
                session.clear()

                return resp

            else:
                session.pop('admin', None)
                return redirect(url_for('case.case_list'))

    def post(self):
        pass


class AccountReg(MethodView):
    # from case.models import User

    def get(self):
        return render_template('admin/reg.html')

    def post(self):

        username = request.form.get('username',None)
        password = request.form.get('password',None)
        email = request.form.get("email",None)
        mobile = request.form.get("mobile",None)
        createTime = datetime.now()

        permission = 1

        user = db.session.query(User).filter(User.username == '{}'.format(username)).all()

        if username is "":
            flash("用户名不能为空")
            return render_template('admin/reg.html')
        elif password is "":
            flash("密码不能为空")
            return render_template('admin/reg.html')

        elif len(user) > 0:
            flash("用户名已经存在")
            return render_template('admin/reg.html')

        else:
            user = User(username,password,email,mobile,permission,createTime)
            db.session.add(user)
            db.session.commit()
            return render_template('admin/login.html')


class PersonalInformation(MethodView):
    def get(self):

        from case.models import User

        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))
        else:

            name = session['admin']

            uservalue = db.session.query(User).filter(User.username == name).first()

            pwd = uservalue.password

            email = uservalue.email

            mobile = uservalue.mobile

            return render_template('admin/per-info.html', name=name, pwd=pwd,email=email,mobile=mobile)


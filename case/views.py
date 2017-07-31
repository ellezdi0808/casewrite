from flask import Flask, render_template, redirect, session, make_response, request, flash, url_for,jsonify,g
from flask.views import View,MethodView  #view 是基类
from flask import Blueprint
from case.models import *
from datetime import datetime, timedelta
import time,json

# 基于类的视图

#
# class LoginUser(View):
#     def dispatch_request(self):
#     # dispatch_request 调度请求，类似于把 @app.route('/admin/project/'）把路径分配到某一个视图函数上
#         return render_template("admin/login.html")


# 基于方法的视图

# class RegUser(MethodView):
#     def get(self):
#         return render_template("admin/login.html")
#
#
#     def post(self):
#         pass

class CaseList(MethodView):
    def get(self,page=1):

        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            key = request.args.get('key', '')
            from case.models import CaseData, caseProject, caseModule,User

            username = session['admin']
            userid = User.query.filter(User.username == username).first()

            if username == "admin":
                getCaseNum = CaseData.query.filter(CaseData.caseName.like('%{}%'.format(key))).all()
                cases = CaseData.query.filter(CaseData.caseName.like('%{}%'.format(key))).paginate(page, per_page=5)

            else:
                getCaseNum = CaseData.query.filter(CaseData.caseName.like('%{}%'.format(key)),CaseData.userId == userid.id).all()
                cases = CaseData.query.filter(CaseData.caseName.like('%{}%'.format(key)),CaseData.userId == userid.id).paginate(page, per_page=5)

            lenCase = len(getCaseNum)

            names = db.session.query(caseProject).join(CaseData, caseProject.id == CaseData.projectId).all()
            modules = db.session.query(caseModule).join(CaseData, caseModule.id == CaseData.moduleId).all()

            proectNames = {}
            for name in names:
                proectNames[name.id] = name.projectName

            moduleNames = {}

            for module in modules:
                moduleNames[module.id] = module.moduleName
            # return str(cases)
            return render_template('admin/case-list.html', key=key, cases=cases, proectNames=proectNames,
                                   moduleNames=moduleNames, lenCase=lenCase)

    def post(self):
        pass



class CaseAdd(MethodView):
    def get(self):

        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            from case.models import CaseData, caseProject, caseModule

            projects = db.session.query(caseProject).all()
            modules = db.session.query(caseModule).all()

            return render_template("admin/add-case.html", modules=modules, projects=projects)


    def post(self):
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:

            from case.models import CaseData, caseProject, caseModule

            projects = db.session.query(caseProject).all()
            modules = db.session.query(caseModule).all()

            projectName = request.form.get("projectName", None)
            moduleName = request.form.get("module", None)
            caseName = request.form.get("caseName", None)
            step = request.form.get("step", None)
            expectResult = request.form.get("expectResult", None)
            writeTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            caseExcute = request.form.get("caseExcute", None)

            username = session['admin']
            userid = User.query.filter(User.username == username).first()

            if caseExcute == "on":
                caseExcute = 1
            else:
                caseExcute = 0


            case = CaseData(projectName, moduleName, caseName, step, expectResult, caseExcute,userid.id, writeTime)
            db.session.add(case)
            db.session.commit()

            return redirect(url_for('case.case_list'))

class CaseAddGetModule(MethodView):
    def get(self):
        pass

    def post(self):
        from case.models import CaseData, caseProject, caseModule
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            # projectName = request.form.get("projectName", None)
            data = json.loads(request.form.get("data"))
            projectId = data['projectId']
            modules = db.session.query(caseModule).filter(caseModule.projectId == '{}'.format(projectId)).all()

            modulelist = []

            for module in modules:
                moduledict = dict()
                moduledict['id'] = module.id
                moduledict['moduleName'] = module.moduleName
                modulelist.append(moduledict)

            return jsonify(modulelist)


class CaseEdit(MethodView):
    def get(self,id=None):

        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            from case.models import CaseData, caseProject, caseModule

            projects = db.session.query(caseProject).all()
            modules = db.session.query(caseModule).all()
            case = db.session.query(CaseData).filter(CaseData.id == id).one()

            return render_template('admin/case-edit.html', case=case, projects=projects, modules=modules)

    def post(self):
        pass


class CaseCheck(MethodView):
    def get(self,id=None):
        from case.models import CaseData, caseProject, caseModule
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            projects = db.session.query(caseProject).all()
            modules = db.session.query(caseModule).all()
            case = db.session.query(CaseData).filter(CaseData.id == id).one()

            return render_template('admin/case-check.html', case=case, projects=projects, modules=modules)


    def post(self):
        pass

class CaseDelete(MethodView):
    def get(self,id=None):
        from case.models import CaseData, caseProject, caseModule
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            case = db.session.query(CaseData).filter(CaseData.id == id).one()
            db.session.delete(case)
            db.session.commit()

            return redirect(url_for('case.case_list'))

    def post(self):
        pass


class CaseSaveEdit(MethodView):
    def get(self):
        pass


    def post(self):
        from case.models import CaseData, caseProject, caseModule
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            rowid = request.form.get("rowid", None)
            projectName = request.form.get("projectName", None)
            moduleName = request.form.get("module", None)
            projectId = "db.session.query(caseProject).filter(caseProject.projectName == {}).one().id".format(
                projectName)
            moduleId = "db.session.query(caseModule).filter(caseModule.moduleName == {}, caseModule.projectId == {}).one().id".format(
                moduleName, projectId)
            caseName = request.form.get("caseName", None)
            step = request.form.get("step", None)
            expectResult = request.form.get("expectResult", None)
            caseExcute = request.form.get("caseExcute", None)
            writeTime = request.form.get("writeTime", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

            if caseExcute == "on":
                caseExcute = 1
            else:
                caseExcute = 0

            db.session.query(CaseData).filter(CaseData.id == rowid).update(
                {CaseData.projectId: projectName, CaseData.moduleId: moduleName, CaseData.caseName: caseName,
                 CaseData.step: step, CaseData.expectResult: expectResult, CaseData.caseExcute: caseExcute,
                 CaseData.writeTime: writeTime})

            db.session.commit()
            return redirect(url_for('case.case_list'))



class CaseExcute(MethodView):

    def get(self):
        from case.models import CaseData,caseProject

        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            user = session['admin']
            uservalue = db.session.query(User).filter(User.username == user).first()

            if user == "admin":
                processed = db.session.query(CaseData).filter(CaseData.caseExcute == 1).all()
                processed = len(processed)

                unprocessed = db.session.query(CaseData).filter(CaseData.caseExcute ==0).all()
                unprocessed = len(unprocessed)

                stateless = db.session.query(CaseData).filter(CaseData.caseExcute != 1,CaseData.caseExcute !=0).all()
                stateless = len(stateless)

                casecount = db.session.query(CaseData).all()
                casecount = len(casecount)

                caseratio =  round(processed/casecount,2)

                project = db.session.query(caseProject).all()

                provalue = {}
                for pro in project:
                    pronum = db.session.query(CaseData).filter(CaseData.projectId == pro.id).all()
                    pronum = len(pronum)
                    provalue[pro.projectName] = pronum

            else:
                processed = db.session.query(CaseData).filter(CaseData.caseExcute == 1,CaseData.userId == uservalue.id).all()
                processed = len(processed)

                unprocessed = db.session.query(CaseData).filter(CaseData.caseExcute == 0,CaseData.userId == uservalue.id).all()
                unprocessed = len(unprocessed)

                stateless = db.session.query(CaseData).filter(CaseData.caseExcute != 1, CaseData.caseExcute != 0,CaseData.userId == uservalue.id).all()
                stateless = len(stateless)

                casecount = db.session.query(CaseData).filter(CaseData.userId == uservalue.id).all()
                casecount = len(casecount)

                caseratio = round(processed / casecount, 2)

                project = db.session.query(caseProject).all()

                provalue = {}
                for pro in project:
                    pronum = db.session.query(CaseData).filter(CaseData.userId == uservalue.id,CaseData.projectId == pro.id).all()
                    pronum = len(pronum)
                    provalue[pro.projectName] = pronum



            if user == "admin":
                user = "所有用户"

            return render_template('admin/case-Excute.html',provalue=provalue,user=user,caseratio=caseratio,casecount=casecount,processed=processed,unprocessed=unprocessed,stateless=stateless)


class CaseBatchAdd(MethodView):
    def get(self):
        from case.models import CaseData, caseProject, caseModule

        projects = db.session.query(caseProject).all()
        modules = db.session.query(caseModule).all()
        return render_template('admin/case-batch-add.html', projects=projects, modules=modules)


class CaseGetJson(MethodView):
    def get(self):
        from case.models import CaseData, caseProject, caseModule

        data = json.loads(request.args.get('data'))

        username = session['admin']
        userid = User.query.filter(User.username == username).first()

        for d in data:
            if d.get("caseName"):
                writeTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                caseExcute = 0

                # case = CaseData(projectName, moduleName, caseName, step, expectResult, caseExcute, userid.id, writeTime)

                case = CaseData(d['projectName'], d['module'], d['caseName'], d['step'], d['expectResult'], caseExcute,userid.id,
                                writeTime)
                db.session.add(case)
            else:
                continue
        db.session.commit()

        return jsonify(result=data)


class CaseSystemHomePage(MethodView):
    def get(self,page=1):

        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            key = request.args.get('key', '')
            from case.models import CaseData, caseProject, caseModule,User

            username = session['admin']
            userid = User.query.filter(User.username == username).first()

            getCaseNum = CaseData.query.filter(CaseData.caseName.like('%{}%'.format(key))).all()
            cases = CaseData.query.filter(CaseData.caseName.like('%{}%'.format(key))).paginate(page, per_page=5)

            lenCase = len(getCaseNum)

            names = db.session.query(caseProject).join(CaseData, caseProject.id == CaseData.projectId).all()
            modules = db.session.query(caseModule).join(CaseData, caseModule.id == CaseData.moduleId).all()

            proectNames = {}
            for name in names:
                proectNames[name.id] = name.projectName

            moduleNames = {}

            for module in modules:
                moduleNames[module.id] = module.moduleName
            # return str(cases)
            return render_template('admin/homePage.html', key=key, cases=cases, proectNames=proectNames,
                                   moduleNames=moduleNames, lenCase=lenCase,userid=userid)

    def post(self):
        pass
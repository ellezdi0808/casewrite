from flask import Flask, render_template, redirect, session, make_response, request, flash, url_for, jsonify, g
from flask.views import View, MethodView  # view 是基类
from flask import Blueprint
from case.models import *
from datetime import datetime, timedelta
import time, json


class AddModule(MethodView):
    def get(self):
        from case.models import CaseData, caseProject, caseModule

        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))
        else:

            projects = db.session.query(caseProject).all()

            return render_template('admin/create-module.html', projects=projects)

    def post(self):
        from case.models import CaseData, caseProject, caseModule


        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))
        else:

            projects = db.session.query(caseProject).all()

            projectName = request.form.get("projectName", None)
            moduleName = request.form.get("moduleName", None)
            module = caseModule(moduleName, projectName)
            db.session.add(module)
            db.session.commit()
            return redirect(url_for('module.module_list'))


class ModuleList(MethodView):
    def get(self, page=1):

        from case.models import CaseData, caseProject, caseModule,db

        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))
        else:

            # cases = CaseData.query.paginate(page,per_page=6)

            modules = caseModule.query.paginate(page, per_page=6)
            names = db.session.query(caseProject).all()

            projects = {}
            for name in names:
                projects[name.id] = name.projectName

            # return str(modules)
            return render_template('admin/module-list.html', modules=modules, projects=projects)


class ModuleDelete(MethodView):
    def get(self, id=None):
        from case.models import CaseData, caseProject, caseModule,db
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            module = db.session.query(caseModule).filter(caseModule.id == id).one()
            db.session.delete(module)
            db.session.commit()

            return redirect(url_for('module.module_list'))


class ModuleEdit(MethodView):
    def get(self, id=None):
        from case.models import CaseData, caseProject, caseModule,db
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            projects = db.session.query(caseProject).all()
            module = db.session.query(caseModule).filter(caseModule.id == id).one()

            return render_template('admin/module-edit.html', module=module, projects=projects)

    def post(self):
        pass



class ModuleSaveEdit(MethodView):
    def post(self):

        from case.models import CaseData, caseProject, caseModule,db

        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))
        else:
            rowid = request.form.get("rowid", None)
            projectName = request.form.get("projectName", None)
            moduleName = request.form.get("moduleName", None)

            db.session.query(caseModule).filter(caseModule.id == rowid).update(
                {caseModule.projectId: projectName, caseModule.moduleName: moduleName})
            db.session.commit()
            return redirect(url_for('module.module_list'))


    def get(self):
        pass




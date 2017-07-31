from flask import Flask, render_template, redirect, session, make_response, request, flash, url_for,jsonify,g
from flask.views import View,MethodView  #view 是基类
from flask import Blueprint
from case.models import *
from datetime import datetime, timedelta
import time,json


class AddProject(MethodView):
    def get(self):
        from case.models import caseProject
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))
        else:
            return render_template('admin/create-project.html')


    def post(self):
        from case.models import caseProject
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))
        else:

            projectName = request.form.get("projectName", None)

            projectNameNow = db.session.query(caseProject).filter(caseProject.projectName == projectName).one_or_none()

            if projectNameNow is None:
                project = caseProject(projectName)
                db.session.add(project)
                db.session.commit()

                return redirect(url_for('project.project_list'))
            else:
                flash('项目名称已存在！')
                return render_template('admin/create-project.html')


class ProjectList(MethodView):
    def get(self,page=1):
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))
        else:

            from case.models import caseProject,db
            projects = caseProject.query.paginate(page, per_page=6)

            return render_template('admin/project-list.html', projects=projects)


class ProjectEdit(MethodView):
    def get(self,id=None):
        from case.models import CaseData, caseProject, caseModule,db
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            project = db.session.query(caseProject).filter(caseProject.id == id).one()
            return render_template('admin/project-edit.html', project=project)


class ProjectSaveEdit(MethodView):
    def post(self):
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:

            from case.models import CaseData, caseProject, caseModule,db

            rowid = request.form.get("rowid", None)
            projectName = request.form.get("projectName", None)

            projectNameGet = db.session.query(caseProject).filter(
                caseProject.projectName == projectName).one_or_none()

            if projectNameGet is None:
                db.session.query(caseProject).filter(caseProject.id == rowid).update(
                    {caseProject.projectName: projectName})
                db.session.commit()
                return redirect(url_for('project.project_list'))
            else:
                flash("项目名称已经存在 ！")
                project = db.session.query(caseProject).filter(caseProject.id == rowid).one()
                return render_template('admin/project-edit.html', project=project)


class ProjectDelete(MethodView):
    def get(self,id=None):
        from case.models import CaseData, caseProject, caseModule,db
        if session.get('admin', None) is None:
            return redirect(url_for('account.login'))

        else:
            project = db.session.query(caseProject).filter(caseProject.id == id).one()
            db.session.delete(project)
            db.session.commit()

            return redirect(url_for('project.project_list'))

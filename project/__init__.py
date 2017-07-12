from flask import Blueprint
from case.models import *
project = Blueprint('project',__name__)
#Blueprint  new 一个实例,article是终结点，链接从article开始

from project.views import *

project_list = ProjectList.as_view("project_list")

project.add_url_rule('/add/',view_func=AddProject.as_view('add_project'))
project.add_url_rule('/list/',view_func=project_list)
project.add_url_rule('/list/<int:page>/',view_func=project_list)
project.add_url_rule('/edit/<id>/',view_func=ProjectEdit.as_view('project_edit'))
project.add_url_rule('/saveEdit/',view_func=ProjectSaveEdit.as_view('saveProject_edit'))
project.add_url_rule('/del/<id>/',view_func=ProjectDelete.as_view('del_project'))



from flask import Blueprint
from case.models import *
module = Blueprint('module',__name__)
#Blueprint  new 一个实例,article是终结点，链接从article开始

from module.views import *

module_list = ModuleList.as_view('module_list')

module.add_url_rule('/list/',view_func=module_list)
module.add_url_rule('/list/<int:page>/',view_func=module_list)

module.add_url_rule('/add/',view_func=AddModule.as_view('add_module'))
module.add_url_rule('/del/<id>/',view_func=ModuleDelete.as_view('del_module'))
module.add_url_rule('/edit/<id>',view_func=ModuleEdit.as_view('module_edit'))
module.add_url_rule('/saveEdit/',view_func=ModuleSaveEdit.as_view('saveModule_edit'))




from flask import Blueprint

case = Blueprint('case',__name__)
#Blueprint  new 一个实例,article是终结点，链接从article开始

from case.views import *

case_list = CaseList.as_view('case_list')

case.add_url_rule('/list/',view_func=case_list)
case.add_url_rule('/list/<int:page>/',view_func=case_list)

case.add_url_rule('/add/',view_func=CaseAdd.as_view('add_case'))
case.add_url_rule('/getModule/',view_func=CaseAddGetModule.as_view('get_module'))
case.add_url_rule('/edit/<id>/',view_func=CaseEdit.as_view('case_edit'))
case.add_url_rule('/check/<id>/',view_func=CaseCheck.as_view('case_check'))
case.add_url_rule('/del/<id>/',view_func=CaseDelete.as_view('case_delete'))
case.add_url_rule('/saveEdit/',view_func=CaseSaveEdit.as_view('save_edit'))
case.add_url_rule('/caseExcute/',view_func=CaseExcute.as_view('case_excute'))
case.add_url_rule('/batch/add/',view_func=CaseBatchAdd.as_view('case_batchadd'))
case.add_url_rule('/get-json/',view_func=CaseGetJson.as_view('get_json'))



from flask import Blueprint,flash,get_flashed_messages,message_flashed

account = Blueprint('account',__name__)
#Blueprint  new 一个实例,article是终结点，链接从article开始

from account.views import *



account.add_url_rule('/login/',view_func=AccountLogin.as_view('login'))
account.add_url_rule('/logout/',view_func=AccountLogout.as_view('logout'))
account.add_url_rule('/reg/',view_func=AccountReg.as_view('reg'))
account.add_url_rule('/personal/info/',view_func=PersonalInformation.as_view('personal_information'))

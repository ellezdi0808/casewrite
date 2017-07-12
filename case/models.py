#encoding = 'utf8'
# from run import db,app
from datetime import datetime
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# migrate = Migrate(app,db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)


class CaseData(db.Model):
    """ case """
    __tablename__ = 'cases'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    caseName = db.Column(db.String(50))
    step = db.Column(db.String(200))
    expectResult = db.Column(db.String(200))
    caseExcute = db.Column(db.Integer)
    writeTime = db.Column(db.String())
    projectId = db.Column(db.Integer,db.ForeignKey('projects.id')) # table id
    moduleId = db.Column(db.Integer,db.ForeignKey('modules.id')) # table id



    def __init__(self,projectId,moduleId,caseName,step,expectResult,caseExcute,writeTime=datetime.now()):
        self.projectId = projectId
        self.moduleId = moduleId
        self.caseName = caseName
        self.step = step
        self.expectResult = expectResult
        self.caseExcute = caseExcute
        self.writeTime = writeTime

    def __repr__(self):
        return '<用例id{}--》用例名称{}>'.format(self.id,self.caseName)

    def to_json(self):
        return dict(id=self.id, name=self.caseName)


class caseProject(db.Model):
    """ project table """
    __tablename__ = 'projects'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    projectName = db.Column(db.String(50),unique=True)

    cases = db.relationship('CaseData',backref='caseProject',lazy='dynamic')
    modules = db.relationship('caseModule',backref='caseProject',lazy='dynamic')

    def __init__(self,projectName):
        self.projectName = projectName


    def __repr__(self):
        return '<项目id{}-->项目名称{}>'.format(self.id,self.projectName)


    def to_json(self):
        return dict(id=self.id, name=self.projectName)


class caseModule(db.Model):
    """ module table """
    __tablename__ = 'modules'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    moduleName = db.Column(db.String(50))

    projectId = db.Column(db.Integer,db.ForeignKey('projects.id')) # table id column
    cases = db.relationship('CaseData',backref='caseModule',lazy='dynamic')



    def __init__(self,moduleName,projectId):
        self.moduleName = moduleName
        self.projectId =projectId


    def __repr__(self):
        return '<模块id{}-->模块名称{}>'.format(self.id,self.moduleName)


    def to_json(self):
        return dict(id=self.id, name=self.moduleName)


class User(db.Model):
    """user table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True,nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def to_json(self):
        return dict(id=self.id, name=self.username)



#
# if __name__ == '__main__':
#     manager.run()
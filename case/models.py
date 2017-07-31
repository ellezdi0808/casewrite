#encoding = 'utf8'
# from run import db,app
from makedb import db
from datetime import datetime
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy()

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
    userId = db.Column(db.Integer,db.ForeignKey("user.id"))



    def __init__(self,projectId,moduleId,caseName,step,expectResult,caseExcute,userId,writeTime=datetime.now()):
        self.projectId = projectId
        self.moduleId = moduleId
        self.caseName = caseName
        self.step = step
        self.expectResult = expectResult
        self.caseExcute = caseExcute
        self.userId = userId
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
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50), unique=True,nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128))
    mobile = db.Column(db.String(11))
    # name = db.Column(db.String(50))
    # gender = db.Column(db.SmallInteger)  # 0 未知， 1 男 2 女
    permission = db.Column(db.Integer)
    createTime = db.Column(db.DateTime,default=datetime.now())

    roles = db.relationship('UserRole',backref='User',lazy='dynamic')
    cases = db.relationship('CaseData',backref='User',lazy='dynamic')


    def __init__(self,username,password,email,mobile,permission,createTime):
        self.username = username
        self.password = password
        self.email = email
        self.mobile = mobile
        # self.name = name
        # self.gender = gender
        self.permission = permission
        self.createTime = createTime


    def __repr__(self):
        return '<用户id{}-->账号{}>'.format(self.id, self.username)

    def to_json(self):
        return dict(id=self.id, name=self.username)

    @property
    def permissions(self):
        permissions = Permission.query.join(RolePermission).join(Role).join(UserRole).join(User).filter(User.id == self.id)

        return permissions


    @property
    def menus(self):
        menus = Menu.query.join(RoleMenu).join(Role).join(UserRole).join(User).filter(User.id == self.id).order_by(Menu.type_,Menu.order).all()

        return menus


class Role(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String, nullable=True, unique=True)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)

    users = db.relationship('UserRole', backref='Role')
    rolePermission = db.relationship('RolePermission',backref='Role',lazy='dynamic')
    roleMenu = db.relationship('RoleMenu',backref='Role',lazy='dynamic')


    def __init__(self,name,default,permissions):
        self.name = name
        self.default = default
        self.permissions = permissions


    def __repr__(self):
        return '<角色id{}-->角色名称{}>'.format(self.id, self.name)


class Permission(db.Model):

    __tablename__ = 'permission'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50))
    action = db.Column(db.String(250), unique=True)

    permissions = db.relationship('RolePermission',backref='Permission',lazy='dynamic')


    def __init__(self,name,action):
        self.name = name
        self.action = action

    def __repr__(self):
        return '<权限id{}-->权限名称{}>'.format(self.id, self.name)


class Menu(db.Model):

    __tablename__ = 'menu'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50))
    icon = db.Column(db.String(50))
    url = db.Column(db.String(250))
    order = db.Column(db.SmallInteger, default=0)
    bg_color = db.Column(db.String(50))

    roleMenu = db.relationship('RoleMenu',backref='Menu',lazy='dynamic')


    def __init__(self,name,icon,url,order,bg_color):
        self.name = name
        self.icon = icon
        self.url = url
        self.order = order
        self.bg_color = bg_color

    def __repr__(self):
        return '<菜单id{}-->菜单名称{}>'.format(self.id, self.name)


class UserRole(db.Model):

    __tablename__ = "userRole"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    createTime = db.Column(db.DateTime,default=datetime.now)

    userId = db.Column(db.Integer,db.ForeignKey('user.id'))
    roleId = db.Column(db.Integer,db.ForeignKey('roles.id'))


    def __init__(self,userId,roleId,createTime):
        self.userId = userId
        self.roleId = roleId
        self.createTime = createTime

    def __repr__(self):
        return '<用户角色id{}-->创建时间{}>'.format(self.id, self.createTime)


class RolePermission(db.Model):

    __tablename__ = "rolePermission"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    createTime = db.Column(db.DateTime,default=datetime.now)

    permissionId = db.Column(db.Integer,db.ForeignKey('permission.id'))
    roleId = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __init__(self,permissionId,roleId,createTime):

        self.permissionId = permissionId
        self.roleId = roleId
        self.createTime = createTime

    def __repr__(self):
        return '<角色权限id{}-->创建时间{}>'.format(self.id, self.createTime)



class RoleMenu(db.Model):

    __tablename__ = "roleMenu"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    createTime = db.Column(db.DateTime,default=datetime.now)
    idDelete = db.Column(db.Boolean,default=False)

    roleId = db.Column(db.Integer,db.ForeignKey('roles.id'))
    menuId = db.Column(db.Integer,db.ForeignKey('menu.id'))


    def __init__(self,roleId,menuId,idDelete,createTime):

        self.roleId = roleId
        self.menuId = menuId
        self.idDelete = idDelete
        self.createTime = createTime

    def __repr__(self):
        return '<角色菜单id{}-->创建时间{}>'.format(self.id, self.createTime)







            # if __name__ == '__main__':
#     manager.run()
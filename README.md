编程环境： python3.5.2


登录账号： user： test  passWord：123456   也可以自行注册账号，现在么有做权限限制，所有账号都可以查看用例



网站启动：首先你要对python flask 有一些了解。代码down到本地之后，启动run.py文件就可以。最好有一个编辑器，用编辑器打开项目。


初衷 ：

学习python Web 编程也有几个月了，一直想写个网站出来，但是没有想好写什么功能。
刚好公司之前用的用例管理是excel，不太好做用例执行统计。
然后，我就想着写一个用例管理系统出来，方便工作。
当然，这中间，我有尝试在测试服务器上安装testlink，但是安装完之后，发现用起来不太顺手，层级之间的关联有点奇葩，同事也反应不太好用。
后面，公司统一用禅道管理用例了。。。其实也不太好用，就是一个接口可能会有很多个case，每次添加不是很顺手。

当然的当然，我的编程能力有限，设计产品能力有限，所以功能实现起来需要时间，当然这不是借口。
但，后面我会慢慢添加功能。



功能实现：

1. 登录添加session，后续那些页面间共享session，通过cookie实现记住密码
2. 添加用例页面通过ajax实现，根据项目名称获取项目对应模块
3. 通过flask-sqlalchemy实现数据建模
4. 用例列表查询功能，目前针对用例名称模糊搜索
5. 用例列表提供修改，删除，查看，翻页功能
6. 项目与模块列表提供查看修改，删除，翻页功能
7. 项目代码通过蓝图管理
8. 蓝图的view下面的代码是采用的基于方法的视图整理代码
9. 用例执行统计，因为没有根据用户权限查看用例数据，所以目前统计的所有的case数
10. 登录，注册，查看个人信息功能




未实现待完成功能：
1. 数据模型更新自动更新数据库
2. 缺少用例池，执行过的用例也可以复用
3. 用户权限，不同的权限可以查看不同的目录或者说是case
4. 代码优化，目前都没有什么备注
5. 批量添加用例页面没有做项目和模块关联功能
6. 删除功能优化，现在是删除项目，项目对应的模块和case还在
7. 缺少批量删除功能
8. 用例统计，可以区分开，自己既可以看自己的用例执行情况，也可以看整个项目的执行情况，还可以看所有项目总计情况

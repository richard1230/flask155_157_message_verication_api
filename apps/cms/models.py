
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash



class CMSPersmission(object):
    # 255的二进制方式来表示 1111 1111
    ALL_PERMISSION = 0b11111111
    # 1. 访问者权限
    VISITOR =        0b00000001
    # 2. 管理帖子权限
    POSTER =         0b00000010
    # 3. 管理评论的权限
    COMMENTER =      0b00000100
    # 4. 管理板块的权限
    BOARDER =        0b00001000
    # 5. 管理前台用户的权限
    FRONTUSER =      0b00010000
    # 6. 管理后台用户的权限
    CMSUSER =        0b00100000
    # 7. 管理后台管理员的权限
    ADMINER =        0b01000000

cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)
)

class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200),nullable=True)#描述信息
    create_time = db.Column(db.DateTime,default=datetime.now)
    permissions = db.Column(db.Integer,default=CMSPersmission.VISITOR)

    users = db.relationship('CMSUser',secondary=cms_role_user,backref='roles')



class CMSUser(db.Model):
    __tablename__='cms_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    join_time =db.Column(db.DateTime,default=datetime.now)
    """
    想要映射到数据库里面必须添加到manage.py里面
  
    """


    def __init__(self,username,password,email):
        self.username=username
        self.password=password
        self.email=email

    @property
    def password(self):
        return self._password


    @password.setter
    def password(self,raw_password):
        self._password= generate_password_hash(raw_password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        #这里也可以写为self._password(代表的是password方法下面的返回值)，其实这里的self.password指的就是这个password方法
        return result
#147讲
    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
        return all_permissions

    #判断是否有这个权限
    def has_permission(self, permission):
        # all_permissions = self.permissions
        # result = all_permissions&permission == permission
        # return result
        return self.permissions & permission == permission

    @property
    def is_developer(self):
        return self.has_permission(CMSPersmission.ALL_PERMISSION)


#
# user = CMSUser()
# print(user.password)



# 密码：对外的字段名叫做password
# 密码：对内的字段名叫做_password
"""
(my_env) $pwd
/Users/mac/PycharmProjects/bbc
(my_env) $python3 manage.py db migrate
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'cms_role'
INFO  [alembic.autogenerate.compare] Detected added table 'cms_role_user'
  Generating /Users/mac/PycharmProjects/bbc/migrations/versions/725375213f6e_.py
  ...  done
(my_env) $python3 manage.py db upgrade
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 08504da615b9 -> 725375213f6e, empty message
(my_env) $
------------------------------------------------------------------------------
mysql> show databases;
+-----------------------+
| Database              |
+-----------------------+
| information_schema    |
| alembic_demo          |
| flask_alembic_demo    |
| flask_migrate_demo    |
| flask_restful_demo    |
| flask_script_demo     |
| flask_sqlalchemy_demo |
| icbc_demo             |
| mysql                 |
| performance_schema    |
| sys                   |
| zlbbs                 |
+-----------------------+
12 rows in set (0.01 sec)

mysql> use zlbbs;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

mysql> show tables;
+-----------------+
| Tables_in_zlbbs |
+-----------------+
| alembic_version |
| cms_role        |
| cms_role_user   |
| cms_user        |
+-----------------+
4 rows in set (0.00 sec
------------------------------------------------------------------------------

(my_env) $python3 manage.py create_role
(my_env) $

------------------=========================

mysql> select * from cms_role
    -> ;
+----+-----------+---------------------------------------------------+---------------------+-------------+
| id | name      | desc                                              | create_time         | permissions |
+----+-----------+---------------------------------------------------+---------------------+-------------+
|  1 | 访问者    | 只能相关数据，不能修改。                          | 2019-12-23 13:03:42 |           1 |
|  2 | 运营      | 管理帖子，管理评论,管理前台用户。                 | 2019-12-23 13:03:42 |          55 |
|  3 | 管理员    | 拥有本系统所有权限。                              | 2019-12-23 13:03:42 |          63 |
|  4 | 开发者    | 开发人员专用角色。                                | 2019-12-23 13:03:42 |         255 |
+----+-----------+---------------------------------------------------+---------------------+-------------+
4 rows in set (0.00 sec)
"""

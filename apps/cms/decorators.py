from flask import session,redirect,url_for,g
from functools import wraps
import config
def login_required(func):

    @wraps(func)
    def inner(*args,**kwargs):
        if config.CMS_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))

    return inner




"""

装饰器的一些说明:
@login_required
def index():
    return 'cms index'

上面三行等价于:
index = login_required(index)  <===>  而login_required函数的返回值为inner这个函数   <===>inner这个函数
联系views这个模块

"""


#这里比较重要,这里是权限的设置(光有前端的权限是不行的，有了这里才会让web开发者无法绕过权限(利用特定的url))
def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args,**kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter

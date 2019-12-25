import os

SECRET_KEY = os.urandom(24)

DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = '123456'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'zlbbs'

# PERMANENT_SESSION_LIFETIME =

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
#
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

#
CMS_USER_ID = 'ASDFASDFSA'

##可以google查qq邮箱发送服务器地址
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USE_SSL : default False
# MAIL_DEBUG : default app.debug
MAIL_USERNAME ="596414331@qq.com"
MAIL_PASSWORD ="yzrrnfejeoebbfaj"
MAIL_DEFAULT_SENDER = "596414331@qq.com"

# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件
# 发送者邮箱的服务器地址
"""
https://service.mail.qq.com/cgi-bin/help?subtype=1&id=20010&no=1000557

"""

"""
容联云相关配置
"""
accountSid="8a216da86f17653b016f3b4046b218ab"
accountToken = "ac156972012a43dab1782f1f89995ac9"
appId ="8a216da86f17653b016f3b40471818b2"


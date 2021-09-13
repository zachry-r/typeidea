# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
from .base import *   #NOQA
import pymysql

DEBUG=True

pymysql.install_as_MySQLdb()
DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.mysql',
        'NAME':'blog',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'localhost',
        'PORT':'3306'
    }
}






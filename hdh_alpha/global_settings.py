"""Settings for hdh_alpha project.

"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!1yv%36_3x61$%fy^1r$gutc@9y1xk!@##wqtu(4go#9est*h5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = []

MIDDLEWARE = []

# Database
DATABASES = {}
"""
DATABASES = {
    'postgresql':{
        'ENGINE': '',
        'NAME': os.path.join(BASE_DIR, '/data/db.postgresql'),
    },
}
"""
# CSV DIRECTORY
CSVDIR = os.path.join(BASE_DIR, '/data/csv/')


LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True


#配置静态文件
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "portal/static/"),
]

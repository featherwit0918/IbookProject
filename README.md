### 项目立项

1. 创建爱书网项目

```python 
django-admin startproject ibook
```

2. 配置开发环境

   因为线上运行的时候, 需要区分开开发环境和生产环境, 所以需要配置开发环境

```python 
# 1. 在项目的路径下新建python包settings
# 2. 将项目中的settings文件复制到settings包中, 并重命名为dev(开发环境)
# 3. 修改manage.py文件, 使其指向dev.py配置文件(manage.py)
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibook.settings.dev')
```

3. 配置文件修改

```python 
# 1. 将创建的apps文件夹添加到环境中(dev.py)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 2. 修改数据库(dev.py)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ibook',
        'HOST': '192.168.38.20',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'mysql'
    }
}
# 3. 添加pymysql引擎(ibook/__init__.py)
import pymysql

pymysql.install_as_MySQLdb()

# 4. 修改语言和时区(dev.py)
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False
```


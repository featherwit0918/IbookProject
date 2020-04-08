### 项目立项

1. 创建爱书网项目

```python 
django-admin startproject ibook
```

2. 配置开发环境

   因为线上运行的时候, 需要区分开发环境和生产环境, 所以需要配置开发环境

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

4. 项目运行

```python
python manage.py runserver 192.168.38.20:8000
```

5. 迁移数据库

```python
1、生成迁移文件
python manage.py makemigrations

2. 执行迁移
python manage.py migrate
```



### 前端准备工作

1. 安装node.js

```python
1. 先下载安装包到 /usr/local路径下
wget https://npm.taobao.org/mirrors/node/v8.0.0/node-v8.0.0-linux-x64.tar.xz

2. 下载完成后解压
tar -xvf  node-v8.0.0-linux-x64.tar.xz

3. 重命名为node
mv node-v8.1.4-linux-x64 node

4. 配置环境变量
vim /etc/profile
在文件的最后添加
#set for nodejs  
export NODE_HOME=/usr/local/node  
export PATH=$NODE_HOME/bin:$PATH

5. 保存退出后执行更新命令
source /etc/profile

6. 如果不生效，重启系统就可以

7. 检测node和npm是否安装成功
node -v
npm -v

8. 切换镜像源
npm config set registry https://registry.npm.taobao.org

9. 查看镜像源是否切换成功
npm config get registry
```

2. 安装Vue

```python
1. 安装vue3
  npm install -g @vue/cli@3.2.1

2. 创建项目
vue create ibooksite

3. 切换到项目目录下, 运行项目
npm run serve
```



### django-cors-headers实现跨域

1. 安装

```python
pip install django-cors-headers
```

2. 注册

```python
INSTALLED_APPS = (
   'corsheaders',
)
```

3. 添加中间件

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]
```

> CorsMiddleware应该放置得尽可能高，特别是在可以产生响应的任何中间件之前， 如Django CommonMiddleware或Whitenoise WhiteNoiseMiddleware。 如果以前没有，则无法将CORS头添加到这些响应中。

4. 配置白名单

```python
#允许携带cookie
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

# 允许的方法
CORS_ALLOW_METHODS = ( 'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT', 'VIEW', )

#允许的请求头
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# 允许的域名
CORS_ORIGIN_WHITELIST = (
    'http://192.168.38.20:8000',
    'http://192.168.0.9:8080'
)

#跨域增加忽略
CORS_ORIGIN_WHITELIST = ( '*')
```


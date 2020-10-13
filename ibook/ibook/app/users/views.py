import re
import random
import json

from django.contrib.auth import authenticate, login, logout
from django.db import DatabaseError
from django.urls import reverse
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
from django_redis import get_redis_connection
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from celery_tasks.sms.tasks import send_sms_code
from .models import Users
from books.models import Book
from ibook.utils.views import LoginRequiredJSONMixin


# Create your views here.
# 短信验证码
class MessageView(View):
    def get(self, request, *args, **kwargs):
        # 获取手机号
        mobile = args[0]

        # 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')

        # 避免频繁发送短信, 使用redis
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return JsonResponse({'code': '1', 'errmsg': '发送短信过于频繁'})

        # 生成随机验证码
        random_code = random.randint(000000, 999999)
        sms_code = '%06d' % random_code

        print(random_code)

        # 保存短信验证码
        redis_conn.setex('sms_%s' % mobile, 60, sms_code)
        # 重新写入send_flag
        redis_conn.setex('send_flag_%s' % mobile, 60, 1)

        # 发送短信验证码
        send_sms_code.delay(mobile, sms_code)

        return JsonResponse({'err_code': '0', 'errmsg': '发送短信验证码成功'})


# 注册页面
class RegisterView(View):

    def get(self, request, *args, **kwargs):
        """ 提供注册页面 """
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        """ 实现用户注册业务逻辑 """

        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code = request.POST.get('sms_code')

        # 校验参数, 前后端建议需要分开, 避免恶意用户越过前端逻辑发请求, 要保证后端的安全, 前后端的校验相同
        # 判断参数是否齐全: all([列表]): 会去校验列表中的元素是否为空, 只要有一个为空, 返回false
        if not all([username, password, password2, mobile, sms_code]):
            return HttpResponseForbidden('缺少必传参数')

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden({'请输入5-20个字符的用户名'})
        # 判断密码是否是8-20个字符
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[34578]\d{9}$', mobile):
            return JsonResponse('请输入正确的手机号')

        # 判断短信验证码是否输入正确
        redis_conn = get_redis_connection('verify_code')
        code_server = redis_conn.get('sms_%s' % mobile)
        if code_server is None:
            return render(request, 'register.html', {'sms_code_errmsg': '短信验证码已失效'})
        if sms_code != code_server.decode():
            return render(request, 'register.html', {'sms_code_errmsg': '输入短信验证码有误'})

        # 保存注册数据, 是注册业务的核心
        try:
            user = Users.objects.create_user(username=username, password=password, phone=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        # 实现状态保持
        login(request, user)

        # 响应结果, 重定向到mine界面
        response = redirect('users:mine')

        # 为了实现在mine页面展示用户名, 我们需要将用户名缓存到cookie中
        # response.set_cookie('key', 'val', 'expiry')
        response.set_cookie('username', username, max_age=3600 * 24 * 15)

        # 响应结果, 重定向到mine界面
        return response


# 手机号重复
class PhoneCountView(View):

    def get(self, request, *args, **kwargs):
        mobile = args[0]

        count = Users.objects.filter(phone=mobile).count()

        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})


# 用户名重复
class UserCountView(View):

    def get(self, request, *args, **kwargs):
        # 从包裹位置参数中获取username
        username = args[0]

        # 实现主体业务逻辑: 使用username查询对应的记录的条数(filter返回的是满足条件的结果集)
        count = Users.objects.filter(username=username).count()

        # 响应结果
        return JsonResponse({'code': 0, 'err_msg': 'OK', 'count': count})


# 用户登录
class LoginView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):

        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        # 校验参数, 前后端建议需要分开, 避免恶意用户越过前端逻辑发请求, 要保证后端的安全, 前后端的校验相同
        # 判断参数是否齐全: all([列表]): 会去校验列表中的元素是否为空, 只要有一个为空, 返回false
        if not all([username, password]):
            return HttpResponseForbidden('缺少必传参数')

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden({'缺少必传参数'})
        # 判断密码是否是8-20个字符
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('密码最少8位, 最长20位')

        # 认证用户: 使用账号查询用户是否存在, 如果用户存在, 再校验密码是否正确
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '账号或密码错误'})

        # 状态保持
        login(request, user)
        # 使用remembered确定状态保持周期(实现记住登录)
        if remembered != 'on':
            # 没有记住登录: 状态保持在浏览器会话结束后销毁
            request.session.set_expiry(0)
        else:
            # 记住登录: 状态保持周期为两周: 默认是两周
            request.session.set_expiry(None)

        # 响应结果
        # 先取出next
        next = request.GET.get('next')
        if next:
            # 重定向到next
            response = redirect(next)
        else:
            # 重定向到mine页面
            response = redirect(reverse("users:mine"))

        # 为了实现在mine页面展示用户名, 我们需要将用户名缓存到cookie中
        # response.set_cookie('key', 'val', 'expiry')
        user_name = user.username
        response.set_cookie('username', user_name, max_age=3600 * 24 * 15)

        return response


# 阅读偏好
class PreferenceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'preference.html')

    def post(self, request, *args, **kwargs):
        user = request.user
        sex = request.POST.get('sex')

        user.preference = sex
        user.save()

        return redirect(reverse('users:mine'))


# 我的页面的实现
class MineView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mine.html')


# 关于我们的页面的实现
class AboutMineView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')


# 版权声明
class CopyrightView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'copyright.html')


# 隐私政策
class PrivacyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'privacy.html')


# 浏览记录
class HistoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'history.html')


# 用户浏览记录
class UserBrowseHistory(LoginRequiredJSONMixin, View):

    def post(self, request, *args, **kwargs):
        """保存用户书籍浏览记录"""
        # 接收参数
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        book_id = json_dict.get('book_id')

        # 校验参数
        try:
            Book.object.get(id=book_id)
        except Book.DoesNotExist:
            return HttpResponseForbidden('参数book_id错误')

        # 保存book_id到redis
        redis_conn = get_redis_connection('history')
        user = request.user
        pl = redis_conn.pipeline()
        # 先去重
        pl.lrem('history_%s' % user.id, 0, book_id)
        # 再保存, 最近浏览的小说在最前面
        pl.lpush('history_%s' % user.id, book_id)
        # 执行
        pl.execute()

        # 响应结果
        return JsonResponse({'code': 0, 'errmsg': "OK"})

    def get(self, request, *args, **kwargs):
        """ 查询用户书籍浏览记录 """

        # 获取登录用户信息
        user = request.user

        # 创建连接到redis对象
        redis_conn = get_redis_connection('history')
        # 取出列表数据
        book_ids = redis_conn.lrange('history_%s' % user.id, 0, -1)

        if not book_ids:
            return JsonResponse({'code': 1, 'errmsg': 'Null', 'books': '暂无浏览记录'})

        # 将模型转字典
        books = []
        for book_id in book_ids:
            book = Book.object.get(id=book_id)
            books.append({
                'id': book.id,
                'book_cover': book.cover,
                'book_name': book.book_name,
                'author_name': book.author_name
            })

        return JsonResponse({'code': 0, 'errmsg': 'OK', 'data': books})

    def delete(self, request, *args, **kwargs):
        # 获取登录用户信息
        user = request.user

        # 创建连接到redis对象
        redis_conn = get_redis_connection('history')

        redis_conn.delete('history_%s' % user.id)

        return JsonResponse({'code': 0, 'errmsg': 'OK', })


class LogoutView(View):
    """ 用户退出登录 """

    def get(self, request):
        # 清除状态保持信息
        logout(request)

        # 退出登录后重定向到首页
        response = redirect(reverse("books:index"))

        # 删除cookies中的用户名
        response.delete_cookie('username')

        # 响应结果
        return response

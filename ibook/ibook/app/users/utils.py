from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import Users


class CustomModelBackend(ModelBackend):  # 继承ModelBackend类，重写authenticate()方法
    """
    自定义用户验证后端：支持用户名或邮箱登录。
    """

    def authenticate(self, request, username=None, password=None, **kwargs):  # 参数username实际是用户输入的登录账号
        try:
            # Q(username=username) | Q(phone=username)，的意思是起到并集作用，只要第一个查到就不会查第二个，第一个没查到就会查第二个
            user = Users.objects.get(Q(username=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

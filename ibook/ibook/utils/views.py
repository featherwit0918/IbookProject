from django.contrib.auth.mixins import LoginRequiredMixin
from django import http


class LoginRequiredJSONMixin(LoginRequiredMixin):
    """ 自定义判断用户是否登录的扩展类: 返回JSON"""

    def handle_no_permission(self):
        """ 直接响应JSON数据 """
        return http.JsonResponse({'code': '1', 'errmsg': '用户未登录'})

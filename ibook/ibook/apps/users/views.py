from django.shortcuts import render
from django.views import View


# Create your views here.
# "我的"模块
class UsersView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mine.html')


# 关于我们
class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')

# 版权声明
class CopyrightView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'copyright.html')

# 隐私政策
class PrivacyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'privacy.html')
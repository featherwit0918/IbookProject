from django.urls import path

from . import views

app_name='users'
urlpatterns = [
    path('mine', views.UsersView.as_view(), name='mine'), # 我的
    path('mine/about', views.AboutView.as_view(), name='about'), # 关于我们
    path('mine/copyright', views.CopyrightView.as_view(), name='copyright'), # 版权声明
    path('mine/privacy', views.PrivacyView.as_view(), name='privacy') # 隐私政策
]
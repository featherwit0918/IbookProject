from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'users'
urlpatterns = [

    path('register/', csrf_exempt(views.RegisterView.as_view()), name="register"),  # 注册
    path('login/', csrf_exempt(views.LoginView.as_view()), name="login"),  # 登录
    path('logout/', csrf_exempt(views.LogoutView.as_view()), name="logout"),  # 登录
    path('preference/', csrf_exempt(views.PreferenceView.as_view()), name="preference"),  # 阅读偏好,
    path('mine/', views.MineView.as_view(), name='mine'),  # 我的页面
    path('mine/about/', views.AboutMineView.as_view(), name="about"),  # 关于我们
    path('mine/about/copyright/', views.CopyrightView.as_view(), name="copyright"),  # 版权声明
    path('mine/about/privacy/', views.PrivacyView.as_view(), name="privacy"),  # 隐私政策
    path('mine/history/', views.HistoryView.as_view(), name="history"),  # 浏览记录

    re_path(r'^usernames/(.*?)/count/$', views.UserCountView.as_view()),  # 用户名重复
    re_path(r'^mobiles/(.*?)/count/$', views.PhoneCountView.as_view()),  # 手机号重复
    re_path(r'^sms_codes/(.*?)/$', views.MessageView.as_view()),  # 短信验证码
    re_path(r'^book_histories/$', csrf_exempt(views.UserBrowseHistory.as_view()))  # 用户浏览记录
]

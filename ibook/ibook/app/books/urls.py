from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'books'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # 首页的实现
    path('category/', views.CategoryView.as_view(), name='category'),  # 分类小说

    re_path(r'^detail/(?P<book_id>\d+)/$', views.DetailView.as_view(), name='detail'),  # 小说详情
    re_path(r'^like/book/(?P<category_id>\d+)/$', views.LikeView.as_view()),  # 热门推荐
    re_path(r'^directory/(?P<book_id>\d+)/(?P<sort>[a-z_-]+)/$', views.DirectorySortView.as_view()),  # 排序目录
    re_path(r'^directory/(?P<book_id>\d+)/$', views.DirectoryView.as_view(), name='directory'),  # 目录
    re_path(r'^content/(?P<book_id>\d+)/(?P<chapter_id>\d+)/$', views.ContentView.as_view(), name='content'),  # 内容
    re_path(r'^category/(?P<gender_id>\d{1})/$', views.CategoryBigView.as_view()),
    re_path(r'^category/detail/(?P<category_id>\d+)/$', views.CategoryDetailView.as_view(), name='category_detail'), # 分类
    re_path(r'^readschedule/(?P<book_id>\d+)/$', csrf_exempt(views.ReadscheduleView.as_view()), name='readschedule'), # 阅读进度
]

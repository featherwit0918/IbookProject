from django.urls import path, re_path

from . import views

app_name = 'bookcase'
urlpatterns = [
    path('bookcase/', views.BookCaseView.as_view(), name="bookcase"),  # 书架
    re_path(r'^addbookcase/(?P<book_id>\d+)/$', views.BookCaseAddBookView.as_view(), name='addbookcase')  # 加入书架
]

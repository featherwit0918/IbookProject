from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django import http

from books.models import Book
from .models import UserOfBookCase, BookCaseOfBook
from bookcase.models import UserOfBookCase, BookCaseOfBook

from ibook.utils.views import LoginRequiredJSONMixin


# Create your views here.
class BookCaseView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # 获取登录用户
        user = request.user

        # 通过登录用户获取书架id
        bookcase = UserOfBookCase.object.filter(user_id=user).first()

        # 如果该用户没有书架, 则为该用户新建书架
        if not bookcase:
            bookcase = UserOfBookCase.object.create(user_id=user)

        # 通过书架id获取书架书籍
        books = BookCaseOfBook.object.filter(bookcase_id=bookcase.id)

        # 如果该用户的书架没有书, 则直接返回
        if not books:
            context = {
                'HaveBook': False,
            }
            return render(request, 'bookcase.html', context=context)

        book_ids = []
        # 通过书架书籍id获取对应的书籍信息
        for book in books:
            book_ids.append(book.book_id.id)

        data = []
        # 遍历book_id获取相应的书籍信息
        for book_id in book_ids:
            book_info = {}
            book_infos = Book.object.get(id=book_id)
            book_info['book_id'] = book_infos.id
            book_info['book_cover'] = book_infos.cover
            book_info['book_name'] = book_infos.book_name

            data.append(book_info)

        context = {
            'HaveBook': True,
            'data': data
        }

        return render(request, 'bookcase.html', context=context)


# 加入书架
class BookCaseAddBookView(LoginRequiredJSONMixin, View):

    def get(self, request, *args, **kwargs):
        # 接收参数
        book_id = kwargs.get('book_id')
        user = request.user

        # 通过book_id获取图书
        book = Book.object.get(id=book_id)

        # 通过登录用户获取书架id
        bookcase = UserOfBookCase.object.filter(user_id=user).first()

        # 如果该用户没有书架, 则为该用户新建书架
        if not bookcase:
            bookcase = UserOfBookCase.object.create(user_id=user)

        # 判断该书籍是否在该用户的书架内
        count = BookCaseOfBook.object.filter(bookcase_id=bookcase.id, book_id=book_id).count()

        # 如果该图书在用户的书架内, 则直接返回
        if count:
            return http.JsonResponse({'code': 1, 'errmsg': '该图书已在书架内'})

        BookCaseOfBook.object.create(bookcase_id=bookcase, book_id=book)

        return http.JsonResponse({'code': 0, 'errmsg': '加入书架成功'})

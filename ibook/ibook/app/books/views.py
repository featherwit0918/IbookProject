import json

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection

from .models import BookCategory, Book, BookChapters, BookChapterContent
from ibook.utils.views import LoginRequiredJSONMixin


# 首页视图
class IndexView(View):
    def get(self, request, *args, **kwargs):

        # 获取所有的小说分类信息
        categorys = BookCategory.object.all()

        # 获取每个分类下的小说
        category_book_info = []
        for category in categorys:
            category_book = {}
            category_id = category.id

            # 通过分类id获取小说信息, 按热度排序, 并且只返回前5个
            books = Book.object.filter(cate_id=category_id).order_by('-heat')[0:5]

            book_infos = []
            for book in books:
                book_info = {}
                book_info['book_id'] = book.id
                book_info['book_name'] = book.book_name
                book_info['cover'] = book.cover
                book_info['author_name'] = book.author_name
                book_info['intro'] = book.intro[3:100] + '...'
                book_info['status'] = book.get_status()

                book_infos.append(book_info)

            category_book['category_id'] = category_id
            category_book['category_name'] = category.cate_name
            category_book['book_infos'] = book_infos

            category_book_info.append(category_book)

        context = {
            'category_book_infos': category_book_info
        }

        return render(request, 'index.html', context=context)


# 分类视图
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'category.html')


# 提供按性别分类的接口
class CategoryBigView(View):

    def get(self, request, *args, **kwargs):
        gender_id = kwargs.get('gender_id')

        # 通过性别获取响应的分类信息
        categorys = BookCategory.object.filter(big_category=gender_id)

        data = []
        for category in categorys:
            category_info = {}
            category_info['category_id'] = category.id
            category_info['category_name'] = category.cate_name

            data.append(category_info)

        return JsonResponse({'code': "OK", 'errmsg': '获取分类成功', 'data': data})


class CategoryDetailView(View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')

        # 通过category_id 查找所有的图书
        books = Book.object.filter(cate_id=category_id)
        category = BookCategory.object.get(id=category_id)

        data = []
        for book in books:
            book_info = {}
            book_info['book_id'] = book.id
            book_info['book_name'] = book.book_name
            book_info['cover'] = book.cover
            book_info['author_name'] = book.author_name
            book_info['intro'] = book.intro[3:100] + '...'
            book_info['status'] = book.get_status()

            data.append(book_info)

        context = {
            'category_name': category.cate_name,
            'data': data,
        }

        return render(request, 'category_detail.html', context=context)


# 小说详情
class DetailView(View):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')

        book_info = Book.object.get(id=book_id)

        data = {}

        # 每次点击, 热度加1
        book_info.heat += 1
        book_info.save()
        data['book_id'] = book_info.id
        data['book_name'] = book_info.book_name
        data['book_cover'] = book_info.cover
        data['author_name'] = book_info.author_name
        data['intro'] = book_info.intro
        data['status'] = book_info.get_status()
        data['collect_count'] = book_info.collect_count
        data['heat'] = book_info.heat
        data['category'] = book_info.cate_id.cate_name
        data['category_id'] = book_info.cate_id.id

        chapters = BookChapters.object.filter(book_id=book_id)

        # 获取最新章节
        last_chapter = chapters.order_by().last()
        data['last_chapter'] = last_chapter.chapter_name

        # 获取第一章节
        first_chapter = chapters.order_by().first()
        data['first_chapter'] = first_chapter.id

        word_count = 0
        for chapter in chapters:
            word_count += chapter.word_count

        word_count = str(word_count // 1000 / 10) + '万字'

        data['word_count'] = word_count
        context = data

        return render(request, 'detail.html', context=context)


# 展示目录页面
class DirectoryView(View):
    def get(self, request, *args, **kwargs):
        # 接收参数: 图书id
        book_id = kwargs.get('book_id')

        # 通过图书id获取图书名称
        book = Book.object.get(id=book_id)
        book_name = book.book_name

        context = {
            'book_id': book_id,
            'book_name': book_name,
        }

        return render(request, 'directory.html', context=context)


# 目录排序
class DirectorySortView(View):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        sort_field = kwargs.get('sort')

        # 通过book_id获取章节信息, 并且按照排序字段排序
        chapters = BookChapters.object.filter(book_id=book_id).order_by(sort_field)

        data = []
        for chapter in chapters:
            chapter_info = {}
            chapter_info['id'] = chapter.id
            chapter_info['name'] = chapter.chapter_name

            data.append(chapter_info)

        return JsonResponse({'code': "OK", 'err_msg': '获取目录成功', 'data': data})


# 小说内容
class ContentView(View):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        chapter_id = kwargs.get('chapter_id')

        chapter_id = int(chapter_id)

        # 通过book_id和chapter_id查询章节内容
        content = BookChapterContent.object.filter(book_id=book_id, chapter_id=chapter_id).first()

        # 通过chapter_id获取章节名称
        chapter_name = BookChapters.object.filter(id=chapter_id, book_id=book_id).first()

        # 通过book_id获取图书名称
        book = Book.object.get(id=book_id)

        # 获取上一章节的id, 如果没有上一章则设置为null
        previous_chapter_id = chapter_id - 1
        previous_count = BookChapterContent.object.filter(book_id=book_id, chapter_id=previous_chapter_id).count()
        if not previous_count:
            previous_chapter_id = chapter_id

        # 获取下一章节的id, 如果没有下一章则设置为null
        next_chapter_id = chapter_id + 1
        next_count = BookChapterContent.object.filter(book_id=book_id, chapter_id=next_chapter_id).count()
        if not next_count:
            next_chapter_id = chapter_id

        context = {
            'book_id': book_id,
            'book_name': book.book_name,
            'chapter_name': chapter_name.chapter_name,
            'content': content.content,
            'previous_chapter_id': previous_chapter_id,
            'next_chapter_id': next_chapter_id,
            'previous_count': previous_count,
            'next_count': next_count,
            'chapter_id': chapter_id
        }

        return render(request, 'content.html', context=context)


# 同类热门推荐
class LikeView(View):

    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')

        books = Book.object.filter(cate_id=category_id).order_by('-heat')[0:4]

        data = []
        for book in books:
            book_info = {}
            book_info['book_id'] = book.id
            book_info['book_cover'] = book.cover
            book_info['book_name'] = book.book_name
            book_info['author_name'] = book.author_name

            data.append(book_info)

        return JsonResponse({'code': 0, 'errmsg': 'OK', 'data': data})


# 阅读进度
class ReadscheduleView(View):
    """ 用户小说阅读进度 """

    def get(self, request, *args, **kwargs):
        user = request.user
        book_id = kwargs.get('book_id')

        # 如果用户未登录, 则直接返回第一章
        if not user.id:
            # 通过book_id获取图书名称
            book = Book.object.get(id=book_id)

            chapter = BookChapters.object.filter(book_id=book).first()

            return redirect(reverse("books:content", kwargs={"book_id": book_id, "chapter_id": chapter.id}))

        # 用户已登录
        # 创建连接到redis对象
        redis_conn = get_redis_connection('progress')

        chapter_id = redis_conn.hget('user_%s' % user.id, 'book_%s' % book_id)

        # 如果没有找到该字段, 那么就将第一个章节id设置进去
        if not chapter_id:
            book = Book.object.get(id=book_id)

            chapter = BookChapters.object.filter(book_id=book).first()

            redis_conn.hset('user_%s' % user.id, 'book_%s' % book_id, chapter.id)

            return redirect(reverse("books:content", kwargs={"book_id": book_id, "chapter_id": chapter.id}))

        chapter_id = chapter_id.decode()
        # 如果找到了该字段, 那么就重定向到该章节的内容
        return redirect(reverse("books:content", kwargs={"book_id": book_id, "chapter_id": chapter_id}))

    def post(self, request, *args, **kwargs):

        # 接收参数
        book_id = kwargs.get('book_id')
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        chapter_id = json_dict.get('chapter_id')
        user = request.user

        # 如果用户未登录, 则直接返回
        if not user.id:
            return JsonResponse({'code': 1, 'errmsg': "用户未登录"})

        # 如果用户已登录, 则将redis中该字段设置为chapter_id
        # 创建连接到redis对象
        redis_conn = get_redis_connection('progress')

        redis_conn.hset('user_%s' % user.id, 'book_%s' % book_id, chapter_id)

        # 响应结果
        return JsonResponse({'code': 0, 'errmsg': "OK"})

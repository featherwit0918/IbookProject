from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'book_name', 'cate_id', 'channel_type', 'author_name', 'is_publish', 'status', 'cover', 'intro', 'showed',
        'collect_count', 'heat')


@admin.register(models.BookBigCategory)
class BookBigCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cate_name', 'showed', 'channel', 'icon')


@admin.register(models.BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cate_name', 'showed', 'icon', 'get_big_category')

    def get_big_category(self, obj):
        return [big.id for big in obj.big_category.all()]


@admin.register(models.BookChapters)
class BookChaptersAdmin(admin.ModelAdmin):
    list_display = ('id', 'chapter_name', 'word_count', 'book_id')


@admin.register(models.BookChapterContent)
class BookChapterContent(admin.ModelAdmin):
    list_display = ('id', 'book_id', 'chapter_id', 'content')

from django.contrib import admin

from . import models


@admin.register(models.UserOfBookCase)
class UserOfBookCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id')


@admin.register(models.BookCaseOfBook)
class BookCaseOfBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'bookcase_id', 'book_id')

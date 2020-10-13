from django.db import models

from users.models import Users
from books.models import Book

# Create your models here.
class UserOfBookCase(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    object = models.Manager()

    class Meta:
        db_table = 'user-bookcase'
        verbose_name = '用户书架'
        verbose_name_plural = verbose_name


class BookCaseOfBook(models.Model):
    bookcase_id = models.ForeignKey('UserOfBookCase', on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    object = models.Manager()

    class Meta:
        db_table = 'bookcase-book'
        verbose_name = '书架书籍'
        verbose_name_plural = verbose_name
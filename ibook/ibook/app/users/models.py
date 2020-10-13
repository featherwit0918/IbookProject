from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Users(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)
    preference = models.IntegerField(default='1') # 1 男 2 女
    headimage = models.CharField(default='', null=True, max_length=128)

    class Meta:
        db_table = 'users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

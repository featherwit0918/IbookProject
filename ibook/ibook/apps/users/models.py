from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=32)
    gender = models.IntegerField(default=1)  #1男 0女
    last_read = models.IntegerField() # 最后阅读的一本书
    last_read_chapter_id = models.IntegerField() # 最后阅读一本书的章节id
    create_time = models.DateTimeField(auto_now_add=True)



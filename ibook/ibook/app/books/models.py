from django.db import models


# Create your models here.
class BaseModel(models.Model):
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Mate:
        abstract = True


class Book(models.Model):
    book_name = models.CharField(max_length=128, verbose_name='书籍名称')
    cate_id = models.ForeignKey('BookCategory', on_delete=models.SET_NULL, null=True, verbose_name='书籍二级分类ID')
    channel_type = models.ForeignKey('BookBigCategory', on_delete=models.SET_NULL, null=True, default=1,
                                     verbose_name='书籍频道')  # 1: 男生 2: 女生 3: 出版 0: 无此属性, 默认为0
    author_name = models.CharField(max_length=32, verbose_name='作者')
    is_publish = models.IntegerField(default=1, verbose_name='是否出版')  # 1: 是 2: 否
    status = models.IntegerField(default=1, verbose_name='连载状态')  # 1: 未完结 2: 已完结
    cover = models.CharField(max_length=128, verbose_name='封面图片')
    intro = models.TextField(verbose_name='简介')
    showed = models.BooleanField(default=0, verbose_name='是否上架')

    collect_count = models.IntegerField(default=0, verbose_name='被收藏的数量')
    heat = models.IntegerField(default=0, verbose_name='热度')

    object = models.Manager()

    class Meta:
        db_table = 'book'
        verbose_name = '书籍基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book_name

    def get_status(self):
        if self.status == 1:
            return '连载'
        else:
            return '已完结'


class BookBigCategory(models.Model):
    cate_name = models.CharField(max_length=64, verbose_name='分类名称')
    showed = models.BooleanField(default=1, verbose_name='展示')
    channel = models.IntegerField(default=1, verbose_name='频道')  # 1: 男生, 2: 女生
    icon = models.CharField(max_length=100, verbose_name='图标')

    object = models.Manager()

    class Meta:
        db_table = 'book_big_category'
        verbose_name = '书籍一级分类信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cate_name


class BookCategory(models.Model):
    cate_name = models.CharField(max_length=64, verbose_name='分类名称')
    showed = models.BooleanField(default='1', verbose_name='展示')
    icon = models.CharField(max_length=100, verbose_name='图标')
    big_category = models.ManyToManyField('BookBigCategory', verbose_name='大分类')

    object = models.Manager()

    class Meta:
        db_table = 'book_category'
        verbose_name = '书籍分类信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cate_name


class BookChapters(models.Model):
    chapter_name = models.CharField(max_length=64, verbose_name='章节名称')
    word_count = models.IntegerField(verbose_name='字数')
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name='书籍ID')

    object = models.Manager()

    class Meta:
        db_table = 'book_chapters'
        verbose_name = '书籍章节信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.chapter_name


class BookChapterContent(models.Model):
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name='书籍ID')
    chapter_id = models.OneToOneField('BookChapters', on_delete=models.CASCADE, verbose_name='章节ID')
    content = models.TextField(verbose_name='章节内容')

    object = models.Manager()

    class Meta:
        db_table = 'book_chapter_content'
        verbose_name = '书籍章节内容信息'
        verbose_name_plural = verbose_name

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Mate:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Mate:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):

    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )

    def __str__(self):
        return self.title

    # 获取文章绝对地址
    def get_absolute_url(self):
        return reverse('blog_main:post_detail', kwargs={'pk': self.pk})

    # 文章状态
    status = models.CharField(verbose_name='状态', max_length=1, choices=STATUS_CHOICES, default='p')

    # 文章标题
    title = models.CharField(verbose_name='标题', max_length=70)

    # 文章正文，我们使用了 TextField。
    body = models.TextField(verbose_name='正文', blank=True, null=True)

    # 文章的创建时间
    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)

    # 文章最后一次修改时间
    modified_time = models.DateTimeField(verbose_name='修改时间', default=timezone.now)

    # 文章浏览量
    views = models.PositiveIntegerField(verbose_name='文章浏览量', default=0)

    # 文章摘要
    excerpt = models.CharField(verbose_name='文章摘要', max_length=200, blank=True)

    # 文章分类
    category = models.ForeignKey(Category, verbose_name='文章分类', on_delete=models.CASCADE)

    # 文章标签
    tags = models.ManyToManyField(Tag, verbose_name='文章标签', blank=True)

    # 文章作者
    author = models.ForeignKey(User, verbose_name='文章作者', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        super().save(*args, **kwargs)

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)

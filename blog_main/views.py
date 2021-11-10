from django.shortcuts import render, get_object_or_404
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.utils import timezone
from .models import Post
import markdown
import re

# Create your views here.


def index_nologin(request):
    # 正序获取所有文章
    post_list = Post.objects.all().order_by('created_time')
    return render(request, 'index.html', context={

        # 替换文字
        'nologin': 'Guest',
        'login': '登录',
        'register': '注册',

        # 插入文章列表
        'post_list': post_list
    })


def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])

    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    post.toc = md.toc

    return render(request, 'post_detail.html', context={
        # 替换文字
        'nologin': 'Guest',
        'login': '登录',
        'register': '注册',

        # 插入文章
        'post': post
    })

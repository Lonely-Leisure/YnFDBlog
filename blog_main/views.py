from django.shortcuts import render, get_object_or_404
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.utils import timezone
from .models import Post, Category, Tag
import markdown
import re

# Create your views here.


# 未登录博客主页
def index(request):
    # 正序获取所有文章
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/main/index.html', context={

        # 替换文字
        'nologin': 'Guest',
        'login': '登录',
        'admin': '博客后台',

        # 插入文章列表
        'post_list': post_list
    })


# 文章详情页
def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',

        # 美化标题锚点 url
        TocExtension(slugify=slugify),
    ])

    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    post.toc = md.toc

    return render(request, 'blog/main/post_detail.html', context={
        # 替换文字
        'nologin': 'Guest',
        'login': '登录',
        'register': '注册',

        # 插入文章
        'post': post
    })


# 归档页
def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')

    return render(request, 'blog/main/index.html', context={
        'post_list': post_list
    })


# 分类页
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')

    return render(request, 'blog/main/index.html', context={
        'post_list': post_list
    })


# 标签云
def tags(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')

    return render(request, 'blog/main/index.html', context={
        'post_list': post_list
    })

from django import template
from ..models import Post, Category, Tag
register = template.Library()


# 最新文章模板标签
@register.inclusion_tag('blog/extra/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }


# 归档模板标签
@register.inclusion_tag('blog/extra/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }


# 分类模板标签
@register.inclusion_tag('blog/extra/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }


# 标签云模板标签
@register.inclusion_tag('blog/extra/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }

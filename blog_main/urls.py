from django.urls import path
from . import views

app_name = 'blog_main'
urlpatterns = [
    path('', views.index, name='index'),                             # 未登录博客主页
    path('posts/<int:pk>/', views.post_details, name='post_detail'),         # 文章详情页
    path('avchives/<int:year>/<int:month>', views.archive, name='archive'),  # 归档页
    path('categories/<int:pk>/', views.category, name='category'),           # 分类页
    path('tags/<int:pk>/', views.tags, name='tag'),                           # 标签云
]

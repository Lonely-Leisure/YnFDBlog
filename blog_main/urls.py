from django.urls import path
from . import views

app_name = 'blog_main'
urlpatterns = [
    path('', views.index_nologin, name='index'),                         # 博客主页
    path('posts/<int:pk>/', views.post_details, name='post_detail'),     # 文章详情页
]

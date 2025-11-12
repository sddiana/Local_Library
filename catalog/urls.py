from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='books'),
    re_path(r'^book/(?P<pk>\d+)/$', views.book_detail, name='book-detail'),
    path('authors/', views.author_list, name='authors'),
    path('author/<int:pk>/', views.author_detail, name='author-detail'),
]

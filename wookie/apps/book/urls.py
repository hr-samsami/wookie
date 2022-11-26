from django.urls import path
from . import views
from .views import BookListView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('mylist/', views.my_books, name='book-mylist'),
    path('detail/<int:pk>/', views.book_detail, name='book-detail'),
    path('create/', views.book_create, name='book-create'),
    path('update/<int:pk>/', views.book_update, name='book-update'),
    path('delete/<int:pk>/', views.book_delete, name='book-delete'),
    path('unpublish/<int:pk>/', views.book_unpublish, name='book-unpublish')
]

from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('books', views.books),
    path('update/<int:id>', views.update),
    path('books/<int:id>', views.books_all),
    path('logout', views.logout),
    path('check_registration', views.check_registration),
    path('check_login', views.check_login),
    path('check_book', views.check_book),
    path('unfavorite/<int:id>', views.unfavorite),
    path('add_favorite_book/<int:id>', views.add_favorite_book),
    path('was_favorited_check/<int:id>', views.was_favorited_check),
    path('delete/<int:id>', views.delete),
]
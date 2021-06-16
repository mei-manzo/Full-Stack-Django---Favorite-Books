from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add),
    path('update', views.update),
    path('all', views.all),
    path('logout', views.logout),
    path('check_registration', views.check_registration),
    path('check_login', views.check_login),
    path('check_book', views.check_book),
]
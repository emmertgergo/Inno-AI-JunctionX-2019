from django.urls import path
from . import views

app_name = 'userhandler_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('accounts/login/', views.user_login, name='user_login'),
    path('accounts/logout/', views.user_logout, name='logout'),

]
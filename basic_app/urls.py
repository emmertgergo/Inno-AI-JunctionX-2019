from django.urls import path
from basic_app import views


app_name = 'basic_app'

urlpatterns = [
    # HOMEPAGE
    path('index/', views.index, name="index"),
    path('login/', views.login, name="login"),
]
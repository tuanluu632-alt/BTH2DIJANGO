from django.urls import path
from .views import hello_world, login

urlpatterns = [
    path("", hello_world, name="hello"),
    path("login/", login, name="login"),
]
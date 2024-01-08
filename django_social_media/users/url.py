from django.urls import path
from users.views import users

urlpatterns = [
    path('user', users.user_login),
    path('signup',users.signup)
]
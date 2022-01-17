
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path('edit', views.edit, name="edit"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("user/<str:username>/", views.index, name="userpage")
]


from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("like/<int:postId>",views.like, name="like"),
    path("edit/<int:postId>",views.edit, name="edit"),
    path("follow/<int:userId>", views.handle_follow, name = "follow"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]


from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/create", views.create_post, name="create_post"),
    path("post/<int:post_id>", views.update_post, name="update_post"),
    path("like/<int:post_id>", views.like_post, name="like_post"),
    path("feed/<int:page_id>", views.index, name="feed"),
    path("follow/<int:profile_id>", views.follow, name="follow"),
    path("feed/<int:page_id>/<str:filter_by>", views.index, name="following"),
    path("profile", views.profile, name="profile"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("profile/<int:profile_id>/<int:page_id>", views.profile, name="profile_feed")
]

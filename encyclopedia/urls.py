from django.urls import path

from . import views
from . import util

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.title, name="title"),
    path("wiki/", views.search, name="search"),
    path("createNewPage", views.createNewPage, name="createNewPage"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("random", views.Random, name="random")
]

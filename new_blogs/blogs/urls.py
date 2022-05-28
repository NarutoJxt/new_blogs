#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from blogs.viiews import BlogCategoryViewSet,BlogViewSet,upload_file,IndexViewSet,PersonView

router = DefaultRouter()
router.register("category",BlogCategoryViewSet)
router.register("article",BlogViewSet)
router.register("index",IndexViewSet)
app_name = "blogs"
urlpatterns = [
    path("",include(router.urls)),
    path("upload_file/",upload_file),
    path("person/articles/",PersonView.as_view(),name="person_articles"),
]
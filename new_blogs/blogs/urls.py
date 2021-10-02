#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from blogs.viiews import BlogCategoryViewSet,BlogViewSet

router = DefaultRouter()
router.register("category",BlogCategoryViewSet)
router.register("article",BlogViewSet)
app_name = "blogs"
urlpatterns = [
    path("",include(router.urls))
]
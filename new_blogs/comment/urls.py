#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from comment.views import CommentModelViewSet

app_name = "comment"
router = DefaultRouter()
router.register("",CommentModelViewSet)
urlpatterns = [
    path("",include(router.urls))
]

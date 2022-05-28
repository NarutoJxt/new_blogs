#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from collection.views import CollectionViewSet

app_name = "collection"
router = DefaultRouter()
router.register("",CollectionViewSet)
urlpatterns = [
    path("", include(router.urls))
]
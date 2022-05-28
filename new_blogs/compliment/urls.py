from django.urls import include, path
from rest_framework.routers import DefaultRouter

from compliment.views import ComplimentViewSet

from compliment.views import ComplientForCommentViewSet

app_name = "compliment"
router = DefaultRouter()
router.register("article",ComplimentViewSet)
router.register("comment",ComplientForCommentViewSet)
urlpatterns = [
    path("",include(router.urls))
]
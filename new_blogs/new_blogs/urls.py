"""new_blogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from account.views import UserViewSet
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    re_path('admin/?', admin.site.urls),
    path("api/",include(router.urls)),
    re_path(r"^login/$",obtain_jwt_token),
    path("refresh_token/",refresh_jwt_token),
    path("blog/",include("blogs.urls")),
    # re_path(r'^auth/', include('rest_framework_social_oauth2.urls')),
    path('', include('social_django.urls', namespace='social')),
    path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]

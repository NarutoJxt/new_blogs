from django.contrib.auth import logout
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from account.models import BlogUser
from account.serializers import UserRegisterSerializer

from account.viewset import MyViewSet


class UserViewSet(MyViewSet):
    queryset = BlogUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        # 在此处生成 token
        res_dict = serializer.data
        # res_dict 还可以根据需要添加其它内容
        headers = self.get_success_headers(serializer.data)
        return Response(res_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    @action(methods=["get"],detail=False,url_path="logout/?")
    def logout(self,request,pk=None):
        logout(request)
        return Response(
            True
        )



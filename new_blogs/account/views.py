import json
import random

from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from account.models import BlogUser,Attention
from account.serializers import UserRegisterSerializer,AttentionSerializer

from account.viewset import MyViewSet
from rest_framework_jwt.views import ObtainJSONWebToken

from account.renders import UserInfoRender

from blogs.models import Article

from account.serializers import UserInfoSerializer


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

class AttentionViewSet(ModelViewSet):
    queryset = Attention.objects.all()
    serializer_class = AttentionSerializer

    def create(self, request, *args, **kwargs):
        type = request.data.get("type")
        if type is not None:
            del request.data["type"]
        if type:
            request.data["user"] = request.user.id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            user = request.user.id
            follower = request.data.get("follower")
            instance = Attention.objects.get(user=user,follower=follower)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"],detail=False,url_path="index/?")
    def get_index_attention(self, request, *args, **kwargs):
        attention_users = Attention.objects.filter(user=request.user.id)
        attention_users = [user.follower.id for user in attention_users]
        users = BlogUser.objects.exclude(Q(pk__in=attention_users) | Q(pk=request.user.id))
        users = set(users)
        length = len(users)
        if length > 5:
            recommended_user_list = random.sample(users, 5)
        elif length != 0:
            recommended_user_list = random.sample(users, length)
        else:
            recommended_user_list = []
        recommended_users = []
        for user in recommended_user_list:
            avatar = user.avatar
            user_id = user.id
            username = user.username
            article_count_list = [category.article_set.count() for category in user.author.all()]
            article_count = sum(article_count_list)
            attention_count = user.user.count()
            temp = {
                "avatar":avatar.url,
                "user_id":user_id,
                "username":username,
                "article_count":article_count,
                "attention_count":attention_count,
                "isConcerned":False
            }
            recommended_users.append(temp)
        data = {
            "recommendedUsers":recommended_users
        }
        data = json.dumps(data)
        return Response(data)

    def list(self,request, *args, **kwargs):
        user = request.user
        page_number = request.GET.get("page",1)
        page_number = int(page_number) if page_number is not None else 1
        if user:
            data = []
            attention = user.user.all()
            followers = map(lambda x:x.follower.id,attention)
            articles = Article.objects.all().filter(category__author__in=followers)
            followers = [
                {
                    "username":att.follower.username,
                    "id":att.follower.id,
                    "pic":str(att.follower.avatar)
                } for att in attention
            ]
            for obj in articles:
                username = obj.category.author.username
                body = obj.body
                title = obj.title
                comment_count = obj.comment_set.count()
                compliment_count = obj.compliment_set.count()
                temp = {
                    "title": title,
                    "id": obj.id,
                    "username": username,
                    "body": body,
                    "comment_count": comment_count,
                    "compliment_count": compliment_count
                }
                data.append(temp)
            page = Paginator(data, 5)
            p = page.page(page_number)
            followers = json.dumps(followers)
            res = {
                "data": p.object_list,
                "hasNext": p.has_next(),
                "followers":followers
            }
            data = json.dumps(res)
            return Response(data)
        else:
            data = {
                "error":"服务器发生错误"
            }
            data = json.dumps(data)
            return Response(data,status=500)


class ObtainJSONWebTokenUser(ObtainJSONWebToken):
    renderer_classes = [UserInfoRender]

obtain_jwt_token = ObtainJSONWebTokenUser.as_view()
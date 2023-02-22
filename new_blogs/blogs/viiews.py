import datetime
import json
import random
from functools import reduce

import pytz
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from blogs.models import ArticleCategory,Article
from blogs.serailizer import ArticleCategorySerializer,ArticleSerializer,ArticleIndexSerializer,IndexSerializer

from new_blogs import settings
from account.models import BlogUser,Attention

from comment.serializers import CommentSerializer

from account.serializers import UserForArticleDetailSerializer

from compliment.models import Compliment

from collection.models import Collection

from comment.models import Comment
from account.serializers import UserForArticleDetailSerializer
from blogs.serailizer import ArticleCategoryIndexSerializer


class BlogCategoryViewSet(ModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer

    def create(self, request, *args, **kwargs):
        author = request.user
        request.data["author"] = author.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=["GET"],detail=False,url_path="blogs/?")
    def get_category_and_blogs(self,request,*args,**kwargs):
        user = request.user
        categories = ArticleCategory.objects.filter(author=user)
        res = {}
        for category in categories:
            res[category.id] = ArticleSerializer(category.article_set.all(),many=True).data
        res = json.dumps(res)
        return JsonResponse(res,safe=False)

    def get_queryset(self):
        return ArticleCategory.objects.filter(author=self.request.user)

class BlogBase:

    @staticmethod
    def sort_article_by_comment(article):
        comment = article.get_latest_comment()
        utc = pytz.timezone('US/Pacific')
        return comment.pub_time if comment else datetime.datetime(1970,1,1,0,0,0,tzinfo=utc)

    def get_extra_article_info_by_user(self,user,condition=None):
        #  0：最新发布 1：热门 2：最新评论
        articles = Article.objects.all().filter(category__author=user.id)
        if condition == 0:
            articles = articles.order_by("-pub_time")
        elif condition == 1:
            articles = articles.order_by("-views")
        elif condition == 2:
            articles = list(sorted(articles,key=self.sort_article_by_comment))

        article_list = []
        for article in articles:
            compliment_count = article.compliment_set.count()
            comment_count = article.comment_set.count()
            collection_count = article.article.count()
            item = {
                "title": article.title,
                "body": article.body,
                "pub_time": article.pub_time.strftime("%Y-%m-%d %H-%M-%S"),
                "compliment_count": compliment_count,
                "comment_count": comment_count,
                "views": article.views,
                "collection_count": collection_count,
                "id":article.id
            }
            article_list.append(item)
        return article_list

class BlogViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def parse_comment_dict(self,comment_dict):
        for key in comment_dict.keys():
            length = len(comment_dict[key])
            for index in range(length):
                comment = CommentSerializer(comment_dict[key][index]).data
                comment["showComment"] = False
                comment_dict[key][index] = comment
        return comment_dict

    def list(self, request, *args, **kwargs):
        id = request.GET.get("id")
        article = Article.objects.get(pk=id)
        article.views += 1
        article.save()
        author = article.category.author
        concerned_count = Attention.objects.filter(user=request.user,follower=author).count()
        is_concerned = False if not concerned_count else True
        category = article.category.category
        try:
            is_complimented = Compliment.objects.get(article=article.id,blog_user=request.user.id)
        except Exception as e:
            is_complimented = 2
        else:
            is_complimented = is_complimented.praise_type
        is_collected = Collection.objects.filter(collected_article=article.id,blog_user=request.user.id).count()
        is_collected = True if is_collected else False
        author_articles = Article.objects.filter(category=article.category)[:3]
        compliment_count = article.compliment_set.filter(praise_type=1).count()
        author = UserForArticleDetailSerializer(author).data
        comments,header = article.get_comment_list()
        comments = self.parse_comment_dict(comments)
        article = self.serializer_class(article).data
        author_articles = self.serializer_class(author_articles,many=True).data
        header = CommentSerializer(header,many=True).data
        data = {
            "article":article,
            "comments":comments,
            "header":header,
            "author":author,
            "complimentCount":compliment_count,
            "category":category,
            "authorArticle":author_articles,
            "isConcerned":is_concerned,
            "isComplimented":is_complimented,
            "isCollected":is_collected,
        }
        data = json.dumps(data)
        return Response(data)


class IndexViewSet(ReadOnlyModelViewSet):
    serializer_class = IndexSerializer
    queryset = Article.objects.all()
    page_size = 10

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # queryset = queryset.filter(status='d')
        page_number = request.GET.get("page",1)
        data = []
        for obj in queryset:
            username = obj.category.author.username
            body = obj.body
            title = obj.title
            comment_count = obj.comment_set.count()
            compliment_count = obj.compliment_set.count()
            temp = {
                "title":title,
                "id":obj.id,
                "username":username,
                "body":body,
                "comment_count":comment_count,
                "compliment_count":compliment_count
            }
            data.append(temp)
        page = Paginator(data,5)
        p = page.page(page_number)
        res = {
            "data":p.object_list,
            "hasNext":p.has_next(),
        }
        data = json.dumps(res)
        return Response(data)

def handle_uploaded_file(f,file_suffix):
    with open(file_suffix, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@api_view(["POST"])
def upload_file(request,*args,**kwargs):
    f = request.FILES.get('image')
    if f:
        file_prefix,file_suffix = f.name.split(".")
        rand = random.randint(0,10000000000)
        image_path = "/blog_image/"+file_prefix+str(rand)+"."+file_suffix
        image_path = image_path.replace(" ","")
        filename = settings.MEDIA_ROOT + image_path
        try:
            handle_uploaded_file(f,filename)
        except Exception as e:
            return Response(e,status=500)
        else:
            url = "http://127.0.0.1:8000"+settings.MEDIA_URL+ image_path
            data = {
                "url":url
            }
            return Response(data)
    else:
        return Response(True)

class PersonView(ListAPIView,BlogBase):

    def get_serializer_class(self,type):
        pass

    def list(self, request, *args, **kwargs):
        author_id = request.GET.get("author_id")
        condition = request.GET.get("condition",None)
        attention_count = 0
        follower_count = 0
        if author_id:
            try:
                author = BlogUser.objects.get(pk=author_id)
            except Exception as e:
                attention_count = 0
                follower_count = 0
            else:
                attention_count = author.user.count()
                follower_count = author.follower.count()
        categories = author.author.all()
        article_list = self.get_extra_article_info_by_user(author,condition=condition)
        collection_count = author.collection.all().count()
        categories = ArticleCategoryIndexSerializer(categories,many=True).data
        concerned_count = Attention.objects.filter(user=request.user,follower=author).count()
        author = UserForArticleDetailSerializer(author).data
        is_concerned = False if not concerned_count else True
        data = {
            "attentionCount":attention_count,
            "followerCount":follower_count,
            "articles":article_list,
            "collectionCount":collection_count,
            "categories":categories,
            "author":author,
            "isConcerned":is_concerned
        }
        data = json.dumps(data)
        return Response(data=data,status=status.HTTP_200_OK)

class BlogSetByAuthorView(ReadOnlyModelViewSet,BlogBase):
    queryset = BlogUser.objects.all()

    def list(self, request, *args, **kwargs):
        author_id = request.GET.get("id")
        condition = request.GET.get("condition",None)
        condition = int(condition) if condition is not None else None
        author = self.queryset.get(pk=author_id)
        follower_count = author.follower.count()
        article_list = self.get_extra_article_info_by_user(author,condition=condition)
        data = {
            "author":UserForArticleDetailSerializer(author).data,
            "follower_count":follower_count,
            "articles":article_list
        }
        data = json.dumps(data)
        return Response(
            data=data
        )
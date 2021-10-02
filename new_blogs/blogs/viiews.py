import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blogs.models import ArticleCategory,Article
from blogs.serailizer import ArticleCategorySerializer,ArticleSerializer



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

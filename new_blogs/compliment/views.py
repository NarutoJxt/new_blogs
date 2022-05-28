from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from compliment.models import Compliment,ComplimentForComment

from compliment.serializers import ComplimentSerializer

from compliment.serializers import ComplimentForCommentSerializer
import compliment


class ComplimentViewSet(ModelViewSet):
    serializer_class = ComplimentSerializer
    queryset = Compliment.objects.all()
    key_field = "article"

    def create(self, request, *args, **kwargs):
        request.data["blog_user"] = request.user.id
        article = request.data.get("article")
        try:
            obj = self.queryset.get(blog_user=request.user.id,article=article)
        except compliment.models.Compliment.DoesNotExist as e:
            return super(ComplimentViewSet, self).create(request,*args,**kwargs)
        else:
            praise_type = request.data.get("praise_type")
            obj.praise_type = praise_type
            obj.save()
            serializer = self.get_serializer(data=obj)
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(methods=["DELETE"],detail=False,url_path="cancel/?")
    def cancel_compliment(self,request,*args,**kwargs):
        article = request.GET.get(self.key_field)
        if article:
            obj = self.queryset.get(blog_user=request.user,article=article)
            try:
               obj.delete()
            except Exception as e:
               return Response(data=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
               return Response(data=True)
        else:
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)

class ComplientForCommentViewSet(ModelViewSet):
    queryset = ComplimentForComment.objects.all()
    serializer_class = ComplimentForCommentSerializer

    def create(self, request, *args, **kwargs):
        blog_user = self.request.user.id
        request.data["blog_user"] = blog_user
        return super(ComplientForCommentViewSet, self).create(request,*args,**kwargs)

    @action(methods=["DELETE"],detail=False,url_path="cancel/?")
    def cancel_compliment(self,request,*args,**kwargs):
        comment = request.GET.get("comment")
        if comment:
            obj = self.queryset.get(blog_user=request.user, comment=comment)
            try:
               obj.delete()
            except Exception as e:
               return Response(data=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
               return Response(data=True)
        else:
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)





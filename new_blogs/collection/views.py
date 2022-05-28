from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from collection.serializers import CollectionSerializer

from collection.models import Collection


class CollectionViewSet(ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    def create(self, request, *args, **kwargs):
        request.data["blog_user"] = request.user.id
        return super(CollectionViewSet, self).create(request,*args,**kwargs)

    @action(methods=["DELETE"],detail=False,url_path="cancel/?")
    def cancel_collection(self,request,*args,**kwargs):
        article = request.GET.get("collected_article")
        if article:
            obj = self.queryset.get(blog_user=request.user,collected_article=article)
            try:
               obj.delete()
            except Exception as e:
               return Response(data=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
               return Response(data=True)
        else:
            return Response(data=False, status=status.HTTP_400_BAD_REQUEST)

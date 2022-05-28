from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from comment.models import Comment

from comment.serializers import CommentAuthorSerializer


class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentAuthorSerializer

    def create(self, request, *args, **kwargs):
        parent_comment = request.data.get("parent_comment",None)
        request.data["parent_comment"] = parent_comment
        request.data["author"] = request.user.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

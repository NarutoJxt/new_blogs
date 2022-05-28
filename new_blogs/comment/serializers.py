from rest_framework import serializers

from comment.models import Comment

from account.serializers import UserForArticleDetailSerializer

from compliment.serializers import ComplimentForCommentSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserForArticleDetailSerializer()
    compliment_comments = ComplimentForCommentSerializer(many=True)
    class Meta:
        fields = ["id","body","author","parent_comment","article","pub_time","compliment_comments"]
        model = Comment

class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id","body","author","parent_comment","article"]
        model = Comment

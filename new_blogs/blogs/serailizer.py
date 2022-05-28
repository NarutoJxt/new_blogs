from django.core import serializers


from rest_framework import serializers

from blogs.models import Article,ArticleCategory

from account.serializers import UserInfoSerializer


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["category","pk","author"]
        model = ArticleCategory
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id","title","body","status","views","category","pub_time"]
        model = Article

# indexView 依赖的序列化器
class ArticleCategoryIndexSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)
    class Meta:
        fields = ["category","pk","author"]
        model = ArticleCategory

class ArticleIndexSerializer(serializers.ModelSerializer):
    category = ArticleCategoryIndexSerializer(read_only=True)
    class Meta:
        fields = ["id","title","body","status","views","category"]
        model = Article

class IndexSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False)
    title = serializers.CharField(allow_blank=False)
    body = serializers.CharField(allow_blank=False)
    comment_count = serializers.IntegerField(allow_null=False)
    compliment_count = serializers.IntegerField(allow_null=False)

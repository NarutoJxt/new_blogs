from django.core import serializers


from rest_framework import serializers

from blogs.models import Article,ArticleCategory


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id","title","body","status","views","thumb_up","category"]
        model = Article
class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["category","pk","author"]
        model = ArticleCategory
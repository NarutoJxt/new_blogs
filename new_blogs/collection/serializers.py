from rest_framework.serializers import ModelSerializer

from collection.models import Collection


class CollectionSerializer(ModelSerializer):
    class Meta:
        fields = ["blog_user","collected_article"]
        model = Collection
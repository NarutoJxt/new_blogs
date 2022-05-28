from rest_framework.serializers import ModelSerializer

from compliment.models import Compliment

from compliment.models import ComplimentForComment


class ComplimentSerializer(ModelSerializer):
    class Meta:
        model = Compliment
        fields = ["blog_user","article","praise_type"]

class ComplimentForCommentSerializer(ModelSerializer):
    class Meta:
        model = ComplimentForComment
        fields = ["blog_user","comment"]

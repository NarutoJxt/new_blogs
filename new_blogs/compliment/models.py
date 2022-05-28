from django.db import models

# Create your models here.
from django.utils.timezone import now

from account.models import BlogUser
from blogs.models import Article

from comment.models import Comment


class Compliment(models.Model):
    praise_type_dict = [
        (1,"赞"),
        (0,"踩")
    ]
    article = models.ForeignKey(Article,verbose_name="被点赞的文章",on_delete=models.CASCADE)
    blog_user = models.ForeignKey(BlogUser,verbose_name="点赞者",on_delete=models.DO_NOTHING)
    praise_time = models.DateTimeField(verbose_name="点赞时间",auto_now=now)
    praise_type = models.IntegerField(verbose_name="赞的类型",choices=praise_type_dict,default=1)

class ComplimentForComment(models.Model):
    comment = models.ForeignKey(Comment,verbose_name="被点赞的文章",on_delete=models.CASCADE,related_name="compliment_comments")
    blog_user = models.ForeignKey(BlogUser,verbose_name="点赞者",on_delete=models.DO_NOTHING)
    praise_time = models.DateTimeField(verbose_name="点赞时间",auto_now=now)
    class Meta:
        db_table = "compliment_for_comment"

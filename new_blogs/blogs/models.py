
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.timezone import now

from account.models import BlogUser



class ArticleCategory(models.Model):
    category = models.CharField(max_length=255, blank=False, null=False, verbose_name="类型")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    author = models.ForeignKey(to=BlogUser,on_delete=models.CASCADE,related_name="author")

    def get_article_list(self):
        return self.Article_set.all()

    class Meta:
        verbose_name = "文集"

class Article(models.Model):
    STATUS = {
        ("d","草稿"),
        ("e","发表")
    }
    title = models.CharField(max_length=128,help_text="请输入标题，不超过128个字符",
                        unique=False)
    body = models.TextField(verbose_name="内容",null=True,blank=True)
    pub_time = models.DateTimeField("发表时间",default=now)
    status = models.CharField("文章状态",choices=STATUS,default="a",max_length=1)
    views = models.PositiveIntegerField(verbose_name="浏览量",default=0)
    category = models.ForeignKey(ArticleCategory,on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse(
            "blog:article_detail",
            kwargs={
                'article_id': self.id,
                'year': self.pub_time.year,
                'month': self.pub_time.month,
                'day': self.pub_time.day
            }
        )
    def viewed(self):
        self.views += 1
        self.save(update_fields=["views"])

    def next_article(self):
        return Article.objects.filter(id__gt=self.id).order_by("id").first()

    def pre_artocle(self):
        return Article.objects.filter(id__lt=self.id).order_by("id").last()

    # 最新评论
    def get_latest_comment(self):
        return self.comment_set.order_by("-pub_time").first()

    def get_comment_list(self):
        comment_list = self.comment_set.filter(article=self)
        comments_dict = {}
        header = []
        for comment in comment_list:
            comments_dict[comment.id] = []
            if comment.parent_comment is None:
                header.append(comment)
            else:
                comments_dict[comment.parent_comment.id].append(comment)
        return comments_dict,header

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ["-views","-pub_time"]
        get_latest_by = "id"

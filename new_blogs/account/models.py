from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# Create your models here.
from django.utils.timezone import now



class BlogUser(AbstractUser):
    TYPE = [
        ("1","github"),
        ("2","google"),
        ("3","self")
    ]
    GENDER = {
        ("0","男"),
        ("1","女"),
        ("2","保密")
    }
    RECEIVE_AREA = [
        (False,"接收所有人的笔信"),
        (True
         ,"只接收我关注的人")
    ]
    IS_ACCESS = [
        (True,"是"),
        (False,"否")
    ]
    gender = models.CharField(
        default="1",verbose_name="性别",choices=GENDER,max_length=6
    )
    avatar = models.ImageField(
        upload_to="static/image/head/",verbose_name="头像",default=r"\image\avatar.jpeg",max_length=128
    )
    signature = models.TextField(
        verbose_name="签名",
        max_length=128,default="",null=True,blank=True
    )
    user_type = models.CharField("用户来源",max_length=16,choices=TYPE,default="3")
    birth_date = models.DateField("出生日期",default=now)
    person_instruction = models.TextField("个人说明",default="",null=True,blank=True)
    is_access = models.BooleanField("允许访问",default=True,choices=IS_ACCESS)
    receiver_area = models.BooleanField("接受笔信的范围",default="0",choices=RECEIVE_AREA,max_length=20)
    email = models.EmailField("邮箱",unique=True,blank=False,null=False)
    class Meta:
        db_table = "用户"
        verbose_name = "用户"


class Attention(models.Model):
    user = models.ForeignKey(BlogUser,verbose_name="用户",on_delete=models.CASCADE,related_name="user")
    follower = models.ForeignKey(BlogUser,verbose_name="被关注者",on_delete=models.CASCADE,related_name="follower")
    class Meta:
        db_table = "attention"
        verbose_name = "关注"
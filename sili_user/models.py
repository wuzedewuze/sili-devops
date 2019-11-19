from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField("姓名", max_length=32, null=True, help_text="姓名")
    phone = models.CharField("电话", max_length=11, null=True, help_text="手机号")
    gitlab_token = models.CharField("gitlab秘钥", max_length=200, null=True, help_text="gitlab秘钥")
    k8s_token = models.CharField("k8s秘钥", max_length=200, null=True, help_text="k8s秘钥")
    other = models.CharField("备用字段", max_length=200, null=True, help_text="字段")
    class Meta:
        verbose_name = "用户"
        ordering = ["id"]

    def __str__(self):
        return self.username




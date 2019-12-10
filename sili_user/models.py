from django.db import models
from django.contrib.auth.models import AbstractUser
from functools import lru_cache
from django.conf import settings
import time


class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="权限名")
    alias = models.CharField(max_length=100, verbose_name="权限别名")

    def __str__(self):
        return self.alias

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = "权限"

class Department(models.Model):
    name = models.CharField(max_length=20, verbose_name="部门名")
    level = models.SmallIntegerField(verbose_name="级别")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="上级部门")
    permissions = models.ManyToManyField(Permission, blank=True, related_name="departments", verbose_name="所有权限")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = verbose_name
        unique_together = ("name", "parent")


class User(AbstractUser):
    name = models.CharField("姓名", max_length=32, null=True, help_text="中文名")
    phone = models.CharField("电话", max_length=11, null=True, help_text="手机号")
    position = models.CharField(blank=True, max_length=20, verbose_name="职位")
    departments = models.ManyToManyField(Department, related_name="users", blank=True, verbose_name="部门集")
    permissions = models.ManyToManyField(Permission, related_name="users", blank=True, verbose_name="权限集")
    gitlab_token = models.CharField("gitlab秘钥", max_length=200, null=True, help_text="gitlab秘钥")
    k8s_token = models.CharField("k8s秘钥", max_length=200, null=True, help_text="k8s秘钥")
    other = models.CharField("备用字段", max_length=200, null=True, help_text="字段")
    class Meta:
        verbose_name = "用户"
        ordering = ["id"]

    def __str__(self):
        return self.username

    def get_all_permissions_no_cache(self):
        perms = [p.name for p in self.permissions.all()]
        perms = set(perms)
        for d in self.departments.all():
            for p in d.permissions.all():
                perms.add(p.name)
        return list(perms)

    @lru_cache(maxsize=64)
    def _get_all_permissions_by_cache(self, refresh_mark_number):
        print(f"{self.name} get_all_permissions_by_cache")
        return self.get_all_permissions_no_cache()

    def get_all_permission_names(self):
        # if settings.PERMISSION_CACHE_TIME == 0:
        #     return self.get_all_permissions_no_cache()
        # return self._get_all_permissions_by_cache(time.time()//settings.PERMISSION_CACHE_TIME)
        return self.get_all_permissions_no_cache()


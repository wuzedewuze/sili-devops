from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.conf import settings
User = get_user_model()

class UserInfoSerializer(serializers.ModelSerializer):
    """
        个人用户信息序列化
    """
    class Meta:
        model = User
        fields = ("id","username","name","phone", "email","password","gitlab_token","k8s_token")
        read_only_fields = [ 'username' ]  # 设置用户名为只读字段
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """
    class Meta:
        model = User
        fields = ("id", "username", "name", "phone", "email", "is_active","password","is_staff")
        #read_only_fields = [ 'username' ]  # 设置用户名为只读字段
        extra_kwargs = {'password':{'write_only':True}}
    # 自定义组信息
    # def to_group_response(self, group_queryset):
    #     ret = []
    #     # 将组信息序列化
    #     for group in group_queryset:
    #         ret.append({
    #             'id': group.id,
    #             'name': group.name
    #         })
    #     return ret

    # 修改返回信息 给返回信息添加自定义的组信息
    # def to_representation(self, instance):
    #     ret = super(UserSerializer, self).to_representation(instance)
    #     # role = self.to_group_response(instance.groups.all())
    #     # ret["role"] = role
    #     ret.pop('password')  # 不返回密码信息
    #     #ret.pop('is_active')
    #     return ret
    # 创建修改
    def create(self, validated_data):
        validated_data["is_active"] = True
        # validated_data["password"] = settings.INIT_PASSWORD  # 初始化密码设置
        password = validated_data.pop("password", None)
        instance = super(UserSerializer, self).create(validated_data=validated_data)
        #instance.email = "{}{}".format(instance.username, settings.DOMAIN)
        instance.set_password(password)
        instance.save()
        return instance

    # 更新修改
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

#



# class Groupserializer(serializers.ModelSerializer):
#     """
#     group序列化类,拿到组内成员个数并序列化输出
#     """
#
#     def to_permission_response(self, permission_queryset):
#         ret = []
#         # 将角色权限信息序列化
#         for permission in permission_queryset:
#             ret.append({
#                 'id': permission.id,
#                 'name': permission.name,
#                 'codename': permission.codename,
#             })
#         return ret
#
#     def to_members_response(self, members_queryset):
#         ret = []
#         # 将角色用户信息序列化
#         for member in members_queryset:
#             ret.append({
#                 'id': member.id,
#                 'username': member.username,
#                 'name': member.name,
#                 'phone': member.phone
#             })
#         return ret
#
#     def to_representation(self, instance):
#         members = self.to_members_response(instance.user_set.all())
#         number = instance.user_set.count()
#         power = self.to_permission_response(instance.permissions.all())
#         ret = super(Groupserializer, self).to_representation(instance)
#         ret["members"] = members
#         ret["number"] = number
#         ret["power"] = power
#         return ret
#
#     class Meta:
#         model = Group
#         fields = ("id", "name")
#
# class PermissionSerializer(serializers.ModelSerializer):
#     # content_type = ContentTypeSerializer()
#
#     class Meta:
#         model = Permission
#         fields = ("id", "name", "codename")
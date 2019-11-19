from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Permission, Group
# from django.db.models import Q
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import UserFilter, GroupFilter, PermissionFilter

# from rest_framework.authentication import TokenAuthentication,BasicAuthentication,SessionAuthentication
# #
# # from .serializers import UserSerializer, Groupserializer, PermissionSerializer

# from .permissions import IsSuperUser

from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes

from .serializers import UserSerializer
from .permissions import IsSelfuserOrSuperuser

User = get_user_model()

# 这里自定义了分页类
class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size' # 返回分页大小的参数名称
    page_query_param = "page"  # 返回分页的参数名称
    max_page_size = 100

class UserInfoViewset(viewsets.ViewSet):
    """
    获取当前登陆的用户信息
    """
    #authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)

    def list(self, request, *args, **kwargs):
        #token, created = Token.objects.get_or_create(user=self.request.user)
        data = {
            "username": self.request.user.username,
            "name": self.request.user.name,
            #"token": token.key
        }
        return Response(data)




class UserViewSet(viewsets.ModelViewSet):
    """
    create:
    创建用户，管理员创建用户
    list:
    获取用户列表，管理员获取所有用户信息列表
    retrieve:
    获取用户所有基础信息，管理员可获取他人信息，自己只能获取自己信息
    update:
    更新用户信息，管理员可更新他人信息，自己只能更新自己信息
    delete:
    删除用户
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #pagination_class = Pagination
    # 自定义权限调用
    permission_classes = [IsSelfuserOrSuperuser, ]
    # 过滤查询和排序方法
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    search_fields = ['name', 'username']
    ordering_fields = ('id', )
    # 自定义过滤方法
    filter_class = UserFilter

# class UsersViewset(viewsets.ModelViewSet):
#     """
#     create:
#     创建用户
#     list:
#     获取用户列表
#     retrieve:
#     获取用户信息
#     update:
#     更新用户信息
#     delete:
#     删除用户
#     """
#     #
#     # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
#     # permission_classes = (permissions.DjangoModelPermissions,)
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     pagination_class = Pagination
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     #filter_class = UserFilter
#     search_fields = ('name', 'username')
#     ordering_fields = ('id',)



# class GroupsViewset(viewsets.ModelViewSet):
#     """
#     create:
#     创建角色
#     list:
#     获取角色列表
#     retrieve:
#     获取角色信息
#     update:
#     更新角色信息
#     delete:
#     删除角色
#     """
#     # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
#     # permission_classes = (permissions.IsAuthenticated,)
#     queryset = Group.objects.all()
#     serializer_class = Groupserializer
#     pagination_class = Pagination
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     #filter_class = GroupFilter
#     search_fields = ('name',)
#     ordering_fields = ('id',)
#
#
# class PermissionsViewset(viewsets.ReadOnlyModelViewSet):
#     """
#     权限列表 视图类
#
#     list:
#     返回permission列表
#
#     """
#     # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
#     # permission_classes = (permissions.IsAuthenticated,)
#
#     queryset = Permission.objects.all()
#     serializer_class = PermissionSerializer
#     pagination_class = Pagination
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     #filter_class = PermissionFilter
#     search_fields = ("name", 'codename')
#     ordering_fields = ('id',)
#
#
# class UserGroupsViewset(mixins.UpdateModelMixin,
#                         viewsets.GenericViewSet):
#
#     """
#     update:
#     修改指定用户的角色
#     """
#     # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
#     # permission_classes = (permissions.IsAuthenticated,)
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     # 重写update方法，只针对用户和组进行单独的处理，类似的场景还有修改密码，更改状态等
#     def update(self, request, *args, **kwargs):
#         user_obj = self.get_object()
#         roles = request.data.get("role", [])
#         user_obj.groups = roles
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class GroupsPermViewset(mixins.UpdateModelMixin,
#                         viewsets.GenericViewSet):
#
#     """
#     update:
#     修改指定角色的权限
#     """
#     # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
#     # permission_classes = (permissions.IsAuthenticated,)
#
#     queryset = Group.objects.all()
#     serializer_class = Groupserializer
#
#     def update(self, request, *args, **kwargs):
#         group_obj = self.get_object()
#         power = request.data.get("power", [])
#         group_obj.permissions = power
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class GroupMembersViewset(mixins.DestroyModelMixin,
#                           viewsets.GenericViewSet):
#     """
#     destroy:
#     从指定组里删除指定成员
#     """
#     # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
#     # permission_classes = (permissions.IsAuthenticated,)
#
#     queryset = Group.objects.all()
#     serializer_class = Groupserializer
#
#     def destroy(self, request, *args, **kwargs):
#         group_obj = self.get_object()
#         uid = request.data.get('uid', 0)
#         group_obj.user_set.remove(int(uid))
#         return Response(status=status.HTTP_200_OK)
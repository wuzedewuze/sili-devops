import django_filters
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group,Permission
User = get_user_model()
class UserFilter(django_filters.rest_framework.FilterSet):
    """
    用户过滤类
    """
    class Meta:
        model = User
        fields = ['username']

# 高级过滤方法
# class ProductFilter(django_filters.rest_framework.FilterSet):
#     min_price = django_filters.NumberFilter(name="price", lookup_expr='gte')
#     max_price = django_filters.NumberFilter(name="price", lookup_expr='lte')
#     class Meta:
#         model = Product
#         fields = ['category', 'in_stock', 'min_price', 'max_price']



class GroupFilter(django_filters.rest_framework.FilterSet):
    """
    用户组过滤类
    """

    class Meta:
        model = Group
        fields = ['name']


class PermissionFilter(django_filters.rest_framework.FilterSet):
    """
    权限过滤类
    """

    class Meta:
        model = Permission
        fields = ['name', 'codename']
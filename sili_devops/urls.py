"""sili_devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter
# from sili_user.router import users_router
# 从路由导入路由
# router = DefaultRouter()
# router.registry.extend(users_router.registry)



# 导入第三方token认证 提供获取和刷新token的方法
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="devops API",
      default_version='v1',
      description="sili-devops 接口文档",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# 写一个apiroot方法，如果用set会自动生成
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
@api_view(['GET'])
def my_api_root(request, format=None):
    return Response({
        'swagger文档': reverse('schema-swagger-ui', request=request, format=format),
        '获取token': reverse('token_obtain_pair', request=request, format=format),
        '刷新token':reverse('token_refresh', request=request, format=format),
        '用户管理':reverse('user_api:api-root', request=request, format=format,),
    })

# 地址路由
urlpatterns = [
    path('', my_api_root),
    path('user_api/', include('sili_user.urls',namespace='user_api')),




    # django自带认证配置
    path('admin/', admin.site.urls),
    # django-restframwrok 基础登录配置
    path('api-auth/', include('rest_framework.urls')),

    # 导入第三方token认证 提供获取和刷新token的方法
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # swagger文档配置 新版django使用re_path方法代替原来默认的正则路由
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]


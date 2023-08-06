## pip install dpyi
### urls.py
```
"""jh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework.schemas import get_schema_view
from django.contrib import admin
from django.urls import path, include
from rest_framework.urls import url
from oa.controller import *
from pyi.core.runtime import router

schema_view = get_schema_view(title='Users API')

urlpatterns = [
    # swagger接口文档路由
    url(r'^docs/', schema_view, name='docs'),
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    # drf登录
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

```

### {app}/controller/{controllername}.py
```
from dpyi.decorators.controller import Controller, PYIController, RequestMapping, RequestMappingMethod
from ..service.test import TestService
from dpyi.utils.response import SuccessDto


@Controller(prefix='oa/oa')
class TestController(PYIController):

    @property
    def service(self): return TestService()

    @RequestMapping(prefix='test', methods=[
        RequestMappingMethod.GET,
        RequestMappingMethod.POST
    ])
    def test(self, request, *args, **kwargs):
        print(self)
        return SuccessDto(data={'name': 'TestController Test'})

    @RequestMapping(prefix='show', methods=[
        RequestMappingMethod.GET,
        RequestMappingMethod.POST
    ])
    def show(self, request, *args, **kwargs):
        return SuccessDto(data={'name': 'TestController Show'})

```

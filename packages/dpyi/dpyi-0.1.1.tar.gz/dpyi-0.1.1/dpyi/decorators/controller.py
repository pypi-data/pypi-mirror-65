from ..core.pyi import PYI
from ..core.runtime import router
from rest_framework import viewsets
from rest_framework.urls import url
from ..utils.response import FailureDto, SuccessDto
from rest_framework.decorators import action
from types import MethodType

# 基础控制器


class PYIController (PYI, viewsets.ViewSet):

    @staticmethod
    def _extends():
        return PYIController
    pass


def routerstruct(target, prefix=''):
    router.register(r''+prefix, target, basename=prefix)
    return target

# 控制器


def Controller(prefix=''):
    if not isinstance(prefix, str) and prefix and prefix._extends and prefix._extends() == PYIController:
        return routerstruct(prefix, '')

    def decorator(target):
        return routerstruct(target, prefix)
    return decorator

# 请求类型


class RequestMappingMethod(object):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'del'
    PATCH = 'patch'
    OPTION = 'option'
    LINK = 'link'
    UNLINK = 'unlink'
    pass


# actions
def RequestMapping(prefix, methods=None):
    def decorator(target): 
        return action(methods=methods, detail=False, url_path=prefix)(target)
    return decorator

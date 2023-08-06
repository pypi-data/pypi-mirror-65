from django.http import HttpResponse
import json


def SuccessDto(message='success', code=0, data={}):
    return HttpResponse(json.dumps({
        'errcode': code,  # code由前后端配合指定
        'message': message,  # 提示信息
        'data': data,  # 返回单个对象
    }), 'application/json')


def FailureDto(message='fial', code=1001, data={}):
    return HttpResponse(json.dumps({
        'errcode': code,
        'message': message,
        'data': data,
    }), 'application/json')

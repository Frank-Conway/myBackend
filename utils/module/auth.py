from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from utils.module import return_code
from apps.base import models
from utils.encrypt import md5
from utils.jwt_auth import create_token, parse_payload
from django.core.validators import RegexValidator


class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        if request.method == "OPTIONS":
            return

        # raise NotImplementedError(".authenticate() must be overridden.")
        # 1.读取请求头中的token
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        # print(authorization)

        # 2.token校验
        # {'user_id': instance.id, 'name': instance.name}
        status, info_or_error = parse_payload(authorization)

        # 3.校验失败，返回失败信息，前端重新登录
        if not status:
            raise exceptions.AuthenticationFailed({"code": 8888, 'msg': info_or_error})

        # 4.校验成功，继续向后  request.user  request.auth
        return (info_or_error, authorization)

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return 'API realm="API"'


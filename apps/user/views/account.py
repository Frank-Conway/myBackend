from rest_framework.views import APIView
from rest_framework.response import Response
from utils.module import return_code
from apps.base import models
from utils.jwt_auth import create_token
from apps.user.serializers.account import LoginSerializer, LoginSmsSerializer, RegisterSerializer, SendSmsSerializer
import random
from django_redis import get_redis_connection

class LoginView(APIView):
    """ 用户登录 """

    def post(self, request):
        # 1. 数据格式校验
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"code": return_code.FIELD_ERROR, 'msg': "error", 'detail': serializer.errors}, status=400)

        # 2. 数据库合法性校验
        instance = models.Company.objects.filter(**serializer.validated_data).first()

        # 2.1 登录失败
        if not instance:
            return Response({"code": return_code.SUMMARY_ERROR, 'msg': "用户名或密码错误"}, status=401)

        # 2.2 登录成功，返回用户信息
        token = create_token({'user_id': instance.id, 'name': instance.name})
        return Response({
            "code": return_code.SUCCESS,
            'msg': "success",
            'data': {"token": token, 'name': instance.name, 'id': instance.id}
        })


class SendSmsView(APIView):

    def post(self, request):
        try:
            # 1. 接收请求数据
            print(request.data)

            # 2. 校验（手机格式 + 手机号必须存在）
            serializer = SendSmsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # 3. 生成随机验证码
            random_code = random.randint(1000, 9999)
            print(random_code)

            # 4. 发送短信（假设有一个发送短信的接口）
            # send_sms(serializer.validated_data['mobile'], random_code)

            # 5. 保存验证码到 Redis
            redis_conn = get_redis_connection("default")
            redis_conn.set(serializer.validated_data['mobile'], random_code, ex=60)

            # 6. 返回成功响应
            return Response({"code": return_code.SUCCESS, 'msg': "success"})

        except Exception as e:
            print(e)
            return Response({"code": return_code.SUMMARY_ERROR, 'msg': "发送失败"}, status=500)

class LoginSmsView(APIView):
    def post(self, request):
        try:
            # 1.获取数据,格式校验（手机格式、手机号存在、短信-去redis中获取+提交=比较）
            ser = LoginSmsSerializer(data=request.data)

            if not ser.is_valid():
                return Response({"code": return_code.FIELD_ERROR, 'msg': "error", 'detail': ser.errors})
            # 3.成功/失败
            instance = models.Company.objects.filter(mobile=ser.validated_data['mobile']).first()

            # 4.生成jwt token返回 + 跳转
            token = create_token({'user_id': instance.id, 'name': instance.name})
            return Response({
                "code": return_code.SUCCESS,
                'msg': "success",
                'data': {"token": token, 'name': instance.name, 'id': instance.id}
            })
        except Exception as e:
            return Response({"code": return_code.SUMMARY_ERROR, 'msg': "发送失败"})


class RegisterSmsView(APIView):
    def post(self, request):
        try:
            # 1.获取数据
            # print(request.data)
            # 2.校验
            ser = RegisterSerializer(data=request.data)
            if not ser.is_valid():
                return Response({"code": return_code.FIELD_ERROR, 'msg': "error", 'detail': ser.errors})

            ser.validated_data.pop("code")
            ser.validated_data.pop("confirm_password")
            # 3.保存到数据库
            # ser.save(auth_type=2)
            ser.save()
            return Response({"code": return_code.SUCCESS})
        except Exception as e:
            return Response({"code": return_code.SUMMARY_ERROR, 'msg': "注册失败"})

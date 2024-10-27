from rest_framework import serializers
from rest_framework import exceptions
from apps.base import models
from utils.encrypt import md5
from django.core.validators import RegexValidator


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_password(self, value):
        md5_string = md5(value)
        return md5_string


class SendSmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        required=True,
        validators=[RegexValidator(r"^1[3-9]\d{9}$", message="手机号码格式错误")]
    )

    def validate_mobile(self, value):
        # 自定义验证
        exists = models.Company.objects.filter(mobile=value).exists()
        if not exists:
            raise exceptions.ValidationError("手机号码未注册")
        return value


class LoginSmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, validators=[RegexValidator(r"^1[3-9]\d{9}$", message="格式错误")])
    code = serializers.CharField(required=True, validators=[RegexValidator(r"\d{4}", message="格式错误")])

    def validate_mobile(self, value):
        print(value)
        # 自定义验证
        exists = models.Company.objects.filter(mobile=value).exists()
        if not exists:
            raise exceptions.ValidationError("手机未注册")
        return value

    def validate_code(self, value):
        mobile = self.initial_data.get('mobile')
        from django_redis import get_redis_connection
        conn = get_redis_connection("default")
        cache_code = conn.get(mobile)
        if not cache_code:
            raise exceptions.ValidationError("验证码不存在或已过期")
        cache_code = cache_code.decode('utf-8')
        if cache_code != value:
            raise exceptions.ValidationError("验证码错误")
        conn.delete(mobile)
        return value


class RegisterSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(required=True, validators=[RegexValidator(r"^1[3-9]\d{9}$", message="格式错误")])
    code = serializers.CharField(required=True, validators=[RegexValidator(r"\d{4}", message="格式错误")])
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = models.Company
        fields = ['name', 'mobile', 'code', 'password', 'confirm_password']

    def validate_mobile(self, value):
        # 自定义验证
        exists = models.Company.objects.filter(mobile=value).exists()
        if exists:
            raise exceptions.ValidationError("手机号已注册")
        return value

    def validate_password(self, value):
        return md5(value)

    def validate_confirm_password(self, value):
        password = self.initial_data.get('password')
        if value != password:
            raise exceptions.ValidationError("密码不一致")
        return value

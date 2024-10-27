from rest_framework import serializers
from rest_framework import exceptions
from apps.base import models
from django.core.validators import RegexValidator
from utils.module.auth import JwtAuthentication

from rest_framework.viewsets import GenericViewSet

from utils.module.mixins import RetrieveModelMixin, UpdateModelMixin
from utils.module.filter import MineFilterBackend


class BasicModelSerializer(serializers.ModelSerializer):
    mobile = serializers.SerializerMethodField()
    ctime = serializers.DateTimeField(format="%Y-%m-%d")
    auth_type_text = serializers.CharField(source="get_auth_type_display")

    class Meta:
        model = models.Company
        fields = ['id', 'name', 'mobile', 'ctime', 'auth_type', 'auth_type_text']

    def get_mobile(self, obj):
        return obj.mobile[0:3] + "****" + obj.mobile[-4:]


class NameModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ['name']


class UpdateMobileSerializer(serializers.ModelSerializer):
    old = serializers.CharField(write_only=True)
    new_mobile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Company
        fields = ['old', "mobile", "new_mobile"]
        extra_kwargs = {
            'old': {'validators': [RegexValidator(r"\d{11}", message="手机格式错误")]},
            'mobile': {'validators': [RegexValidator(r"\d{11}", message="手机格式错误"), ], "write_only": True},
        }

    def validate_old(self, val):
        # 当前登录用的手机号是不是
        request = self.context['request']
        user_id = request.user['user_id']
        # user_dict = {"id": 1, "name": "xxx"}
        # # {'user_id': 1, 'name': '大和实业', 'exp': 1670212872}
        exists = models.Company.objects.filter(id=user_id, mobile=val).exists()
        if not exists:
            raise exceptions.ValidationError("原手机号错误")
        return val

    def get_new_mobile(self, obj):
        return obj.mobile[0:3] + "****" + obj.mobile[-4:]


class BasicView(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    # authentication_classes = [JwtAuthentication, ]
    filter_backends = [MineFilterBackend]

    # 筛选时会自动加上get(id=1或其它)
    queryset = models.Company.objects.all()
    # 对获取到的数据进行序列化处理
    serializer_class = BasicModelSerializer

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            req_type = self.request.query_params.get('type')
            if req_type == "name":
                return NameModelSerializer
            elif req_type == 'mobile':
                return UpdateMobileSerializer
        return BasicModelSerializer

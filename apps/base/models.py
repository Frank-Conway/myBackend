from django.db import models

# Create your models here.
class Company(models.Model):
    """ 供应商 """
    name = models.CharField(verbose_name="企业简称", max_length=32)

    mobile = models.CharField(verbose_name="手机号", max_length=11)
    password = models.CharField(verbose_name="密码", max_length=32)

    auth_type_class_map = {1: "danger", 2: "primary", 3: "success"}
    auth_type = models.SmallIntegerField(verbose_name="认证类型", choices=((1, "未认证"), (2, "认证中"), (3, "已认证")), default=1)
    ctime = models.DateTimeField(verbose_name="注册时间", auto_now_add=True)

    # 可用余额
    balance = models.DecimalField(verbose_name="可用余额", default=0, max_digits=10, decimal_places=2)
    # 不可用余额
    freeze_balance = models.DecimalField(verbose_name="不可用余额", default=0, max_digits=10, decimal_places=2)

class CompanyAuth(models.Model):
        """ 供应商认证 """
        # company = models.ForeignKey(verbose_name="公司", to="Company", on_delete=models.CASCADE)
        company = models.OneToOneField(verbose_name="公司", to="Company", on_delete=models.CASCADE)

        title = models.CharField(verbose_name="公司全称", max_length=64)
        unique_id = models.CharField(verbose_name="信用代码", max_length=64)
        licence_path = models.CharField(verbose_name="营业执照", max_length=64)  # 文件路径
        leader = models.CharField(verbose_name="法人", max_length=64)
        leader_identity = models.CharField(verbose_name="法人身份", max_length=64)
from django.urls import path
from .views import account, userinfo
from rest_framework import routers

# 导入视图，点号.代表当前包或目录。两个点号..，意味着从父级目录中导入
router = routers.SimpleRouter()
router.register(r'info', userinfo.BasicView)
urlpatterns = [
    path('login', account.LoginView.as_view()),
    path('send/sms', account.SendSmsView.as_view()),
    path('login/sms', account.LoginSmsView.as_view()),
    path('register', account.RegisterSmsView.as_view()),

]
urlpatterns += router.urls
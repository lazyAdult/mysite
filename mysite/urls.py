"""mysite URL Configuration

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
from django.urls import path, include

from login import views

urlpatterns = [
    path('superuser/', admin.site.urls),
    # 为了防止机器人频繁登录网站或者破坏恶意登录,很多用户登录和注册系统都提供了图形验证功能
    # 验证码(CAPTCHA)验证码（CAPTCHA）是“Completely Automated Public Turing test to tell Computers and Humans Apart”
    # （全自动区分计算机和人类的图灵测试）的缩写，是一种区分用户是计算机还是人的公共全自动程序。可以防止恶意破解密码、刷票、论坛灌水，
    # 有效防止某个黑客对某一个特定注册用户用特定程序暴力破解方式进行不断的登陆尝试。
    # 图形验证码的历史比较悠久，到现在已经有点英雄末路的味道了。因为机器学习、图像识别的存在，
    # 机器人已经可以比较正确的识别图像内的字符了。但不管怎么说，作为一种防御手段，至少还是可以抵挡一些低级入门的攻击手段，抬高了攻击者的门槛。
    path('captcha/', include('captcha.urls')),  # 增加captcha图片验证路由
    path('', include(('login.urls', 'login'), namespace="login")),
    # 处理邮件请求
    path('confirm/', views.user_confirm),
]

import datetime
import hashlib
from django.core.mail import EmailMultiAlternatives

# 定义一个hash值进行密码的隐藏使用hash值加盐,让后台管理员也不能看到明文密码
# 在这里设置一个形参pwd,一个实参salt
from login import models
from mysite import settings


def hash_code(pwd, salt="hello"):
    # 导入hashlib模块 python自带hashlib模块
    h = hashlib.sha256()
    # 将需要密码和一个自定义的数据进行组合防止密码被破译
    pwd += salt
    # update只能接受编码
    h.update(pwd.encode())
    # 返回十六进制数字
    return h.hexdigest()


# 创建确认码对象
def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code


def send_email(email, code):
    subject = "来自Django的模拟确认邮件"
    text_content = "如果你看到这条消息说明你的邮箱服务不提供html连接功能,请联系管理员"
    html_content = """""<p>感谢注册<a href='http://{}/confirm/?code={}' target=_blank>确认连接</a></p>"
                        <p> 请点击站点连接完成注册 </p>
                        <p>此链接的有效期为{}天</p>
                    """.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

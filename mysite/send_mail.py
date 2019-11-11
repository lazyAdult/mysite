import os

from django.core.mail import send_mail, EmailMultiAlternatives

# 由于我们当前是单独运行send_mail.py文件,无法自动连接Django环境,需要通过os模块对环境变量进行设置
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':
    """
    对于send_mail方法:
    第一个参数:邮件主题subjects
    第二个参数:邮件具体内容
    第三个参数:邮件发送方, 需要和你setting中的一致;
    第四个参数:接收方的邮件地址列表
    """
    # send_mail(
    #     '来自django的测试文件',
    #     '发送邮件的具体内容',
    #     '18638321931@163.com',
    #     ['1209250028@qq.com'],
    # )

    # 发送html格式的邮件
    subjects, form_email, to = '来自django的测试邮箱信息发送', '18638321931@163.com', '1209250028@qq.com'
    # 使用text_content是用于当html内容无效时的替代text文本
    text_content = "测试文件的具体内容"
    html_content = """"<p><h1 style="color:red">测试文件<h1></p>"
                        "<p><a href="http://www.baidu.com">百度</a></p>"
                    """
    msg = EmailMultiAlternatives(subjects, text_content, form_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

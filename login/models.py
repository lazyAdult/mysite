from django.db import models

# Create your models here.


class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='男')
    c_time = models.DateField(auto_now_add=True)
    # 关联邮箱是否已经确认
    has_confirmed = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'login'
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class ConfirmString(models.Model):
    code = models.CharField(max_length=128)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ": " + self.code

    class Meta:
        db_table = "confirm_code"
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = verbose_name

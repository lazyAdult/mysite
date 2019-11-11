from django.contrib import admin

# Register your models here.
from login.models import User, ConfirmString


@admin.register(User)
class LoginAdmin(admin.ModelAdmin):
    model = User
    list_display = ['id', 'name', 'password', 'email', 'sex', 'c_time']


@admin.register(ConfirmString)
class ConfirmAdmin(admin.ModelAdmin):
    model = ConfirmString
    list_display = ["id", "code", "user", "c_time"]

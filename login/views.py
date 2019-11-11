import datetime

from django.shortcuts import render, redirect

from mysite import settings
from . import diy_method

# Create your views here.
from login import models, forms


def index(request):
    return render(request, "login/index.html")


def login(request):
    if request.session.get("is_login", None):   # 不允许重复登录
        return redirect('login:index')

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        error = "请检查填写的内容"
        # 验证表单
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            try:
                user = models.User.objects.get(name=username)
                # 通过下面的语句,我们往session字典里面写入用户状态和数据
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
            except:
                error = "用户名不存在"
                return render(request, "login/login.html", locals())
            # 提醒用户进行邮箱验证
            if not user.has_confirmed:
                message = "该用户未经过邮箱确认"
                return render(request, "login/login.html", locals())
            # 使用自定义方法进行转换对比
            if user.password == diy_method.hash_code(password):
                return redirect("login:index")
            else:
                error = "密码不正确"
                return render(request, "login/login.html", locals())

        return render(request, "login/login.html", locals())

    login_form = forms.UserForm()
    return render(request, "login/login.html", locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect("login:index")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容"
        print(register_form)
        print(1111111)
        if register_form.is_valid():
            username = register_form.cleaned_data.get("username")
            password1 = register_form.cleaned_data.get("password1")
            password2 = register_form.cleaned_data.get("password2")
            email = register_form.cleaned_data.get("email")
            sex = register_form.cleaned_data.get("sex")
            if password1 != password2:
                message = "两次密码不一致"
                return render(request, "login/register.html", locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = "用户名已经存在"
                    return render(request, "login/register.html", locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = "该邮箱已经被注册"
                    return render(request, "login/register.html", locals())

                # 把验证通过的注册信息存入数据库
                new_user = models.User()
                new_user.name = username
                # 将注册的密码转为十六进制数据存入到数据库
                new_user.password = diy_method.hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                code = diy_method.make_confirm_string(new_user)
                diy_method.send_email(email, code)
                message = "请前往邮箱进行确认!"
                return render(request, "login/confirm.html", locals())

                """
                # 让用户在注册过后跳转到首页不需要再次登录
                user = models.User.objects.get(name=new_user.name)
                # 通过下面的语句,我们往session字典里面写入用户状态和数据
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect("login:index")
                """

        return render(request, "login/register.html", locals())
    register_form = forms.RegisterForm()
    return render(request, "login/register.html", locals())


def logout(request):
    # 判断是否已经登录
    if not request.session.get('is_login', None):
        return redirect("login:login")
    # flush()方法是比较安全的一种做法,而且一次性将session中的所有内容全部清空,确保不留后患.但也有不好的地方,那就是如果你在session中
    # 夹带了一点私货,也会一并删除,这一点一定要注意
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("login:index")


# 处理邮件的视图
def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''

    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = "无效的确认请求"
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = "你的邮件已经过期,请重新注册"
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = "邮箱已经确认,请登录"
        return render(request, 'login/confirm.html', locals())

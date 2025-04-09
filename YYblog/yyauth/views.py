from django.shortcuts import render ,redirect,reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import  RegisterForm,LoginForm
from django.contrib.auth import get_user_model,login,logout

User = get_user_model()
# Create your views here.

@require_http_methods(['GET','POST'])
def yylogin(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                #登录
                login(request, user)
                #判断用户是否需要记住我
                if not remember:
                    # 如果没有点击记住我，那么就设置过期时间为0，游览器关闭后就会过期
                    request.session.set_expiry(0)
                #如果点击了就什么都不做，默认两周过期
                return redirect('/')
            else:
                print('邮箱或密码错误')
                return redirect(reverse('yyauth:login'))

def yylogout(request):
    logout(request)
    return redirect('/')



@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email,username=username,password=password)
            return redirect(reverse('yyauth:login'))
        else:
            print(form.errors)
            #重新跳转到登录页面
            return redirect(reverse('yyauth:register'))
def send_email_captcha(request):
 #?email=xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code':400,'msg':'必须传递邮箱'})
    #生成验证码（取四位阿拉伯数字）
    captcha="".join(random.sample(string.digits, k=4))
    #存储到数据库当中
    CaptchaModel.objects.update_or_create(email=email,defaults={'captcha':captcha})
    send_mail("YY博客注册验证码",f"您的注册验证码是：{captcha}",recipient_list=[email],from_email=None)
    return JsonResponse({"code":200 ,"message":"邮箱验证码发送成功"})
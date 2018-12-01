import os
import random
import string
import time

import re
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from main_app.tools.image import ImageCaptcha
from user_app.models import Baizhi
from django.core.mail import send_mail,EmailMultiAlternatives
import datetime
import hashlib
from django.shortcuts import render
from . import models
from zhongji import settings



def makepwd(pwd,salt = None):
    print('this is make pwd')
    h = hashlib.md5()
    if not salt:
        abc = '123456789!@#$%^&*()_+abcdefghijklmnopqrstuvwxyz<>?/.,'
        salt = ''.join(random.sample(abc,10)).replace(' ','')
        pwd = pwd+salt
        h.update(pwd.encode())
        mypwd = h.hexdigest()
        return mypwd,salt
    else:
        pwd = pwd + salt
        h.update(pwd.encode())
        mypwd = h.hexdigest()
        return mypwd

def hash_code(s,salt='oracle'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.user, now)
    models.ConfirmString.objects.create(code=code, user=user)

    return code


def send_email(email, code):
    subject = '来自项目的注册确认邮件'

    text_content = '''欢迎你来验证你的邮箱，验证结束你就可以登录了！\                     如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联 系管理员！'''
    html_content = '''<p>感谢注册<a href="http://172.16.14.57:8000/user/register/confirm/?code={}" >点击验证</a>，\  欢迎你来验证你的邮箱，验证结束你就可以登录 了！</p>                     <p>请点击站点链接完成注册确认！</p>                     <p>此链接有效期为7天！</p>                     '''.format(
         code)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def ajax_test1(request):
    time.sleep(3)
    user=request.POST.get("userid")
    print(user)
    # data = Baizhi.objects.filter(user=user)
    rule='.{1,10}'
    results = re.compile(rule)
    # if results.findall(user):
    if request:
        print("ajax is pk")
        return HttpResponse("0")
    print("ajax is ok")
    return HttpResponse("1")


def login_page(request):

    return render(request,'user_app/login.html')

def login_logic(request):
    # 接受username和password
    realcode = request.session.get("code")
    # 2.获取用户输入码
    usercode = request.POST.get("number")
    # 3.判断

    user = request.POST.get("userid")
    # user1=models.Baizhi.objects.get(user=user)
    pwd = request.POST.get("pwd")
    print(user,pwd)
    salt=Baizhi.objects.filter(user=user)
    print('salt:',salt)

    salt = salt[0].salt
    pwd = makepwd(pwd, salt)
    print(salt,pwd)

    # check = Baizhi.objects.filter(user=user)
    # print(check)
    a=models.Baizhi.objects.get(user=user)
    if pwd:
        print(111111)
        if not a.has_confirmed:
            # a='1'
            message = '没有进行邮箱确认，请前往邮箱进行确认'
            # return render(request,'user_app/login.html',{a:"0"})
            return HttpResponse("0")
        else:
            return HttpResponse("1")
            # return render(request,'main_app/main.html', {a:"1"})
    #     request.session['labal']=1
    #     # return HttpResponse('1')
    else:
        return HttpResponse('0')


def register_page(request):

    return render(request,'user_app/register.html')


def register_logic(request):
    user=request.POST.get('userid')
    usertel=request.POST.get('usertel')
    email=request.POST.get('email')
    pwd=request.POST.get('pwd')
    # data = Baizhi.objects.filter(user=user)
    # if data:
    result = makepwd(pwd)
    pwd = result[0]
    new_user = Baizhi.objects.create(user=user, usertel=usertel, email=email, pwd=pwd)
    print(user, usertel, email, pwd)
# print(data)
# print(user,usertel,email,pwd)
    code = make_confirm_string(new_user)
    print(code)
    send_email(email, code)
    message='请前往邮箱验证，进行确认'
    return render(request,'user_app/confirm.html',locals())

def user_confirm(request):
    code=request.GET.get('code',None)
    message=''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的请求'
        return render(request, 'user_app/confirm.html', locals())
    confirm.user.has_confirmed = True
    confirm.user.save()
    confirm.delete()
    message = '感谢确认，请登录'
    return render(request, 'user_app/login.html', locals())



def get_captcha(request):
    """
    生成验证码，响应给浏览器
    1.随机码（字符串）
    2将码放在图片上
    3响应给浏览器
    :param request:
    :return:
    """
    #1创建一个ImageCaptcha对象
    cap = ImageCaptcha(fonts=[os.path.abspath("captcha/font/segoesc.ttf")])
    # 2.获取5位长度 随机验证码值
    code_list = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 5)
    code="".join(code_list)
    #3.将验证码存入session
    request.session["mycode"]=code
    print("验证码是",code)
    #4.生成验证码图片
    data=cap.generate(code)
    #5写出图片
    return HttpResponse(data,"image/png")

def checkcode(request):
    print('this is check code')
    code = request.GET.get("code")
    mycode = request.session.get('mycode')
    print('mycode',mycode,'usercode',code)
    if code.lower() == mycode.lower():
        return HttpResponse('1')
    else:
        return HttpResponse('0')







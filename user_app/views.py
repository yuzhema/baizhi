from django.shortcuts import render, redirect

# Create your views here.
from user_app.models import Baizhi


def login_page(request):

    return render(request,'user_app/login.html')

def login_logic(request):
    user=request.POST.get('userid')
    pwd=request.POST.get('pwd')

    check=Baizhi.objects.filter(user=user,pwd=pwd)
    if check:
        request.session['labal']=1
        return redirect('main:display')
    return redirect('user:login:page')


def register_page(request):

    return render(request,'user_app/register.html')


def register_logic(request):
    user=request.POST.get('userid')
    usertel=request.POST.get('usertel')
    email=request.POST.get('email')
    pwd=request.POST.get('pwd')
    print(user,usertel,email,pwd)
    try:
        Baizhi(user=user,usertel=usertel,email=email,pwd=pwd).save()
        request.session['labal']='1'
        return redirect('main:display')
    except:
        return redirect('user:register:page')

# import happybase
# connection=happybase.Connection(host='192.168.245.36',port=9090)
# connection.open()
#
# def test_hbase(request):
#     table = connection.table('t_projects:aa')
#     # table.put('002',{'choosed:name':'xiaohei','choosed:sex':'male','refused:salary':'2000'})
#
#     info = table.scan()
#     return render(request,'hbase.html',{'info':info})










import os,random,string,time,happybase,requests

from django.views.decorators.cache import cache_page
from lxml import etree

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from main_app.models import Projects
from main_app.tools.image import ImageCaptcha
from . daily import logs
import happybase
connection=happybase.Connection(host='172.16.14.84',port=9090)
connection.open()
table=connection.table('AI133:t_project')



def display(request):
    labal=request.session.get('labal')

    return render(request,'main_app/main.html')


def intro(request):

    return render(request,'main_app/introduce.html')



#封装的左边栏方法
def datas(ID):
    if ID == '1':
        data = Projects.objects.filter(city__contains='北京', title__icontains='web')

    elif ID == '2':
        data = Projects.objects.filter(city__contains='北京', title__contains='爬')
    elif ID == '3':
        data = Projects.objects.filter(city__contains='北京', title__contains='数据')
    elif ID == '4':
        data = Projects.objects.filter(city__contains='北京', title__icontains='ai')
    elif ID == '5':
        data = Projects.objects.filter(city__contains='上海', title__icontains='web')
    elif ID == '6':
        data = Projects.objects.filter(city__contains='上海', title__contains='爬')
    elif ID == '7':
        data = Projects.objects.filter(city__contains='上海', title__contains='数据')
    elif ID == '8':
        data = Projects.objects.filter(city__contains='上海', title__icontains='ai')
    elif ID == '9':
        data = Projects.objects.filter(city__contains='广州', title__icontains='web')
    elif ID == '10':
        data = Projects.objects.filter(city__contains='广州', title__contains='爬')
    elif ID == '11':
        data = Projects.objects.filter(city__contains='广州', title__contains='数据')
    elif ID == '12':
        data = Projects.objects.filter(city__contains='广州', title__icontains='ai')
    elif ID == '13':
        data = Projects.objects.filter(city__contains='深圳', title__icontains='web')
    elif ID == '14':
        data = Projects.objects.filter(city__contains='深圳', title__contains='爬')
    elif ID == '15':
        data = Projects.objects.filter(city__contains='深圳', title__contains='数据')
    elif ID == '16':
        data = Projects.objects.filter(city__contains='深圳', title__icontains='ai')
    return data

#hbase过滤封装的函数
def cover_hbase(ID):
    if ID=='1':
        filters="RowFilter(=,'regexstring:.*?(web|python|Python|WEB|Web|后台|全栈).*?北京.*')"
    elif ID=='2':
        filters="RowFilter(=,'regexstring:.*?(爬虫|搜索).*?北京.*')"
    elif ID=='3':
        filters="RowFilter(=,'regexstring:.*?(大数据|算法).*?北京.*')"
    elif ID=='4':
        filters="RowFilter(=,'regexstring:.*?(ai|AI|智能).*?北京.*')"
    elif ID=='5':
        filters="RowFilter(=,'regexstring:.*?(web|python|Python|WEB|Web|后台|全栈).*?上海.*')"
    elif ID=='6':
        filters="RowFilter(=,'regexstring:.*?(爬虫|搜索).*?上海.*')"
    elif ID=='7':
        filters="RowFilter(=,'regexstring:.*?(大数据|算法).*?上海.*')"
    elif ID=='8':
        filters="RowFilter(=,'regexstring:.*?(ai|AI|智能).*?上海.*')"
    elif ID=='9':
        filters="RowFilter(=,'regexstring:.*?(web|python|Python|WEB|Web|后台|全栈).*?广州.*')"
    elif ID=='10':
        filters="RowFilter(=,'regexstring:.*?(爬虫|搜索).*?广州.*')"
    elif ID=='11':
        filters="RowFilter(=,'regexstring:.*?(大数据|算法).*?广州.*')"
    elif ID=='12':
        filters="RowFilter(=,'regexstring:.*?(ai|AI|智能).*?广州.*')"
    elif ID=='13':
        filters="RowFilter(=,'regexstring:.*?(web|python|Python|WEB|Web|后台|全栈).*?深圳.*')"
    elif ID=='14':
        filters="RowFilter(=,'regexstring:.*?(爬虫|搜索).*?上海.*')"
    elif ID=='15':
        filters="RowFilter(=,'regexstring:.*?(大数据|算法).*?上海.*')"
    elif ID=='16':
        filters="RowFilter(=,'regexstring:.*?(ai|AI|智能).*?上海.*')"
    info=table.scan(columns=('choosed',),filter=filters)
    return info

#搜索
def hbase_search(val):
    info = table.scan(filter="RowFilter(=,'regexstring:.*?{}.*')".format(val), columns=('choosed',))
    return info

#hbase中获取数据
def get_hbase(num,number,sum_num,ID=None,val=None):
    l=[]

    if val:
        info=hbase_search(val)
    else:
        info=cover_hbase(ID)

    if num==sum_num:

        for i in list(info)[:10-number]:
            d = {}
            for j,k in i[1].items():
                d.update({j.decode().split(':')[1]:k.decode()})
            print(d)
            l.append(d)

    else:

        for i in list(info)[(num-sum_num)*10+10-number:(num-sum_num+1)*10+10-number]:
            d = {}
            for j,k in i[1].items():
                d.update({j.decode().split(':')[1]:k.decode()})
            print(d)
            l.append(d)


    return l

# @cache_page(timeout=60,key_prefix="cacheRedis")    # timeout 缓存时效(秒)
@logs
def ms(request):
    #左边栏点击的是哪个
    ID=request.GET.get('ID')
    num=request.GET.get('num')
    del_num=request.GET.get('del_num')
    nums=request.GET.get('nums')
    #时间标识
    time1=request.session.get('time1')
    #访问次数
    count=request.session.get('count')
    v=request.GET.get('v')
    #搜索框传来的数据
    val=request.GET.get('val')
    selec=request.GET.get('selec')

    #判断是否是爬虫
    if "Mozilla/5.0" not in request.META['HTTP_USER_AGENT']:
        return render(request,'main_app/404.html')

    if not time1:
        time1=time.time()
        count=1
        request.session['count']=count
        request.session['time1']=time1
    else:
        if int(count)>=8:
            time2=time.time()
            if time2-int(time1) <= 5:
                time.sleep(5)

            del request.session['time1']
            del request.session['count']
        else:
            request.session['count']=int(count)+1
    num = request.GET.get('num')
    labal=request.session.get('labal')
    #判断点击的是不是下一页
    if num:
        num=int(num)+1
    if (not num and not del_num) or del_num=='1':

        num=1

    #判断是不是点击的是上一页，以及当前页是否为1
    if del_num and int(del_num)>1:

        num=int(del_num)-1
    if nums:
        if 0>int(float(nums)) or int(nums)>int(v):
            num=1
        else:
            num=int(nums)
    #判断是否登录
    if not labal:
        if int(num)>10:
            return redirect('user:login:page')
    else:
        # if int(labal)>100:
        #     request.session['labal'] = 50
        #     num=50
        request.session['labal'] = int(labal) + 1

    #判断是不是从搜索条件处转来的
    if val and selec and val!='None' and selec!='None':

        if selec=='1':
            data=Projects.objects.filter(city__contains=val)

        else:
            data=Projects.objects.filter(title__contains=val)
        hbase_num=len(list(hbase_search(val)))
    else:

        data=datas(ID)
        # hbase中数据的数量
        hbase_num = len(list(cover_hbase(ID)))
    #从hbase中获取数据
    l=[]
    page=None
    p = Paginator(object_list=data, per_page=10)
    #mysql中的总页数
    sum_num=p.page(1).paginator.num_pages


    print(hbase_num)
    #mysql中存储的数量
    mysql_num=len(list(data))
    #hbase和mysql中的总数量
    sum_hbase_mysql=hbase_num+mysql_num

    # mysql中最后一页的数量
    number =mysql_num -(sum_num-1)*10

    # 判断是不是从搜索条件处转来的

    if val and selec and val != 'None' and selec != 'None':

        if num<sum_num:
            page=p.page(num)
        elif num==sum_num:
            page=p.page(num)
            l=get_hbase(num,number,sum_num,val)
        else:
            l = get_hbase(num, number, sum_num, val)
    else:

        if num<sum_num:
            page=p.page(num)
        elif num==sum_num:
            page=p.page(num)

            #hbase中获取的第一页数据
            l=get_hbase(num,number,sum_num,ID=ID)

        else:
            l = get_hbase(num, number, sum_num,ID=ID)

    print(l)
    return render(request,'main_app/menu.html',{'page':page,'data':data,"ID":ID,'val':val,'selec':selec,'num':num,'del_num':num,'l':l,'number':number,'sum_hbase_mysql':sum_hbase_mysql})






def get_captcha(request):
    image=ImageCaptcha(fonts=[os.path.abspath('font/segoesc.ttf')])
    code_list=random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,4)
    code="".join(code_list)
    request.session['code']=code
    print(code)
    data=image.generate(code)
    return HttpResponse(data,'image/png')

def trance_captcha(request):
    return render(request,'main_app/captcha.html')

def check_capt(request):
    capt=request.GET.get('capt')
    code=request.session.get('code')
    if capt==code:
        return redirect('main:ms')
    return redirect('main:trance')


def key_up(request):

        val=request.GET.get('val')
        selec=request.GET.get('selec')
        rs=[]

        def myconverter(a):
            if isinstance(a,Projects):
                return {"id":a.id,'title':a.title,'salary':a.salary,"academics":a.academics,'experience':a.experience,'company':a.company,'city':a.city,'describes':a.describes}
        if selec=='1':

            result=Projects.objects.filter(city__contains=val)[:5]

            return JsonResponse({'rs':list(result)},json_dumps_params={'default':myconverter})
        elif selec=='2':

            result=Projects.objects.filter(title__contains=val)[:5]
            return JsonResponse({'rs': list(result)}, json_dumps_params={'default': myconverter})








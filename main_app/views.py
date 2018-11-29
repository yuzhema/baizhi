import os,random,string,time,happybase,requests
from lxml import etree

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from main_app.models import Projects
from main_app.tools.image import ImageCaptcha

import happybase
connection=happybase.Connection(host='172.16.14.84',port=9090)
connection.open()
table=connection.table('AI133:t_project')
info=table.scan(columns=('choosed',))



def display(request):
    labal=request.session.get('labal')

    return render(request,'main_app/main.html')


def intro(request):

    return render(request,'main_app/introduce.html')


#通过ip地址查询用户所在地
def ip_address(ip):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
    html=requests.post('http://ip.tool.chinaz.com/{}'.format(ip),headers=headers).text
    labal=etree.HTML(html)
    address=labal.xpath('//p[@class="WhwtdWrap bor-b1s col-gray03"]/span/text()')[-1]
    return address

#插件，日志
def logs(fun):
    def cha(args):
        t=time.localtime()
        years=t.tm_year
        month=t.tm_mon
        day=t.tm_mday
        hours=t.tm_hour
        minute=t.tm_min
        visit_time=str(years)+'-'+str(month)+'-'+str(day)+' '+str(hours)+':'+str(minute)
        ID=args.GET.get('ID')
        username=args.session.get('username')
        ip=args.META['HTTP_HOST']
        address=ip_address(ip)
        if ID:
            if 1<=int(ID)<=4:
                city='北京'
            elif 6<int(ID)<9:
                city='上海'
            elif 9<=int(ID)<13:
                city='广州'
            else:
                city='深圳'
            if ID in ['1', '5', '9', '13']:
                jobs='python web'
            elif ID in ['2','6','10','14']:
                jobs='爬虫'
            elif ID in ['3','7','11','15']:
                jobs='大数据'
            else:
                jobs='AI'
        else:
            ID=''
            jobs=''
        if not username:
            username=ip
        connection = happybase.Connection(host='172.16.14.84', port=9090)
        connection.open()
        table = connection.table('AI133:journal_file')
        table.put(str(time.time()),{'daily:username':username,'daily:address':address,'daily:visit_time':visit_time,'daily:jobs':jobs,'daily:city':city})
        return fun(args)

    return cha

@logs
def ms(request):
    #左边栏点击的是哪个
    ID=request.GET.get('ID')
    #搜索框传来的数据
    val=request.GET.get('val')
    selec=request.GET.get('selec')
    if "Mozilla/5.0" not in request.META['HTTP_USER_AGENT']:
        return render(request,'main_app/404.html')
    num = request.GET.get('num')
    labal=request.session.get('labal')
    if not num:
        num=1
    if not labal:
        if int(num)>10:
            num=1
    else:
        if int(labal)>100:
            request.session['labal'] = 50
            num=50
        request.session['labal'] = int(labal) + 1

    #判断是不是从搜索条件处转来的
    if val and selec and val!='None' and selec!='None':

        if selec=='1':
            data=Projects.objects.filter(city__contains=val)
        else:
            data=Projects.objects.filter(title__contains=val)
    else:
        # 从hbase中获取数据
        if int(num)>5:
            for i in list(info)[(int(num) - 6) * 20:(int(num) - 5) * 20]:
                for j, k in i[1].items():
                    d.update({j.decode().split(':')[1]: k.decode()})
                l.append(d)
            return render(request, 'main_app/menu.html', {'l': l})

        if ID=='1':
            data=Projects.objects.filter(city__contains='北京',title__icontains='web')

        elif ID=='2':
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
    page = Paginator(object_list=data, per_page=20).page(int(num))

    return render(request,'main_app/menu.html',{'page':page,'data':data,"ID":ID,'val':val,'selec':selec})



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








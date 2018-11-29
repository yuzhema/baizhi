from django.shortcuts import render
from main_app.models import Projects
import happybase
# Create your views here.
connection=happybase.Connection(host='172.16.14.84',port=9090)
connection.open()
table=connection.table('AI133:t_project')
#柱状图
def bars(request):
    #查询四大城市招聘数量
    beijing=Projects.objects.filter(city__contains='北京').count()
    shanghai=Projects.objects.filter(city__contains='上海').count()
    guangzhou=Projects.objects.filter(city__contains='广州').count()
    shenzhen=Projects.objects.filter(city__contains='深圳').count()
    scanner=table.scan(columns=("refused",))
    for key,value in scanner:
        city=value[b'refused:city'].decode()
        if '北京' in city:
            beijing+=1
        elif '上海'in city:
            shanghai+=1
        elif '广州'in city:
            guangzhou+=1
        elif '深圳'in city:
            shenzhen+=1
    return render(request,"echarts/柱状图.html",{'beijing':beijing,'shanghai':shanghai,'guangzhou':guangzhou,'shenzhen':shenzhen})
def pie(request):
    #查询四大城市招聘数量
    web=Projects.objects.filter(title__icontains='web').count()
    ai=Projects.objects.filter(title__icontains='ai').count()
    big_data=Projects.objects.filter(title__icontains='数据').count()
    crawl=Projects.objects.filter(title__icontains='爬虫').count()
    scanner=table.scan(columns=("choosed",))
    for key,value in scanner:
        title=value[b'choosed:title'].decode()
        if 'web' in title or 'Web' in title or 'WEB'in title:
            web+=1
        elif 'ai'in title or 'AI' in title or 'Ai' in title or '算法'in title:
            ai+=1
        elif '数据'in title:
            big_data+=1
        elif '爬虫'in title:
            crawl+=1
    return render(request,"echarts/饼图.html",{'web':web,'ai':ai,'big_data':big_data,'crawl':crawl})

def maps(request):
    table = connection.table('AI133:journal_file')
    scanner = table.scan(columns=("daily",))
    city_count=[0 for i in range(34)]
    city_list=['北京','天津','上海','重庆','河北','河南','云南','辽宁','黑龙江','湖南','安徽', '山东',  '新疆', '江苏','浙江', '江西','湖北', '广西', '甘肃', '山西', '内蒙古', '陕西', '吉林', '福建', '贵州', '广东', '青海', '西藏', '四川', '宁夏', '海南', '台湾', '香港', '澳门']
    for i in range(34):
        for key,value in scanner:
            city=value[b'daily:address'].decode()
            if city==city_list[i]:
                city_count[i]+=1
    return render(request,'echarts/地图.html',{'counts':city_count})
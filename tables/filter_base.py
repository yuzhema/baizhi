import happybase

from main_app.models import Projects

connection=happybase.Connection(host='172.16.14.84',port=9090)
connection.open()
table=connection.table('AI133:t_project')
city_list=['北京','上海','广州','深圳']
job_list=['web','爬','数据','ai']
detail_list=[(i,j)for i in city_list for j in job_list]
scanner=table.scan(columns=("choosed",))
def sum_count():
    bj_web=Projects.objects.filter(city__contains='北京', title__icontains='web').count()
    bj_crawl=Projects.objects.filter(city__contains='北京', title__contains='爬').count()
    bj_data=Projects.objects.filter(city__contains='北京', title__contains='数据').count()
    bj_ai=Projects.objects.filter(city__contains='北京', title__icontains='ai').count()
    sh_web=Projects.objects.filter(city__contains='上海', title__icontains='web').count()
    sh_crawl=Projects.objects.filter(city__contains='上海', title__contains='爬').count()
    sh_data=Projects.objects.filter(city__contains='上海', title__contains='数据').count()
    sh_ai=Projects.objects.filter(city__contains='上海', title__icontains='ai').count()
    gz_web=Projects.objects.filter(city__contains='广州', title__icontains='web').count()
    gz_crawl=Projects.objects.filter(city__contains='广州', title__contains='爬').count()
    gz_data=Projects.objects.filter(city__contains='广州', title__contains='数据').count()
    gz_ai=Projects.objects.filter(city__contains='广州', title__icontains='ai').count()
    sz_web=Projects.objects.filter(city__contains='深圳', title__icontains='web').count()
    sz_crawl=Projects.objects.filter(city__contains='深圳', title__contains='爬').count()
    sz_data=Projects.objects.filter(city__contains='深圳', title__contains='数据').count()
    sz_ai=Projects.objects.filter(city__contains='深圳', title__icontains='ai').count()
    return bj_web,bj_crawl,bj_data, bj_ai,sh_web,sh_crawl,sh_data,sh_ai,gz_web,gz_crawl,gz_data,gz_ai,sz_web,sz_crawl,sz_data,sz_ai
def hbase_list():
    global detail_list
    c=list(sum_count())
    num=0
    for key,value in scanner:
        for i in range(16):
            if detail_list[i][0] in (key.decode()) and detail_list[i][1] in (key.decode()):
                c[i]+=1
    return c

                    


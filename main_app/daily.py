#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/28 11:06
# @Author  : Ryu
# @Site    :
# @File    : daily.py
# @Software: PyCharm




#插件，日志
from lxml import etree

import happybase
import time

#通过ip地址查询用户所在地
import requests


def ip_address(ip):
    try:
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
        html=requests.post('http://ip.tool.chinaz.com/{}'.format(ip),headers=headers).text
        labal=etree.HTML(html)
        address=labal.xpath('//p[@class="WhwtdWrap bor-b1s col-gray03"]/span/text()')[-1]
    except:
        address=''
    return address



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
        val=args.GET.get('val')
        selec=args.GET.get('selec')
        address=ip_address(ip)
        if selec and val:
            if selec=='1':

                if val in '北京-东城区,北京-朝阳区,北京-海淀区' or '北京' in val:
                    city='北京'
                elif val in '上海' or '上' in val or '海' in val:
                    city='上海'
                elif val in '广州' or '广州' in val:
                    city='广州'
                elif val in '深圳' or '深圳' in val:
                    city='深圳'
                else:
                    city=''
                jobs=''
            else:

                if val in 'Python,python,PYTHON,WEB,web,Web,全栈' or 'python' in val or 'web' in val or 'Web' in val or 'WEB' in val or '后台' in val or '全栈' in val:
                    jobs='python web'
                elif val in '爬虫，搜索' or '爬虫' in val or '搜索' in val:
                    jobs='爬虫'
                elif val in '大数据,算法' or '数据' in val or '算法' in val:
                    jobs='大数据'
                elif val in 'ai,AI,智能' or 'ai' in val or 'AI' in val or '智能' in val:
                    jobs='AI'
                else:
                    jobs=''
                city=''


        else :

            if 1<=int(ID)<=4:
                city='北京'
            elif 3<int(ID)<9:
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
        if not username:
            username=ip
        connection = happybase.Connection(host='172.16.14.77', port=9090)
        connection.open()
        table = connection.table('AI133:journal_file')
        table.put(str(int(time.time())),{'daily:username':username,'daily:address':address,'daily:visit_time':visit_time,'daily:jobs':jobs,'daily:city':city})
        return fun(args)

    return cha
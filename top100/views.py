from django.shortcuts import render
from .models import Relations,Customer,Interface,Attack
from django.http import HttpResponse,StreamingHttpResponse
import os
from .webtools import db_connection
import urllib
import urllib.parse
import json
from django.utils.safestring import mark_safe
import time
import datetime
import calendar
from elasticsearch import Elasticsearch
# Create your views here.



def get_timestamp(str):
    str = str+" 00:00:00"
    return int(time.mktime(time.strptime(str,'%Y-%m-%d %H:%M:%S')))

def getstart_end(year,month):
    time = datetime.date(int(year), int(month), 15)
    first_day = datetime.date(time.year, time.month, 1) #获取本月第一天
    days_num = calendar.monthrange(first_day.year, first_day.month)[1] #获取一个月有多少天
    first_day_of_next_month = first_day + datetime.timedelta(days = days_num)
    return get_timestamp(str(first_day)),get_timestamp(str(first_day_of_next_month))-1

def elastic(ip,port,index):
    ## 创建连接
    es = Elasticsearch([{'host': 'xx.xx.xx.xx', 'port': 9200, 'timeout': 10000}])
    ## 闪断次数
    flash = 0
    ## 端口总中断时间
    duration_all = 0
    ## 输出的信息
    info = {}
    detail = []
    ## 错误时输出的信息
    info_Exception = []
    ## 端口down的时间戳列表
    list_downtime = []
    ## 端口断开总时长
    try:
        ## 端口down,up查询语句
        question_down = 'host:"{}" AND message:"{}" AND message:"down"'.format(ip,port)
        question_up = 'host:"{}" AND message:"{}" AND message:"up"'.format(ip,port)
        # print(question_down)
        res_down = es.search(index=index,q=question_down,size=10000)
        # print(res_down)

        for hit_down in res_down['hits']['hits']:
            downtime_str = hit_down['_source']['@timestamp']
            downtime_float = downtime_str[:-5]
            downtime_struct = datetime.datetime.strptime(downtime_float, '%Y-%m-%dT%H:%M:%S')
            downtime_stamp = time.mktime(downtime_struct.timetuple())
            list_downtime.append(downtime_stamp)
            list_downtime.sort()
            # print('list_downtime:{}'.format(list_downtime))

        ## 列表去重
        list_downtime = list(set(list_downtime))
        # print('list_downtime:{}'.format(list_downtime))

        for downtime in list_downtime:
            # print('downtime:{}'.format(downtime))
            list_uptime = []
            res_up = es.search(index=index, q=question_up, size=10000)
            # print('res_up：{}'.format(res_up))
            for hit_up in res_up['hits']['hits']:
                uptime_str = hit_up['_source']['@timestamp']
                uptime_float = uptime_str[:-5]
                uptime_struct = datetime.datetime.strptime(uptime_float, '%Y-%m-%dT%H:%M:%S')
                uptime_stamp = time.mktime(uptime_struct.timetuple())
                if uptime_stamp >= downtime:
                    list_uptime.append(uptime_stamp)
            list_uptime.sort()
            uptime = list_uptime[0]
            # print('uptime:{}'.format(uptime))
            ## 断开时长
            duration = uptime - downtime
            duration_all += duration
            # print('duration:{}'.format(duration))
            # print('duration_all:{}'.format(duration_all))
            ## 端口闪断
            if duration == 0:
                flash += 1

            ## 将时间戳转化为时间
            downtime_local = time.localtime(downtime)
            # print('downtime_local:{}'.format(downtime_local))
            downtime_view = time.strftime("%Y-%m-%d %H:%M:%S", downtime_local)
            # print('downtime_view:{}'.format(downtime_view))

            uptime_local = time.localtime(uptime)
            # print('uptime_local:{}'.format(uptime_local))
            uptime_view = time.strftime("%Y-%m-%d %H:%M:%S", uptime_local)
            # print('uptime_view:{}'.format(uptime_view))

            ## 追加到info
            info_dic = {}
            info_dic['downtime'] = downtime_view
            info_dic['uptime'] = uptime_view
            info_dic['duration'] = duration
            # print('info_dic:{}'.format(info_dic))
            detail.append(info_dic)
        ## 可用率
        ratio = (1 - (duration_all / (30 * 24 * 60 * 60))) * 100
        ratio = round(ratio,2)
        # print('ratio:{}'.format(ratio))
        # print('detail:{}'.format(detail))
        # print('flash:{}'.format(flash))
        info['detail'] = detail
        info['flash'] = flash
        info['ratio'] = ratio
        print(info)

        return info

    except Exception:
        exception = 'Exception'
        return exception



def yuebao(request):
    code = request.GET.get("code")
    year = request.GET.get("year")
    month = request.GET.get("month")
    result_cust = list(db_connection.db_12_boss.query("select * from vnet_zz_port where code = '%s' group by port_code_key" % (code)))
    ctx = {}
    ctx['port_list'] = result_cust
    cust_name = result_cust[0]['name']
    print('cust_name：{}\n______'.format(cust_name))

    #生成时间戳
    start_times,end_times = getstart_end(year, month)
    ctx['start_timestamp'] = start_times
    ctx['end_timestamp'] = end_times
    ctx['year'] = year
    ctx['month'] = month


    # urllib
    response = urllib.request.urlopen(r'http://xx.xx.xx.xx/nusoap/custclient.php?code=%s' % (code))
    page = response.read()
    page = page.decode('utf-8')
    php_json = json.loads(page)
    temp_list = []
    for php_one in php_json[0]['interfacerlist']:
        temp = {}
        temp['name'] = php_one['contactName']
        temp['type'] = php_one['type']
        temp_list.append(temp)
    # print('temp_list：{}\n______'.format(temp_list))

    inter_list = temp_list
    inter_list_format = []
    for inter_person in inter_list:
        if inter_person in inter_list_format:
            continue
        else:
            if inter_person['type'] != "SF":
                inter_list_format.append(inter_person)
    print('person_list：{}\n______'.format(inter_list_format))

    cust_name_utf8 = urllib.parse.quote(cust_name)
    url_80 = 'http://xx.xx.xx.xx/index.php/Home/Flow/getjson/name/{}.html'.format(cust_name_utf8)
    # print(url_80)
    response = urllib.request.urlopen(url_80)
    page = response.read()
    page = page.decode('utf-8')
    php_json = json.loads(page)
    graph_list = []
    for php_json_single in php_json:
        graph_list.append(php_json_single['local_graph_id'])
    # print(graph_list)
    print('graph_list：{}\n______'.format(graph_list))


    # elastic模块
    # 从5.12获取设备名及端口对照表
    device_sqllist = db_connection.db_12_boss.query('SELECT common_name,ipv4 from vnet_ipdb_items')
    device_list = list(device_sqllist)
    device_name_list = [] #对照表
    for device in device_list:
        device_name_list.append(device['common_name'])
    # print(device_name_list)
    # 判断该客户的设备是否在5.12设备列表中，如存在，返回设备ip
    search_list = []
    for result_cust_single in result_cust:
        device_name = result_cust_single['wl_device_name']
        device_interface = result_cust_single['port_desc']
        # print(device_interface)
        for device_single in device_list:
            search_list_dic = {}
            if device_single['common_name'] == device_name:
                search_list_dic['ip'] = device_single['ipv4']
                search_list_dic['port'] = device_interface
                search_list_dic['name'] = device_name
                search_list.append(search_list_dic)
    # print(search_list)   #设备ip和端口对照表
    #拼出当月索引
    month_str = ''
    if int(month) < 10:
        month_str = "0" + str(month)
    es_index = 'ordinary-' + year + '.' + month_str + '*'
    # print(es_index)

    for search in search_list:

        # search_ip = search['ip']
        # search_port = search['port']
        # # print("search:{}".format(search))
        # search_info = elastic(search_ip,search_port,es_index)
        # search['flash'] = search_info['flash']
        # search['ratio'] = search_info['ratio']
        # if len(search_info['detail']):
        #     search['detail'] = search_info['detail']
        # else:
        #     search_info_empty = []
        #     search_info_dic_empty = {}
        #     downtime_empty = '-'
        #     uptime_empty = '-'
        #     duration_empty = '-'
        #     search_info_dic_empty['downtime'] = downtime_empty
        #     search_info_dic_empty['uptime'] = uptime_empty
        #     search_info_dic_empty['duration'] = duration_empty
        #     search_info_empty.append(search_info_dic_empty)
        #     print('search_info_empty:{}'.format(search_info_empty))
        #     search['detail'] = search_info_empty
        # # print("search:{}".format(search))

        print("search:{}".format(search))
        search['downtime'] = ''
        search['uptime'] = ''
        search['duration'] = ''

    # print(search_list)
    ctx['search_list'] = search_list




    ctx['custname'] = cust_name
    ctx['person_list'] = inter_list_format
    ctx['graphid_list'] = graph_list
    # print(ctx)
    return render(request,'yuebao.html',ctx)



def download_file(request):
    one = request.GET.get("code")
    two = request.GET.get("year")
    three = request.GET.get("month")
    file_name = "%s_%s_%s.pdf" % (one,two,three)
    os.system("python /root/status/top100/htmltopdf.py %s %s %s" % (one,two,three))
    #next
    the_file_name = '/etc/script/'+ file_name
    fileget = open(the_file_name,'rb')
    response = StreamingHttpResponse(fileget)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachement;filename="{0}"'.format(file_name)
    return response
    #return HttpResponse('11111')


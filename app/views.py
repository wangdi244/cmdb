#! /usr/bin/env python 
#encoding=utf-8
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render
from django.template import Template,loader,RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import auth
from django import  forms
from app.models import *
from app.backend.saltapi  import SaltAPI
from app.backend.asset_info import *
import MySQLdb as mysql
import ConfigParser,sys,json,os,time,pickle
from app import common
from app import html_helper
from app import html_helper_idc
from models import User
from django.contrib.sessions.models import Session
import datetime
from app.form import NewUserForm
from cmdb.settings import ALLOWED_HOSTS

db = mysql.connect(host="192.168.31.250",user="root", passwd="123456", db="monitor", charset="utf8")
db.autocommit(True)
c = db.cursor()

def saltstack():
    config = ConfigParser.ConfigParser()  
    config.read("D:\\eclipse\\work\\cmdb\\app\\backend\\config.ini")
    url = config.get("saltstack","url")
    user = config.get("saltstack","user")
    passwd = config.get("saltstack","pass")
    device = config.get("network","device")
    result_api={'url':url,'user':user,'passwd':passwd,'device':device}
    return result_api

def wirte_track_mark(num):
    f = open("D:\\eclipse\\work\\cmdb\\app\\backend\\track_num.conf",'w')
    try:
        f.write(num)
    finally:
        f.close()
    return "ok"

def read_track_mark():
    f = open("D:\\eclipse\\work\\cmdb\\app\\backend\\track_num.conf")
    try:
	num = f.read()
    finally:
	f.close()
    return num

def date_result(data):
    timeArray = time.strptime(data, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray)) - 50400
    return timeStamp
 
@login_required
def index(request): 
    total_idc =Idc.objects.aggregate(Count('idc_name'))
    idc_num = total_idc["idc_name__count"]
    total_host = HostList.objects.aggregate(Count('hostname'))
    host_num = total_host["hostname__count"]
    login_user = request.user
    online_sessions = Session.objects.filter(expire_date__gte=datetime.datetime.now())
    count = online_sessions.count()
    return render_to_response("index.html",locals()) 

def login(request):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    return render_to_response("login.html")

def logout(request):
    try:
        del request.session['username']
    except Exception,e:
        print e.message
    return render_to_response("login.html")
    

def authin(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    total_idc =Idc.objects.aggregate(Count('idc_name'))
    idc_num = total_idc["idc_name__count"]
    user = auth.authenticate(username=username,password=password)
    total_host = HostList.objects.aggregate(Count('hostname'))
    host_num = total_host["hostname__count"]
    if user is not None:
        auth.login(request,user)
        online_sessions = Session.objects.filter(expire_date__gte=datetime.datetime.now())
        count = online_sessions.count()
        role= NewUser.objects.filter(username=username).values("manage_role")[0]['manage_role']
        if role in u'manage':
            return  render_to_response('index_manage.html',{'login_user':request.user,
                                                     'idc_num':idc_num,
                                                     'host_num':host_num,
                                                     'count':count})
        else:
            return  render_to_response('index.html',{'login_user':request.user,
                                                     'idc_num':idc_num,
                                                     'host_num':host_num,
                                                     'count':count})
    else:
        return render_to_response('login.html',{'login_err':'Wrong username or password'})

@login_required
def idc(request,page):
    all_idc = Idc.objects.all()
    per_item = 5
    page = common.try_int(page, 1)
    count = Idc.objects.all().count()
    pageObj = html_helper_idc.PageInfo(page,count,per_item)
    result = Idc.objects.all()[pageObj.start:pageObj.end]
    page_string = html_helper_idc.Page(page,pageObj.all_page_count)
    ret = {'data':result,'count':count,'page':page_string}
    response = render_to_response('idc.html',ret)
    response.set_cookie('page_num',per_item)
    return response
    return render_to_response("idc.html",{'data':all_idc})



@login_required
def addidc(request):
    nameInput = request.GET['idc_name'] 
    msgInput = request.GET['idc_remark'] 
    addressInput = request.GET['idc_address']
    idc_add = Idc(idc_name=nameInput,remark=msgInput,idc_address=addressInput)
    idc_add.save()
    return HttpResponse('ok')

@login_required
def idc_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        Idc.objects.filter(id=id).delete()
        return HttpResponseRedirect('/idc/')
    
@login_required
def mac(request):
    all_host = HostList.objects.all()
    all_idc = Idc.objects.all()
    return render_to_response("mac.html",locals())

@login_required
def mac_develop(request):
    all_host = HostList_Develop.objects.all()
    all_idc = Idc.objects.all()
    return render_to_response("mac_develop.html",locals())

@login_required
def mac_test(request):
    all_host = HostList_Test.objects.all()
    all_idc = Idc.objects.all()
    return render_to_response("mac_test.html",locals())

@login_required
def mac_pre_release(request):
    all_host = HostList_Pre_Release.objects.all()
    all_idc = Idc.objects.all()
    return render_to_response("mac_pre_release.html",locals())

@login_required
def addmac(request):
    if request.method == 'GET':
        name = request.GET['name']
        ip = request.GET['ip'] 
        idc_name = request.GET['idc_name']
        service = request.GET['service']
        idc_bh = request.GET['idc_jg'] 
        manage_ip = request.GET['manage_ip']
        mac_add = HostList(ip=ip,
                           hostname=name,
                           application=service,
                           idc_name=idc_name,
                           bianhao=idc_bh,
                           manage_ip=manage_ip) 
        mac_add.save()
        return HttpResponse('ok')

@login_required
def addmac_develop(request):
    if request.method == 'GET':
        name = request.GET['name']
        ip = request.GET['ip'] 
        idc_name = request.GET['idc_name']
        service = request.GET['service']
        idc_bh = request.GET['idc_jg'] 
        manage_ip = request.GET['manage_ip']
        mac_add = HostList_Develop(ip=ip,
                           hostname=name,
                           application=service,
                           idc_name=idc_name,
                           bianhao=idc_bh,
                           manage_ip=manage_ip) 
        mac_add.save()
        return HttpResponse('ok')

@login_required
def addmac_test(request):
    if request.method == 'GET':
        name = request.GET['name']
        ip = request.GET['ip'] 
        idc_name = request.GET['idc_name']
        service = request.GET['service']
        idc_bh = request.GET['idc_jg'] 
        manage_ip = request.GET['manage_ip']
        mac_add = HostList_Test(ip=ip,
                           hostname=name,
                           application=service,
                           idc_name=idc_name,
                           bianhao=idc_bh,
                           manage_ip=manage_ip) 
        mac_add.save()
        return HttpResponse('ok')

@login_required
def addmac_pre_release(request):
    if request.method == 'GET':
        name = request.GET['name']
        ip = request.GET['ip'] 
        idc_name = request.GET['idc_name']
        service = request.GET['service']
        idc_bh = request.GET['idc_jg'] 
        manage_ip = request.GET['manage_ip']
        mac_add = HostList_Pre_Release(ip=ip,
                           hostname=name,
                           application=service,
                           idc_name=idc_name,
                           bianhao=idc_bh,
                           manage_ip=manage_ip) 
        mac_add.save()
        return HttpResponse('ok')


@login_required
def mac_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        HostList.objects.filter(id=id).delete()
        return HttpResponseRedirect('/mac/')

@login_required
def mac_develp_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        HostList_Develop.objects.filter(id=id).delete()
        return HttpResponseRedirect('/mac_develop/')

@login_required
def mac_test_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        HostList_Test.objects.filter(id=id).delete()
        return HttpResponseRedirect('/mac_test/')
    
@login_required
def mac_pre_release_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        HostList_Pre_Release.objects.filter(id=id).delete()
        return HttpResponseRedirect('/mac_pre_release/')

@login_required
def mac_edit(request,id=None):
    id = request.GET.get('id')
    all_idc = Idc.objects.all()   
    if request.method == 'GET':
        all_host=HostList.objects.filter(id=id)
	return render_to_response("mac_edit.html",locals())

@login_required
def mac_develop_edit(request,id=None):
    id = request.GET.get('id')
    all_idc = Idc.objects.all()   
    if request.method == 'GET':
        all_host=HostList_Develop.objects.filter(id=id)
    return render_to_response("mac_develop_edit.html",locals())

@login_required
def mac_test_edit(request,id=None):
    id = request.GET.get('id')
    all_idc = Idc.objects.all()   
    if request.method == 'GET':
        all_host=HostList_Test.objects.filter(id=id)
    return render_to_response("mac_test_edit.html",locals())

@login_required
def mac_pre_release_edit(request,id=None):
    id = request.GET.get('id')
    all_idc = Idc.objects.all()   
    if request.method == 'GET':
        all_host=HostList_Pre_Release.objects.filter(id=id)
    return render_to_response("mac_pre_release_edit.html",locals())

@login_required
def mac_check_host(request):
    idc_name = request.GET['idc_name']
    result = HostList.objects.filter(idc_name=idc_name)
    return render_to_response("check_hostlist.html",{'data':result})

@login_required
def macresult(request):
    if request.method =='GET':
        id = request.GET['id']
        ip = request.GET['ip']
        name = request.GET['name']
        idc_name = request.GET['idc_name']
        service = request.GET['service']
        idc_bh = request.GET['idc_jg']
        manage_ip = request.GET['manage_ip']
        try:
            mac_update = HostList.objects.filter(id=id).update(ip=ip,
                                                               hostname=name,
                                                               application=service,
                                                               idc_name=idc_name,
                                                               bianhao=idc_bh,
                                                               manage_ip=manage_ip)
            mac_update.save()
        except:
            print "get exception"
        finally: 
            host = ALLOWED_HOSTS[0]
            HOST = "http://%s/mac/" %host
            send = {'value':'ok','loginUrl':HOST}
            return HttpResponse(json.dumps(send)) 

@login_required
def macresult_develop(request):
    if request.method =='GET':
        id = request.GET['id']
        ip = request.GET['ip']
        name = request.GET['name']
        idc_name = request.GET['idc_name']
        service = request.GET['service']
        idc_bh = request.GET['idc_jg']
        manage_ip = request.GET['manage_ip']
        try:
            mac_update = HostList_Develop.objects.filter(id=id).update(ip=ip,
                                                               hostname=name,
                                                               application=service,
                                                               idc_name=idc_name,
                                                               bianhao=idc_bh,
                                                               manage_ip=manage_ip)
            mac_update.save()
        except:
            print "get exception"
        finally: 
            host = ALLOWED_HOSTS[0]
            HOST = "http://%s/mac_develop/" %host
            send = {'value':'ok','loginUrl':HOST}
            return HttpResponse(json.dumps(send)) 

@login_required
def macresult_test(request):
    if request.method =='GET':
        id = request.GET['id']
        ip = request.GET['ip']
        name = request.GET['name']
        idc_name = request.GET['idc_name']
        service = request.GET['service']
        idc_bh = request.GET['idc_jg']
        manage_ip = request.GET['manage_ip']
        try:
            mac_update = HostList_Test.objects.filter(id=id).update(ip=ip,
                                                               hostname=name,
                                                               application=service,
                                                               idc_name=idc_name,
                                                               bianhao=idc_bh,
                                                               manage_ip=manage_ip)
            mac_update.save()
        except:
            print "get exception"
        finally: 
            host = ALLOWED_HOSTS[0]
            HOST = "http://%s/mac_test/" %host
            send = {'value':'ok','loginUrl':HOST}
            return HttpResponse(json.dumps(send))

@login_required
def macresult_pre_release(request):
    if request.method =='GET':
        id = request.GET['id']
        ip = request.GET['ip']
        name = request.GET['name']
        idc_name = request.GET['idc_name']
        service = request.GET['service']
        idc_bh = request.GET['idc_jg']
        manage_ip = request.GET['manage_ip']
        try:
            mac_update = HostList_Pre_Release.objects.filter(id=id).update(ip=ip,
                                                               hostname=name,
                                                               application=service,
                                                               idc_name=idc_name,
                                                               bianhao=idc_bh,
                                                               manage_ip=manage_ip)
            mac_update.save()
        except:
            print "get exception"
        finally: 
            host = ALLOWED_HOSTS[0]
            HOST = "http://%s/mac_pre_release/" %host
            send = {'value':'ok','loginUrl':HOST}
            return HttpResponse(json.dumps(send))  


@login_required
def contain(request,page):
    all_contain = ContainsList.objects.all()
    all_contain_of_host = HostList.objects.all()
    per_item = 15
    page = common.try_int(page, 1)
    count = ContainsList.objects.all().count()
    pageObj = html_helper.PageInfo(page,count,per_item)
    result = ContainsList.objects.all()[pageObj.start:pageObj.end]
    page_string = html_helper.Page(page,pageObj.all_page_count)
    ret = {'data':result,'count':count,'page':page_string}
    response = render_to_response('contain.html',ret)
    response.set_cookie('page_num',per_item)
    return response
    return render_to_response("contain.html",{'data':all_contain})

@login_required
def contain_develop(request,page):
    all_contain = ContainsList_Develop.objects.all()
    all_contain_of_host = HostList_Develop.objects.all()
    per_item = 15
    page = common.try_int(page, 1)
    count = ContainsList_Develop.objects.all().count()
    pageObj = html_helper.PageInfo(page,count,per_item)
    result = ContainsList_Develop.objects.all()[pageObj.start:pageObj.end]
    page_string = html_helper.Page(page,pageObj.all_page_count)
    ret = {'data':result,'count':count,'page':page_string}
    response = render_to_response('contain_develop.html',ret)
    response.set_cookie('page_num',per_item)
    return response
    return render_to_response("contain_develop.html",{'data':all_contain})

@login_required
def contain_test(request,page):
    all_contain = ContainsList_Test.objects.all()
    all_contain_of_host = HostList_Test.objects.all()
    per_item = 15
    page = common.try_int(page, 1)
    count = ContainsList_Test.objects.all().count()
    pageObj = html_helper.PageInfo(page,count,per_item)
    result = ContainsList_Test.objects.all()[pageObj.start:pageObj.end]
    page_string = html_helper.Page(page,pageObj.all_page_count)
    ret = {'data':result,'count':count,'page':page_string}
    response = render_to_response('contain_test.html',ret)
    response.set_cookie('page_num',per_item)
    return response
    return render_to_response("contain_test.html",{'data':all_contain})

@login_required
def contain_pre_release(request,page):
    all_contain = ContainsList_Pre_Release.objects.all()
    all_contain_of_host = HostList_Pre_Release.objects.all()
    per_item = 15
    page = common.try_int(page, 1)
    count = ContainsList_Pre_Release.objects.all().count()
    pageObj = html_helper.PageInfo(page,count,per_item)
    result = ContainsList_Pre_Release.objects.all()[pageObj.start:pageObj.end]
    page_string = html_helper.Page(page,pageObj.all_page_count)
    ret = {'data':result,'count':count,'page':page_string}
    response = render_to_response('contain_pre_release.html',ret)
    response.set_cookie('page_num',per_item)
    return response
    return render_to_response("contain_pre_release.html",{'data':all_contain})

@login_required
def addcontain(request):
    if request.method == 'GET':
        contain_department = request.GET["contain_department"]
        contain_service = request.GET["contain_service"]
        contain_development = request.GET["contain_development"]
        contain_num = request.GET["contain_num"]
        contain_num = int(contain_num.decode("utf-8"))
        for i in range(0,contain_num):
            ContainsList.objects.create(contain_id = "",
                         contain_ip = "",
                         contain_netmask = "",
                         contain_port = "",
                         contain_http = "",
                         create_datetime = "",
                         contain_cpu_core = "",
                         contain_host = "",
                         contain_memory = "",
                         contain_hostname = "",
                         service_pack = "",
                         service_depend = "",
                         service_env = "",
                         project_name = "",
                         principal = "",
                         state = "",
                         flag = "",
                         x_flag= "", 
                         project_section = contain_department,
                         release_application = contain_service,
                         proposer = contain_development)
        return HttpResponse('ok')

@login_required
def addcontain_develop(request):
    if request.method == 'GET':
        contain_department = request.GET["contain_department"]
        contain_service = request.GET["contain_service"]
        contain_development = request.GET["contain_development"]
        contain_num = request.GET["contain_num"]
        contain_num = int(contain_num.decode("utf-8"))
        for i in range(0,contain_num):
            ContainsList_Develop.objects.create(contain_id = "",
                         contain_ip = "",
                         contain_netmask = "",
                         contain_port = "",
                         contain_http = "",
                         create_datetime = "",
                         contain_cpu_core = "",
                         contain_host = "",
                         contain_memory = "",
                         contain_hostname = "",
                         service_pack = "",
                         service_depend = "",
                         service_env = "",
                         project_name = "",
                         principal = "",
                         state = "",
                         flag = "",
                         x_flag= "", 
                         project_section = contain_department,
                         release_application = contain_service,
                         proposer = contain_development)
        return HttpResponse('ok')
    
@login_required
def addcontain_test(request):
    if request.method == 'GET':
        contain_department = request.GET["contain_department"]
        contain_service = request.GET["contain_service"]
        contain_development = request.GET["contain_development"]
        contain_num = request.GET["contain_num"]
        contain_num = int(contain_num.decode("utf-8"))
        for i in range(0,contain_num):
            ContainsList_Test.objects.create(contain_id = "",
                         contain_ip = "",
                         contain_netmask = "",
                         contain_port = "",
                         contain_http = "",
                         create_datetime = "",
                         contain_cpu_core = "",
                         contain_host = "",
                         contain_memory = "",
                         contain_hostname = "",
                         service_pack = "",
                         service_depend = "",
                         service_env = "",
                         project_name = "",
                         principal = "",
                         state = "",
                         flag = "",
                         x_flag= "", 
                         project_section = contain_department,
                         release_application = contain_service,
                         proposer = contain_development)
        return HttpResponse('ok')


@login_required
def addcontain_pre_release(request):
    if request.method == 'GET':
        contain_department = request.GET["contain_department"]
        contain_service = request.GET["contain_service"]
        contain_development = request.GET["contain_development"]
        contain_num = request.GET["contain_num"]
        contain_num = int(contain_num.decode("utf-8"))
        for i in range(0,contain_num):
            ContainsList_Pre_Release.objects.create(contain_id = "",
                         contain_ip = "",
                         contain_netmask = "",
                         contain_port = "",
                         contain_http = "",
                         create_datetime = "",
                         contain_cpu_core = "",
                         contain_host = "",
                         contain_memory = "",
                         contain_hostname = "",
                         service_pack = "",
                         service_depend = "",
                         service_env = "",
                         project_name = "",
                         principal = "",
                         state = "",
                         flag = "",
                         x_flag= "", 
                         project_section = contain_department,
                         release_application = contain_service,
                         proposer = contain_development)
        return HttpResponse('ok')

@login_required
def contain_edit(request,id=None):
    id = request.GET.get('id')
    all_host = HostList.objects.all()   
    if request.method == 'GET':
        all_contain=ContainsList.objects.filter(id=id)
    return render_to_response("contain_edit.html",locals())

@login_required
def contain_develop_edit(request,id=None):
    id = request.GET.get('id')
    all_host = HostList_Develop.objects.all()   
    if request.method == 'GET':
        all_contain=ContainsList_Develop.objects.filter(id=id)
    return render_to_response("contain_develop_edit.html",locals())

@login_required
def contain_test_edit(request,id=None):
    id = request.GET.get('id')
    all_host = HostList_Test.objects.all()   
    if request.method == 'GET':
        all_contain=ContainsList_Test.objects.filter(id=id)
    return render_to_response("contain_test_edit.html",locals())

@login_required
def contain_pre_release_edit(request,id=None):
    id = request.GET.get('id')
    all_host = HostList_Pre_Release.objects.all()   
    if request.method == 'GET':
        all_contain=ContainsList_Pre_Release.objects.filter(id=id)
    return render_to_response("contain_pre_release_edit.html",locals())

@login_required
def contain_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        ContainsList.objects.filter(id=id).delete()
        return HttpResponseRedirect('/contain/')
    
@login_required
def contain_develop_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        ContainsList_Develop.objects.filter(id=id).delete()
        return HttpResponseRedirect('/contain_develop/')

@login_required
def contain_test_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        ContainsList_Test.objects.filter(id=id).delete()
        return HttpResponseRedirect('/contain_test/')

@login_required
def contain_pre_release_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        ContainsList_Pre_Release.objects.filter(id=id).delete()
        return HttpResponseRedirect('/contain_pre_release/')

@login_required
def containresult(request):
    if request.method =='GET':
        id = request.GET['id']
        contain_id = request.GET['contain_id']
        contain_hostname = request.GET['contain_hostname']
        contain_ip = request.GET['contain_ip']
        contain_cpu = request.GET['contain_cpu']
        contain_memory = request.GET['contain_memory']
        host_ip = request.GET['host_ip']
        project_section = request.GET['project_section']
        release_application = request.GET['release_application']
        contain_netmask = request.GET['contain_netmask']
        contain_port = request.GET['contain_port']
        contain_http = request.GET['proposer']
        service_pack = request.GET['service_pack']
        service_env = request.GET['service_env']
        project_name = request.GET['project_name']
        principal = request.GET['principal']
        proposer = request.GET['proposer']
        service_depend = request.GET['service_depend']
        try:
            contain_update = ContainsList.objects.get(id=id)
            contain_update.contain_id=contain_id
            contain_update.contain_hostname=contain_hostname
            contain_update.contain_ip=contain_ip
            contain_update.contain_cpu_core=contain_cpu
            contain_update.contain_memory=contain_memory
            contain_update.contain_host=host_ip
            contain_update.project_section=project_section
            contain_update.release_application=release_application
            contain_update.proposer=proposer
            contain_update.contain_netmask=contain_netmask
            contain_update.contain_port=contain_port
            contain_update.contain_http=contain_http
            contain_update.service_pack=service_pack
            contain_update.service_env=service_env
            contain_update.project_name=project_name
            contain_update.principal=principal
            contain_update.service_depend=service_depend
            contain_update.save()
        except Exception,e:
            print e.message
        finally: 
            host = ALLOWED_HOSTS[0]
            HOST = "http://%s/contain/" %host
            send = {'value':'ok','loginUrl':HOST}
            return HttpResponse(json.dumps(send))  

@login_required
def containresult_develop(request):
    if request.method =='GET':
        id = request.GET['id']
        contain_id = request.GET['contain_id']
        contain_hostname = request.GET['contain_hostname']
        contain_ip = request.GET['contain_ip']
        contain_cpu = request.GET['contain_cpu']
        contain_memory = request.GET['contain_memory']
        host_ip = request.GET['host_ip']
        project_section = request.GET['project_section']
        release_application = request.GET['release_application']
        contain_netmask = request.GET['contain_netmask']
        contain_port = request.GET['contain_port']
        contain_http = request.GET['proposer']
        service_pack = request.GET['service_pack']
        service_env = request.GET['service_env']
        project_name = request.GET['project_name']
        principal = request.GET['principal']
        proposer = request.GET['proposer']
        service_depend = request.GET['service_depend']
        try:
            contain_update = ContainsList_Develop.objects.get(id=id)
            contain_update.contain_id=contain_id
            contain_update.contain_hostname=contain_hostname
            contain_update.contain_ip=contain_ip
            contain_update.contain_cpu_core=contain_cpu
            contain_update.contain_memory=contain_memory
            contain_update.contain_host=host_ip
            contain_update.project_section=project_section
            contain_update.release_application=release_application
            contain_update.proposer=proposer
            contain_update.contain_netmask=contain_netmask
            contain_update.contain_port=contain_port
            contain_update.contain_http=contain_http
            contain_update.service_pack=service_pack
            contain_update.service_env=service_env
            contain_update.project_name=project_name
            contain_update.principal=principal
            contain_update.service_depend=service_depend
            contain_update.save()
        except Exception,e:
            print e.message
        finally: 
            host = ALLOWED_HOSTS[0]
            HOST = "http://%s/contain_develop/" %host
            send = {'value':'ok','loginUrl':HOST}
            return HttpResponse(json.dumps(send))  

@login_required
def containresult_test(request):
    if request.method =='GET':
        id = request.GET['id']
        contain_id = request.GET['contain_id']
        contain_hostname = request.GET['contain_hostname']
        contain_ip = request.GET['contain_ip']
        contain_cpu = request.GET['contain_cpu']
        contain_memory = request.GET['contain_memory']
        host_ip = request.GET['host_ip']
        project_section = request.GET['project_section']
        release_application = request.GET['release_application']
        contain_netmask = request.GET['contain_netmask']
        contain_port = request.GET['contain_port']
        contain_http = request.GET['proposer']
        service_pack = request.GET['service_pack']
        service_env = request.GET['service_env']
        project_name = request.GET['project_name']
        principal = request.GET['principal']
        proposer = request.GET['proposer']
        service_depend = request.GET['service_depend']
        try:
            contain_update = ContainsList_Test.objects.get(id=id)
            contain_update.contain_id=contain_id
            contain_update.contain_hostname=contain_hostname
            contain_update.contain_ip=contain_ip
            contain_update.contain_cpu_core=contain_cpu
            contain_update.contain_memory=contain_memory
            contain_update.contain_host=host_ip
            contain_update.project_section=project_section
            contain_update.release_application=release_application
            contain_update.proposer=proposer
            contain_update.contain_netmask=contain_netmask
            contain_update.contain_port=contain_port
            contain_update.contain_http=contain_http
            contain_update.service_pack=service_pack
            contain_update.service_env=service_env
            contain_update.project_name=project_name
            contain_update.principal=principal
            contain_update.service_depend=service_depend
            contain_update.save()
        except Exception,e:
            print e.message
        finally: 
            host = ALLOWED_HOSTS[0]
            HOST = "http://%s/contain_test/" %host
            send = {'value':'ok','loginUrl':HOST}
            return HttpResponse(json.dumps(send))  

@login_required
def containresult_pre_release(request):
    if request.method =='GET':
        id = request.GET['id']
        contain_id = request.GET['contain_id']
        contain_hostname = request.GET['contain_hostname']
        contain_ip = request.GET['contain_ip']
        contain_cpu = request.GET['contain_cpu']
        contain_memory = request.GET['contain_memory']
        host_ip = request.GET['host_ip']
        project_section = request.GET['project_section']
        release_application = request.GET['release_application']
        contain_netmask = request.GET['contain_netmask']
        contain_port = request.GET['contain_port']
        contain_http = request.GET['proposer']
        service_pack = request.GET['service_pack']
        service_env = request.GET['service_env']
        project_name = request.GET['project_name']
        principal = request.GET['principal']
        proposer = request.GET['proposer']
        service_depend = request.GET['service_depend']
        try:
            contain_update = ContainsList_Pre_Release.objects.get(id=id)
            contain_update.contain_id=contain_id
            contain_update.contain_hostname=contain_hostname
            contain_update.contain_ip=contain_ip
            contain_update.contain_cpu_core=contain_cpu
            contain_update.contain_memory=contain_memory
            contain_update.contain_host=host_ip
            contain_update.project_section=project_section
            contain_update.release_application=release_application
            contain_update.proposer=proposer
            contain_update.contain_netmask=contain_netmask
            contain_update.contain_port=contain_port
            contain_update.contain_http=contain_http
            contain_update.service_pack=service_pack
            contain_update.service_env=service_env
            contain_update.project_name=project_name
            contain_update.principal=principal
            contain_update.service_depend=service_depend
            contain_update.save()
        except Exception,e:
            print e.message
        finally: 
            host = ALLOWED_HOSTS[0]
            HOST = "http://%s/contain_pre_release/" %host
            send = {'value':'ok','loginUrl':HOST}
            return HttpResponse(json.dumps(send))  

class UploadForm(forms.Form):
    headImg = forms.FileField()

@login_required
def file(request):
#    if request.method == 'POST':
    all_group = Group.objects.all()
    all_file = Upload.objects.all()
    uf = UploadForm(request.POST,request.FILES)
    if uf.is_valid():
        headImg = uf.cleaned_data['headImg']
        user = Upload()
        user.headImg = headImg
        user.save()
    return render_to_response('file.html',locals())

@login_required
def file_result(request):
    if request.method == 'GET':
	import sys
	reload(sys)
	sys.setdefaultencoding("utf-8")
	g_name = request.GET.get('g_name')
	file = request.GET.get('file')
	dir = request.GET.get('dir')
	GroupList = Group.objects.all()
	list_coun = []
        project_success = []
        project_fail = []
	for groupname in GroupList:
            if groupname.name in g_name:
                print "slected group:",groupname.name
                for selected_ip in HostList.objects.filter(group__name = groupname.name):
                    host = HostList.objects.filter(ip=selected_ip.ip)
                    for host in host:
			key_id = host.hostname
			cmd = "salt %s cp.get_file salt://%s %s"%(key_id,file,dir)
     		        os.popen(cmd).read()
			list_coun.append(host)
                num = len(list_coun)
                wirte_track_mark(str(num))
                all_result = salt_return.objects.all()[0:num]
                for projects in all_result:
                    project=projects.success
                    if project == '1':
                        project_success.append(project)
                    else:
                        project_fail.append(project)
                success_num = len(project_success)
                fail_num = len(project_fail)
                result = {'success':success_num,'fail':fail_num}
                return HttpResponse(json.dumps(result))
#			key_id = {'host':key_id,'ret':result}
#			file_result.append(key_id)
#		data = json.dumps(file_result)
#		print data
#		return HttpResponse(data)
@login_required
def command(request):
    if request.method == 'GET':
	    all_host = HostList.objects.all()
    return render_to_response("command.html",locals())

@login_required
def command_result(request):
    if request.method == 'GET':
        ret_api = saltstack()
        ip = request.GET.get('ip')
        command = request.GET.get('command')
        host = HostList.objects.filter(ip=ip)
        for host in host:
            key_id = host.hostname
            sapi = SaltAPI(url=ret_api["url"],username=ret_api["user"],password=ret_api["passwd"])
            ret = sapi.remote_execution(key_id,'cmd.run',command) 
	    all_result = salt_return.objects.all().order_by("-id")[0:1]
	    for ret in all_result:
		key_id = ret.host
		ret = ret.result
		r_data = {'host':key_id,'ret':ret}
                data = json.dumps(r_data)
#                print data
                return HttpResponse(data)
@login_required
def command_group(request):
    if request.method == 'GET':
	    all_group = Group.objects.all()
    return render_to_response("command_group.html",locals())

def command_group_result(request):
    ret_api = saltstack()
    if request.method == 'GET':
        g_name = request.GET.get('g_name')
        command = request.GET.get('command')
        selectIps = []
	list_coun = []
        project_success = []
	project_fail = []
        GroupList = Group.objects.all()
        for groupname in GroupList:
            if groupname.name in g_name:
                print "slected group:",groupname.name
                for selected_ip in HostList.objects.filter(group__name = groupname.name):
                    host = HostList.objects.filter(ip=selected_ip.ip) 	
                    for host in host:
                        #key_id = host.hostname 
                        key_id = host.ip
                        sapi = SaltAPI(url=ret_api["url"],username=ret_api["user"],password=ret_api["passwd"])
                        ret = sapi.remote_execution(key_id,'cmd.run',command)
		        list_coun.append(host)
		num = len(list_coun)	
	        wirte_track_mark(str(num))
		all_result = salt_return.objects.all()[0:num]
		for projects in all_result:
		    project=projects.success 
		    if project == '1':
			project_success.append(project) 
		    else:
			project_fail.append(project)
		success_num = len(project_success)
		fail_num = len(project_fail)
		result = {'success':success_num,'fail':fail_num}
                return HttpResponse(json.dumps(result))
@login_required
def check_result(request):
    num = int(read_track_mark())
    all_result = salt_return.objects.all().order_by("-id")[0:num]
    return render_to_response("check_result.html",locals())
@login_required
def job(request):
    return render_to_response("job.html")
@login_required
def asset(request):
    all_asset = ServerAsset.objects.all()    
    return render_to_response("asset.html",locals())
@login_required
def asset_auto(request):
    all_host = HostList.objects.all()
    return render_to_response("asset_auto.html",locals())
@login_required
def asset_auto_result(request):
     if request.method == 'GET':
	ret_api = saltstack()
	try:
	    client = request.GET.get('client')
            result = get_server_asset_info(client,ret_api["url"],ret_api["user"],ret_api["passwd"],ret_api["device"]) 
            result_data = ServerAsset()
            result_data.manufacturer = result[0][0]
            result_data.productname = result[0][1]
            result_data.service_tag = result[0][2]
            result_data.cpu_model = result[0][3]
            result_data.cpu_nums = result[0][4]
            result_data.cpu_groups = result[0][5]
            result_data.mem = result[0][6]
            result_data.disk = result[0][7]
            result_data.hostname = result[0][8]
            result_data.ip = result[0][9][0]
            result_data.os = result[0][10]
            result_data.save() 
	except:
	    print "print check you asset"
	    return HttpResponse('ok')
	else:     
            data = json.dumps(result)       	
            return HttpResponse(data)
@login_required
def asset_delete(request,id=None):
    if request.method == 'GET':
	id = request.GET.get('id')
        ServerAsset.objects.filter(id=id).delete()
	return HttpResponseRedirect('/asset/')
@login_required
def group(request):
    all_group = Group.objects.all()
    return render_to_response("group.html",locals())
@login_required
def group_result(request):
    if request.method == 'GET':
	group = request.GET.get('g_name')
	data = Group()
	data.name = group
	data.save()
	return HttpResponse("ok")
@login_required
def group_delete(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        Group.objects.filter(id=id).delete()
        return HttpResponseRedirect('/group/')
@login_required
def group_manage(request,id=None):
    if request.method == 'GET':
	id = request.GET.get('id')
	group_name = Group.objects.get(id=id)	
 	all_ip = group_name.hostlist_set.all()
	all_host = HostList.objects.all()	
        return render_to_response("group_manage.html",locals())
@login_required
def group_manage_delete(request,group_name=None,ip=None):
    if request.method == 'GET':
	group_name = request.GET.get('group_name')
	ip = request.GET.get('ip')
	all_group = Group.objects.filter(name=group_name)
	all_host = HostList.objects.filter(ip=ip)
	for group in all_group:
	    group_id= group.id 
	for host in all_host:
	    host_id= host.id
	h = HostList.objects.get(id=host_id)
	g = Group.objects.get(id=group_id)
	h.group.remove(g)
	return HttpResponse('ok')
@login_required
def addgroup_host(request):
    if request.method == 'GET':
	group = request.GET.get('nameInput')
	ip = request.GET.get('hostInput')
	all_group = Group.objects.filter(name=group)
        all_host = HostList.objects.filter(ip=ip)
	for group in all_group:
            group_id= group.id
        for host in all_host:
            host_id= host.id
        h = HostList.objects.get(id=host_id)
        g = Group.objects.get(id=group_id)
	h.group.add(g)
	return HttpResponse('ok')
def monitor(request):
    data = []
    host = []
    c = db.cursor()
    c.execute("SELECT `name` from `key_name`")
    one = c.fetchall()
    d = db.cursor()
    d.execute("SELECT `hostname` from `statusinfo`")
    hostname = d.fetchall()
    for i in one:
        data.append(i[0])
    for x in hostname:
	host.append(x[0])
    host = list(set(host))
    print host
    return render_to_response("monitor.html",locals())
def getdata(request):
    if request.method == 'GET':
	data_list = []
	item = str(request.GET.get('item'))
	start =str(request.GET.get('from'))
	stop  = str(request.GET.get('to'))
	host = str(request.GET.get('host'))
	if item != 'None':
	    data_list = [item,start,stop,host]
	    print data_list
	    f = open("/web/CMDB/app/backend/monitor_data.txt",'w')
            try:
	        for i in data_list:
                    f.write(i)
		    f.write("\n")
            finally:
                f.close()
	if item == 'None':
	    pass 
	return HttpResponse('ok')
def monitor_result(request):
    return render_to_response('monitor_result.html')
def monitor_data(request):
    data = []
    f = open("/web/CMDB/app/backend/monitor_data.txt")
    try:
        lines = f.readlines()
    finally:
        f.close()
    for line in lines:
        data.append(line.strip())
    item = data[0]
    start = data[1]
    stop = data[2]
    host = data[3]
    if start == '' and stop == '':
	starttime = int(time.time())
	c.execute("SELECT `time`,`%s` FROM `statusinfo` where `hostname` = '%s' and `time` < %d" %(item,host,starttime))
	ones = [[i[0]*1000 + 28800000, i[1]] for i in c.fetchall()]
	return HttpResponse(json.dumps(ones))	
    if start == '' and stop != '':
	stop = stop.strip()
    	timeStamp = date_result(stop)
	c.execute("SELECT `time`,`%s` FROM `statusinfo` where `hostname` = '%s' and `time` < %d" %(item,host,timeStamp))
        ones = [[i[0]*1000 + 28800000, i[1]] for i in c.fetchall()]
	return HttpResponse(json.dumps(ones))
    if start != '' and stop == '':
	timeStamp=date_result(data)
	c.execute("SELECT `time`,`%s` FROM `statusinfo` where `hostname` = '%s' and `time` > %d" %(item,host,timeStamp))
	ones = [[i[0]*1000 + 28800000, i[1]] for i in c.fetchall()]
        return HttpResponse(json.dumps(ones))
    if start != '' and stop != '': 
        start_timeStamp = date_result(start) 
        stop_timeStamp = date_result(stop)
        c.execute("SELECT `time`,`%s` FROM `statusinfo` where `hostname` = '%s' and `time` > %d and `time` < %d" %(item,host,start_timeStamp,stop_timeStamp))	
	ones = [[i[0]*1000 + 28800000, i[1]] for i in c.fetchall()]
        return HttpResponse(json.dumps(ones))

def user_manage(request):
    user = NewUser.objects.all()
    form = NewUserForm()
    return render_to_response("user_manage.html",{'data':user,
                                                  'role':form})
def user_manage_man(request):
    user_manage = NewUser.objects.all()
    form_manage = NewUserForm()
    return render_to_response("user_manage_man.html",{'data_man':user_manage,
                                                      'role':form_manage})                                      #'role':form_manage})
@login_required
def adduser(request):
    username = request.GET['username'] 
    password = request.GET['password'] 
    last_name = request.GET['last_name']
    first_name = request.GET['first_name']
    email = request.GET['email']
    role = request.GET['role']
    user_add = NewUser.objects.create_user(username=username,
                                   password=password,
                                   email=email,
                                   manage_role=role)
    user_add.first_name = first_name
    user_add.last_name = last_name
    user_add.save()
    return HttpResponse('ok')

@login_required
def deluser(request,id=None):
    if request.method == 'GET':
        id = request.GET.get('id')
        NewUser.objects.filter(id=id).delete()
        return HttpResponseRedirect('/user_manage/')
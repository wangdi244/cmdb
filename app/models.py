#coding: utf-8
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import *
import time
from django.contrib.auth.models import AbstractUser


class Idc(models.Model):
    idc_name = models.CharField(max_length=40, verbose_name=u'机房名称')
    idc_address = models.CharField(max_length=80, verbose_name=u'机房地址')
    remark = models.CharField(max_length=40, verbose_name=u'备注')
    
    def __unicode__(self):
	   return self.idc_name
    
    class Meta:
	    verbose_name = u'机房列表'
    verbose_name_plural = u'机房列表'	
        
class HostList(models.Model):
    ip = models.GenericIPAddressField(unique=True, verbose_name=u'物理机IP地址')
    manage_ip = models.GenericIPAddressField(unique=True, verbose_name=u'管理IP地址')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    group = models.ManyToManyField("Group",blank=True ,verbose_name=u'组名') 
    application = models.CharField(max_length=20, verbose_name=u'应用')
    bianhao = models.CharField(max_length=30, verbose_name=u'编号') 
    idc_name = models.CharField(max_length=40,null=True,blank=True, verbose_name=u'所属机房') 
    
    def __unicode__(self):
        return self.ip
    
    class Meta:
        verbose_name = u'主机列表'
	verbose_name_plural = u'主机列表'

class HostList_Develop(models.Model):
    ip = models.GenericIPAddressField(unique=True, verbose_name=u'物理机IP地址')
    manage_ip = models.GenericIPAddressField(unique=True, verbose_name=u'管理IP地址')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    group = models.ManyToManyField("Group_Develop",blank=True ,verbose_name=u'组名') 
    application = models.CharField(max_length=20, verbose_name=u'应用')
    bianhao = models.CharField(max_length=30, verbose_name=u'编号') 
    idc_name = models.CharField(max_length=40,null=True,blank=True, verbose_name=u'所属机房') 
    
    def __unicode__(self):
        return self.ip
    
    class Meta:
        verbose_name = u'开发主机列表'
    verbose_name_plural = u'开发主机列表'

class HostList_Test(models.Model):
    ip = models.GenericIPAddressField(unique=True, verbose_name=u'物理机IP地址')
    manage_ip = models.GenericIPAddressField(unique=True, verbose_name=u'管理IP地址')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    group = models.ManyToManyField("Group_Test",blank=True ,verbose_name=u'组名') 
    application = models.CharField(max_length=20, verbose_name=u'应用')
    bianhao = models.CharField(max_length=30, verbose_name=u'编号') 
    idc_name = models.CharField(max_length=40,null=True,blank=True, verbose_name=u'所属机房') 
    
    def __unicode__(self):
        return self.ip
    
    class Meta:
        verbose_name = u'测试主机列表'
    verbose_name_plural = u'测试主机列表'

class HostList_Pre_Release(models.Model):
    ip = models.GenericIPAddressField(unique=True, verbose_name=u'物理机IP地址')
    manage_ip = models.GenericIPAddressField(unique=True, verbose_name=u'管理IP地址')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    group = models.ManyToManyField("Group_Test",blank=True ,verbose_name=u'组名') 
    application = models.CharField(max_length=20, verbose_name=u'应用')
    bianhao = models.CharField(max_length=30, verbose_name=u'编号') 
    idc_name = models.CharField(max_length=40,null=True,blank=True, verbose_name=u'所属机房') 
    
    def __unicode__(self):
        return self.ip
    
    class Meta:
        verbose_name = u'预发布主机列表'
    verbose_name_plural = u'预发布主机列表'

class ContainsList(models.Model):
    contain_id = models.CharField(max_length=20,verbose_name=u'容器ID',null=True,blank=True)
    contain_ip = models.GenericIPAddressField(max_length=20, verbose_name=u'IP地址',null=True,blank=True)
    contain_netmask = models.CharField(max_length=20,verbose_name=u'容器掩码',null=True,blank=True)
    contain_port = models.CharField(max_length=10,verbose_name=u'容器监听端口',null=True,blank=True)
    contain_http = models.CharField(max_length=10,verbose_name=u'服务url',null=True,blank=True)
    create_datetime = models.CharField(max_length=20,verbose_name=u'容器创建时间',null=True,blank=True)
    contain_cpu_core = models.CharField(max_length=10,verbose_name=u'cpu绑定核号',null=True,blank=True)
    contain_host = models.CharField(max_length=30, verbose_name=u'物理机主机名',null=True,blank=True)
    contain_memory = models.CharField(max_length=10,verbose_name=u'内存分配',null=True,blank=True)
    contain_hostname = models.CharField(max_length=30, verbose_name=u'容器主机名',null=True,blank=True)
    release_application=models.CharField(max_length=20, verbose_name=u'应用名称',null=True,blank=True)
    service_pack = models.CharField(max_length=30, verbose_name=u'应用包名',null=True,blank=True)
    service_depend = models.CharField(max_length=50, verbose_name=u'应用依赖',null=True,blank=True)
    service_env = models.CharField(max_length=20, verbose_name=u'服务环境',null=True,blank=True)
    project_name = models.CharField(max_length=20, verbose_name=u'项目名称',null=True,blank=True)
    proposer = models.CharField(max_length=30, verbose_name=u'项目开发者',null=True,blank=True)
    principal = models.CharField(max_length=30, verbose_name=u'项目负责人',null=True,blank=True)
    project_section = models.CharField(max_length=30, verbose_name=u'项目所属部门',null=True,blank=True)
    state = models.CharField(max_length=30, verbose_name=u'容器状态',null=True,blank=True)
    flag= models.CharField(max_length=5, verbose_name=u'容器标记位',null=True,blank=True)
    x_flag= models.CharField(max_length=30, verbose_name=u'容器处理情况',null=True,blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'容器列表'
        verbose_name_plural = u'容器列表'

class ContainsList_Develop(models.Model):
    contain_id = models.CharField(max_length=20,verbose_name=u'容器ID',null=True,blank=True)
    contain_ip = models.CharField(max_length=16, verbose_name=u'IP地址',null=True,blank=True)
    contain_netmask = models.CharField(max_length=20,verbose_name=u'容器掩码',null=True,blank=True)
    contain_port = models.CharField(max_length=10,verbose_name=u'容器监听端口',null=True,blank=True)
    contain_http = models.CharField(max_length=10,verbose_name=u'服务url',null=True,blank=True)
    create_datetime = models.CharField(max_length=20,verbose_name=u'容器创建时间',null=True,blank=True)
    contain_cpu_core = models.CharField(max_length=10,verbose_name=u'cpu绑定核号',null=True,blank=True)
    contain_host = models.CharField(max_length=30, verbose_name=u'物理机主机名',null=True,blank=True)
    contain_memory = models.CharField(max_length=10,verbose_name=u'内存分配',null=True,blank=True)
    contain_hostname = models.CharField(max_length=30, verbose_name=u'容器主机名',null=True,blank=True)
    release_application=models.CharField(max_length=20, verbose_name=u'应用名称',null=True,blank=True)
    service_pack = models.CharField(max_length=30, verbose_name=u'应用包名',null=True,blank=True)
    service_depend = models.CharField(max_length=50, verbose_name=u'应用依赖',null=True,blank=True)
    service_env = models.CharField(max_length=20, verbose_name=u'服务环境',null=True,blank=True)
    project_name = models.CharField(max_length=20, verbose_name=u'项目名称',null=True,blank=True)
    proposer = models.CharField(max_length=30, verbose_name=u'项目开发者',null=True,blank=True)
    principal = models.CharField(max_length=30, verbose_name=u'项目负责人',null=True,blank=True)
    project_section = models.CharField(max_length=30, verbose_name=u'项目所属部门',null=True,blank=True)
    state = models.CharField(max_length=30, verbose_name=u'容器状态',null=True,blank=True)
    flag= models.CharField(max_length=5, verbose_name=u'容器标记位',null=True,blank=True)
    x_flag= models.CharField(max_length=30, verbose_name=u'容器处理情况',null=True,blank=True)
    
    def __unicode__(self):
        return self.contain_ip
    
    class Meta:
        verbose_name = u'开发环境容器列表'
        verbose_name_plural = u'开发环境容器列表'

class ContainsList_Test(models.Model):
    contain_id = models.CharField(max_length=20,verbose_name=u'容器ID',null=True,blank=True)
    contain_ip = models.GenericIPAddressField(max_length=20, verbose_name=u'IP地址',null=True,blank=True)
    contain_netmask = models.CharField(max_length=20,verbose_name=u'容器掩码',null=True,blank=True)
    contain_port = models.CharField(max_length=10,verbose_name=u'容器监听端口',null=True,blank=True)
    contain_http = models.CharField(max_length=10,verbose_name=u'服务url',null=True,blank=True)
    create_datetime = models.CharField(max_length=20,verbose_name=u'容器创建时间',null=True,blank=True)
    contain_cpu_core = models.CharField(max_length=10,verbose_name=u'cpu绑定核号',null=True,blank=True)
    contain_host = models.CharField(max_length=30, verbose_name=u'物理机主机名',null=True,blank=True)
    contain_memory = models.CharField(max_length=10,verbose_name=u'内存分配',null=True,blank=True)
    contain_hostname = models.CharField(max_length=30, verbose_name=u'容器主机名',null=True,blank=True)
    release_application=models.CharField(max_length=20, verbose_name=u'应用名称',null=True,blank=True)
    service_pack = models.CharField(max_length=30, verbose_name=u'应用包名',null=True,blank=True)
    service_depend = models.CharField(max_length=50, verbose_name=u'应用依赖',null=True,blank=True)
    service_env = models.CharField(max_length=20, verbose_name=u'服务环境',null=True,blank=True)
    project_name = models.CharField(max_length=20, verbose_name=u'项目名称',null=True,blank=True)
    proposer = models.CharField(max_length=30, verbose_name=u'项目开发者',null=True,blank=True)
    principal = models.CharField(max_length=30, verbose_name=u'项目负责人',null=True,blank=True)
    project_section = models.CharField(max_length=30, verbose_name=u'项目所属部门',null=True,blank=True)
    state = models.CharField(max_length=30, verbose_name=u'容器状态',null=True,blank=True)
    flag= models.CharField(max_length=5, verbose_name=u'容器标记位',null=True,blank=True)
    x_flag= models.CharField(max_length=30, verbose_name=u'容器处理情况',null=True,blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'测试环境容器列表'
        verbose_name_plural = u'测试环境容器列表'

class ContainsList_Pre_Release(models.Model):
    contain_id = models.CharField(max_length=20,verbose_name=u'容器ID',null=True,blank=True)
    contain_ip = models.GenericIPAddressField(max_length=20, verbose_name=u'IP地址',null=True,blank=True)
    contain_netmask = models.CharField(max_length=20,verbose_name=u'容器掩码',null=True,blank=True)
    contain_port = models.CharField(max_length=10,verbose_name=u'容器监听端口',null=True,blank=True)
    contain_http = models.CharField(max_length=10,verbose_name=u'服务url',null=True,blank=True)
    create_datetime = models.CharField(max_length=20,verbose_name=u'容器创建时间',null=True,blank=True)
    contain_cpu_core = models.CharField(max_length=10,verbose_name=u'cpu绑定核号',null=True,blank=True)
    contain_host = models.CharField(max_length=30, verbose_name=u'物理机主机名',null=True,blank=True)
    contain_memory = models.CharField(max_length=10,verbose_name=u'内存分配',null=True,blank=True)
    contain_hostname = models.CharField(max_length=30, verbose_name=u'容器主机名',null=True,blank=True)
    release_application=models.CharField(max_length=20, verbose_name=u'应用名称',null=True,blank=True)
    service_pack = models.CharField(max_length=30, verbose_name=u'应用包名',null=True,blank=True)
    service_depend = models.CharField(max_length=50, verbose_name=u'应用依赖',null=True,blank=True)
    service_env = models.CharField(max_length=20, verbose_name=u'服务环境',null=True,blank=True)
    project_name = models.CharField(max_length=20, verbose_name=u'项目名称',null=True,blank=True)
    proposer = models.CharField(max_length=30, verbose_name=u'项目开发者',null=True,blank=True)
    principal = models.CharField(max_length=30, verbose_name=u'项目负责人',null=True,blank=True)
    project_section = models.CharField(max_length=30, verbose_name=u'项目所属部门',null=True,blank=True)
    state = models.CharField(max_length=30, verbose_name=u'容器状态',null=True,blank=True)
    flag= models.CharField(max_length=5, verbose_name=u'容器标记位',null=True,blank=True)
    x_flag= models.CharField(max_length=30, verbose_name=u'容器处理情况',null=True,blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'预生产环境容器列表'
        verbose_name_plural = u'预生产环境容器列表'

class ServerAsset(models.Model):
    manufacturer = models.CharField(max_length=20, verbose_name=u'厂商')
    productname = models.CharField(max_length=30, verbose_name=u'产品型号')
    service_tag = models.CharField(max_length=80, unique=True, verbose_name=u'序列号')
    cpu_model = models.CharField(max_length=50, verbose_name=u'CPU型号')
    cpu_nums = models.PositiveSmallIntegerField(verbose_name=u'CPU线程数')
    cpu_groups = models.PositiveSmallIntegerField(verbose_name=u'CPU物理核数')
    mem = models.CharField(max_length=100, verbose_name='内存大小')
    disk = models.CharField(max_length=300, verbose_name='硬盘大小')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    ip = models.CharField(max_length=20, verbose_name=u'IP地址')
    os = models.CharField(max_length=20, verbose_name=u'操作系统')
    
    def __unicode__(self):
        return u'%s - %s' %(self.ip, self.hostname )

    class Meta:
        verbose_name = u'主机资产信息'
        verbose_name_plural = u'主机资产信息管理'

class Group(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'主机组信息'
        verbose_name_plural = u'主机组信息管理'

class Group_Develop(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'开发主机组信息'
        verbose_name_plural = u'开发主机组信息管理'

class Group_Test(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'测试主机组信息'
        verbose_name_plural = u'测试主机组信息管理'
        
class Upload(models.Model):
    headImg = models.FileField(upload_to = './upload/')
    
    def __unicode__(self):
        return self.headImg
    
    class Meta:
	verbose_name = u'文件上传'
        verbose_name_plural = u'文件上传'
        
class cmd_run(models.Model):
    ip = models.GenericIPAddressField(verbose_name=u'IP地址')
    command = models.CharField(max_length=30, verbose_name=u'命令')
    track_mark = models.IntegerField() 
    
    def __unicode__(self):
	   return self.ip
    
    class Meta:    
	   verbose_name = u'命令管理'
	   verbose_name_plural = u'命令管理'
    
class salt_return(models.Model):
   fun = models.CharField(max_length=50)
   jid = models.CharField(max_length=255)
   result = models.TextField()
   host = models.CharField(max_length=255)
   success = models.CharField(max_length=10)
   full_ret = models.TextField()
   
   def __unicode__(self):
        return self.host
   
   class Meta:
        verbose_name = u'命令返回结果'
        verbose_name_plural = u'命令返回结果'

class NewUser(AbstractUser):
    manage_choice = (
            ('super',u'超级管理员'),
            ('manage',u'管理员'),
        )
    manage_role = models.CharField(u'角色',max_length=30,
                                   choices=manage_choice)
    
    def __unicode__(self):
        return self.username
   
    class Meta:
        verbose_name = u'用户管理'
        verbose_name_plural = u'用户管理'

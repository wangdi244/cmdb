from django.contrib.auth.views import login as account_login
from django.conf.urls import include, url
#from django.contrib.auth.views import login, logout_then_login
# Uncomment the next two lines to enable the admin:
from django.contrib import admin 
from app import search_indexes
admin.autodiscover()
from app.views import *
from haystack.views import SearchView

urlpatterns = [
    # Examples:
    # url(r'^$', 'CMDB.views.home', name='home'),
    # url(r'^CMDB/', include('CMDB.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$',index),
    #url(r'^index_manage/$',index_manage),
    url(r'^$',login),
    url(r'^login/$',login),
    url(r'^logout/$',logout),
    url(r'^idc/(\d*)$',idc),
    url(r'^addidc/$',addidc),
    url(r'^idc/idc_delete/$',idc_delete),
    url(r'^mac/$',mac),
    url(r'^mac_develop/$',mac_develop),
    url(r'^mac_test/$',mac_test),
    url(r'^mac_pre_release/$',mac_pre_release),
    url(r'^addmac/$',addmac),
    url(r'^addmac_develop/$',addmac_develop),
    url(r'^addmac_test/$',addmac_test),
    url(r'^addmac_pre_release/$',addmac_pre_release),
    url(r'^mac/mac_delete/$',mac_delete),
    url(r'^mac/mac_develop_delete/$',mac_develp_delete),
    url(r'^mac/mac_test_delete/$',mac_test_delete),
    url(r'^mac/mac_pre_release_delete/$',mac_pre_release_delete),
    url(r'^mac/mac_edit/$',mac_edit),
    url(r'^mac/mac_develop_edit/$',mac_develop_edit),
    url(r'^mac/mac_test_edit/$',mac_test_edit),
    url(r'^mac/mac_pre_release_edit/$',mac_pre_release_edit),
    url(r'^mac/check_host/$',mac_check_host),
    url(r'^macresult/$',macresult),
    url(r'^macresult_develop/$',macresult_develop),
    url(r'^macresult_test/$',macresult_test),
    url(r'^macresult_pre_release/$',macresult_pre_release),
    url(r'^contain/(\d*)$',contain),
    url(r'^contain_develop/(\d*)$',contain_develop),
    url(r'^contain_test/(\d*)$',contain_test),
    url(r'^contain_pre_release/(\d*)$',contain_pre_release),
    url(r'^contain/search/', include("haystack.urls")),
    url(r'^contain_develop/search/',
        SearchView(template=u'search/search_develop.html'),
        name='haystack_search'),
    url(r'^contain_test/search/',
        SearchView(template=u'search/search_test.html'),
        name='haystack_search'),
    url(r'^contain/contain_edit/$',contain_edit),
    url(r'^contain/contain_develop_edit/$',contain_develop_edit),
    url(r'^contain/contain_test_edit/$',contain_test_edit),
    url(r'^contain/contain_pre_release_edit/$',contain_pre_release_edit),
    url(r'^addcontain/$',addcontain),
    url(r'^addcontain_develop/$',addcontain_develop),
    url(r'^addcontain_test/$',addcontain_test),
    url(r'^addcontain_pre_release/$',addcontain_pre_release),
    url(r'^contain/contain_delete/$',contain_delete),
    url(r'^contain/contain_develop_delete/$',contain_develop_delete),
    url(r'^contain/contain_test_delete/$',contain_test_delete),
    url(r'^contain/contain_pre_release_delete/$',contain_pre_release_delete),
    url(r'^containresult/$',containresult),
    url(r'^containresult_develop/$',containresult_develop),
    url(r'^containresult_test/$',containresult_test),
    url(r'^containresult_pre_release/$',containresult_pre_release),
    url(r'^group/$',group),
    url(r'^group_result/$',group_result),
    url(r'^group/group_delete/$',group_delete),
    url(r'^group_manage/$',group_manage),
    url(r'^group_manage/group_manage_delete/$',group_manage_delete), 
    url(r'addgroup_host/$',addgroup_host),
    url(r'^file/$',file),
    url(r'^file_result',file_result),
    url(r'^command/$',command),
    url(r'^command_group/$',command_group),
    url(r'^command_group/check_result/$',check_result),
    url(r'^command_group_result/$',command_group_result), 
    url(r'^command_result/$',command_result),
    url(r'^job/$',job),
    url(r'^asset/$',asset),
    url(r'^asset_auto/$',asset_auto),
    url(r'^asset_auto_result/$',asset_auto_result),
    url(r'asset/asset_delete/$',asset_delete),
    url(r'^authin/$',authin),
    url(r'accounts/login/$',account_login,{'template_name':'login.html'}),
    url(r'^monitor/$',monitor),
    url(r'^data/$',getdata),
    url(r'monitor_result/$',monitor_result),
    url(r'monitor_data/$',monitor_data),
    url(r'user_manage/$',user_manage),
    url(r'user_delete/$',deluser),
    url(r'user_manage_man/$',user_manage_man),
    url(r'adduser/$',adduser)
]
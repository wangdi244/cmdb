#!/usr/bin/env python    
#coding=utf-8

from django.utils.safestring import mark_safe

def Page(page,all_page_count):
    '''
    page:当前页
    all_page_count:总页数
    '''
    page_html = []
    frist_html = "<a href='/contain/%d'>首页</a>" %(1)
    page_html.append(frist_html)
    
    if page<=1:
        prev_html="<a href='#'>上一页</a>"
    else:
        prev_html ="<a href='/contain/%d'>上一页</a>" %(page-1,)
    page_html.append(prev_html)
    
    #11个页码
    if all_page_count < 11:
        begin = 0
        end = all_page_count
    #总页数大于11
    else:
        if page<6:
            begin=0
            end=11
        else:
            if page +6>all_page_count:
                begin = page-6
                end = all_page_count
            else:
                begin=page-6
                end =page+5
    
    for i in range(begin,end):
        if page == i+1:
            a_html = "<a class='selected' href='/contain/%d'>%d</a>" %(page,page)
        else:
            a_html = "<a href='/contain/%d'>%d</a>" %(i+1,i+1)
        page_html.append(a_html)
    
    next_html = "<a href='/contain/%d'>下一页</a>" %(page+1,)
    page_html.append(next_html)
    
    end_html = "<a href='/contain/%d'>尾页</a>" %(all_page_count)
    page_html.append(end_html)
    page_string = mark_safe(''.join(page_html))
    return page_string



class PageInfo:
    def __init__(self,current_page,all_count,per_item):
        self.CurrentPage=current_page
        self.AllCount=all_count
        self.PerItem=per_item
    
    @property
    def start(self):
        return (self.CurrentPage-1)*self.PerItem
    @property
    def end(self):
        return self.CurrentPage*self.PerItem
    @property
    def all_page_count(self):
        '''
        temp = divmod(count, per_item)
        if temp[1] == 0:
            all_page_count = temp[0]
        else:
            all_page_count = temp[0]+1
        '''
        temp = divmod(self.AllCount,self.PerItem)
        if temp[1] == 0:
            all_page_count = temp[0]
        else:
            all_page_count = temp[0]+1
        return all_page_count
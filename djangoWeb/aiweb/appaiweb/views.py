#coding=UTF-8
from django.shortcuts import render
#render响应渲染前端模板页面的
from django.http import HttpResponse
#res响应req请求
from .models import *
from django.core import serializers
from django.core import paginator
import json
pageSize = 3 #3条记录一页
#post请求限制打开

def index(request):
    #返回静态字符串
    #return HttpResponse('Hello world')#响应字符串
    #后台值用render返回到前端
    context = {}
    context['name'] = 'huan'#向前端而面传递字符串
    #响应模板index.html
    return render(request,'index.html',context)
    '''
    rs = Test.objects.all()
    context2 = {
        'datas':rs
    }
    print("==rs==")
    print(rs)
    #前端用模块for语句取datas，用render返回可以直接渲染
    return render(request,'index.html',context=context2)
    '''
#post请求限制打开    

def doShow(request):
    request.encoding='utf-8'
    page = request.GET.get('curPage')
    #从数据库表对象取数据
    #Test.objects.get(id=1).classname#取指定id的记录
    #Test.objects.all()或 filter().order_by('?')#取全部记录
    #all()返回的是QuerySet 数据类型
    rs = PyAiwebCnewsTbl.objects.all()
    rs = paginator.Paginator(rs,pageSize)#第二参数，几条数据分一页
    rs = rs.page(page)#取第几页
    #前端改为ajax连接
    #return HttpResponse('111111')#前端调取可打印，请求路径已连通
    #rs是QuerySet格式，需序列化后才能返回给前端
    rsAjax = serializers.serialize('json',rs)
    #print(rsAjax)
    return HttpResponse(rsAjax)
    

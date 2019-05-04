from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    return render(request,'add.html')
user_list = []
@csrf_exempt
def doAdd(request):
    uName = request.POST.get('uName')
    uPassword = request.POST.get('uPassword')
    temp = {'uName':uName,'uPassword':uPassword}
    print("====前端传过来的数据====")
    user_list.append(temp)
    print(user_list)
    return HttpResponse(user_list)
    #return render(request,'addshow.html',{'datas':user_list})
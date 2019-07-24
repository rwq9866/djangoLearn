from django.shortcuts import render
from django.shortcuts import HttpResponse
from myApp import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core import serializers
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import uuid
import urllib.parse
# import schedule
from hyperlpr import *
import cv2
from django.conf import settings


# Create your views here.

# 登录页面
def login(request):
    return render(request, 'login.html')
# 登录验证
def loginData(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        password = request.POST.get('password', None)
        resultData = {'state':'0', 'msg':''}
        try:
            # 从指定表中获取需求数据
            userData = models.UserInfo.objects.get(user=name)
            if userData.pwd == password:
                request.session['name'] = name
                request.session.set_expiry(180)
                resultData['state'] = '1'
                return JsonResponse(resultData)
            else:
                resultData['msg'] = '密码错误'
                return JsonResponse(resultData)
        except ObjectDoesNotExist:
            resultData['msg'] = '查无此人'
            return JsonResponse(resultData)
    # 从指定的数据库中查询所有的数据
    # userList = models.UserInfo.objects.all()


# 注册页面
def register(request):
    return render(request, 'register.html')
# 注册用户
def registerData(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        password = request.POST.get('password', None)
        # 向指定表中添加数据
        models.UserInfo.objects.create(user=name, pwd=password)

    # 从指定的数据库中查询所有的数据
    # userList = models.UserInfo.objects.all()
    # return render(request, 'login.html', {'userList': userList})

    return HttpResponse("注册成功!!!")

# 主页
def index(request):
    # name = request.session['name']
    name = request.session.get('name', '登录超时了耶!')
    return render(request, 'index.html', {'name': name})

# 获取人员信息
def ryxxb(request):
    userList = models.UserInfo.objects.all()
    # return JsonResponse(userList, safe=False)
    return HttpResponse(serializers.serialize('json', userList))

# 获取新闻
def news(request):
    word = urllib.parse.quote(request.POST.get("word", None))
    url = "http://news.baidu.com/ns?word={0}".format(word)
    req = Request(url)
    req.add_header("User-agent",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36")
    bs = BeautifulSoup(urlopen(req), "html.parser")
    for i in bs.find_all("a"):
        if "data-click" in i.attrs:
            if "class" not in i.attrs:
                print("{0}  网址:".format(i.get_text()), end="")
                print(i.attrs["href"])
                models.Pc.objects.create(id=uuid.uuid1(), tit=i.get_text(), hre=i.attrs["href"])
    tit_list = models.Pc.objects.all()
    # return render(request, "index6.html", {"data": tit_list})
    return HttpResponse(serializers.serialize('json', tit_list))
    # return JsonResponse(tit_list, safe=False)


def newsdemo(request):
    tit_list = models.Pc.objects.all()
    return HttpResponse(serializers.serialize('json', tit_list))

# 车牌识别
def lpr(request):
    if request.method == "POST":
        img = request.FILES.get("img")
        imageName = os.path.join(settings.MEDIA_ROOT, img.name)
        with open(imageName, 'wb') as f:
            for image_part in img.chunks():
                f.write(image_part)
        # 读入图片
        image = cv2.imread(imageName)
        # image = cv2.imread(settings.STATICFILES_DIRS[0] + "\\images\\" + img.name)
        # 识别结果
        lp = HyperLPR_PlateRecogntion(image)
        if lp:
            lpr = lp[0][0]
            if lpr[1] == "新":
                lpr = lpr[0] + "O " + lpr[2:len(lpr)]
            else:
                lpr = lpr[0:2] + " " + lpr[2:len(lpr)]
            return HttpResponse(lpr)
        else:
            return HttpResponse("不好意思,我识别不出来!!!")

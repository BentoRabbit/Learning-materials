# from PyQt5.QtCore.QUrl import setPassword
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import pyecharts.options as opts
from django.shortcuts import render, redirect
from pyecharts.charts import Timeline, Bar, Pie, Bar3D

from clinicaltrial.models import *

import math
import json
from random import randrange
import hashlib

from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView

from pyecharts.charts import Bar, Pie
from pyecharts import options as opts


# Create your views here.
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


def index_view(request):
    #查询所有数据
    # clinialtrials = Clinicaltrial.objects.all()
    a = 0
    b = 0
    c = 0
    d = 0
    all_data = Clinicaltrial.objects.all()
    for x in all_data:
        if x.start_year == 2018:
            a = a+1
        elif x.start_year == 2019:
            b = b+1
        elif x.start_year == 2020:
            c = c+1
        elif x.start_year == 2021:
            d = d+1
    fads = ForAnzsrcData.objects.order_by('-quantity')[0:5]
    states = State.objects.order_by('-state_count')[0:5]

    na = Clinicaltrial.objects.filter(phase='N/A').count()
    phase0 = Clinicaltrial.objects.filter(phase='Phase 0').count()
    phase1 = Clinicaltrial.objects.filter(phase='Phase 1').count()
    phase2 = Clinicaltrial.objects.filter(phase='Phase 2').count()
    phase3 = Clinicaltrial.objects.filter(phase='Phase 3').count()
    phase4 = Clinicaltrial.objects.filter(phase='Phase 4').count()

    search_name = request.POST.get('clinialtrial', '')
    clinialtrials = Clinicaltrial.objects.filter(title__icontains=search_name)
    if clinialtrials.exists():
        return render(request, 'guest.html',
                      {'clinialtrials': clinialtrials,"a":a,"b":b,"c":c,"d":d, 'fads':fads, 'states':states,
                       'na':na,'phase0':phase0,'phase1':phase1,'phase2':phase2,'phase3':phase3,'phase4':phase4
                       })

    return render(request, 'guest.html')


def index3_view(request):

    a = 0
    b = 0
    c = 0
    d = 0
    all_data = Clinicaltrial.objects.all()
    for x in all_data:
        if x.start_year == 2018:
            a = a+1
        elif x.start_year == 2019:
            b = b+1
        elif x.start_year == 2020:
            c = c+1
        elif x.start_year == 2021:
            d = d+1
    fads = ForAnzsrcData.objects.order_by('-quantity')[0:5]
    states = State.objects.order_by('-state_count')[0:5]

    na = Clinicaltrial.objects.filter(phase='N/A').count()
    phase0 = Clinicaltrial.objects.filter(phase='Phase 0').count()
    phase1 = Clinicaltrial.objects.filter(phase='Phase 1').count()
    phase2 = Clinicaltrial.objects.filter(phase='Phase 2').count()
    phase3 = Clinicaltrial.objects.filter(phase='Phase 3').count()
    phase4 = Clinicaltrial.objects.filter(phase='Phase 4').count()

    search_name = request.POST.get('clinialtrial', '')
    clinialtrials = Clinicaltrial.objects.filter(title__icontains=search_name)
    if clinialtrials.exists():
        return render(request, 'test01.html',
                      {'clinialtrials': clinialtrials,"a":a,"b":b,"c":c,"d":d, 'fads':fads, 'states':states,
                       'na':na,'phase0':phase0,'phase1':phase1,'phase2':phase2,'phase3':phase3,'phase4':phase4
                       })

    return render(request, 'test01.html')



def bar_base() -> Bar:
    bar = (
        Bar()
            .add_xaxis([2018, 2019, 2020, 2021])
            .add_yaxis("各个年份", [Clinicaltrial.objects.filter(start_year=2018).count(),
                                Clinicaltrial.objects.filter(start_year=2019).count(),
                                Clinicaltrial.objects.filter(start_year=2020).count(),
                                Clinicaltrial.objects.filter(start_year=2021).count()])
            .set_global_opts(title_opts=opts.TitleOpts(title="每年注册的临床试验数量（近四年）"),legend_opts=opts.LegendOpts(is_show=False))
            .dump_options_with_quotes()
    )
    return bar
    # bar.render("E:\\final design\\test01\\templates\\bar_base.html")





class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(bar_base()))


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/index01.html").read())

# SHA1加密
def SHA1(password):
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    password = sha1.hexdigest()
    return str(password)

#用户注册
def register(request):
    if request.method == "POST" and request.POST:
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        phone = data.get("phone")
        User.objects.create(
            username=username,
            password=SHA1(password),
            # password=password,
            email=email,
            phone=phone,
        )
        return HttpResponseRedirect('/clinicaltrial/login/')
    return render(request,"register.html")

#用户登入
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login_n.html')
    else:
        # 1 获取请求参数
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 2 查询数据库
        s = User.objects.filter(username=username).first()
        # 3 判断是否登录成功
        if s:
            now_password = SHA1(password)
            db_password = s.password
            if now_password == db_password:
                response = HttpResponseRedirect('/clinicaltrial/show/')
                response.set_cookie("username", s.username)
                return response
            else:
                return render(request, "login_s.html")
        # 2 查询数据库
    #     if username and password:
    #         c = User.objects.filter(username=username, password=password).count()
    #
    #         # 3 判断是否登录成功
    #         if c == 1:
    #             # return HttpResponse('登录成功！')
    #             return HttpResponseRedirect('/clinicaltrial/')
    # return HttpResponse('登录失败！')

#修改信息
def edit_view(request):
        if request.method == "POST" and request.POST:
            data = request.POST
            edit_username = data.get("edit_username")
            edit_password = data.get("edit_password")
            edit_email = data.get("edit_email")
            edit_phone = data.get("edit_phone")
            User.objects.filter(username=edit_username).update(
                username=edit_username,
                password=SHA1(edit_password),
                # password=edit_password,
                email=edit_email,
                phone=edit_phone,
            )
            return render(request, "edit_success.html")
        return render(request, "edit.html")



#大屏
def data_view(request):
    return render(request,'final_n.html')


def test_show(request):
    clinialtrials = Clinicaltrial.objects.all()
    return render(request, 'test01.html', {'clinialtrials': clinialtrials})


def search_view(request):
    search_name = request.POST.get('title','')
    users = Clinicaltrial.objects.filter(title__icontains=search_name)
    if users.exists():
        return render(request, 'show2.html',{"users":users})
    return render(request,'show2.html')

def add_show(request):
    if request.method == 'POST':
        new_trial_id = request.POST.get('trial_id')
        new_title = request.POST.get('title')
        new_brief_title = request.POST.get('brief_title')
        new_acronym = request.POST.get('acronym')
        new_abstract = request.POST.get('abstract')
        new_detailed_description = request.POST.get('detailed_description')
        new_start_year = request.POST.get('start_year')
        new_phase = request.POST.get('phase')
        new_gender = request.POST.get('gender')
        new_registry = request.POST.get('registry')
        new_investigators_contacts = request.POST.get('investigators_contacts')
        new_dimensions_url = request.POST.get('dimensions_url')
        new_for_anzsrc_categories = request.POST.get('for_anzsrc_categories')
        new_city1 = request.POST.get('city1')
        new_state1 = request.POST.get('state1')
        new_country1 = request.POST.get('country1')

        Clinicaltrial.objects.create(
            trial_id=new_trial_id,title=new_title,brief_title=new_brief_title,acronym=new_acronym,
            abstract=new_abstract,detailed_description=new_detailed_description,start_year=new_start_year,
            phase=new_phase,registry=new_registry,city1=new_city1,state1=new_state1,country1=new_country1,
            dimensions_url=new_dimensions_url,investigators_contacts=new_investigators_contacts,for_anzsrc_categories=new_for_anzsrc_categories,gender=new_gender,
        )
        return render(request, "add_success.html")
    # # res = models.Clinicaltrial.objects.all()
    return render(request, 'show_add.html')

def edit_show(request):
    search_name = request.POST.get('trial_id', '')
    show = Clinicaltrial.objects.filter(trial_id=search_name)
    if show.exists():
        return render(request, 'show_edit.html', {"show": show})
    if request.method == 'POST':
        edit_trial_id = request.POST.get('trial_id')
        new_title = request.POST.get('title')
        new_brief_title = request.POST.get('brief_title')
        new_acronym = request.POST.get('acronym')
        new_abstract = request.POST.get('abstract')
        new_detailed_description = request.POST.get('detailed_description')
        new_start_year = request.POST.get('start_year')
        new_phase = request.POST.get('phase')
        new_gender = request.POST.get('gender')
        new_registry = request.POST.get('registry')
        new_investigators_contacts = request.POST.get('investigators_contacts')
        new_dimensions_url = request.POST.get('dimensions_url')
        new_for_anzsrc_categories = request.POST.get('for_anzsrc_categories')
        new_city1 = request.POST.get('city1')
        new_state1 = request.POST.get('state1')
        new_country1 = request.POST.get('country1')
        Clinicaltrial.objects.filter(trial_id=edit_trial_id).update(
            title=new_title, brief_title=new_brief_title, acronym=new_acronym,
            abstract=new_abstract, detailed_description=new_detailed_description, start_year=new_start_year,
            phase=new_phase, registry=new_registry, city1=new_city1, state1=new_state1, country1=new_country1,
            dimensions_url=new_dimensions_url, investigators_contacts=new_investigators_contacts,
            for_anzsrc_categories=new_for_anzsrc_categories, gender=new_gender,
        )
        return render(request, "edit_success.html")
    return render(request,'show_edit.html')

def bar_view(request):
    return render(request, 'my_test.html')

def pie_view(request):
    return render(request, 'my_pie.html')

def city_view(request):
    return render(request, 'timeline_bar.html')

def phase_view(request):
    return render(request, 'my_phase.html')

# bar_base(),


# nums = Clinicaltrial.objects.filter(start_year=2018).count()
# for clinialtrial in clinialtrials:
#     print(clinialtrial.title)

# num = Clinicaltrial.objects.filter(start_year=2018).count()
# print(num)

# url = Clinicaltrial.objects.values("dimensions_url")[0:2]
# print(url)

# name = Clinicaltrial.objects.values("investigators_contacts")[30:100]
# print(name)






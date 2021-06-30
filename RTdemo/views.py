from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from .models import Chapter, TestValue, Parameters, Projects, Paragraph, Table, Template, TestValue, ParameterValue
from RTdemo.common.response import json_response, json_error, read_file
from django.db import models
from django.db.models import Q
import os


# 获取章节全名，返回有问题，不用
def chapter_name(cid):
    data = Chapter.objects.filter(id=cid).values("layer", "parent_id", "sort", "name")
    d_list = data[:]
    return json_response(d_list)


# 获取参数列表
def para_in_new(request):
    # cursor = connection.cursor()
    # cursor.execute(
    #     "select p.para_name,p.display_name,p.unit,c.chapter_name from rtdemo_parameters p,rtdemo_Chapter c where v.chapter_id=c.id")
    # rows = cursor.fetchall()
    # data = {"paras": rows}
    # 获取所有参数列表
    # 有参数对应的章节ID
    q = None
    d_list = []
    if 'q' in request.GET:
        q = request.GET['q']
        # 显示章节名称。未完成。搜索章节时会引起报错。
        d_list = Chapter.objects.filter(id=q).values("layer", "parent_id", "sort", "name")
        p_val_list = Parameters.objects.filter(chp_id=q).values("id", "name", "display_name", "testvalue__value",
                                                                "testvalue__id", "unit", "testvalue__proj_id")
    else:
        # para_list = Parameters.objects.all()
        p_val_list = Parameters.objects.values("id", "name", "display_name", "testvalue__value", "testvalue__id",
                                               "unit", "testvalue__proj_id")
    values = filter_none(p_val_list)
    chapter = filter_none(d_list)
    # values = values.append(d_list)
    context = {"list": values, "chapter": chapter}
    print(context)
    return render(request, "new_demo_page.html", context)


# 获取参数列表
def para_in(request):
    q = None
    d_list = []
    if 'q' in request.GET:
        q = request.GET['q']
        # 显示章节名称。未完成。搜索章节时会引起报错。
        d_list = Chapter.objects.filter(id=q).values("layer", "parent_id", "sort", "name")
        p_val_list = Parameters.objects.filter(chp_id=q).values("id", "name", "display_name", "testvalue__value",
                                                                "testvalue__id", "unit", "testvalue__proj_id")
    else:
        # para_list = Parameters.objects.all()
        p_val_list = Parameters.objects.values("id", "name", "display_name", "testvalue__value", "testvalue__id",
                                               "unit", "testvalue__proj_id")
    values = filter_none(p_val_list)
    chapter = filter_none(d_list)
    # values = values.append(d_list)
    context = {"list": values, "chapter": chapter}
    print(context)
    return render(request, "demo_page_old.html", context)


# 保存（更新、插入）参数值
def save_parameter(request):
    if request.POST:
        # data = eval(data) #如果前端用了serializeStr的話需要
        if request.POST['id'] != "":
            # 更新一个参数值
            tv = TestValue.objects.get(id=request.POST['id'])
            tv.value = request.POST['value']
            tv.save()
        else:
            # 插入一个参数值
            value = TestValue(parameter_id=request.POST['parameter'], value=request.POST['value'],
                              proj_id=request.POST['pid'])
            value.save()
    return json_response('保存成功！')


# 保存章节参数
# def save_parameters(request,chpid):


# 加载章节明细页面
def load_detail(request, chpid):
    # 章节名称信息。
    c_detail = Chapter.objects.filter(id=chpid).values("layer", "parent_id", "sort", "name")
    p_val_list = Parameters.objects.filter(chp_id=chpid).values("id", "name", "display_name", "testvalue__value",
                                                                "testvalue__id", "unit", "testvalue__proj_id")
    values = filter_none(p_val_list)
    c_value = filter_none(c_detail)
    title = []
    if c_value[0]['layer'] == 1:
        # 只有一级
        title = c_value
    elif c_value[0]['layer'] == 2:
        # 有两级，再向上获取一级的信息
        # 此分支未测试
        p_detail = Chapter.objects.filter(id=c_value[0].parent_id).values("layer", "parent_id", "sort", "name")
        p_value = filter_none(p_detail)
        title = p_value
        title.append(c_value)
    context = {"list": values, "chapter": title}
    return render(request, "filing.html", context)


def test_load_detail(request, chpid):
    # 章节名称信息。
    c_detail = Chapter.objects.filter(id=chpid).values("layer", "parent_id", "sort", "name")
    p_val_list = Parameters.objects.filter(chp_id=chpid).values("id", "name", "display_name", "testvalue__value",
                                                                "testvalue__id", "unit", "testvalue__proj_id")
    values = filter_none(p_val_list)
    c_value = filter_none(c_detail)
    title = []
    if c_value[0]['layer'] == 1:
        # 只有一级
        title = c_value
    elif c_value[0]['layer'] == 2:
        # 有两级，再向上获取一级的信息
        # 此分支未测试
        p_detail = Chapter.objects.filter(id=c_value[0].parent_id).values("layer", "parent_id", "sort", "name")
        p_value = filter_none(p_detail)
        title = p_value
        title.append(c_value)
    context = {"list": values, "chapter": title}
    return render(request, "testfiling.html", context)


# 加载主题页面tooltip
def tooltip(request):
    return render(request, "tooltip.html")


# 避免前端出現none相關的錯誤
def filter_none(values):
    ret = []
    for row in values:
        for key in row:
            if row[key] is None:
                row[key] = ''
            else:
                row[key]
        ret.append(row)
    return ret

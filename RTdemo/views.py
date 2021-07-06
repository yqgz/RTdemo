from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from .models import Chapter, TestValue, Parameters, Projects, Paragraph, Table, Template, TestValue, ParameterValue
from RTdemo.common.response import json_response, json_error, read_file
from django.db import models
from django.db.models import Q
import os
from django.http import HttpResponse

def test(request):
    cid = 1
    chapter = chapter_name(cid)
    return json_response(str(chapter['sort']) + '.' + chapter['name'])

def test1(request):
    p_val_list = Parameters.objects.filter(chp_id=1).values("id", "name", "display_name", "testvalue__value",
                                                                "testvalue__id", "unit", "testvalue__proj_id")
    context = {'list': p_val_list}
    return render(request, "test1.html", context)


# 获取章节全名，简单
def chapter_name(cid):
    data = Chapter.objects.filter(id=cid).values("layer", "parent_id", "sort", "name")
    d_list = data[0]
    return d_list


# 获取参数列表（测试用）
def para_in_new(request):
    # cursor = connection.cursor()
    # cursor.execute(
    #     "select p.para_name,p.display_name,p.unit,c.chapter_name from rtdemo_parameters p,rtdemo_Chapter c where v.chapter_id=c.id")
    # rows = cursor.fetchall()
    # data = {"paras": rows}
    # 获取所有参数列表
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
        # 显示章节名称。
        d_list = chapter_name(q)
        p_val_list = Parameters.objects.filter(chp_id=q).values("id", "name", "display_name", "testvalue__value",
                                                                "testvalue__id", "unit", "testvalue__proj_id")

    else:
        # para_list = Parameters.objects.all()
        p_val_list = Parameters.objects.values("id", "name", "display_name", "testvalue__value", "testvalue__id",
                                               "unit", "testvalue__proj_id")
    values = filter_none(p_val_list)
    # chapter = filter_none(d_list)
    # values = values.append(d_list)
    context = {"list": values, "chapter": d_list}
    print(context)
    return render(request, "new_demo_page.html", context)


# 保存（更新、插入）单个参数值
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


# ？保存一个章节的全部内容？
def save_paragraph(request, chpid):
    if request.POST:
        if request.POST['chpid'] != "":
            pg = Paragraph.objects.get(chp_id=request.POST['chpid'])
            # ？判断是否已存在
            # 如果已有数据，更新一个值
            pg.content = request.POST.data
            pg.save()
        else:
            return json_response('没有提供章节id！')
    return json_response('本章节保存成功！')


# 加载章节明细页面
def load_detail(request, chpid):
    # 获取章节名称信息
    c_detail = chapter_name(chpid)
    # 获取章节参数列表
    p_val_list = Parameters.objects.filter(chp_id=chpid).values("id", "name", "display_name", "testvalue__value",
                                                                "testvalue__id", "unit", "testvalue__proj_id")
    # 获取章节段落文本
    paragraph = Paragraph.objects.filter(chp_id=chpid).values("id", "content", "temp_id", "proj_id")

    values = filter_none(p_val_list)
    # 处理章节名称层次
    # c_value = filter_none(c_detail)
    title = []
    print(c_detail['layer'])
    if c_detail['layer'] == 1:
        # 只有一级
        title = str(c_detail['sort']) + '.' + c_detail['name']
    elif c_detail['layer'] == 2:
        # 有两级，再向上获取一级的信息
        # 此分支未测试
        p_detail = chapter_name(c_detail.parent_id)
        # p_value = filter_none(p_detail)
        title = str(p_detail['sort']) + '.'
        title.append(str(c_detail['sort']) + '.' + c_detail['name'])
    context = {"list": values, "chapter": title}
    return render(request, "filing.html", context)


# Excel表测试页加载
def sheet_show(request):
    tid = 1
    # 获取章节中所有表
    table_list = Table.objects.filter(id=tid)
    # for tb in table_list:
    context = {"tb_list": table_list}
    return render(request, "sheet_demo.html", context)


# sheet表数据保存
def save_table(request):
    rid=0,
    tid=0,
    name='',
    sort=0,
    chpid=0
    data = request.POST['data']
    # 给模板设置表值
    if type == 'template':
        tb = Table.objects.filter(temp_id=rid, id=tid)
        # 对象为空，不存在，需要插入
        if not tb:
            tb = Table(name=name, sort=sort, table_data=data, chp_id=chpid, temp_id=rid)
        # 更新
        else:
            tb.save()
    # 给项目表填值
    elif type == 'project':
        tb = Table.objects.filter(proj_id=rid, id=tid)
        # 对象为空，不存在，需要插入
        if not tb:
            tb = Table(name=name, sort=sort, table_data=data, chp_id=chpid, proj_id=rid)
        else:
            tb.save()

    return json_response('保存成功！')


# 测试章节明细页面用
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
        ret.append(row)
    return ret

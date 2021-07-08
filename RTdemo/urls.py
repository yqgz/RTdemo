"""RTdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from RTdemo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("parameter",views.para_in,name='demo_page'),
    path("para_save/", views.save_parameter, name='para_save'),
    # 显示当前章节名
    path("show_chapter/<int:cid>", views.chapter_name, name='show_chapter'),
    # 按章节填写值
    path("filing/<int:chpid>/", views.load_detail, name='filing'),
    path("testfiling/<int:chpid>/", views.test_load_detail, name='testfiling'),

    path("", views.para_in, name='demo'),
    path("<int:cid>/", views.para_in, name='demo'),
    path("demo/", views.para_in_new, name='demo_new'),

    # 主题示例页面
    path("tooltip/", views.tooltip, name='tooltip'),

    # Excel sheet示例页
    path("sheet_demo/", views.sheet_show, name='sheet_demo'),
    path("save_table/", views.save_table, name='save_table'),
    path("csvsheet/", views.csv_show, name='csvsheet'),
    path("test/", views.test, name='test'),
    path("test1/", views.test1, name='test1'),
]

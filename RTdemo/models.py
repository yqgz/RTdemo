from django.db import models
from django.contrib.auth.models import User


# 报告章节
class Chapter(models.Model):
    name = models.CharField('章节名', max_length=100)
    layer = models.IntegerField('层级')
    order = models.IntegerField('排序', default=0)
    parent_id = models.IntegerField('父级', null=True, blank=True)

    def __str__(self):
        return self.name


# 全局参数
class Parameters(models.Model):
    name = models.CharField('参数名', max_length=50)
    display_name = models.CharField('参数中文名', max_length=100)
    unit = models.CharField('单位', max_length=10, null=True, blank=True)
    chp = models.ForeignKey(Chapter, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.name


# 项目
class Projects(models.Model):
    name = models.CharField('报告名', max_length=100, null=False)
    report_num = models.CharField('报告编号', max_length=50, null=False)
    create_time = models.DateTimeField('创建时间', auto_now=True)
    content = models.TextField('内容', null=True, blank=True)

    def __str__(self):
        return self.name


# 章节段落内容
class Paragraph(models.Model):
    content = models.TextField('内容', null=True, blank=True)
    chp = models.ForeignKey(Chapter, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.chp


# 表
class Table(models.Model):
    name = models.CharField('表名称', max_length=200, null=False)
    order = models.IntegerField('排序', null=False)
    # row_count = models.IntegerField('初始行数', null=False, default=1)
    table_data = models.TextField('表格内容')

    def __str__(self):
        return self.name


# 表字段
class Column(models.Model):
    name = models.CharField('列名称', max_length=200, null=False)
    header = models.CharField('二层表头列名', max_length=200, null=True, blank=True)
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE, db_index=True)
    formula = models.CharField('公式', max_length=500, null=True, blank=True)
    h_col_span = models.IntegerField('表头列数', null=True, blank=True)

    def __str__(self):
        return self.name


# 按单元格的位置存值
class TableCellValue(models.Model):
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE, db_index=True)
    coordinate = models.CharField('单元格坐标', max_length=10, null=False)
    value = models.CharField('值', max_length=100, null=False)
    proj_id = models.IntegerField('项目ID', null=True, blank=True)

    def __str__(self):
        return self.coordinate


# 模板
class Template(models.Model):
    name = models.CharField('模板名称', max_length=200, null=False)
    content = models.TextField('内容', null=True, blank=True)

    def __str__(self):
        return self.name


# demo显示参数用
class TestValue(models.Model):
    parameter = models.ForeignKey(Parameters, on_delete=models.CASCADE, db_index=True)
    value = models.CharField('参数值', max_length=100, null=False)

    def __str__(self):
        return self.parameter

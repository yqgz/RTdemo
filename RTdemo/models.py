from django.db import models
from django.contrib.auth.models import User


# 报告章节
class Chapter(models.Model):
    name = models.CharField('章节名', max_length=100)
    layer = models.IntegerField('层级')
    sort = models.IntegerField('排序', default=0)
    parent_id = models.IntegerField('父级', null=True, blank=True)

    def __str__(self):
        return self.sort + self.name + self.layer + self.parent_id


# 报告模板
class Template(models.Model):
    name = models.CharField('模板名称', max_length=200, null=False)
    content = models.TextField('内容', null=True, blank=True)

    def __str__(self):
        return self.name


# 全局参数
class Parameters(models.Model):
    name = models.CharField('参数名', max_length=50)
    display_name = models.CharField('参数中文名', max_length=100)
    unit = models.CharField('单位', max_length=10, null=True, blank=True, default='')
    chp = models.ForeignKey(Chapter, on_delete=models.CASCADE, db_index=True)
    temp = models.ForeignKey(Template, on_delete=models.CASCADE, db_index=True, default=1)

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
    temp = models.ForeignKey(Template, on_delete=models.CASCADE, db_index=True, default=1)
    proj = models.ForeignKey(Projects, on_delete=models.CASCADE, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.chp


# 表基本信息和表头
class Table(models.Model):
    name = models.CharField('表名称', max_length=200, null=False)
    sort = models.IntegerField('排序', null=False)
    # table_headers = models.TextField('表格头', null=True, blank=True)
    chp = models.ForeignKey(Chapter, on_delete=models.CASCADE, db_index=True, default=1)
    temp = models.ForeignKey(Template, on_delete=models.CASCADE, db_index=True, default=1)
    # proj = models.ForeignKey(Projects, on_delete=models.CASCADE, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.name


# 表内容
class TableData(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, db_index=True, default=1)
    data = models.TextField('表值', null=True, blank=True)
    # chp = models.ForeignKey(Chapter, on_delete=models.CASCADE, db_index=True, default=1)
    temp = models.ForeignKey(Template, on_delete=models.CASCADE, db_index=True, default=1)
    proj = models.ForeignKey(Projects, on_delete=models.CASCADE, db_index=True, blank=True, null=True)


# 表头（字段）
class Column(models.Model):
    name = models.CharField('列名', max_length=200, null=False)
    header = models.CharField('二层表头列名', max_length=200, null=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, db_index=True)
    formula = models.CharField('公式', max_length=500, null=True, blank=True)
    h_col_span = models.IntegerField('表头列数', null=True, blank=True)

    def __str__(self):
        return self.name


# 按单元格的位置存值
class TableCellValue(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, db_index=True)
    coordinate = models.CharField('单元格坐标', max_length=10, null=False)
    value = models.CharField('值', max_length=100, null=False)
    proj_id = models.IntegerField('项目ID', null=True, blank=True)

    def __str__(self):
        return self.coordinate


# demo显示参数用
class TestValue(models.Model):
    parameter = models.ForeignKey(Parameters, on_delete=models.CASCADE, db_index=True)
    value = models.CharField('参数值', max_length=100, null=False)
    proj = models.ForeignKey(Projects, on_delete=models.CASCADE, db_index=True, default=1)

    def __str__(self):
        return self.parameter


class ParameterValue(models.Model):
    parameter = models.ForeignKey(Parameters, on_delete=models.CASCADE, db_index=True)
    value = models.CharField('参数值', max_length=100, null=False)
    proj = models.ForeignKey(Projects, on_delete=models.CASCADE, db_index=True, default=1)

    def __str__(self):
        return self.parameter

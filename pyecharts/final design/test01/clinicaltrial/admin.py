from django.contrib import admin

# Register your models here.
from clinicaltrial.models import *

# admin.site.register(Clinicaltrial)

admin.site.register(User)

class ClinicaltrialAdmin(admin.ModelAdmin):
    # 显示表格列表字段
    list_display = ('trial_id','title', 'start_year', 'phase','city1',)
    # 条件查询字段
    list_filter = ('city1','start_year','phase','title',)
    # 搜索框中根据某些字段进行查询
    search_fields = ('trial_id','title')
    # 在admin后台类中加入raw_id_fields（只适用于外键）后，会显示外键的详细信息
    # raw_id_fields = ("author",)
    # 以某个日期字段分层次查询 hierarchy:层级
    # date_hierarchy = 'start_year'
    # 排序字段
    ordering = ['title', 'start_year','phase',]

admin.site.register(Clinicaltrial, ClinicaltrialAdmin)

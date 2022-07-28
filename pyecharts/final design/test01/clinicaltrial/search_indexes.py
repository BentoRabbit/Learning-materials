from haystack import indexes
from clinicaltrial.models import *


class ClinicaltrialIndex(indexes.SearchIndex, indexes.Indexable):
    # text字段是固定的
    text = indexes.CharField(document=True, use_template=True)
    # 给title 设置索引,对应模型类中的字段
    title = indexes.NgramField(model_attr='title')

    # 重写以下的两个方法
    def get_model(self):
        return Clinicaltrial

    # 整个结果的返回
    def index_queryset(self, using=None):
        return self.get_model().objects.order_by('-created')


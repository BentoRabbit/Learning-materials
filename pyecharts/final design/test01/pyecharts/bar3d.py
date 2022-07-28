import pyecharts.options as opts
from pyecharts.charts import Bar3D

from clinicaltrial.models import Clinicaltrial

"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://echarts.apache.org/examples/editor.html?c=bar3d-punch-card&gl=1

目前无法实现的功能:

1、光照和阴影暂时无法设置
"""

registry = [
    "ANZCTR",
    "CHICTR",
    "ClinicalTrials.gov",
    "EU-CTR",
    "UMIN-CTR"
]

citys = ["Shanghai", "Beijing", "Guangzhou", "Chengdu", "Hangzhou"]

data = [
    [0, 0, Clinicaltrial.objects.filter(registry="ANZCTR").filter(city1="Shanghai").count()],
    [0, 1, Clinicaltrial.objects.filter(registry="ANZCTR").filter(city1="Beijing").count()],
    [0, 2, Clinicaltrial.objects.filter(registry="ANZCTR").filter(city1="Guangzhou").count()],
    [0, 3, Clinicaltrial.objects.filter(registry="ANZCTR").filter(city1="Chengdu").count()],
    [0, 4, Clinicaltrial.objects.filter(registry="ANZCTR").filter(city1="Hangzhou").count()],
    [1, 0, Clinicaltrial.objects.filter(registry="CHICTR").filter(city1="Shanghai").count()],
    [1, 1, Clinicaltrial.objects.filter(registry="CHICTR").filter(city1="Beijing").count()],
    [1, 2, Clinicaltrial.objects.filter(registry="CHICTR").filter(city1="Guangzhou").count()],
    [1, 3, Clinicaltrial.objects.filter(registry="CHICTR").filter(city1="Chengdu").count()],
    [1, 4, Clinicaltrial.objects.filter(registry="CHICTR").filter(city1="Hangzhou").count()],
    [2, 0, Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(city1="Shanghai").count()],
    [2, 1, Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(city1="Beijing").count()],
    [2, 2, Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(city1="Guangzhou").count()],
    [2, 3, Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(city1="Chengdu").count()],
    [2, 4, Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(city1="Hangzhou").count()],
    [3, 0, Clinicaltrial.objects.filter(registry="EU-CTR").filter(city1="Shanghai").count()],
    [3, 1, Clinicaltrial.objects.filter(registry="EU-CTR").filter(city1="Beijing").count()],
    [3, 2, Clinicaltrial.objects.filter(registry="EU-CTR").filter(city1="Guangzhou").count()],
    [3, 3, Clinicaltrial.objects.filter(registry="EU-CTR").filter(city1="Chengdu").count()],
    [3, 4, Clinicaltrial.objects.filter(registry="EU-CTR").filter(city1="Hangzhou").count()],
    [4, 0, Clinicaltrial.objects.filter(registry="UMIN-CTR").filter(city1="Shanghai").count()],
    [4, 1, Clinicaltrial.objects.filter(registry="UMIN-CTR").filter(city1="Beijing").count()],
    [4, 2, Clinicaltrial.objects.filter(registry="UMIN-CTR").filter(city1="Guangzhou").count()],
    [4, 3, Clinicaltrial.objects.filter(registry="UMIN-CTR").filter(city1="Chengdu").count()],
    [4, 4, Clinicaltrial.objects.filter(registry="UMIN-CTR").filter(city1="Hangzhou").count()],
]
data = [[d[1], d[0], d[2]] for d in data]


c = (
    Bar3D(init_opts=opts.InitOpts(width="1600px", height="800px"))
    .add(
        series_name="",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(type_="category", data=registry),
        yaxis3d_opts=opts.Axis3DOpts(type_="category", data=citys),
        zaxis3d_opts=opts.Axis3DOpts(type_="value"),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            max_=20,
            range_color=[
                "#313695",
                "#4575b4",
                "#74add1",
                "#abd9e9",
                "#e0f3f8",
                "#ffffbf",
                "#fee090",
                "#fdae61",
                "#f46d43",
                "#d73027",
                "#a50026",
            ],
        )
    )
    .render("bar3d_punch_card.html")
)

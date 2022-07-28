import pyecharts.options as opts
from pyecharts.charts import Timeline, Bar, Pie

from clinicaltrial.models import Clinicaltrial

"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://www.echartsjs.com/examples/editor.html?c=mix-timeline-finance

目前无法实现的功能:

1、暂无
"""
total_data = {}
name_list = ["Shanghai",
             "Beijing",
             "Guangzhou",
             "Chengdu",
             "Hangzhou",
]

data_pi = {
    2011: [
        136.27,
        159.72,
        2905.73,
        641.42,
        1306.3,
    ],
    2010: [
        124.36,
        145.58,
        2562.81,
        554.48,
        1095.28,
    ],
    2009: [
        118.29,
        128.85,
        2207.34,
        477.59,
        929.6,
    ],
    2008: [
        112.83,
        122.58,
        2034.59,
        313.58,
        907.95,
    ],

}

data_si = {
    2011: [
        3752.48,
        5928.32,
        13126.86,
        6635.26,
        8037.69,
    ],
    2010: [
        3388.38,
        4840.23,
        10707.68,
        5234,
        6367.69,
    ],
    2009: [
        2855.55,
        3987.84,
        8959.83,
        3993.8,
        5114,
    ],
    2008: [
        2626.41,
        3709.78,
        8701.34,
        4242.36,
        4376.19,
    ],
}

data_ti = {
    2011: [
        12363.18,
        5219.24,
        8483.17,
        3960.87,
        5015.89,
    ],
    2010: [
        10600.84,
        4238.65,
        7123.77,
        3412.38,
        4209.03,
    ],
    2009: [
        9179.19,
        3405.16,
        6068.31,
        2886.92,
        3696.65,
    ],
    2008: [
        8375.76,
        2886.65,
        5276.04,
        2759.46,
        3212.06,
    ],
}



def format_data(data: dict) -> dict:
    for year in range(2008, 2012):
        max_data, sum_data = 0, 0
        temp = data[year]
        max_data = max(temp)
        for i in range(len(temp)):
            sum_data += temp[i]
            data[year][i] = {"name": name_list[i], "value": temp[i]}
        data[str(year) + "max"] = int(max_data / 100) * 100
        data[str(year) + "sum"] = sum_data
    return data


# 第一产业
total_data["dataPI"] = format_data(data=data_pi)
# 第二产业
total_data["dataSI"] = format_data(data=data_si)
# 第三产业
total_data["dataTI"] = format_data(data=data_ti)


#####################################################################################
# 2018 - 2021 年的数据
def get_year_overlap_chart(year: int) -> Bar:
    bar = (
        Bar()
        .add_xaxis(xaxis_data=name_list)
        .add_yaxis(
            series_name="CHICTR",
            y_axis=total_data["dataPI"][year],
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="ClinicalTrials.gov",
            y_axis=total_data["dataSI"][year],
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="etc",
            y_axis=total_data["dataTI"][year],
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="我国临床试验注册{}年数量".format(year), subtitle="数据来自xxx"
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="shadow"
            ),
        )
    )
    return bar


# 生成时间轴的图
timeline = Timeline(init_opts=opts.InitOpts(width="1600px", height="800px"))

for y in range(2008, 2012):
    timeline.add(get_year_overlap_chart(year=y), time_point=str(y))

# 1.0.0 版本的 add_schema 暂时没有补上 return self 所以只能这么写着
timeline.add_schema(is_auto_play=True, play_interval=1000)
timeline.render("finance_indices_2002.html")




tl = Timeline()
for i in range(2018, 2022):
    bar = (
        Bar()
        .add_xaxis(["Shanghai","Beijing","Guangzhou","Chengdu","Hangzhou"])
        .add_yaxis("CHICTR",
                   [Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=i).filter(city1="Shanghai").count(),
                    Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=i).filter(city1="Beijing").count(),
                    Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=i).filter(city1="Guangzhou").count(),
                    Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=i).filter(city1="Chengdu").count(),
                    Clinicaltrial.objects.filter(registry="CHICTR").filter(start_year=i).filter(city1="Hangzhou").count(),
                    ])
        .add_yaxis("ClinicalTrials.gov",
                   [Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=i).filter(city1="Shanghai").count(),
                    Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=i).filter(city1="Beijing").count(),
                    Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=i).filter(city1="Guangzhou").count(),
                    Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=i).filter(city1="Chengdu").count(),
                    Clinicaltrial.objects.filter(registry="ClinicalTrials.gov").filter(start_year=i).filter(city1="Hangzhou").count(),
                    ])
        .add_yaxis("etc.",
                   [Clinicaltrial.objects.exclude(registry="CHICTR").exclude(registry="ClinicalTrials.gov").filter(start_year=i).filter(city1="Shanghai").count(),
                    Clinicaltrial.objects.exclude(registry="CHICTR").exclude(registry="ClinicalTrials.gov").filter(start_year=i).filter(city1="Beijing").count(),
                    Clinicaltrial.objects.exclude(registry="CHICTR").exclude(registry="ClinicalTrials.gov").filter(city1="Guangzhou").count(),
                    Clinicaltrial.objects.exclude(registry="CHICTR").exclude(registry="ClinicalTrials.gov").filter(city1="Chengdu").count(),
                    Clinicaltrial.objects.exclude(registry="CHICTR").exclude(registry="ClinicalTrials.gov").filter(city1="Hangzhou").count(),
                    ]
                   )
        .set_global_opts(title_opts=opts.TitleOpts("我国临床试验注册{}年数量".format(i)))
    )
    tl.add(bar, "{}年".format(i))
tl.render("timeline_bar.html")


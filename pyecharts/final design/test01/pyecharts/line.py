import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker
from pymysql import *

namelist = ['2018','2019','2020','2021']
numlist = []


conn = connect(host='127.0.0.1',
                   port=3306,
                   user='root',
                   password='kk20130126',
                   db='clinicaltrial',
                   charset='utf8')
cursors = conn.cursor()
try:
    for i in namelist:
        sql = "select count(*) from clinicaltrial where start_year=\"{a}\"".format(a=i)
        # print(sql)
        sql_name = """{sql}""".format(sql=sql)
        cursors.execute(sql_name)
        nums = cursors.fetchall()
        for num in nums:
            numlist.append(num[0])
    # print(numlist)
    # numlist.sort(reverse=True)

except:
    print("未查询到数据！")
    conn.rollback()
finally:
    conn.close()


c = (
    Line()
    .add_xaxis(namelist)
    .add_yaxis("各个年份", numlist, is_smooth=True)
    .set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Line-面积图（紧贴 Y 轴）"),
        xaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            is_scale=False,
            boundary_gap=False,
        ),
    )
    .render("line_areastyle_boundary_gap.html")
)

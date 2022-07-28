from pyecharts import options as opts
from pyecharts.charts import Pie, Page
from pyecharts.faker import Faker

from pymysql import *

namelist = []
numlist = []


conn = connect(host='127.0.0.1',
                   port=3306,
                   user='root',
                   password='kk20130126',
                   db='clinicaltrial',
                   charset='utf8')
cursors = conn.cursor()
try:
        sql_name = """ select no from for_anzsrc_data order by quantity DESC"""
        cursors.execute(sql_name)
        names = cursors.fetchall()
        for name in names:
            namelist.append(name[0])
        # print(namelist)
        # namelist.sort(reverse=True)

        sql_num = """ select quantity from for_anzsrc_data order by quantity DESC"""
        cursors.execute(sql_num)
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
    Pie()
    .add(
        "",
        [list(z) for z in zip(namelist[0:10], numlist[0:10])],
        radius=["40%", "75%"],
        center=["25%", "50%"],
    )
    .add(
        "",
        [list(z) for z in zip(namelist[69:79], numlist[69:79])],
        radius=["40%", "75%"],
        center=["75%", "50%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="研究方向",subtitle="左：前十    右：后十"),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

    .render("pie_radius.html")
)

def pie1():
    pie = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(namelist[0:10], numlist[0:10])],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="研究方向(前十)"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

            # .render("pie_radius.html")
    )
    return pie

def pie2():
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(namelist[69:79], numlist[69:79])],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="研究方向(后十)"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c

def page_default_layout():
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        pie1(),
        pie2(),
    )
    page.render("pie_no.html")

    # Page.save_resize_html("page_default_layout.html",
    #                       cfg_file="chart_config.json",
    #                       dest="my_test.html")

if __name__ == "__main__":
    page_default_layout()

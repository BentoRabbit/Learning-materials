from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Page
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pymysql import *

namelist = ['Basic Science','Diagnostic New Technique Clincal Study','Health Services Research','N/A'
,'New Treatment Measure Clinical Study'
,'Phase 0'
,'Phase 1'
,'Phase 1/2'
,'Phase 2'
,'Phase 2/3'
,'Phase 3'
,'Phase 4'
,'Post Authorisation Studies'
,'Retrospective study'
]
numlist = []

# for i in namelist:
#     sql = "select count(Phase) from clinicaltrial where Phase=\"{a}\"".format(a=i)
#     print(sql)
    # print(i)


conn = connect(host='127.0.0.1',
                   port=3306,
                   user='root',
                   password='kk20130126',
                   db='clinicaltrial',
                   charset='utf8')
cursors = conn.cursor()
try:
        for i in namelist:
            sql = "select count(Phase) from clinicaltrial where Phase=\"{a}\"".format(a=i)
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

def bar_p():
    c = (
        Bar()
        .add_xaxis(namelist)
        .add_yaxis("阶段", numlist, category_gap=0, color=Faker.rand_color())
        .set_global_opts(title_opts=opts.TitleOpts(title="我国临床试验阶段"))
        # .render("bar_histogram.html")
    )
    return c
def pie_p():
    pie_p = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add(
        "",
        [list(z) for z in zip(namelist, numlist)],
        radius=["40%", "75%"],
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="我国临床试验阶段"),
        legend_opts=opts.LegendOpts( orient="vertical", pos_top="15%", pos_left="2%"),
    )
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        # .render("pie_radius.html")
    # .render("pie_radius.html")
)
    return pie_p

def page_default_layout():
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        bar_p(),
        pie_p(),
    )
    page.render("phase.html")

    # Page.save_resize_html("page_default_layout.html",
    #                       cfg_file="chart_config.json",
    #                       dest="my_test.html")

if __name__ == "__main__":
    page_default_layout()
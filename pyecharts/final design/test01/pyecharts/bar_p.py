from pyecharts import options as opts
from pyecharts.charts import Pie, Bar
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

def getdata():
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

def drawbar_p():
    c = (
        Bar()
        .add_xaxis(namelist)
        .add_yaxis("阶段", numlist, category_gap=0, color=Faker.rand_color())
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-直方图"))
        .render("bar_histogram.html")
    )

pie_p = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add(
        "",
        [list(z) for z in zip(namelist, numlist)],
        radius=["40%", "75%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Pie-Radius"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("pie_radius.html")
)


if __name__ == '__main__':
    getdata()
    drawbar_p()
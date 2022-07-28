from pyecharts.charts import Bar, Line,Page


# bar = (
#     Bar()
#     .add_xaxis([2018,2019,2020,2021])
#     .add_yaxis("各个年份",[Clinicaltrial.objects.filter(start_year=2018).count(),Clinicaltrial.objects.filter(start_year=2019).count(),Clinicaltrial.objects.filter(start_year=2020).count(),Clinicaltrial.objects.filter(start_year=2021).count()])
#     .set_global_opts(title_opts=opts.TitleOpts(title="每年注册的临床试验数量（近四年）"))
# )
# bar.render("E:\\final design\\test01\\templates\\bar_base.html")
#

from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pymysql import *

namelist = ['2018','2019','2020','2021']
numlist1 = []
numlist2 = []
numlist3 = []


conn = connect(host='127.0.0.1',
                   port=3306,
                   user='root',
                   password='kk20130126',
                   db='clinicaltrial',
                   charset='utf8')
cursors = conn.cursor()
try:
    for i in namelist:
        sql = "select count(*) from clinicaltrial where start_year=\"{a}\" and registry='CHICTR'".format(a=i)
        # print(sql)
        sql_name = """{sql}""".format(sql=sql)
        cursors.execute(sql_name)
        nums = cursors.fetchall()
        for num in nums:
            numlist1.append(num[0])
    # print(numlist)
    # numlist.sort(reverse=True)
    for i in namelist:
        sql = "select count(*) from clinicaltrial where start_year=\"{a}\" and registry='ClinicalTrials.gov'".format(a=i)
        # print(sql)
        sql_name = """{sql}""".format(sql=sql)
        cursors.execute(sql_name)
        nums = cursors.fetchall()
        for num in nums:
            numlist2.append(num[0])

    for i in namelist:
        sql = "select count(*) from clinicaltrial where start_year=\"{a}\" and registry!='CHICTR' and registry!='ClinicalTrials.gov'".format(a=i)
        # print(sql)
        sql_name = """{sql}""".format(sql=sql)
        cursors.execute(sql_name)
        nums = cursors.fetchall()
        for num in nums:
            numlist3.append(num[0])
except:
    print("未查询到数据！")
    conn.rollback()
finally:
    conn.close()

def bar() -> Bar:
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(namelist)
        .add_yaxis("各个年份CHICTR注册数量", numlist1)
        .add_yaxis("各个年份ClinicalTrials.gov注册数量", numlist2)
        .add_yaxis("各个年份其他注册数量", numlist3)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="每年注册的临床试验数量（近四年）"),
            toolbox_opts=opts.ToolboxOpts(is_show=True,orient="vertical",pos_left="95%",pos_top="5%"),
            legend_opts=opts.LegendOpts(is_show=True, pos_top="5%"),)
        # .render("bar_toolbox.html")
    )
    return bar


from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts


def table_base() -> Table:
    table = Table()

    headers = ["年份", "CHICTR", "ClinicalTrials.gov", "其他"]
    rows = [
        ["2018", numlist1[0], numlist2[0], numlist3[0]],
        ["2019", numlist1[1], numlist2[1], numlist3[1]],
        ["2020", numlist1[2], numlist2[2], numlist3[2]],
        ["2021", numlist1[3], numlist2[3], numlist3[3]],
    ]
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="每年注册的临床试验数量", subtitle="")
    )

    return table

def page_default_layout():
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        bar(),
        table_base(),
    )
    page.render("page_default_layout.html")

    # Page.save_resize_html("page_default_layout.html",
    #                       cfg_file="chart_config.json",
    #                       dest="my_test.html")

if __name__ == "__main__":
    page_default_layout()



# line = (
#     Line()
#     .add_xaxis(xaxis_data=namelist)
#     .add_yaxis(
#         series_name="各个年份",
#         yaxis_index=1,
#         y_axis = numlist,
#         label_opts=opts.LabelOpts(is_show=False),
#     )
# .render("line.html")
# )
#
# bar.overlap(line).render("bar_line.html")




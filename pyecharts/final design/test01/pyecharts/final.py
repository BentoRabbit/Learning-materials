import jieba
from bs4 import BeautifulSoup
from pyecharts import options as opts
from pyecharts.charts import WordCloud, Timeline
from pyecharts.charts import Bar, Map, Geo, Page
from pyecharts.charts import Pie
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType, SymbolType
from pymysql import *

bar_namelist = ['2018','2019','2020','2021']
bar_numlist1 = []
bar_numlist2 = []
bar_numlist3 = []

state_namelist = ['Jiangsu',
'Sichuan',
'Shanghai',
'Beijing',
'HongKong',
'Shaanxi',
'Hubei',
'Chongqing',
'Jiangxi',
'Guangdong',
'Shandong',
'Tianjin',
'Heilongjiang',
'Zhejiang',
'Anhui',
'Yunnan',
'Guangxi',
'Jilin',
'Gansu',
'Fujian',
'Hunan',
'Guizhou',
'Xinjiang',
'Liaoning',
'Hebei',
'Henan',
'Hainan',
'Ningxia',
'Shanxi',
'Macau',
'Tibet',
'Qinghai',
'Taipei'
]
state_list = ['江苏',
'四川',
'上海',
'北京',
'香港',
'陕西',
'湖北',
'重庆',
'江西',
'广东',
'山东',
'天津',
'黑龙江',
'浙江',
'安徽',
'云南',
'广西',
'吉林',
'甘肃',
'福建',
'湖南',
'贵州',
'新疆',
'辽宁',
'河北',
'河南',
'海南',
'宁夏',
'山西',
'澳门',
'西藏',
'青海',
'台湾'
]
numlist =[]

namelist_pie = []
numlist_pie = []

namelist_bar_p = ['Basic Science','Diagnostic New Technique Clincal Study','Health Services Research','N/A'
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
numlist_bar_p = []


name_list = ["Shanghai",
             "Beijing",
             "Guangzhou",
             "Chengdu",
             "Hangzhou",
]
numlist1 =[]
numlist2 =[]
numlist3 =[]


# def getdata():
conn = connect(host='127.0.0.1',
                   port=3306,
                   user='root',
                   password='kk20130126',
                   db='clinicaltrial',
                   charset='utf8')
cursors = conn.cursor()
try:
    ###地图数据
    for i in state_namelist:
        sql = "select count(*) from clinicaltrial where state1=\"{a}\"".format(a=i)
        # print(sql)
        sql_name = """{sql}""".format(sql=sql)
        cursors.execute(sql_name)
        nums = cursors.fetchall()
        for num in nums:
            numlist.append(num[0])
        # print(numlist)
        # numlist.sort(reverse=True)

    ###直方图数据
    for i in namelist_bar_p:
        sql = "select count(Phase) from clinicaltrial where Phase=\"{a}\"".format(a=i)
        # print(sql)
        sql_name = """{sql}""".format(sql=sql)
        cursors.execute(sql_name)
        nums = cursors.fetchall()
        for num in nums:
            numlist_bar_p.append(num[0])

    ###饼图数据
    sql_name = """ select no from for_anzsrc_data """
    cursors.execute(sql_name)
    names = cursors.fetchall()
    for name in names:
        namelist_pie.append(name[0])
    # print(namelist)
    # namelist.sort(reverse=True)

    sql_num = """ select quantity from for_anzsrc_data """
    cursors.execute(sql_num)
    nums = cursors.fetchall()
    for num in nums:
        numlist_pie.append(num[0])
        # print(numlist)
        # numlist.sort(reverse=True)

###直方图年份数据
    for i in bar_namelist:
        sql = "select count(*) from clinicaltrial where start_year=\"{a}\" and registry='CHICTR'".format(a=i)
        # print(sql)
        sql_name = """{sql}""".format(sql=sql)
        cursors.execute(sql_name)
        nums = cursors.fetchall()
        for num in nums:
            bar_numlist1.append(num[0])
    # print(numlist)
    # numlist.sort(reverse=True)
    for i in bar_namelist:
        sql = "select count(*) from clinicaltrial where start_year=\"{a}\" and registry='ClinicalTrials.gov'".format(a=i)
        # print(sql)
        sql_name = """{sql}""".format(sql=sql)
        cursors.execute(sql_name)
        nums = cursors.fetchall()
        for num in nums:
            bar_numlist2.append(num[0])

    for i in bar_namelist:
        sql = "select count(*) from clinicaltrial where start_year=\"{a}\" and registry!='CHICTR' and registry!='ClinicalTrials.gov'".format(a=i)
        # print(sql)
        sql_name = """{sql}""".format(sql=sql)
        cursors.execute(sql_name)
        nums = cursors.fetchall()
        for num in nums:
            bar_numlist3.append(num[0])


    ###动态柱状图
    for n in range(2018, 2022):
        for i in name_list:
            sql1 = "select count(*) from clinicaltrial where registry='CHICTR' and city1=\"{a}\" and Start_Year=\"{b}\"".format(a=i, b=n)
            # print(sql1)
            sql_name = """{sql}""".format(sql=sql1)
            cursors.execute(sql_name)
            nums = cursors.fetchall()
            for num in nums:
                numlist1.append(num[0])

    for n in range(2018, 2022):
        for i in name_list:
            sql2 = "select count(*) from clinicaltrial where registry='ClinicalTrials.gov' and city1=\"{a}\" and Start_Year=\"{b}\"".format(a=i, b=n)
            # print(sql1)
            sql_name = """{sql}""".format(sql=sql2)
            cursors.execute(sql_name)
            nums = cursors.fetchall()
            for num in nums:
                numlist2.append(num[0])
    for n in range(2018, 2022):
        for i in name_list:
            sql3 = "select count(*) from clinicaltrial where registry!='CHICTR' and registry!='ClinicalTrials.gov' and city1=\"{a}\" and Start_Year=\"{b}\"".format(
                    a=i, b=n)
            # print(sql1)
            sql_name = """{sql}""".format(sql=sql3)
            cursors.execute(sql_name)
            nums = cursors.fetchall()
            for num in nums:
                numlist3.append(num[0])


except:
    print("未查询到数据！")
    conn.rollback()
finally:
    conn.close()


###地图
# def drawmap():
    map = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add("地区", [list(z) for z in zip(state_list, numlist)], "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="中国各地区临床试验注册数量"), visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                                                pieces=[
                                                  {"max": 5000, "min": 1000, "label": ">1500", "color": "#B40404"},
                                                  {"max": 1000, "min": 500, "label": "1000-1500", "color": "#DF0101"},
                                                  {"max": 500, "min": 100, "label": "500-1000", "color": "#F78181"},
                                                  {"max": 100, "min": 20, "label": "100-500", "color": "#F5A9A9"},
                                                  {"max": 20, "min": 0, "label": "0-100", "color": "#FFFFCC"},
                                              ])
    )
    # .render("map_china.html")
    )

###饼图（编号）
# def drawpie():
pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK, width='500px', height='350px'))
        .add("",[namelist for namelist in zip(namelist_pie,numlist_pie)])
        .set_global_opts(title_opts=opts.TitleOpts(title="饼图（研究编号）"),legend_opts=opts.LegendOpts(is_show=False))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        # .render("pie_base.html")
    )

###（phase）环形
# def drawbar_p():
# bar_p = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
#         .add_xaxis(namelist_bar_p)
#         .add_yaxis("阶段", numlist_bar_p)
#         .set_global_opts(title_opts=opts.TitleOpts(title="我国临床试验阶段直方图"))
#         # .render("bar_histogram.html")
#     )
pie_p = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add(
        "",
        [list(z) for z in zip(namelist_bar_p, numlist_bar_p)],
        radius=["40%", "75%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="我国临床试验阶段"),
        legend_opts=opts.LegendOpts(is_show=False,orient="vertical", pos_top="15%", pos_left="2%"),
    )
    # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    # .render("pie_radius.html")
)

###直方图（year）
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add_xaxis(bar_namelist)
        .add_yaxis("各个年份CHICTR注册数量", bar_numlist1)
        .add_yaxis("各个年份ClinicalTrials.gov注册数量", bar_numlist2)
        .add_yaxis("各个年份其他注册数量", bar_numlist3)
        .set_global_opts(
        title_opts=opts.TitleOpts(title="每年注册的临床试验数量（近四年）"),
        toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="95%", pos_top="5%"),
        legend_opts=opts.LegendOpts(is_show=True, pos_top="5%"), )
    # .render("bar_toolbox.html")
)


###词云图
txt = open("E:\毕设\data\city-new3.txt", encoding='utf-8').read()

words = jieba.lcut(txt)
counts = {}
for word in words:
    if len(word) == 1:
        continue
    else:
        counts[word] = counts.get(word, 0) + 1

items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)

wordcloud = (
    WordCloud(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add("",data_pair=items,word_size_range=[10,50],mask_image="E:\毕设\p1.jpg", width="800",height="800")
    # .add("", words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
    .set_global_opts()
    # .render("E:\\final design\\test01\\templates\wordcloud.html")
)
# c = (
#     WordCloud()
#     .add("", words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
#     .set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-shape-diamond"))
#     .render("wordcloud_diamond.html")
# )


###动态柱状图
bar_1 = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
                .add_xaxis(["Shanghai", "Beijing", "Guangzhou", "Chengdu", "Hangzhou"])
                .add_yaxis("CHICTR",numlist1[0:5])
                .add_yaxis("ClinicalTrials.gov",numlist2[0:5])
                .add_yaxis("etc.",numlist3[0:5])
                .set_global_opts(title_opts=opts.TitleOpts("我国临床试验注册2018年数量"))
        )
bar_2 = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
                .add_xaxis(["Shanghai", "Beijing", "Guangzhou", "Chengdu", "Hangzhou"])
                .add_yaxis("CHICTR",numlist1[5:10])
                .add_yaxis("ClinicalTrials.gov",numlist2[5:10])
                .add_yaxis("etc.",numlist3[5:10])
                .set_global_opts(title_opts=opts.TitleOpts("我国临床试验注册2019年数量"))
        )
bar_3 = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
                .add_xaxis(["Shanghai", "Beijing", "Guangzhou", "Chengdu", "Hangzhou"])
                .add_yaxis("CHICTR",numlist1[10:15])
                .add_yaxis("ClinicalTrials.gov",numlist2[10:15])
                .add_yaxis("etc.",numlist3[10:15])
                .set_global_opts(title_opts=opts.TitleOpts("我国临床试验注册2020年数量"))
        )
bar_4 = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
                .add_xaxis(["Shanghai", "Beijing", "Guangzhou", "Chengdu", "Hangzhou"])
                .add_yaxis("CHICTR",numlist1[15:20])
                .add_yaxis("ClinicalTrials.gov",numlist2[15:20])
                .add_yaxis("etc.",numlist3[15:20])
                .set_global_opts(title_opts=opts.TitleOpts("我国临床试验注册2021年数量"))
        )

tl = (
        Timeline(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .add(bar_1, "2018年")
        .add(bar_2, "2019年")
        .add(bar_3, "2020年")
        .add(bar_4, "2021年")
        # .render("timeline_bar.html")
    )

big_title = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        .set_global_opts(
        title_opts=opts.TitleOpts(title="我国临床试验情况可视化大屏",pos_left="40%",
                                  title_textstyle_opts=opts.TextStyleOpts(font_size=40, color='#ffffff',
                                                                          border_radius=True, border_color="white"),
                                  pos_top=0)))
if __name__ == '__main__':
    # getdata()
    # pie = drawpie()
    # bar_p = drawbar_p()
    # map = drawmap()
    # bar_m = drawbar_m()
    page = (Page(page_title="我国临床试验情况可视化大屏",layout=Page.DraggablePageLayout)
        .add(pie)
        .add(pie_p)
        .add(bar)
        .add(map)
        .add(wordcloud)
        .add(tl)
        .add(big_title)
    ).render('E:\\final design\\test01\\templates\\final.html')

    # with open("E:\\final design\\test01\\templates\\final.html", "r+", encoding='utf-8') as html:
    #     html_bf = BeautifulSoup(html, 'lxml')
    #     divs = html_bf.select('.chart-container')
    #     divs[0][
    #         'style'] = "width:550px;height:500px;position:absolute;top:50px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"
    #     divs[1][
    #         "style"] = "width:450px;height:400px;position:absolute;top:50px;left:1100px;border-style:solid;border-color:#444444;border-width:0px;"
    #     divs[2][
    #         "style"] = "width:409px;height:405px;position:absolute;top:50px;left:650px;border-style:solid;border-color:#444444;border-width:0px;"
    #     divs[3][
    #         "style"] = "width:505px;height:455px;position:absolute;top:520px;left:50px;border-style:solid;border-color:#444444;border-width:0px;"
    #     divs[4][
    #         "style"] = "width:800px;height:455px;position:absolute;top:520px;left:650px;border-style:solid;border-color:#444444;border-width:0px;"
    #     # divs[5][
    #     #     "style"] = "width:590px;height:500px;position:absolute;top:480px;left:1100px;border-style:solid;border-color:#444444;border-width:0px;"
    #     divs[5][
    #         "style"] = "width:1000px;height:800px;position:absolute;top:0px;left:650px;border-style:solid;border-color:#444444;border-width:0px;"
    #
    #     body = html_bf.find("body")
    #     body["style"] = "background-color:#FFFFFF;"
    #     html_new = str(html_bf)
    #     html.seek(0, 0)
    #     html.truncate()
    #     html.write(html_new)
    #     html.close()

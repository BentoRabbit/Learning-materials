from bs4 import BeautifulSoup
from pymysql import *
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline, Bar, Page
from pyecharts.faker import Faker

total_data = {}
name_list = ["Shanghai",
             "Beijing",
             "Guangzhou",
             "Zhejiang",
             "Jiangsu",
]
numlist1 =[]
numlist2 =[]
numlist3 =[]



conn = connect(host='127.0.0.1',
                   port=3306,
                   user='root',
                   password='kk20130126',
                   db='clinicaltrial',
                   charset='utf8')
cursors = conn.cursor()
try:
    for n in range(2018, 2022):
        for i in name_list:
            sql1 = "select count(*) from clinicaltrial where registry='CHICTR' and city1=\"{a}\" and Start_Year=\"{b}\"".format(a=i,b=n)
            # print(sql1)
            sql_name = """{sql}""".format(sql=sql1)
            cursors.execute(sql_name)
            nums = cursors.fetchall()
            for num in nums:
                numlist1.append(num[0])
        # print(numlist)
        # numlist.sort(reverse=True)
    for n in range(2018, 2022):
        for i in name_list:
            sql2 = "select count(*) from clinicaltrial where registry='ClinicalTrials.gov' and city1=\"{a}\" and Start_Year=\"{b}\"".format(a=i,b=n)
            # print(sql1)
            sql_name = """{sql}""".format(sql=sql2)
            cursors.execute(sql_name)
            nums = cursors.fetchall()
            for num in nums:
                numlist2.append(num[0])
    for n in range(2018, 2022):
        for i in name_list:
            sql3 = "select count(*) from clinicaltrial where registry!='CHICTR' and registry!='ClinicalTrials.gov' and city1=\"{a}\" and Start_Year=\"{b}\"".format(a=i,b=n)
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



# def drawbar_m():
for i in range(2018, 2022):
    if i == 2018:
        a = numlist1[0:5]
        b = numlist2[0:5]
        c = numlist3[0:5]
    elif i == 2019:
        a = numlist1[5:10]
        b = numlist2[5:10]
        c = numlist3[5:10]
    elif i == 2020:
        a = numlist1[10:15]
        b = numlist2[10:15]
        c = numlist3[10:15]
    elif i == 2021:
        a = numlist1[15:20]
        b = numlist2[15:20]
        c = numlist3[15:20]
    bar = (
            Bar()
                .add_xaxis(["Shanghai", "Beijing", "Guangzhou", "Zhejiang", "Jiangsu"])
                .add_yaxis("CHICTR",a)
                .add_yaxis("ClinicalTrials.gov",b)
                .add_yaxis("etc.",c)
                .set_global_opts(title_opts=opts.TitleOpts("我国临床试验注册{}年数量".format(i)))
        )

    tl = (
        Timeline()
        .add(bar, "{}年".format(i))
        .render("timeline_bar.html")
    )




page = (Page(page_title="我国临床试验情况可视化大屏")
        .add(tl)
        # .add(bar_p)
        # .add(map)
        # .add(wordcloud)
        # .add(bar_m)
    ).render('E:\\final design\\test01\\templates\\final_t.html')

with open("E:\\final design\\test01\\templates\\final_t.html", "r+", encoding='utf-8') as html:
        html_bf = BeautifulSoup(html, 'lxml')
        divs = html_bf.select('.chart-container')
        divs[0][
        'style'] = "width:550px;height:500px;position:absolute;top:50px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"
        # divs[1][
        # "style"] = "width:450px;height:400px;position:absolute;top:50px;left:1100px;border-style:solid;border-color:#444444;border-width:0px;"
        # divs[2][
        # "style"] = "width:409px;height:405px;position:absolute;top:50px;left:650px;border-style:solid;border-color:#444444;border-width:0px;"
        # divs[3][
        # "style"] = "width:505px;height:455px;position:absolute;top:520px;left:50px;border-style:solid;border-color:#444444;border-width:0px;"
        # # divs[4][
        # "style"] = "width:409px;height:304px;position:absolute;top:520px;left:650px;border-style:solid;border-color:#444444;border-width:0px;"

        body = html_bf.find("body")
        body["style"] = "background-color:#ffffff;"
        html_new = str(html_bf)
        html.seek(0, 0)
        html.truncate()
        html.write(html_new)
        html.close()
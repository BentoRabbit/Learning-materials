from pymysql import *
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline, Bar
from pyecharts.faker import Faker

total_data = {}
name_list = ["Shanghai",
             "Beijing",
             "Guangzhou",
             "Chengdu",
             "Hangzhou",
]
numlist1 =[]
numlist2 =[]
numlist3 =[]


def getdata():
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



def drawbar_m():
    tl = Timeline()
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
                .add_xaxis(["Shanghai", "Beijing", "Guangzhou", "Chengdu", "Hangzhou"])
                .add_yaxis("CHICTR",a)
                .add_yaxis("ClinicalTrials.gov",b)
                .add_yaxis("etc.",c)
                .set_global_opts(title_opts=opts.TitleOpts("我国临床试验注册{}年数量".format(i)))
        )
        tl.add(bar, "{}年".format(i))
    tl.render("timeline_bar.html")



if __name__ == '__main__':
    getdata()
    drawbar_m()
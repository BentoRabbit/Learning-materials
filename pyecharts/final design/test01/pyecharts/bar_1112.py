from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker
from pymysql import *

namelist = [1,2,3,4,5]
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
        sql = "select count(Completion_Year-Start_Year)  from clinicaltrial.clinicaltrial where `FOR (ANZSRC) Categories` like '%1112 Oncology and Carcinogenesis%' and Completion_Year-Start_Year=\"{a}\";".format(a=i)
        # sql = "select count(*) from clinicaltrial where start_year=\"{a}\" and registry='CHICTR'".format(a=i)
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

namelist = ["1年","2年","3年","4年","5年"]

c = (
    Bar()
    .add_xaxis(namelist)
    .add_yaxis("研究周期统计数量", numlist, category_gap=0, color=Faker.rand_color())
    .set_global_opts(title_opts=opts.TitleOpts(title="关于肿瘤学和癌变的研究周期"))
    .render("bar_1112.html")
)

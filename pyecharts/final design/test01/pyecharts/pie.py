from pyecharts import options as opts
from pyecharts.charts import Pie
from pymysql import *

namelist = []
numlist = []

def getdata():
    conn = connect(host='127.0.0.1',
                   port=3306,
                   user='root',
                   password='kk20130126',
                   db='clinicaltrial',
                   charset='utf8')
    cursors = conn.cursor()
    try:
        sql_name = """ select no from for_anzsrc_data """
        cursors.execute(sql_name)
        names = cursors.fetchall()
        for name in names:
            namelist.append(name[0])
        # print(namelist)
        # namelist.sort(reverse=True)

        sql_num = """ select quantity from for_anzsrc_data """
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



def drawpie():
    pie = (
        Pie()
        .add("",[namelist for namelist in zip(namelist,numlist)])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="For Anzsrc Data"),
            legend_opts=opts.LegendOpts(is_show=True,pos_left="80%")
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .render("pie_base.html")
    )

if __name__ == '__main__':
    getdata()
    drawpie()
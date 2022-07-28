from pymysql import *
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker

namelist = ['Jiangsu',
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
            sql = "select count(*) from clinicaltrial where state1=\"{a}\"".format(a=i)
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



def drawmap():
    c = (
    Map()
    .add("商家A", [list(z) for z in zip(state_list, numlist)], "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Map-地图"), visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                                                pieces=[
                                                  {"max": 5000, "min": 1500, "label": ">1500", "color": "#B40404"},
                                                  {"max": 1500, "min": 1000, "label": "1000-1500", "color": "#DF0101"},
                                                  {"max": 1000, "min": 500, "label": "500-1000", "color": "#F78181"},
                                                  {"max": 500, "min": 100, "label": "100-500", "color": "#F5A9A9"},
                                                  {"max": 100, "min": 0, "label": "0-100", "color": "#FFFFCC"},
                                              ])
    )
    .render("map_china.html")
    )


if __name__ == '__main__':
    getdata()
    drawmap()
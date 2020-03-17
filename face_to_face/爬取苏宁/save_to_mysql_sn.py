# 若能避开猛烈的欢喜,自然也不会有悲痛的来袭,
# 迎着风雨走 孤独且自由,
# Author: xyy, time:2020/3/9

import pymysql
import random

def get_info_from_mysql(title,price,assess):# 返回结果的第一个 字典 "{}" 为空返回空 以某个字开头的
    conn = pymysql.connect(host='39.108.15.78', port=3306, user='root', passwd='Xueyiyang', db='commpany_of_lan',
                           charset='utf8mb4')
    cursor = conn.cursor()

    sql = """insert into su_ning2(title,price,assess) VALUES("{}","{}","{}")""".format(title,price,assess)
    # print(sql)
    cursor.execute(sql)  # escape_string(floor_content_html.decode('utf-8'))
    conn.commit()



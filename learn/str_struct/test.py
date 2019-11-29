"""
1. 字符串，单双引号都可以
2. 三个引号的可以换行
3. 使用反斜杠转义
4. 反斜杠可以接8、16进制和 Unicode 编码
5. 如果不希望反斜杠转义，那么在字符串最前面加个 r
"""

# import yaml
# import pymysql
#
# try:
#     config = yaml.load(open('../../config/config.yml', 'r'), Loader=yaml.FullLoader)
#     conn = pymysql.connect(**config['DB'], cursorclass=pymysql.cursors.DictCursor)
#     c = conn.cursor()
#     c.execute('select * from users limit 2')
#     rst = c.fetchall()
#     print(rst)
# finally:
#     pass

import os
import datetime


# def get_last_sync_time():
#     filename = os.getcwd() + '/last_sync_time.txt'
#     now = datetime.datetime.now()
#     fmt = '%Y-%m-%d %H:%M:%S'
#     end = now.strftime(fmt)
#     try:
#         r = open(filename, mode='r')
#         start = datetime.datetime.strptime(r.readline(), fmt)
#     except:
#         start = now.strftime('%Y-%m-%d 00:00:00')
#     finally:
#         w = open(filename, 'w')
#         w.write(end)
#         w.flush()
#
#     return {
#         'start': start,
#         'end': end
#     }


# get_last_sync_time()
# */1 * * * * /usr/local/python3/SYNC_ENV/bin/python /root/workspace/sync_es/es_sync_data.py
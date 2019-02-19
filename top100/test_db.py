import os
from webtools import db_connection
import pymysql

results = list(db_connection.db_12_boss.query('SELECT code,`name` from vnet_zz_port WHERE `code` != "" GROUP BY `code` '))
result_cust = list(db_connection.db_12_boss.query("select * from vnet_zz_port where code = '%s' group by port_code_key" % ('0010035230')))

db_cacti_6 = pymysql.connect("xx.xx.xx.6","cselect","mysql_cacti","cacti")
cursor = db_cacti_6.cursor()
cursor.execute("SELECT DISTINCT users.full_name,perm.item_id,graph.local_graph_id,graph.title_cache FROM user_auth_perms perm JOIN user_auth users ON perm.user_id = users.id JOIN graph_templates_graph graph ON perm.item_id = graph.local_graph_id WHERE graph.title_cache IS NOT NULL AND graph.title_cache != '' AND users.full_name like '%拉扎斯%'")
data = cursor.fetchall()
print(data)



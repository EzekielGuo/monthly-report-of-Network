import web

web.config.debug = True

db_80 = web.database(dbn='mysql',user='xx',pw='xx',host='xx',db='',charset='utf8')
db_98_pingdb = web.database(dbn='mysql',user='xx',pw='xx',host='xx',db='pingdb',charset='utf8')
db_12_boss = web.database(dbn='mysql',user='xx',pw='xx',host='xx',db='boss',charset='utf8')
db_54_boss = web.database(dbn='mysql',user='xx',pw='xx',host='xx',db='erpapi',charset='utf8')
import time
import datetime

localtime = time.localtime(time.time())
year_str = str(localtime[0])
month = localtime[1]
month_str = 0
if month < 10:
    month_str = "0" + str(month)
es_index = 'ordinary-' + year_str + '.' + month_str + '*'
print(es_index)
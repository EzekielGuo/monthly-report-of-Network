import os
import sys
import web
os.system('cd /etc/script')

num = sys.argv[1]
year = sys.argv[2]
month = sys.argv[3]
command = 'xvfb-run --server-args="-screen 0, 1366x768" wkhtmltopdf "http://xx:8000/yuebao?code={}&year={}&month={}" /etc/script/{}_{}_{}.pdf'.format(num,year,month,num,year,month)
os.system(command)


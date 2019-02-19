from urllib import request
import json
from django.utils.safestring import mark_safe

response = request.urlopen(r'http://xx.xx.xx.xx/index.php/Home/Flow/getjson/name/{}.html'.format('%E6%8B%89%E6%89%8E%E6%96%AF%E7%BD%91%E7%BB%9C%E7%A7%91%E6%8A%80%EF%BC%88%E4%B8%8A%E6%B5%B7%EF%BC%89%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8'))
page = response.read()
page = page.decode('utf-8')
php_json = json.loads(page)
graph_list = []
for php_json_single in php_json:
    graph_list.append(php_json_single['local_graph_id'])
print(graph_list)
# inter_list = php_json[0]['interfacerlist']
# print(inter_list)
# inter_list_format = []
# for inter_person in inter_list:
#     if inter_person['type'] == 'SA':
#         inter_dic = {}
#         inter_dic.update(name=inter_person['contactName'],type='SA')
#         inter_list_format.append(inter_dic)
#     elif inter_person['type'] == 'KF':
#         inter_dic = {}
#         inter_dic.update(name=inter_person['contactName'], type='KF')
#         inter_list_format.append(inter_dic)
#     else:
#         continue
# print(inter_list_format)




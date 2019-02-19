import os
if_desc = os.popen('snmpwalk -v 2c -cWG@21vianet-RO xx.xx.xx.xx .ifDescr')
if_desc_read = if_desc.read()
if_desc_read_split = if_desc_read.split('\n')
list_port = []
for single in if_desc_read_split:
    single_split = single.split(' = STRING: ')
    if len(single_split) >= 2:
        port_dic = {}
        port_desc = single_split[1]
        id = int(single_split[0].split('ifDescr.')[1])
        port_dic.update(id=id,port=port_desc)
        list_port.append(port_dic)
# print(list_port)

if_status = os.popen('snmpwalk -v 2c -cWG@21vianet-RO xx.xx.xx.xx .ifOperStatus')
if_status_read = if_status.read()
if_status_read_split = if_status_read.split('\n')
list_status = []
for single in if_status_read_split:
    single_split = single.split(' = INTEGER: ')
    if len(single_split) >= 2:
        status_dic = {}
        port_status = single_split[1].split('(')[0]
        id_status = int(single_split[0].split('ifOperStatus.')[1])
        for port in list_port:
            if port['id'] == id_status:
                port['status'] = port_status
print(list_port)


#! /usr/bin/python3
  
# Retrieves list of IPv4 networks and masks from Atlassian's published info and generates ready-to-apply commands for the Cisco ASA platform
  
import json
import urllib.request
import datetime
  
now = datetime.datetime.now()

url = urllib.request.urlopen('https://ip-ranges.atlassian.com/')
data = json.loads(url.read().decode())
  
# JSON data is now a Python dictionary
  
# Define variables to be used in various strings
  
acl_name = 'outside-pri_access_in'
src_obj_grp = 'ATLASSIAN-SUBNETS'
dst_obj_grp = 'DST-SERVER'
line_num_remark = 'line 3'
line_num_acl = 'line 4'
svc = 'https'
  
# Return the timestamp published within the data, indicating last update
  
print()
print('Last updated on ' + str(data['creationDate']))
print()
  
# Define the object group in ASA CLI syntax
  
print('object-group network ' + src_obj_grp)
print(' description Atlassian networks from ip-ranges.atlassian.com ' + str(now.strftime('%Y-%m-%d')))
  
# Loop through the dictionary, retrieving network and mask key values

# Exclude any IPv6 networks, characterized by the : symbol
  
for item in data['items']:
    if item.get('network').__contains__(':'):
        continue
    else:
        print(' network-object ' + str((item.get('network'))) + ' ' + str((item.get('mask'))))
  
# Remove old entries--do this manually!
  
# print('no access-list ' + acl_name + line_num + ' extended permit tcp object-group ' + src_obj_grp + ' object ' + dst_obj_grp + ' eq ' + svc)
  
# Define the new ACL with today's date
  
print()
print('access-list ' + acl_name + ' ' + line_num_remark + ' some remark ' + str(now.strftime('%Y-%m-%d')))
print('access-list ' + acl_name + ' ' + line_num_acl + ' extended permit tcp object-group ' + src_obj_grp + ' object ' + dst_obj_grp + ' eq ' + svc)
print()
  
# --
#
# Reference:
#
# https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
# https://stackoverflow.com/questions/45898550/storing-json-data-in-python

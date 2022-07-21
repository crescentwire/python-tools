#! /usr/bin/python3
  
# Retrieves list of IPv4 networks and masks from Microsoft and Zoom's published info and generates ready-to-apply commands for the Cisco ASA platform
  
import json
import urllib.request
import datetime
from functools import reduce
import time
  
start_time = time.time()
  
now = datetime.datetime.now()
  
### MICROSOFT 365
  
# Define the URLs as data sources
  
msft_url_ver = urllib.request.urlopen('https://endpoints.office.com/version?clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7')
  
msft_url_data = urllib.request.urlopen('https://endpoints.office.com/endpoints/worldwide?clientrequestid=b10c5ed1-bad1-445f-b386-b919946339a7')
  
# Retrieve the data at the URLs and store
  
# Step 1: Retrieve URL data for date modified info and store it as JSON, decoding it into a Python list
  
msft_data_ver = json.loads(msft_url_ver.read().decode())
  
# Step 2: Confirm the data type is a list
  
# print()
# print('Version data type is: ' + str(type(msft_data_ver)))
# print()
  
# Step 3: Retrieve the date modified for the first list item
  
print('Last updated on: ' + str(msft_data_ver[0]['latest']), file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'w'))
print('', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
  
# Step 4: Retrieve URL data for actual subnet ranges and store it as JSON, decoding it into a Python list (with nested dictionaries)
  
msft_data = json.loads(msft_url_data.read().decode())
  
# Step 5: Confirm the data type is a list
  
# print('Actual data type is: ' + str(type(data)))
# print()
  
# Step 6: Count and display the number of items in the list (each with a possible nested dictionary )

# print('Total elements to process: ' + str(len(data)))
# print()
  
# Step 7: Require interactive response to continue
  
# print('Press any key to continue...')
# input()
  
# Step 8: Retrieve values from key 'ips'
  
# print ('Data type is: ' + str(type(data)))
# print()
  
# print('All subnets (IPv4, IPv6): ')
# print(data[0]['ips'])
# print()
  
# Step 9: Remove IPv6 values from list using list comprehension
  
# data_ipv4 = [ip for ip in data[0]['ips'] if ':' not in ip]
  
# print('IPv4 subnets only: ')
# print(data_ipv4)
# print()
  
# print('Data type is: ' + str(type(data_ipv4)))
# print()
  
# print('Number of elements in the above list: ' + str(len(data_ipv4)))
# print()
  
# Begin iterating using a for loop
# Step 10: Confirm the range of values needing iterated
  
# print(range(len(data)))
  
# Step 11: Define new list variable and iterate, adding items to the list
# Ignore missing key 'ips' - https://stackoverflow.com/questions/53928345/how-to-handle-missing-key-in-python-dictionary
  
msft_data_final = []
  
for item in range(len(msft_data)):
    try:
        msft_data_final.append(msft_data[item]['ips'])
    except KeyError:
        pass
  
# Remove nested elements and flatten to a single list
# Reference: https://stackoverflow.com/questions/17485747/how-to-convert-a-nested-list-into-a-one-dimensional-list-in-python
  
msft_data_final_flat_list = reduce(lambda x,y: x+y, msft_data_final)
  
# Remove IPv6 values
  
msft_data_final_flat_list_ipv4 = [ip for ip in msft_data_final_flat_list if ':' not in ip]
  
# Remove duplicates using list comprehension
# Reference: https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/
  
msft_data_list_dedup = []
  
[msft_data_list_dedup.append(ip) for ip in msft_data_final_flat_list_ipv4 if ip not in msft_data_list_dedup]
  
# Print result
  
# print(msft_data_list_dedup)
# print()
  
# Format ASA commands using list elements
# Convert CIDR to netmask format
# Reference: https://gist.github.com/nboubakr/4344773

msft_data_list_netmask = []
  
for item in range(len(msft_data_list_dedup)):
    (addr_str, cidr_str) = msft_data_list_dedup[item].split('/')
    addr = addr_str.split('.')
    cidr = int(cidr_str)
    mask = [0,0,0,0]
    for i in range(cidr):
        mask[i//8] = mask[i//8] + (1 << (7 - i % 8))
    net = []
    for i in range(4):
        net.append(int(addr[i]) & mask[i])
    msft_data_list_netmask.append(".".join(map(str, net)) + " " + ".".join(map(str, mask)))
    # print(".".join(map(str, net)) + " " + ".".join(map(str, mask)))
  
# print(msft_data_list_netmask)
  
### ZOOM
zoom_url_data = urllib.request.urlopen('https://assets.zoom.us/docs/ipranges/Zoom.txt')
  
# Crazy nonsense to decode as UTF-8 and remove empty lines ('\n' character)
# Reference: https://www.kite.com/python/answers/how-to-remove-empty-lines-from-a-string-in-python
# Reference: https://www.kite.com/python/answers/how-to-read-a-text-file-from-a-url-in-python
  
zoom_network_list = []
  
for line in zoom_url_data:
    decoded_line = line.decode('utf-8')
    decoded_line_strip = decoded_line.split('\n')
    decoded_line_clean = [x for x in decoded_line_strip if x.strip() != ""]
    zoom_network_list.append(decoded_line_clean)
  
# Remove nested elements and flatten to a single list
# Reference: https://stackoverflow.com/questions/17485747/how-to-convert-a-nested-list-into-a-one-dimensional-list-in-python
  
zoom_network_list_final = reduce(lambda x,y: x+y, zoom_network_list)
  
# Show the result

# print(zoom_network_list_final)
  
zoom_network_list_netmask = []
  
for item in range(len(zoom_network_list_final)):
    (addr_str, cidr_str) = zoom_network_list_final[item].split('/')
    addr = addr_str.split('.')
    cidr = int(cidr_str)
    mask = [0,0,0,0]
    for i in range(cidr):
        mask[i//8] = mask[i//8] + (1 << (7 - i % 8))
    net = []
    for i in range(4):
        net.append(int(addr[i]) & mask[i])
    zoom_network_list_netmask.append(".".join(map(str, net)) + " " + ".".join(map(str, mask)))
  
# print(zoom_network_list_netmask)
  
print('group-policy DEFAULTGRPPOLICY attributes', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
print(' no split-tunnel-network-list value SPLIT-TUNNEL-EXCLUDE', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
print('', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
  
print('no access-list SPLIT-TUNNEL-EXCLUDE', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
print('', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
  
for item in msft_data_list_netmask:
    print('access-list SPLIT-TUNNEL-EXCLUDE remark Microsoft 365 - ' + str(now.strftime('%Y-%m-%d')), file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
    print('access-list SPLIT-TUNNEL-EXCLUDE standard permit ' + str(item), file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
  
for item in zoom_network_list_netmask:
    print('access-list SPLIT-TUNNEL-EXCLUDE remark Zoom - ' + str(now.strftime('%Y-%m-%d')), file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
    print('access-list SPLIT-TUNNEL-EXCLUDE standard permit ' + str(item), file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))

print('access-list SPLIT-TUNNEL-EXCLUDE remark WSL2 - Cisco bug ID CSCvw81982', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
print('access-list SPLIT-TUNNEL-EXCLUDE standard permit host 0.0.0.0', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
print('', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
  
print('group-policy DEFAULTGRPPOLICY attributes', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
print(' split-tunnel-network-list value SPLIT-TUNNEL-EXCLUDE', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
print('', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
print('', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
  

print('Number of subnet entries in the above list: ' + str(int(len(msft_data_list_netmask)) + int(len(zoom_network_list_netmask))), file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
print('', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
  
print("--- Completed in %s seconds ---" % (time.time() - start_time), file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))
print('', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))

print('END', file=open(str(now.strftime('%Y-%m-%d')) + ' SPLIT-TUNNEL-EXCLUDE-UPDATE.txt', 'a'))

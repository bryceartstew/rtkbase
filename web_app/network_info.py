#!/usr/bin/python

import psutil

def get_up_if():
    #filtering available interface
    if_stats = psutil.net_if_stats()
    if_stats.pop('lo')
    if_stats = {k:v for (k,v) in if_stats.items() if if_stats[k].isup} # keep only up interface
    if_stats = {k:v for (k,v) in if_stats.items() if if_stats[k].speed > 0} # keep only interface with speed > 0
    if_stats = {k:v for (k,v) in if_stats.items() if not k.startswith('docker')} # remove docker interface
    return if_stats
    
#print(get_up_if())
up_interface = get_up_if()
#then filter psutil.net_if_addrs()
if_addrs = psutil.net_if_addrs()
up_interface = {k:if_addrs[k] for (k,v) in up_interface.items() if if_addrs[k]}
#then filter to keep only AF_INET and AF_INET6
for k,v in up_interface.items():
    up_interface[k] = [ x for x in v if x.family.name == 'AF_INET' or x.family.name == 'AF_INET6']
#then filter ipv6 link local address
for k,v in up_interface.items():
    up_interface[k] = [ x for x in v if not x.address.startswith('fe80')]
for k,v in up_interface.items():
    print('key: ', k)
    print('value: ', v)
    for part in v:
        print("{%8} : {}".format(part.family.name, part.address))
    #for snicaddr in interface:
    #    print(snicaddr.address)
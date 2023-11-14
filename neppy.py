#!/usr/bin/env python3

import nep.config
nep.config.load_conf()

from nep.netbox import nb_fetch_ip_addr,nb_fetch_ip_range,nb_fetch_prefix
from nep.convert import ip_addr_to_object,ip_range_to_object,prefix_to_object

import panos
import panos.panorama
import panos.objects

objects=[]

for i in nb_fetch_ip_addr():
    obj=ip_addr_to_object(i)
    if type(obj) is list:
        for o in obj:
            objects.append(o)
    else:
        objects.append(obj)
    
for i in nb_fetch_ip_range():
    obj=ip_range_to_object(i)
    if type(obj) is list:
        for o in obj:
            objects.append(o)
    else:
        objects.append(obj)

for i in nb_fetch_prefix():
    obj=prefix_to_object(i)
    if type(obj) is list:
        for o in obj:
            objects.append(o)
    else:
        objects.append(obj)
        
print(objects)

pan=panos.panorama.Panorama(hostname=nep.config.conf["panorama"]["host"], api_key=nep.config.conf["panorama"]["token"])

print("shared:")
addr=panos.objects.AddressObject.refreshall(pan,add=False)
for x in addr:
    print (x.name,x.value,x.type,x.description,x.tag)

d=pan.refresh_devices()

for i in d:
    print (i.name)
    addr=panos.objects.AddressObject.refreshall(i,add=False)
    for x in addr:
        print (x.name,x.value,x.type,x.description,x.tag)
    
# LOGIC TODO:
# - find if panorama has objects without netbox tag that have duplicate names with netbox-generated objects -> error
# - find if netbox-generated objects need updating on panorama
# - find if netbox-generated objects need to be created on panorama
# - find if panorama has objects with netbox tag that are not on netbox -> suggest delete
#!/usr/bin/env python3

import nep.config
nep.config.load_conf()

from nep.netbox import nb_fetch_ip_addr,nb_fetch_ip_range,nb_fetch_prefix
from nep.convert import ip_addr_to_object,ip_range_to_object,prefix_to_object

import nep.db

import panos
import panos.panorama
import panos.objects

for i in nb_fetch_ip_addr():
    obj=ip_addr_to_object(i)
    nep.db.db_push(0,obj)
    
for i in nb_fetch_ip_range():
    obj=ip_range_to_object(i)
    nep.db.db_push(0,obj)

for i in nb_fetch_prefix():
    obj=prefix_to_object(i)
    nep.db.db_push(0,obj)
        
pan=panos.panorama.Panorama(hostname=nep.config.conf["panorama"]["host"], api_key=nep.config.conf["panorama"]["token"])

addr=panos.objects.AddressObject.refreshall(pan,add=False)
for x in addr:
    tag=0
    if x.tag != None:
        for t in x.tag:
            if nep.config.conf["panorama"]["tag"] in t:
                tag=1
    nep.db.db_push(1,{"name": x.name,
                     "value": x.value,
                     "fieldtype": x.type,
                     "description": x.description,
                     "tag": tag,
                     "location": "shared"})

# list of device groups. If you have devices that are outside any group, you might be in trouble.
d=pan.refresh_devices()

for i in d:
    addr=panos.objects.AddressObject.refreshall(i,add=False)
    for x in addr:
        tag=0
        if x.tag != None:
            for t in x.tag:
                if nep.config.conf["panorama"]["tag"] in t:
                    tag=1
        nep.db.db_push(1,{"name": x.name,
                        "value": x.value,
                        "fieldtype": x.type,
                        "description": x.description,
                        "tag": tag,
                        "location": i.name})

# check if duplicate objects without tags
if nep.db.db_sanitycheck():
    exit()

# update/add shared objects

obj=[]
for i in nep.db.db_nbobjects("shared"):
    ao=panos.objects.AddressObject(i["name"],i["value"],i["fieldtype"],i["description"],[nep.config.conf["panorama"]["tag"]])
    obj.append(ao)
    pan.add(ao)
obj[0].create_similar()

# list of device groups. If you have devices that are outside any group, you might be in trouble.
d=pan.refresh_devices()
# device groups
for n in d:
    obj=[]
    for i in nep.db.db_nbobjects(n.name):
        ao=panos.objects.AddressObject(i["name"],i["value"],i["fieldtype"],i["description"],[nep.config.conf["panorama"]["tag"]])
        obj.append(ao)
        n.add(ao)
    # for some incomprehensible reason create_similar does not work with device groups
    # obj[0].create_similar()
    
    # so need to use slower method of creating each object separately
    for i in obj:
        i.create()
 
# check for orphan objects without counterparts in Netbox
nep.db.db_nbmissing()
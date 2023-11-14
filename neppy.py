#!/usr/bin/env python3

import nep.config
nep.config.load_conf()

from nep.netbox import nb_fetch_ip_addr,nb_fetch_ip_range,nb_fetch_prefix
from nep.convert import ip_addr_to_object,ip_range_to_object,prefix_to_object

import nep.db

import panos
import panos.panorama
import panos.objects

import argparse

argParser=argparse.ArgumentParser()
argParser.add_argument("--slay", help="Remove orphaned objects from Panorama", action="count", default=0)

args=argParser.parse_args()

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

addr=panos.objects.AddressObject.refreshall(pan)
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

d=panos.panorama.DeviceGroup.refreshall(pan)

for i in d:
    addr=panos.objects.AddressObject.refreshall(i)
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

d=panos.panorama.DeviceGroup.refreshall(pan)
# device groups
for n in d:
    obj=[]
    for i in nep.db.db_nbobjects(n.name):
        ao=panos.objects.AddressObject(i["name"],i["value"],i["fieldtype"],i["description"],[nep.config.conf["panorama"]["tag"]])
        obj.append(ao)
        n.add(ao)
    if len(obj)>0: 
        obj[0].create_similar()
    
# check for orphan objects without counterparts in Netbox
r=nep.db.db_nbmissing()
if len(r)>0:
    print("These objects are missing from Netbox but do have the Netbox tag. Re-run with the --slay parameter to delete them.")
    for i in r:
        print(i[0],i[1],i[2])
    

if args.slay:
    # check shared first
    r=nep.db.db_nbmissing("shared")    
    for i in r:
        ao=pan.find(i[0])
        print(f"Deleting {ao}")
        ao.delete()
    # then device groups
    d=panos.panorama.DeviceGroup.refreshall(pan)
    for n in d:
        r=nep.db.db_nbmissing(n.name)
        for i in r:
            ao=n.find(i[0])
            print(f"Deleting {ao}")
            ao.delete()
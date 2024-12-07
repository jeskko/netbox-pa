#!/usr/bin/env python3
#
# VERY MUCH IN PROGRESS, DOES SOMETHING BUT NOT NEARLY FINISHED

import nep.config
nep.config.load_conf()

from nep.netbox import nb_fetch_vlan
from nep.db import db_push_vlan,db_find_missing_vlan,db_find_orphan_vlan

import mistapi,pprint

apisession=mistapi.APISession(host=nep.config.conf["mist"]["host"] , apitoken=nep.config.conf["mist"]["token"])

apisession.login()

x=mistapi.api.v1.orgs.networktemplates.listOrgNetworkTemplates(apisession,org_id=nep.config.conf["mist"]["org_id"]).data

templates=[]

for i in x:
    tmpl_id=i['id']
    tmpl_name=i['name']
    templates.append({"tmpl_name": tmpl_name, "tmpl_id": tmpl_id})
    tmpl_net=[]
    for key,values in i["networks"].items():
        net_name=key
        net_vid=values["vlan_id"]
        db_push_vlan(1,tmpl_name,tmpl_id,net_name,net_vid)
                
for i in nep.config.conf["mist"]["template_mapping"]:
    tmpl_name=i["name"]
    tmpl_id=[x for x in templates if x["tmpl_name"]==tmpl_name][0]["tmpl_id"]
    tag=i["nb_tag"]
    
    r=nb_fetch_vlan(tag)
    for j in r:
        db_push_vlan(0,tmpl_name,tmpl_id,j[1],j[0])

r=db_find_missing_vlan()
print("Networks missing from Mist:")
for i in r:
    print(f"{i['tmpl_name']}: {i['vlan_name']} ({i['vlan_id']})")

print("Updating missing vlans to mist")

for i in r:
    x=mistapi.api.v1.orgs.networktemplates.getOrgNetworkTemplate(apisession,org_id=nep.config.conf["mist"]["org_id"], networktemplate_id=i["tmpl_id"]).data
    j={nep.config.conf["mist"]["prefix"]+i['vlan_name']: {'vlan_id': i['vlan_id']}}
    x['networks'].update(j)
    mistapi.api.v1.orgs.networktemplates.updateOrgNetworkTemplates(apisession,org_id=nep.config.conf["mist"]["org_id"], networktemplate_id=i["tmpl_id"], body=x)

r=db_find_orphan_vlan()
print("Networks in Mist but not in Netbox:")
for i in r:
    print(f"{i['tmpl_name']}: {i['vlan_name']} ({i['vlan_id']})")




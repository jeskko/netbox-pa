import pynetbox, requests
import nep.config
import urllib3

urllib3.disable_warnings()

session=requests.Session()
session.verify=False

nb = pynetbox.api(nep.config.conf["netbox"]["url"], token=nep.config.conf["netbox"]["token"])
nb.http_session=session

def nb_fetch_ip_addr():
    """find all ip addresses from netbox that have distribution groups"""
    i=nb.ipam.ip_addresses.all()
    ip_addr = list(filter(lambda ip: ip.custom_fields['fw_obj_distrib'] != None, i))
    return ip_addr

def nb_fetch_ip_range():
    """find all ip ranges from netbox that have distribution groups"""
    i=nb.ipam.ip_ranges.all()
    ip_ranges = list(filter(lambda ip: ip.custom_fields['fw_obj_distrib'] != None, i))
    return ip_ranges

def nb_fetch_prefix():
    """find all prefixes from netbox that have distribution groups"""
    i=nb.ipam.prefixes.all()
    prefixes = list(filter(lambda p: p.custom_fields['fw_obj_distrib'] != None, i))
    return prefixes

def nb_fetch_vlan(tag):
    """Fetch all vlans that have a tag"""
    i=nb.ipam.vlans.filter(tag=tag)
    vlans=[]
    for v in i:
        vlans.append((v.vid, v.name))
    return vlans
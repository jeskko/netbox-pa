import nep.config

def ip_addr_to_object(i):
    """Convert IP address from Netbox data to something that resembles more a firewall object."""

    res={}
    # strip prefix length as we're ip addresses    
    addr=i.address.split("/")[0]
    res["ip-netmask"]=addr
    # naming logic
    # use custom name
    if i.custom_fields["fw_address"]!=None:
        name=i.custom_fields["fw_address"].replace("{ip}",f"{addr}")
    else:
        # use fqdn + address if custom name is empty
        if i.dns_name!=None:
            name=f"{i.dns_name}-{addr}"
        else:
        # if fqdn is empty, use "ip-1.2.3.4" format
            name=f"ip-{addr}"
    res["name"]=name        
    res["description"]=i.description
    res["tag"]={"member": [nep.config.conf["panorama"]["tag"]]}
    if i.custom_fields["fw_obj_distrib"][0]=="Shared":
        res["location"]="shared"
    else:
        res["location"]="device-group"
        # easy if only 1 device group
        if len(i.custom_fields["fw_obj_distrib"])==1:
            res["device-group"]=i.custom_fields["fw_obj_distrib"][0]
        else:
            # now we need to make many new objects
            reslist=[]
            for d in i.custom_fields["fw_obj_distrib"]:
                res["device-group"]=d
                reslist.append(res)
            res=reslist
    
    return (res)

def ip_range_to_object(i):
    """Convert IP range from Netbox data to something that resembles more a firewall object."""

    res=dict()
    addr1=i.start_address.split("/")[0]
    addr2=i.end_address.split("/")[0]
    res["ip-range"]=f"{addr1}-{addr2}"
    # use custom name
    if i.custom_fields["fw_address"]!=None:
        name=i.custom_fields["fw_address"].replace("{ip}",f"{addr1}-{addr2}")
    else:
        name=f"range-{addr1}-{addr2}"
    res["name"]=name

    res["description"]=i.description
    res["tag"]={"member": [nep.config.conf["panorama"]["tag"]]}
    if i.custom_fields["fw_obj_distrib"][0]=="Shared":
        res["location"]="shared"
    else:
        res["location"]="device-group"
        # easy if only 1 device group
        if len(i.custom_fields["fw_obj_distrib"])==1:
            res["device-group"]=i.custom_fields["fw_obj_distrib"][0]
        else:
            # now we need to make many new objects
            reslist=[]
            for d in i.custom_fields["fw_obj_distrib"]:
                res["device-group"]=d
                reslist.append(res)
            res=reslist
    return(res)

def prefix_to_object(i):
    """Convert prefix from Netbox data to something that resembles more a firewall object."""
    
    res={}
    # strip prefix length as we're ip addresses    
    addr=i.prefix.split("/")[0]
    prefix=i.prefix.split("/")[1]
    res["ip-netmask"]=f"{addr}/{prefix}"
    # use custom name
    if i.custom_fields["fw_address"]!=None:
        name=i.custom_fields["fw_address"].replace("{ip}",f"{addr}-{prefix}")
    else:
        name=f"range-{addr}-{prefix}"
    res["name"]=name

    res["description"]=i.description
    res["tag"]={"member": [nep.config.conf["panorama"]["tag"]]}
    if i.custom_fields["fw_obj_distrib"][0]=="Shared":
        res["location"]="shared"
    else:
        res["location"]="device-group"
        # easy if only 1 device group
        if len(i.custom_fields["fw_obj_distrib"])==1:
            res["device-group"]=i.custom_fields["fw_obj_distrib"][0]
        else:
            # now we need to make many new objects
            reslist=[]
            for d in i.custom_fields["fw_obj_distrib"]:
                res["device-group"]=d
                reslist.append(res)
            res=reslist
    return(res)

import nep.config

def ip_addr_to_object(i):
    """Convert IP address from Netbox data to something that resembles more a firewall object."""

    res={}
    res["fieldtype"]="ip-netmask"
    # strip prefix length as we're ip addresses    
    addr=i.address.split("/")[0]
    res["value"]=addr
    # naming logic
    # use custom name
    if i.custom_fields["fw_address"]!=None:
        name=i.custom_fields["fw_address"].replace("{ip}",f"{addr}")
    else:
        # use fqdn + address if custom name is empty
        if len(i.dns_name)>0:
            name=f"{i.dns_name}-{addr}"
        else:
        # if fqdn is empty, use "ip-1.2.3.4" format
            name=f"ip-{addr}"
    res["name"]=nep.config.conf["panorama"]["prefix"]+"_"+name.replace(":","_")   
    res["description"]=i.description
    res["tag"]=1
    if i.custom_fields["fw_obj_distrib"][0]=="Shared":
        res["location"]="shared"
    else:
        # easy if only 1 device group
        if len(i.custom_fields["fw_obj_distrib"])==1:
            res["location"]=i.custom_fields["fw_obj_distrib"][0]
        else:
            # now we need to make many new objects
            reslist=[]
            for d in i.custom_fields["fw_obj_distrib"]:
                res["location"]=d
                reslist.append(res.copy())
            res=reslist
    return (res)

def ip_range_to_object(i):
    """Convert IP range from Netbox data to something that resembles more a firewall object."""

    res=dict()
    res["fieldtype"]="ip-range"
    addr1=i.start_address.split("/")[0]
    addr2=i.end_address.split("/")[0]
    res["value"]=f"{addr1}-{addr2}"
    # use custom name
    if i.custom_fields["fw_address"]!=None:
        name=i.custom_fields["fw_address"].replace("{ip}",f"{addr1}-{addr2}")
    else:
        name=f"range-{addr1}-{addr2}"
    res["name"]=nep.config.conf["panorama"]["prefix"]+"_"+name.replace(":","_")

    res["description"]=i.description
    res["tag"]=1
    if i.custom_fields["fw_obj_distrib"][0]=="Shared":
        res["location"]="shared"
    else:
        # easy if only 1 device group
        if len(i.custom_fields["fw_obj_distrib"])==1:
            res["location"]=i.custom_fields["fw_obj_distrib"][0]
        else:
            # now we need to make many new objects
            reslist=[]
            for d in i.custom_fields["fw_obj_distrib"]:
                res["location"]=d
                reslist.append(res)
            res=reslist
    return(res)

def prefix_to_object(i):
    """Convert prefix from Netbox data to something that resembles more a firewall object."""
    
    res={}
    res["fieldtype"]="ip-netmask"
    # strip prefix length as we're ip addresses    
    addr=i.prefix.split("/")[0]
    prefix=i.prefix.split("/")[1]
    res["value"]=f"{addr}/{prefix}"
    # use custom name
    if i.custom_fields["fw_address"]!=None:
        name=i.custom_fields["fw_address"].replace("{ip}",f"{addr}-{prefix}")
    else:
        name=f"range-{addr}-{prefix}"
    res["name"]=nep.config.conf["panorama"]["prefix"]+"_"+name.replace(":","_")

    res["description"]=i.description
    res["tag"]=1
    if i.custom_fields["fw_obj_distrib"][0]=="Shared":
        res["location"]="shared"
    else:
        # easy if only 1 device group
        if len(i.custom_fields["fw_obj_distrib"])==1:
            res["location"]=i.custom_fields["fw_obj_distrib"][0]
        else:
            # now we need to make many new objects
            reslist=[]
            for d in i.custom_fields["fw_obj_distrib"]:
                res["location"]=d
                reslist.append(res)
            res=reslist
    return(res)

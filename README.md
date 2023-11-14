A hack for synchronizing address objects from Netbox data to Panorama.

Add customization to netbox:
 - Custom field choices: fw_devgroups, add your device groups and "shared" here
 - Custom fields:
 ```Name,Content Types,Label,Group name,Type,Required,Description
fw_address,"ipam.ipaddress,ipam.prefix,ipam.iprange",Name,Firewall Object,Text,False,"Firewall object name. If left empty, will try to use DNS name. {ip} gets replaced with ip (and mask if other than /32 or /128)"
fw_obj_distrib,"ipam.ipaddress,ipam.prefix,ipam.iprange",Distribution,Firewall Object,Multiple selection,False,Distribute this object to these object groups.```
 
Will try to sync anything that has the fw_obj_distrib set to the panorama.
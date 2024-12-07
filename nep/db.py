import sqlite3

conn = sqlite3.connect('nep.db',detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

cursor = conn.cursor()

with open('./seed.sql') as f:
    cursor.executescript(f.read())
    conn.commit()

def db_push_vlan(system, tmpl_name, tmpl_id, vlan_name, vlan_id):
    """Push vlan to db
       System: 0 = netbox, 1 = mist"""
    
    ins="""INSERT INTO 'networks' (
        system, tmpl_name, tmpl_id, vlan_name, vlan_id)
        VALUES (?,?,?,?,?)"""
    
    cursor.execute(ins,(system, tmpl_name,tmpl_id,vlan_name,vlan_id))
    conn.commit()

def db_find_missing_vlan():
    """Find vlans that are in Netbox but not in Mist or that have conflicting vlan name"""

    sel="""SELECT tmpl_name,tmpl_id,vlan_name,vlan_id FROM 'networks'
    where system=0 AND (tmpl_name,vlan_id,vlan_name) NOT IN 
    (SELECT tmpl_name,vlan_id,vlan_name FROM 'networks' WHERE SYSTEM=1);"""
    
    r=cursor.execute(sel).fetchall()
    res=[]
    for i in r:
        res.append({"tmpl_name": i[0],
                    "tmpl_id": i[1],
                    "vlan_name": i[2],
                    "vlan_id": i[3]})
    return res
    
def db_find_orphan_vlan():
    """Find vlans that are only on Mist"""
    
    sel="""SELECT tmpl_name,tmpl_id,vlan_name,vlan_id FROM 'networks' 
    where system=1 AND (tmpl_name,vlan_id) NOT IN 
    (SELECT tmpl_name,vlan_id FROM 'networks' WHERE SYSTEM=0);"""

    r=cursor.execute(sel).fetchall()
    res=[]
    for i in r:
        res.append({"tmpl_name": i[0],
                    "tmpl_id": i[1],
                    "vlan_name": i[2],
                    "vlan_id": i[3]})
    return res

def db_push(system, data):
    """Push object or list of objects to db.
       System: 0 = netbox, 1 = firewall"""
    
    ins="""INSERT INTO 'object' (
        system, name, value,
        type, tag, description,
        location)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
    if type(data) is list:
        for l in data:
            cursor.execute(ins,(system,l["name"],l["value"],l["fieldtype"],l["tag"],l["description"],l["location"]))
    else:
        cursor.execute(ins,(system,data["name"],data["value"],data["fieldtype"],data["tag"],data["description"],data["location"]))        
    conn.commit()

def db_sanitycheck():
    """Verify that there are no objects that have same name and location in netbox and fw and that do not have netbox tag set on fw"""
    
    sel="SELECT * from object where system=1 AND tag=0 and (name,location) IN (SELECT name,location FROM object WHERE system=0);"
    r=cursor.execute(sel).fetchall()
    if len(r)>0:
        print("Error: duplicate items in Panorama without the proper tag:")
        print(r)
        return True
    return 

def db_nbobjects(location):
    """Fetch all netbox objects for a location"""
    
    sel="SELECT name,value,type,description from object WHERE system=0 AND location=?;"
    r=cursor.execute(sel,(location,)).fetchall()
    res=[]
    for i in r:
        res.append({"name": i[0],
                    "value": i[1],
                    "fieldtype": i[2],
                    "description": i[3]})
    return res

def db_nbmissing(location=None):
    """Check for objects with netbox tag, but which are missing from Netbox"""
    if location==None:
        sel="SELECT name,value,location from object where system=1 AND tag=1 and (name,location) NOT IN (SELECT name,location FROM object WHERE system=0);"
        r=cursor.execute(sel).fetchall()
    else:
        sel="SELECT name,value,location from object where system=1 AND tag=1 AND location=? and (name,location) NOT IN (SELECT name,location FROM object WHERE system=0);"
        r=cursor.execute(sel,(location,)).fetchall()
    return r
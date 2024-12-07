DROP TABLE IF EXISTS 'object';

CREATE TABLE 'object'
(
    'system' integer,
    'name'  text,
    'value' text,
    'type'  integer,
    'tag'  text,
    'description' text,
    'location' text 
);

DROP TABLE IF EXISTS 'networks';

CREATE TABLE 'networks'
(
    'system' integer,
    'tmpl_name' text,
    'tmpl_id' text,
    'vlan_name' text,
    'vlan_id' integer
)
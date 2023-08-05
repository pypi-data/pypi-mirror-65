```

 _       _   _                 _ _ _     
(_)     | | (_)               | (_) |    
 _  ___ | |_ _ _   _ _ __ ___ | |_| |__  
| |/ _ \| __| | | | | '_ ` _ \| | | '_ \ 
| | (_) | |_| | |_| | | | | | | | | |_) |
|_|\___/ \__|_|\__,_|_| |_| |_|_|_|_.__/ 
                                         
                                         

```

# Definition and Usage

The **iotiumlib** module allows you to access ioTium Orchestrator using APIs in Python.

# Download and Install

``pip install iotiumlib==19.11.26``

## Org

``iotiumlib.org.methodname(params)``

| Method        	| Required Params                       	| Optional Params                                                 	|
|---------------	|---------------------------------------	|-----------------------------------------------------------------	|
| get           	| NA                                      	| org_id                                                          	|
| getv2         	| NA                                    	| filters                                                         	|
| add           	| org_name, billing_name, billing_email 	| domain_name, timezone, headless_mode, two_factor, vlan_support 	|
| delete        	| org_id                                	|                                                                 	|

> returns a **Response** Object with all the response data (output, code, formattedOutput).

## Node

``iotiumlib.node.methodname(params)``

| Method 	| Required Params                       	| Optional Params                                         	|
|--------	|---------------------------------------	|---------------------------------------------------------	|
| getv2  	| NA                                    	| filters                                                 	|
| add    	| inode_name, serial_number, profile_id 	| standalone_expires, label, data_saving_mode             	|
| edit   	| node_id                               	| inode_name, label, standalone_expires, data_saving_mode 	|
| delete 	| node_id                               	| NA                                                      	|
| reboot 	| node_id                               	| NA                                                      	|
| notifications 	| node_id                                      	| type, filters                                                   	|

> returns a **Response** Object with all the response data (output, code, formattedOutput).


## PKI

``iotiumlib.pki.methodname(params)``

| Method 	| Required Params 	| Optional Params 	|
|--------	|-----------------	|-----------------	|
| getv2  	| NA              	| filters         	|

> returns a **Response** Object with all the response data (output, code, formattedOutput).


## Profile

``iotiumlib.profile.methodname(params)``

| Method 	| Required Params 	| Optional Params 	|
|--------	|-----------------	|-----------------	|
| getv2  	| NA              	| filters         	|

> returns a **Response** Object with all the response data (output, code, formattedOutput).

## Network

``iotiumlib.network.methodname(params)``


| Method       	| Required Params                        	| Optional Params                                                                                                                                                      	|
|--------------	|----------------------------------------	|----------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| getv2        	| NA                                     	| filters                                                                                                                                                              	|
| add          	| network_name, cidr,  start_ip, node_id 	| gateway_ip, end_ip, label, default_destination, connect_networks, firewall_selector, vlan_id, network_addressing, firewall_policy, service_addressing, static_routes 	|
| edit         	| network_id                             	| network_name, cidr, gateway_ip, start_ip, end_ip, label, default_destination, connect_networks, firewall_selector,  vlan_id, firewall_policy, static_routes          	|
| delete       	| network_id                             	| firewall_policy, service_addressing, static_routes                                                                                                                   	|
| resetcounter 	| network_id                             	|                                                                                                                                                                      	|                                                                                  	|
> returns a **Response** Object with all the response data (output, code, formattedOutput).

## Firewall

``iotiumlib.firewall.methodname(params)``

| Method 	| Required Params     	| Optional Params         	|
|--------	|---------------------	|-------------------------	|
| getv2  	| NA                  	| filters                 	|
| add    	| name, org_id, rules 	| label                   	|
| edit   	| firewallgroup_id    	| name, label, edit_rules 	|
| delete 	| firewallgroup_id    	| NA                      	|

> returns a **Response** Object with all the response data (output, code, formattedOutput).

## Service

``iotiumlib.service.methodname(params)``

| Method         	| Required Params     	| Optional Params 	|
|----------------	|---------------------	|-----------------	|
| getv2          	| NA                  	| filters         	|
| getv2_template 	| NA                  	| filters         	|
| add            	| payload             	|                 	|
| edit           	| service_id, payload 	| NA              	|
| delete         	| service_id          	| NA              	|

> returns a **Response** Object with all the response data (output, code, formattedOutput).

## Secret

``iotiumlib.secret.methodname(params)``

| Method 	| Required Params 	| Optional Params 	|
|--------	|-----------------	|-----------------	|
| getv2  	| NA              	| filters         	|
| add    	| name, filename  	| type            	|
| edit   	| secret_id       	| name, filename  	|
| delete 	| secret_id       	| NA              	|

> returns a **Response** Object with all the response data (output, code, formattedOutput).

## User

``iotiumlib.user.methodname(params)``

| Method 	| Required Params             	| Optional Params 	|
|--------	|-----------------------------	|-----------------	|
| getv2  	| NA                          	| filters         	|
| add    	| name, email, password, role 	| NA        	    |
| edit   	| user_id                     	| name, role      	|
| delete 	| user_id                     	| NA              	|
| notifications 	| NA                                      	| org_id, node_id, type, filters                                                   	|

> returns a **Response** Object with all the response data (output, code, formattedOutput).

``iotiumlib.user.mysubscriptions.methodname(params)``

| Method 	| Required Params          	| Optional Params                                                	|
|--------	|--------------------------	|----------------------------------------------------------------	|
| getv2  	| NA                       	| filters                                                        	|
| add    	| alert_name, type, org_id 	| node_id, include_child, duration pod_id, network_id, tunnel_id 	|
| delete 	| sub_id                   	| NA                                                               	|

> returns a **Response** Object with all the response data (output, code, formattedOutput).


## Package Helper Functions

``iotiumlib.helper.get_resource_id_by_name(resource, argument)``

| Resource                      	| Argument     	|
|-------------------------------	|--------------	|
| iotiumlib.node                	| node_name    	|
| iotiumlib.network             	| network_name 	|
| iotiumlib.service             	| service_name 	|
| iotiumlib.secret              	| secret_name  	|
| iotiumlib.profile             	| profile_name 	|
| iotiumlib.org                 	| org_name     	|
| iotiumlib.firewall            	| csp_name     	|
| iotiumlib.user                	| user_name    	|
| iotiumlib.org.mysubscriptions 	| alert_name   	|

``iotiumlib.helper.get_resource_name_by_id(resource, argument)``

| Resource                      	| Argument   	|
|-------------------------------	|------------	|
| iotiumlib.node                	| node_id    	|
| iotiumlib.network             	| network_id 	|
| iotiumlib.service             	| pod_id     	|
| iotiumlib.secret              	| secret_id  	|
| iotiumlib.profile             	| profile_id 	|
| iotiumlib.org                 	| org_id     	|
| iotiumlib.firewall            	| csp_id     	|
| iotiumlib.user                	| user_id    	|
| iotiumlib.org.mysubscriptions 	| alert_id   	|


``iotiumlib.helper.get_all_networks_from_node(name)``

``iotiumlib.helper.get_resource_by_label(resource, labelname)``

### Python example

```python

## Importing the Library
import iotiumlib

# Login to Orchestartor
iotiumlib.orch.ip = "OrchHostIp" # Orchestrator IP
respObj=iotiumlib.orchlogin.login("useremail@domain.io", "password")

# Getting the Token
iotiumlib.orch.token = respObj.Response.output['token']

# Get ORG ID for logged in User
iotiumlib.orch.id = iotiumlib.org.get(org_id=None).Response.output['organization']['id']

# Alternate Way to get ORG ID for logged in User
ORG_ID = iotiumlib.helper.get_resource_id_by_name(iotiumlib.org, "Org Name")

# Get PROFILE ID. Options: Edge, Virtual Edge, Virtual
edge_profile_id = iotiumlib.helper.get_resource_id_by_name(iotiumlib.profile, "Edge")

# Get list of Available Serial for Node provision
avail_serial_list = iotiumlib.pki.getv2(filters={"assigned":"false", "own":"true"}).Response.output
for pki in avail_serial_list:
    print(pki['id'])

###### Managing Users #######
# Get User Roles for Your Organization
#TODO

# Adding a New User
userRespObj = iotiumlib.user.add(name="User Name", email="email@domain.com", password="Password@1234", role="24c416ab-483c-402a-9b76-69bce4dd97ae")

# Getting User ID for specfic User
USER_ID = iotiumlib.helper.get_resource_id_by_name(iotiumlib.user, "User Name")

# Editing the User for name and role
iotiumlib.user.edit(user_id=USER_ID, role="ROLL_ID")
iotiumlib.user.edit(user_id=USER_ID)
iotiumlib.user.edit(user_id=USER_ID, name="New User Name", role="ROLL_ID")
iotiumlib.user.edit(user_id=USER_ID, name="New User Name")

# Deleting specfic User
iotiumlib.user.delete(user_id=USER_ID)

###### Provising an Edge iNode #######
# Other avail params: 
# standalone_expires (int) in minutes. Default=0
# data_saving_mode (string). Default="Fast", Options: "Slow", "Off"
respObj = iotiumlib.node.add(inode_name="Node Name", serial_number="pki-id", profile_id=edge_profile_id, org_id=ORG_ID, label="key:value")
print(respObj.Response.output)

# Get Node ID for Node edit/delete/reboot/notifications
NODE_ID = iotiumlib.helper.get_resource_id_by_name(iotiumlib.node, "Node Name")

# Edit Edge iNode for inode_name, label, standalone_expires, data_saving_mode
respObj_e = iotiumlib.node.edit(node_id=NODE_ID)

# Initiate Reboot on specfic Edge iNode
respObj_r = iotiumlib.node.reboot(node_id=NODE_ID)

# Delete Edge iNode
respObj_d = iotiumlib.node.delete(node_id=NODE_ID)

# List iNode specfic event. Default: All Event. Options: type=node, network, service
#start_date and end_date are in Epoch Time Stamp format
respObj_n = iotiumlib.node.notifications(node_id=NODE_ID)
respout = iotiumlib.node.notifications(node_id=NODE_ID, type="node").Response.output
respout = iotiumlib.node.notifications(node_id=NODE_ID, type="node", filters={"start_date":"", "end_date":""}).Response.output


###### Adding Local Network to Edge iNode #######
iotiumlib.network.add(node_id=NODE_ID, network_name="TAN Network", cidr="192.168.0.0/28", start_ip="192.168.0.1", end_ip="192.168.0.14")

# Get Network ID for Network edit/delete
TAN_ID = iotiumlib.helper.get_resource_id_by_name(iotiumlib.network, "TAN Network")

# Setting the Default Destination for Local Network to Edge iNode’s WAN Network
iotiumlib.network.edit(network_id=TAN_ID, default_destination="WAN_ID")

# Connecting an Edge iNode Network to a Remote Virtual iNode network
iotiumlib.network.edit(network_id=TAN_ID, connect_networks=[{"network_id":"Remote_Network_Id", "node_id":"Remote_Node_Id"}])

# Delete Edge Local Network
iotiumlib.network.delete(network_id=TAN_ID)

###### Using Custom Security Policy #######
iotiumlib.firewall.add(name='FWG', org_id=ORG_ID,
                        rules=[
                            {'from_network':'name=TAN Network', 'to_network':'id="NETWORK-ID"', 'protocol':'SSH'},
                            {'from_network':'label=key:value', 'to_network':'type=wan', 'action':'ALLOW'},
                            {'from_network':'label=key:value', 'to_network':'type=wan', 'action':'ALLOW', 'priority':'3000'},
                        ])

###### Using Secrets #######
iotiumlib.secret.add(name="Service Secret Name", filename={'.dockerconfigjson': 'ContentInBase64Format'},type="Dockerconfigjson")

iotiumlib.secret.add(name="Service Volume Name", filename=[],type="Opaque")

###### Using Mysubscriptions #######
#type: NODE_STATE_CHANGE, TUNNEL_STATE_CHANGE, SERVICE_STATE_CHANGE, NODE_IP_CHANGE, NODE_UPGRADE, HEADLESS_EXPIRY, CERT_EXPIRY
#include_child(bool): True to include child orgs. Scope: ORG level
#duration(int): default 5min. 
#node_id: Scope: iNode level
#tunnel_id: for type=TUNNEL_STATE_CHANGE
#pod_id: for type=SERVICE_STATE_CHANGE
iotiumlib.user.mysubscriptions.add(alert_name="Alert Name", type="SERVICE_STATE_CHANGE", org_id="OrgID")

###### Listing Events #######
#Default: All Event. Options: type=node, network, service
#start_date and end_date are in Epoch Time Stamp format
iotiumlib.user.notifications(filters={"start_date":"", "end_date":""}, type="node").Response.output
iotiumlib.user.notifications(node_id=NODE_ID, filters={"start_date":"", "end_date":""}, type="node").Response.output
iotiumlib.user.notifications(org_id=ORG_ID, filters={"start_date":"", "end_date":""}, type="node").Response.output


```  
import iotiumlib, json, requests

iotiumlib.orch.ip = "18.189.32.83"
r=iotiumlib.orchlogin.login("rashtrapathy.c@iotium.io", "f@bIoT17291729")
iotiumlib.orch.token = r.Response.output['token']
#iotiumlib.orch.id = iotiumlib.org.get(org_id=None).Response.output['organization']['id']

if False:
    edge_profile_id = iotiumlib.helper.get_resource_id_by_name(iotiumlib.profile, "Edge")
    free_serial = iotiumlib.pki.getv2(filters={"assigned":"false", "own":"true"}).Response.output
    for free in free_serial:
        print(free['id'])
    respObj=iotiumlib.node.add(inode_name="Node Name", serial_number="K22Y-4YDB", profile_id=edge_profile_id, org_id=ORG_ID, label="key:value")
    #print(respObj.Response.output)

    #ORG_ID = iotiumlib.helper.get_resource_id_by_name(iotiumlib.org, "Rash QA")
NODE_ID = iotiumlib.helper.get_resource_id_by_name(iotiumlib.node, "edge4")
print(NODE_ID)

#r=iotiumlib.network.add(node_id=NODE_ID, network_name="TAN Network", cidr="192.168.0.0/28", start_ip="192.168.0.1", end_ip="192.168.0.14")
#print(r.Response.output)

TAN_ID = iotiumlib.helper.get_resource_id_by_name(iotiumlib.network, "TAN")

WAN_ID = default_net_id = str()
for net in iotiumlib.helper.get_all_networks_from_node("edge4"):
    if 'WAN Network' in net:
       WAN_ID = net['WAN Network']
#WAN_ID = iotiumlib.helper.get_all_networks_from_node("edge4")[0]['WAN Network']
virtual_ID = iotiumlib.helper.get_resource_id_by_name(iotiumlib.network, "virtual1")

#default_net_id = iotiumlib.helper.get_all_networks_from_node("virtual1")[0]['default']
for net in iotiumlib.helper.get_all_networks_from_node("virtual1"):
    if 'default' in net:
        default_net_id = net['default']

#iotiumlib.network.edit(network_id=TAN_ID, default_destination=WAN_ID, connect_networks=[{"node_id":virtual_ID, "network_id":default_net_id}])
print(TAN_ID, WAN_ID)

ORG_ID = iotiumlib.helper.get_resource_id_by_name(iotiumlib.org, "Rash QA")
r=iotiumlib.firewall.add(name='FWG', org_id=ORG_ID,
                        rules=[
                            {'from_network':'name=TAN Network', 'to_network':'id={}'.format(default_net_id), 'protocol':'SSH'},
                            {'from_network':'label=key:value', 'to_network':'type=wan', 'action':'ALLOW'},
                            {'from_network':'label=key:value', 'to_network':'type=wan', 'action':'ALLOW', 'priority':'3000'},
                        ])
print(r.Response.code)
iotiumlib.logout()
exit()
# print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.node, "edge4"))
#
# print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.network, "TAN"))
# print(iotiumlib.helper.get_resource_name_by_id(iotiumlib.network, "n-b3c5f1f87b1446e8"))
#
#
# print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.service, "ddd"))
# print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.profile, "Edge"))
# print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.org, "Rash QA"))
# print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.firewall, "test"))
# print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.secret, "rashqa edge2 id_rsa.pub"))
# print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.user, "raja"))
# print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.org.mysubscriptions, "ALert"))

#iotiumlib.orch.token = "oUlE8sdi2DCrB3Isxtb10vpfBJTGIwgT"
#
#print(json.dumps(iotiumlib.org.get(org_id=None).Response.output, indent=1))

#r=iotiumlib.user.add(name="A", email="a@a.io", password="Welcome@1234", role="24c416ab-483c-402a-9b76-69bce4dd97ae")
#r=iotiumlib.user.edit(user_id="bfbaad8e-194e-4a52-b1fc-9fc2a259b169", name="EDITEEEEE")
#print(r.Response.output)

#r= iotiumlib.user.getv2().Response.formattedOutput
#print(json.dumps(r, indent=1))

#print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.user, "raja"))

#r=iotiumlib.org.mysubscriptions.getv2()
#print(r.Response.output)

#a=iotiumlib.helper.get_resource_id_by_name(iotiumlib.org.mysubscriptions, "test1")
#print('>>A= {}'.format(a))
#r=iotiumlib.org.mysubscriptions.delete(sub_id="22d16888-bc90-46cc-a0c0-05191757cda4")
#print(r.Response.output)

#r=iotiumlib.org.mysubscriptions.add(alert_name="test1", type="SERVICE_STATE_CHANGE", node_id="065aced9-d889-4d78-ac5d-eff857f99204", org_id="4c8a2e14-4500-4c0e-8bd2-8a7b6c9a0b83")
#if r.Response.code == 200:
#    print(r.Response.output["id"])
#    r = iotiumlib.org.mysubscriptions.delete(sub_id=r.Response.output["id"])
#    print(r.Response.output)
#else:
#    print(r.Response.output["message"])

#print(iotiumlib.orch.id)

#r=iotiumlib.notifications.getv2(filters={"type":"node"})

#r=iotiumlib.org.notifications(node_id="f70e9b92-d4c2-44d2-9abd-a1e9c77039a9", type="node")
#print(r.Response.code, len(r.Response.output))

#r=iotiumlib.org.notifications()
#print(r.Response.code, len(r.Response.output))

#r=iotiumlib.org.notifications(type="node")
#print(r.Response.code, len(r.Response.output))

#r=iotiumlib.org.notifications(node_id="f70e9b92-d4c2-44d2-9abd-a1e9c77039a9", type="network")
#print(r.Response.code, len(r.Response.output))

#r=iotiumlib.org.notifications(node_id="f70e9b92-d4c2-44d2-9abd-a1e9c77039a9", type="service")
#print(r.Response.code, len(r.Response.output))

#r=iotiumlib.node.notifications(node_id="f70e9b92-d4c2-44d2-9abd-a1e9c77039a9")
#print(r.Response.code, len(r.Response.output))

#r=iotiumlib.node.notifications(node_id="f70e9b92-d4c2-44d2-9abd-a1e9c77039a9", type="network")
#print(r.Response.code, len(r.Response.output))

#r=iotiumlib.org.getv2(filters={"org_id":"100a1f67-36ca-4a12-8abf-e7859ee3e677"})
#print(len(r.Response.output))

iotiumlib.orchlogin.logout()

exit(1)

"""

import os, base64, requests
filename='/home/rashtrapathy/dockerconfigjson'
type="Dockerconfigjson"

resp = iotiumlib.secret.add(name=os.path.basename(filename),
                             filename={'.dockerconfigjson':base64.b64encode(open(filename, 'rb').read()).decode('ascii')},
                             type=type)
print(resp.Response.output)
"""

#iotiumlib.node.log(node_id="bb5ee72f-c8c8-440a-acc1-c1ecdc9adbc9", filters={"logFilePosition":"end", "offsetFrom": "164", "offsetTo": "264", "lineNum": "-1", "referenceTimestamp":"2019-07-16T11:44:00.707011853Z"})
#for i in range(10):
    #resp = iotiumlib.service.log(service_id='p-59df0ff8cbef7f74', container_id='s-1bff2b3bee01fa37')
 #   resp = iotiumlib.node.log(node_id="bb5ee72f-c8c8-440a-acc1-c1ecdc9adbc9")
 #   if resp.Response.code != 200:
 #       print(resp.Response.output)

#print(iotiumlib.service.download_log(service_id='p-64198d1cb3249ce1', container_id='s-32eeca9c22504ce5').Response.code)


#import iotiumlib
#iotiumlib.orch.ip="qa.staging.iotium.io"
#r=iotiumlib.orchlogin.login("rashtrapathy@gmail.com", "f@bIoT1729172917291729")
#iotiumlib.orch.token = r.Response.output['token']
#iotiumlib.orch.id = 'eae1626e-01dc-47f3-be76-1d91828174cf'
#
#
#resp=iotiumlib.image.delete(node_id='37e6da02-e589-4ab3-bc56-20c6fc7b469a',
#                            image_id='rashtrapathy/tcpdump:latest')
#print(resp.Response.code, resp.Response.output)
#resp=iotiumlib.image.getv2(node_id='37e6da02-e589-4ab3-bc56-20c6fc7b469a')
#print(resp.Response.code, resp.Response.output, resp.Response.formattedOutput)
#
#import requests

# import iotiumlib
# import tabulate
# import json
# iotiumlib.orch.ip="qa.staging.iotium.io"
# #iotiumlib.orch.id="100a1f67-36ca-4a12-8abf-e7859ee3e677"
#
# #print(iotiumlib.helper.get_resource_by_label(iotiumlib.node, "version:latest"))
# #print(iotiumlib.helper.get_resource_by_label(iotiumlib.network, "owner:rash"))
# #print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.node, "edge node 1531502943059"))
# #print(iotiumlib.helper.get_resource_id_by_name(iotiumlib.network, "test"))
# #print(iotiumlib.helper.get_all_networks_from_node("edge node 1531502943059"))
# r=iotiumlib.orchlogin.login("rashtrapathy@gmail.com", "f@bIoT1729172917291729")
# iotiumlib.orch.token = r.Response.output['token']
# iotiumlib.orch.id = 'eae1626e-01dc-47f3-be76-1d91828174cf'
# iotiumlib.firewall.add(name='test', org_id="eae1626e-01dc-47f3-be76-1d91828174cf",
#                        rules=[
#                            {'from_network':'name=edited connected tan', 'to_network':'id=n-4f65daa7b0c44918'},
#                            {'from_network':'name=edited connected tan', 'to_network':'id=None', 'action':'ALLOW'},
#                        ])
#
# exit(0)
#
# #print(json.dumps(iotiumlib.org.getv2().Response.formattedOutput, indent=1))
# import os
# filename='/home/rashtrapathy/ws/iotium.qa/latqa/pem/lic.props'
# type='Opaque'
# resp = iotiumlib.secret.add(name=os.path.basename(filename),
#                             filename=[filename],
#                             type=type)
# print(resp.Response.output)
# #iotiumlib.orch.token = "r64bWs9w1RuSqDT9kauGfN3lfk0gdpT9"
#
# #print(iotiumlib.org.getv2(filters={'org_id':"100a1f67-36ca-4a12-8abf-e7859ee3e677"}).Response.code)
# #print(iotiumlib.node.getv2(filters={'org_id':"eae1626e-01dc-47f3-be76-1d91828174cf"}).Response.code)
#
# r=iotiumlib.orchlogin.logout()
#
# exit()
#
# def tableprint(orchcli_resp):
#     if orchcli_resp == []:
#         return None
#     header = orchcli_resp[0].keys()
#     rows = [x.values() for x in orchcli_resp]
#     print(tabulate.tabulate(rows, header, tablefmt='grid'))
#
# r= iotiumlib.node.getv2()
# print(r.inodeResponse.code, len(r.inodeResponse.output))
# tableprint(r.inodeResponse.formattedOutput)
#
# r= iotiumlib.network.getv2()
# print(r.networkResponse.code, len(r.networkResponse.output))
# tableprint(r.networkResponse.formattedOutput)
#
# r= iotiumlib.org.getv2()
# print(r.orgResponse.code, len(r.orgResponse.output))
# tableprint(r.orgResponse.formattedOutput)
#
# r= iotiumlib.pki.getv2()
# print(r.pkiResponse.code, len(r.pkiResponse.output))
# tableprint(r.pkiResponse.formattedOutput)
#
# r= iotiumlib.secret.getv2()
# print(r.secretResponse.code, len(r.secretResponse.output))
# tableprint(r.secretResponse.formattedOutput)
#
# r= iotiumlib.service.getv2()
# print(r.serviceResponse.code, len(r.serviceResponse.output))
# tableprint(r.serviceResponse.formattedOutput)
#
# r= iotiumlib.firewall.getv2()
# print(r.firewallResponse.code, len(r.firewallResponse.output))
# tableprint(r.firewallResponse.formattedOutput)
#
# exit()
#
# #r=iotiumlib.org.add(org_name='a', billing_email='a1@a.com', billing_name='ras')
# #print(r.orgResponse.code, r.orgResponse.output)
# #r=iotiumlib.org.get((r.orgResponse.output['id']))
# #print(r.orgResponse.code, r.orgResponse.output)
# r=iotiumlib.org.delete("4df04fec-d5a3-4317-b0a0-219f3eaf1284")
# print(r.orgResponse.code, r.orgResponse.output)
#
# exit()
#
# #r=iotiumlib.secret.add(name="SkyLic1", filename=['/home/rashtrapathy/Downloads/lic-2090aa68-b47583c8.props'], type="Opaque")
# #r=iotiumlib.secret.add(name="SkyLic1", filename='/home/rashtrapathy/Downloads/lic-2090aa68-b47583c8.props', type="Opaque")
# #print(r)
# #r=iotiumlib.secret.delete("6cd8e405-7741-4457-9cff-a29a987a4bee")
# r=iotiumlib.secret.get("f673813c-008d-45eb-b453-2cad9c825548")
# print(r.resp.statusCode, r.resp.responseOutput)
#
# r=iotiumlib.secret.get()
# for i in r.resp.responseOutput:
#     print(i['name'], i['id'], i['type'], len(i['data']))
#
# r=iotiumlib.secret.edit(secret_id="f673813c-008d-45eb-b453-2cad9c825548", name='fuck', filename=['/home/rashtrapathy/Downloads/lic-2090aa68-b47583c8.props', '/home/rashtrapathy/Downloads/lic-2090aaf3-a9efb58a.props'])
# print(r.resp.statusCode, r.resp.responseOutput)
#
# r=iotiumlib.secret.get()
# for i in r.resp.responseOutput:
#     print(i['name'], i['id'], i['type'], len(i['data']))
#
# exit()
#
# r=iotiumlib.node.add(inode_name='rash', serial_number='avcd', profile_id='aaa', org_id='aaaa', label='aaa')
# print(r.resp.responseMessage, r.resp.statusCode)
# exit()
# #r=iotiumlib.inode.add(inode_name='rash', profile_id='b30981d7-e02c-42a2-b44b-eef2bf22a8f8', org_id='eae1626e-01dc-47f3-be76-1d91828174cf', serial_number='e29e646ec5384fee8554f43bc953588f')
# #r=iotiumlib.inode.edit(node_id="b94781df-7c7c-4282-b3f9-0cba2cafc0d4", label="new:node", inode_name="newinode")
# #r=iotiumlib.inode.delete(node_id="b94781df-7c7c-4282-b3f9-0cba2cafc0d4")
# #print(r.resp.statusCode, r.resp.responseOutput)
#
# #exit()
# #iotiumlib.inode.add(inode_name='rash',profile_id='b30981d7-e02c-42a2-b44b-eef2bf22a8f8', org_id='eae1626e-01dc-47f3-be76-1d91828174cf', serial_number='e29e646ec5384fee8554f43bc953588f')
#
# #print(iotiumlib.inode.edit(node_id="cfa341f0-a476-4d14-acd1-f0fc4bfca6ed", label="").resp.statusCode)
# '''
# print(iotiumlib.network.add(network_name='Full TAN Network', cidr='1.1.1.1/24', start_ip='1.1.1.1',
#                             label="tan:rash,tan1:raja", firewall_selector="all", firewall_policy=False,
#                             node_id='37e6da02-e589-4ab3-bc56-20c6fc7b469a', end_ip='1.1.1.14', vlan_id=180,
#                             default_destination='n-4f65daa7b0c44918').resp.responseOutput)
#
#
#
# print(iotiumlib.network.add(network_name='Plain TAN Network', cidr='1.1.2.1/24', start_ip='1.1.2.1',
#                             connect_networks=[{"5f2b9d44-fbfc-40a2-bb72-bdb65dd8e02a":"n-67be5653c68411c7"},
#                                               {"53256b5a-a30f-4a32-812b-cc93e18bd6bd":"n-0d3551af2b76ecc4"}],
#                             node_id='37e6da02-e589-4ab3-bc56-20c6fc7b469a').resp.responseOutput)
# '''
# iotiumlib.network.edit(network_id="n-fc5b59c8b44b0858", label="node:tan", vlan_id=200, connect_networks=[])
# exit()
#
# for i in iotiumlib.network.get().resp.responseOutput:
#     print(i['name'], i['id'], i['node']['name'], i['node']['id'])
#
# for j in iotiumlib.node.get().resp.responseOutput:
#     print(j['name'], j['id'])
#
#
# #import json
# #print(json.dumps(iotiumlib.network.get(network_id="n-bf6177f74c7c5879").resp.responseOutput, indent=1))
# #print(json.dumps(iotiumlib.network.get(network_id="n-61ef44de21c8ae1c").resp.responseOutput, indent=1))
#
#
#
# #print(iotiumlib.network.edit(network_id="n-bf6177f74c7c5879").resp.responseOutput)
# #iotiumlib.network.delete(network_id="n-014acac54c604d91")
# #print(iotiumlib.network.get(network_id="n-014acac54c604d91").resp.responseOutput)
#
# r=iotiumlib.firewall.edit(firewallgroup_id="db947cd5-1890-4510-b05d-3b015b84cb0c", name="raja", label="all:tan",
#                           rules=[{"priority":"1002"}])
# print(r.resp.statusCode, r.resp.responseOutput)
#
# exit()
#
# iotiumlib.firewall.add(name='test', org_id="eae1626e-01dc-47f3-be76-1d91828174cf",
#                        rules=[
#                            {'from_network':'name=edited connected tan', 'to_network':'id=n-4f65daa7b0c44918'},
#                            {'from_network':'name=edited connected tan', 'to_network':'id=n-4f65daa7b0c44918', 'action':'ALLOW'},
#                        ])
# exit()
#
#
#
# for i in iotiumlib.firewall.get().resp.responseOutput:
#     print(i['id'], i['name'])
#
# import json
# print(json.dumps(iotiumlib.firewall.get(firewallgroup_id="db947cd5-1890-4510-b05d-3b015b84cb0c").resp.responseOutput, indent=1))
#
# print(iotiumlib.firewall.delete(firewallgroup_id="db947cd5-1890-4510-b05d-3b015b84cb0c").resp.responseOutput)

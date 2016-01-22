#!/usr/bin/env python

import sys
import requests

odl_user = 'admin'
odl_pass = 'admin'

ip = '127.0.0.1'

#dev_name = 'kcy'
#prifix = '111.0.0.0/24'
#dest = '30.0.0.1'

#static_route_url_temp = "http://%s:8181/restconf/config/opendaylight-inventory:nodes/node/%s/yang-ext:mount" + \
#       "/Cisco-IOS-XR-ip-static-cfg:router-static/default-vrf/address-family/vrfipv4/vrf-unicast/vrf-prefixes/%s"

static_route_url_temp = "http://%s:8181/restconf/config/opendaylight-inventory:nodes/node/%s/yang-ext:mount/Cisco-IOS-XR-ip-static-cfg:router-static/default-vrf/address-family/vrfipv4/vrf-unicast/vrf-prefixes/vrf-prefix/%s"
req_static_route_body_temp = '''
{
    "vrf-prefix": [
        {
            "prefix": "%s",
            "vrf-route": {
                "vrf-next-hops": {
                    "next-hop-address": [
                        {
                            "next-hop-address": "%s"
                        }
                    ]
                }
            },
            "prefix-length": %d
        }
    ]
}
'''

req_hdrs = { 'Content-Type' : 'application/json' }

# 1.1.1.1/24
#out put : 24
def  get_prefix_lenth (prefix):
    ret = prefix.split('/')
    return  ret[0],int(ret[1])

def del_static_route(odlip, dev_name, prefix, dest) :
    url = static_route_url_temp % (odlip, dev_name, prefix)
    ip_prefix,prefix_lenth = get_prefix_lenth(prefix)
    request_body = req_static_route_body_temp % (ip_prefix, dest,prefix_lenth)

    print (url)
    print (request_body)

    resp = requests.delete(url, data=request_body, headers=req_hdrs, auth=(odl_user, odl_pass))
    print (resp)

if __name__ == '__main__':
     del_static_route('127.0.0.1', 'kcy', '111.0.0.0/24', '1.1.1.1')
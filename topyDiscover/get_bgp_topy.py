#!/usr/bin/env python

import sys
import requests
import json

odl_user = 'admin'
odl_pass = 'admin'

ip = '127.0.0.1'

get_bgp_route_url_temp = "http://%s:8181/restconf/operational/network-topology:network-topology/topology/example-linkstate-topology"

req_hdrs = { 'Content-Type' : 'application/json' }

def get_bgp_topy() :
    url = get_bgp_route_url_temp % ip
    resp = requests.get(url, headers=req_hdrs, auth=(odl_user, odl_pass))

    if (resp.status_code == 200):
        #c = json.loads(resp.text)
	#c = json.dumps(resp.text)
	return resp.text
        #return c
    else:
        print ('unable to get bgp topology')
	sys.exit(0)

if __name__ == '__main__':
     topy = get_bgp_topy()
     print (topy)
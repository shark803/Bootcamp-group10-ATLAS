import json
import re
from get_bgp_topy import *

Debug = True
file_name = "/home/chuck/workspace/ATLAS/topyDiscover/topy.json"

'''
    topy anilayse
'''
def topy_load ():
    if Debug :
        get_bgp_topy()
        fp = open (file_name, "r")
        js = json.load(fp)
        fp.close()
        print(js)
        return js
    else:
        return get_bgp_topy()

#"tp-id": "bgpls://IsisLevel2:0/type=tp&ipv4=56.0.0.29",
def get_ip(tp_id):
    reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
    ip = reip.findall(tp_id)
    return ip

# node : " bgpls://IsisLevel2:0/type=node&as=65504&domain=505290270&router=0000.0000.0026"
def get_id (node):
    reip = re.compile(r'(?<![\.\d])(?:\d{1,4}\.){2}\d{1,4}(?![\.\d])')
    id = reip.findall(node)
    return id[0]

'''
 function : topy_parse_node(my_topology)
 out put : nodes
 output format:
    [
      {
        'id': '0000.0000.0029',
        'port_list': [
          {
            'port-ip': [
              '54.0.0.29'
            ]
          },
          {
            'port-ip': [
              '56.0.0.29'
            ]
          }
        ],
        'name': 'sfc'
      },
       ....
    ]
'''
def topy_parse_node (topy):
    node_list =[]
    #try:
    if True:
        for nodes in topy['topology']['node']:
            temp_node = {}

            #1. get node name and all temp_node_prefixs
            if "igp-node-attributes" in nodes.keys():
                if "name" in nodes["igp-node-attributes"].keys():
                    temp_node["name"] = nodes["igp-node-attributes"]["name"]
            #2. get id
            if "node-id" in nodes.keys():
                temp_node["id"] = get_id(nodes["node-id"])

            #3. get interface and ip address
            if "termination-point" in nodes.keys():
                port_list = []
                for ports in nodes["termination-point"]:
                    if "tp-id" in ports.keys():
                         temp_port = {}
                         tp_id = ports["tp-id"]
                         temp_port["port-ip"] = get_ip(tp_id)
                         port_list.append(temp_port)
                temp_node ["port_list"] = port_list

            #4.  get all node parsed
            node_list.append(temp_node)
    #except Exception as ex:
        #print("BGP get node error2: %s" % ex)

    return node_list

def find_router_name_by_id(name_id_map , id):
    find = False
    name = None
    for i in name_id_map:
        if i['id'] == id :
            find = True
            name = i['name']

    if find:
        return True,name
    else:
        return False,None


'''
 function : topy_parse_links(my_topology)
 out put : links
 output format:
     [
      {
        'src': {
          'id': '0000.0000.0027',
          'port_ip': [
            '45.0.0.27'
          ],
          'name': 'san'
        },
        'dst': {
          'id': '0000.0000.0021',
          'port_ip': [
            '45.0.0.21'
          ],
          'name': 'kcy'
        },
        'metric': 10
      },
      {
        ....
      }
     ]
'''
def topy_parse_links(my_topology):
    link_list = []
    route_name_id_map = []
    try:
        # get the map of router's name and id
        for nodes in my_topology['topology']['node']:
            temp_node = {} #id, name

            #1. get node name
            if "igp-node-attributes" in nodes.keys():
                if "name" in nodes["igp-node-attributes"].keys():
                    temp_node["name"] = nodes["igp-node-attributes"]["name"]
            #2. get id
            if "node-id" in nodes.keys():
                temp_node["id"] = get_id(nodes["node-id"])

            route_name_id_map.append(temp_node)

        # get link
        for link in my_topology['topology']['link']:
            temp_link = {}
            temp_src_node = {}
            temp_dest_node = {}
            #1.src node
            if "source-node"  in link["source"].keys() :
                temp_src_node ["id"] = get_id(link['source']["source-node"])
                sucess,name = find_router_name_by_id(route_name_id_map, temp_src_node ["id"])
                #get name
                if sucess :temp_src_node ["name"] = name
                else:raise RuntimeError("not find router's name by id: %s" %temp_src_node ["id"])

            if "source-tp"  in link["source"].keys() :
                temp_src_node ["port_ip"] = get_ip(link['source']["source-tp"])
            temp_link["src"] = temp_src_node

            #2.dest node
            if "dest-node"  in link["destination"].keys() :
                temp_dest_node ["id"] = get_id(link['destination']["dest-node"])
                #get name
                sucess,name = find_router_name_by_id(route_name_id_map, temp_dest_node ["id"])
                if sucess :temp_dest_node ["name"] = name
                else:raise RuntimeError("not find router's name by id: %s" %temp_dest_node ["id"])

            if "dest-tp"  in link["destination"].keys() :
                temp_dest_node ["port_ip"] = get_ip(link['destination']["dest-tp"])
            temp_link["dst"] = temp_dest_node

            #3.get metric
            if "metric" in link["igp-link-attributes"].keys() :
                temp_link['metric'] = int(link["igp-link-attributes"]["metric"])

            link_list.append(temp_link)
    except Exception as ex:
        print("BGP get link error3: %s" % ex)
    return link_list

if __name__ == '__main__':
    topy = topy_load()

    print ("get nodes:")
    nodes = topy_parse_node(topy)
    print (nodes)

    links = topy_parse_links(topy)
    print ("get links:")
    print (links)





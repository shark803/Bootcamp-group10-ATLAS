#!/usr/bin/env python2.7

'''
This module recalculate the path for the special traffic

Author: shark803
Date :2016/1/21

'''
from __future__ import print_function


from  network_topo import *
import networkx as nx
import matplotlib.pyplot as plt

'''

NodeList =  ['iosxrv-1', 'iosxrv-2', 'iosxrv-3', 'iosxrv-4', 'iosxrv-5', 'iosxrv-6', 'iosxrv-7', 'iosxrv-8']
LinkList=[('iosxrv-1', 'iosxrv-2',43),('iosxrv-2', 'iosxrv-3',47),('iosxrv-3', 'iosxrv-4',51),
           ('iosxrv-4', 'iosxrv-5',62),('iosxrv-5', 'iosxrv-8',91),
            ('iosxrv-6', 'iosxrv-7',81),('iosxrv-1', 'iosxrv-6',88),
            ('iosxrv-2', 'iosxrv-7',78),('iosxrv-7', 'iosxrv-8',93),('iosxrv-3', 'iosxrv-7',85),('iosxrv-4', 'iosxrv-8',99)]
'''

#origin_path = []
#color_list = ['r'] 

def logic_topo_gen(graph, conges_edge_start,conges_edge_end):
    graph.remove_edge(conges_edge_start,conges_edge_end)
    return graph

def get_service_chain(SCStr):
    return SCStr.split(',')


def get_key_point(SVList,src,dst):
    SVList.insert(0,src)
    SVList.append(dst)
    return SVList 


def cal_optimal_path(graph,keylist):
    opt_path = [keylist[0]]
    pre_graph = graph.copy()
    for i in range(len(keylist)-1):
        pro_graph = pre_graph.copy()
        #print(pro_graph.nodes())
        #print(keylist)
        for j in range(i):
            if keylist[j] in pro_graph.nodes():
                pro_graph.remove_node(keylist[j])
        for k in range(i+2,len(keylist)):        
            #print(keylist[k])
            if keylist[k] in pro_graph.nodes():
                pro_graph.remove_node(keylist[k])
        seg_path = [p for p in nx.all_shortest_paths(pro_graph,source = keylist[i], target = keylist[i+1], weight = 'weight')][0]
        pre_graph.remove_nodes_from(seg_path[:-1])
        opt_path = opt_path + seg_path[1:]
    return opt_path


def path_config(path,phynodes,phylinks,protect_prefix):
    path_set={}
    path_set['prefix']= protect_prefix
    path_opt_config = []
    for item in path:
        node_item = {}
        node_item['node_name'] = item
        for phy_item in phynodes:
            if phy_item ['name'] == item:
                node_item['node_id'] = phy_item['id']
                if path.index(item) == 0:
                    node_item['UP_Interface_IP'] = ['']
                if path.index(item) == len(path)-1:
                    node_item['Down_Interface_IP'] = ['']
        for link_item in phylinks:
            if path.index(item)!=len(path)-1:    
                if link_item['src'] ['name'] == item and link_item['dst']['name'] == path[path.index(item)+1]:
                    node_item['Down_Interface_IP'] = link_item['src']['port_ip']
            if path.index(item)!=0:
                if link_item['src']['name'] == path[path.index(item)-1] and link_item['dst']['name'] == item:
                    node_item['UP_Interface_IP'] = link_item['dst']['port_ip']    
        path_opt_config.append(node_item)
    path_set['path'] = path_opt_config
    return path_set


if __name__ == "__main__":
    SClist1 = "sea,kcy"
    SClist2 = "sea"

    SVList = get_service_chain(SClist1) 
    SVK = get_service_chain(SClist2) 
    SVList = get_key_point(SVList,src,dst)
    SVK = get_key_point(SVK,src,dst)
    #print(SVK) 

    topo = network_topo()
    logic_map = map()

    phy_topy = topy_load()

    phy_nodes = topy_parse_node(phy_topy)

    phy_links = topy_parse_links(phy_topy)

    # print(phy_nodes) 
    logic_nodes = logic_map.getNodes(phy_nodes)
    #print(logic_nodes)
    logic_links = logic_map.getLinks(phy_links)
    #print(logic_links)

    '''
    topo.topo_discover(NodeList,LinkList)
    print(topo.get_origin_path(src,dst))
    topo.show_topo(topo.get_origin_path(src,dst))
    '''
    topo.topo_discover(logic_nodes,logic_links)

    
    #topo.topo_discover(NodeList,LinkList)
    logic_graph = logic_topo_gen (topo.get_graph(),'sfc','por')
    

    #print(logic_graph.edges())
    opt_path = cal_optimal_path(logic_graph,SVK)
    print(opt_path)
    #topo.show_topo(topo.get_origin_path(src,dst))
    color_list = ['r'] * 8

    topo.show_topo(opt_path,logic_nodes,logic_links,'path_opt.png')
    pathset = path_config(opt_path,phy_nodes,phy_links,'87.87.87.87-89.89.89.89')
    print(pathset)
    

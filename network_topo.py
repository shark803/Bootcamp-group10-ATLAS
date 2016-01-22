#!/usr/bin/env python2.7
'''
This network_topo api read the json and show the topology
Author: shark803
Date: 2016/1/20

'''

from __future__ import print_function
import networkx as nx
import matplotlib.pyplot as plt
import string

from Map import *


'''
NodeList =  ['iosxrv-1', 'iosxrv-2', 'iosxrv-3', 'iosxrv-4', 'iosxrv-5', 'iosxrv-6', 'iosxrv-7', 'iosxrv-8']
LinkList=[('iosxrv-1', 'iosxrv-2',43),('iosxrv-2', 'iosxrv-3',47),('iosxrv-3', 'iosxrv-4',51),
           ('iosxrv-4', 'iosxrv-5',62),('iosxrv-5', 'iosxrv-8',91),
            ('iosxrv-6', 'iosxrv-7',81),('iosxrv-1', 'iosxrv-6',88),
            ('iosxrv-2', 'iosxrv-7',78),('iosxrv-7', 'iosxrv-8',93),('iosxrv-3', 'iosxrv-7',85),('iosxrv-4', 'iosxrv-8',99)]
'''





src = u'san'
dst = u'sfc'





class network_topo(object):
    def __init__(self):
        self.network_graph = nx.Graph()

    def get_graph(self):
        return self.network_graph
     
    def topo_discover(self,NodeList,LinkList):
	
        self.network_graph.add_nodes_from(NodeList)
        self.network_graph.add_weighted_edges_from(LinkList)
        '''
        for edge in self.network_graph.edges():
            self.network_graph [edge[0]][edge[1]]['metric']  = str(self.network_graph.get_edge_data(edge[0],edge[1])) 
        '''
    def get_origin_path(self,src,dst):
        origin_path = [p for p in nx.all_shortest_paths(self.network_graph,source = src, target = dst, weight = 'weight')]
        return origin_path[0]

    def show_topo(self,path,nodelist,linklist,name):

        color_list = ['r'] * 8
        #nx.draw(self.network_graph)
        pos = nx.spring_layout(self.network_graph)
        '''
        for i in range(len(path)-2):
            self.network_graph[path[i]][path[i+1]] ['color'] = 'blue'

       '''
        for node in path:
            color_list[nodelist.index(node)] = 'g'
        nx.draw(self.network_graph, pos, with_labels = True,nodelist = nodelist, node_size = 680, node_color = color_list)
        # nx.draw_networkx_edges(self.network_graph, pos, with_labels = True, alpha=0.5 )  
        plt.savefig(name)
	#plt.close()
        plt.show()


if __name__ == "__main__":
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
    print(topo.get_origin_path(src,dst))
    topo.show_topo(topo.get_origin_path(src,dst),logic_nodes,logic_links,'origin_path.png')
      

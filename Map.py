#!/usr/bin/env python2.7



from __future__ import print_function
import networkx as nx
import matplotlib.pyplot as plt


from topyDiscover.topyService import *


class map(object):
    def __init__(self):
        self.logic_nodes = []
        self.logic_links = []


    def getNodes(self,phy_nodes):
        self.logic_nodes =  [ item['name'] for item in phy_nodes]
        return self.logic_nodes


    def getLinks(self, phy_links):
        
        for edge in phy_links:
            src_node = edge['src']['name']
            dst_node = edge['dst']['name']
            weight = edge['metric']
            self.logic_links.append((src_node,dst_node,weight))
        return self.logic_links
        
        







#!/usr/bin/env python

from create_static_route import *
from del_static_route import *

path_set = {'path': [{'Down_Interface_IP': [u'45.0.0.27'], 'UP_Interface_IP': [''], 'node_id': u'0000.0000.0027', 'node_name': u'san'}, 
{'Down_Interface_IP': [u'44.0.0.21'], 'UP_Interface_IP': [u'45.0.0.21'], 'node_id': u'0000.0000.0021', 'node_name': u'kcy'},
 {'Down_Interface_IP': [u'51.0.0.24'], 'UP_Interface_IP': [u'44.0.0.24'], 'node_id': u'0000.0000.0024', 'node_name': u'min'}, {'Down_Interface_IP': [u'55.0.0.28'], 'UP_Interface_IP': [u'51.0.0.28'], 'node_id': u'0000.0000.0028', 'node_name': 'sea'}, {'Down_Interface_IP': [u'56.0.0.30'], 'UP_Interface_IP': [u'55.0.0.30'], 'node_id': u'0000.0000.0030', 'node_name': u'sjc'}, {'Down_Interface_IP': [''], 'UP_Interface_IP': [u'56.0.0.29'], 'node_id': u'0000.0000.0029', 'node_name': u'sfc'}], 'prefix': '89.89.89.89/32'}

'''
path_set = {
             "prefix" : "3.1.1.0/24",
             "path"  : [  {"node_name": "xr-1",
                           "node_id": "10.0.0.1",

                           "Up_Interface_IP" : NULL,

                           "Down_Interface_IP" : "1.1.1.1/32",
                          } ,
                          {
                              ......
                          },
                          {
                             ......
                          }
                       ]
           }
'''
odlip = '127.0.0.1'

def path_adjust(path_set):
    prefix = path_set['prefix']
    path = path_set['path']

    lenth = len(path)

    i = 0
    while i < lenth :
        node_name = path[i]['node_name']

	dest = path[i+1]['UP_Interface_IP'][0]
	
        if i == lenth -2:
            break

        i += 1

        put_static_route(odlip, node_name, prefix, dest)


def path_adjust_undo(path_set):
    prefix = path_set['prefix']
    path = path_set['path']

    
    lenth = len(path)

    i = 0
    while i < lenth :
        node_name = path[i]['node_name']

        dest = path[i+1]['UP_Interface_IP'][0]
        if i == lenth -2:
            break

        i += 1
        del_static_route(odlip, node_name, prefix, dest)


if __name__ == '__main__':
     print('path set')
     #path_adjust(path_set)
     path_adjust_undo(path_set)


#!/usr/bin/python
#coding=utf-8






from Tkinter import *
import datetime
import time
import string
from network_topo import *
from path_opt import *
from pathAdjust.pathAdjust import *
import copy

root = Tk()
root.title('ATLAS GUI')




global_opt_path = {}








def topo_get():
    
    
    
    
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
    topo.topo_discover(logic_nodes,logic_links)


    for item in phy_links:

        str_link=''
        str_link = str_link + item['src']['name'] + '('+ item['src']['port_ip'][0] +')' + '---->'  \
               + item['dst']['name'] + '('+ item['dst']['port_ip'][0] +')' + '   metrics:'+str(item['metric'])
        mylist.insert(END, str_link)

    origin_path = topo.get_origin_path(src,dst)
    str_path = "Path:"
    for node in origin_path:
        if origin_path.index(node) == len(origin_path)-1:
	    str_path = str_path + node
        else:
            str_path = str_path + node + '->'
    var.set(str_path)
    current_name = 'orgin_path.png'
    topo.show_topo(origin_path,logic_nodes,logic_links,current_name)

    
    topo_pic = PhotoImage(file='orgin_path.png')
    label_pic.configure(image = topo_pic)
    
    root.update()
    time.sleep(5)
    

def congestion_proc():
    
    
    #SClist1 = "sea,kcy"
    SClist2 = e_SVC.get()

    #SVList = get_service_chain(SClist1) 
    SVK = get_service_chain(SClist2) 
    #SVList = get_key_point(SVList,src,dst)
    SVK = get_key_point(SVK,src,dst)
    #print(SVK) 

    topo_1 = network_topo()
    logic_map_1 = map()

    phy_topy_1 = topy_load()

    phy_nodes_1 = topy_parse_node(phy_topy_1)

    phy_links_1 = topy_parse_links(phy_topy_1)

    # print(phy_nodes) 
    logic_nodes_1 = logic_map_1.getNodes(phy_nodes_1)
    #print(logic_nodes)
    logic_links_1 = logic_map_1.getLinks(phy_links_1)
    #print(logic_links)

  
    topo_1.topo_discover(logic_nodes_1,logic_links_1)

    
    #topo.topo_discover(NodeList,LinkList)

    str_con = e_con.get()
    con_src = str_con.split('-')[0]
    con_dst = str_con.split('-')[1]
    logic_graph_1 = logic_topo_gen (topo_1.get_graph(),con_src,con_dst)
    

    #print(logic_graph.edges())
    opt_path = cal_optimal_path(logic_graph_1,SVK)

    str_path_opt = "Path:"
    for node in opt_path:
        if opt_path.index(node) == len(opt_path)-1:
	    str_path_opt = str_path_opt + node
        else:
            str_path_opt = str_path_opt + node + '->'
    var.set(str_path_opt)
    print(opt_path)
    #topo.show_topo(topo.get_origin_path(src,dst))
    color_list = ['r'] * 8
    str_prefix = e_prefix.get()

    pathset = path_config(opt_path,phy_nodes_1,phy_links_1,str_prefix)

    #global_opt_path =copy.copy(pathset)
    #print(pathset)

    print ("------------------------------------------------t")
    print ("set path %s" %pathset)
    path_adjust(path_set)
    print ("------------------------------------------------t")
    print (global_opt_path)

    topo_1.show_topo(opt_path,logic_nodes_1,logic_links_1,'path_opt.png')

def call_undo():
    print ("#####################################################t")
    #SClist1 = "sea,kcy"
    SClist2 = e_SVC.get()

    #SVList = get_service_chain(SClist1) 
    SVK = get_service_chain(SClist2) 
    #SVList = get_key_point(SVList,src,dst)
    SVK = get_key_point(SVK,src,dst)
    #print(SVK) 

    topo_2 = network_topo()
    logic_map_2 = map()

    phy_topy_2 = topy_load()

    phy_nodes_2 = topy_parse_node(phy_topy_2)

    phy_links_2 = topy_parse_links(phy_topy_2)

    # print(phy_nodes) 
    logic_nodes_2 = logic_map_2.getNodes(phy_nodes_2)
    #print(logic_nodes)
    logic_links_2 = logic_map_2.getLinks(phy_links_2)
    #print(logic_links)

  
    topo_2.topo_discover(logic_nodes_2,logic_links_2)

    
    #topo.topo_discover(NodeList,LinkList)

    str_con = e_con.get()
    con_src = str_con.split('-')[0]
    con_dst = str_con.split('-')[1]
    logic_graph_2 = logic_topo_gen (topo_2.get_graph(),con_src,con_dst)
    

    #print(logic_graph.edges())
    opt_path = cal_optimal_path(logic_graph_2,SVK)

   
    #topo.show_topo(topo.get_origin_path(src,dst))
    color_list = ['r'] * 8
    str_prefix = e_prefix.get()

    pathset_2 = path_config(opt_path,phy_nodes_2,phy_links_2,str_prefix)
    
    path_adjust_undo(pathset_2)

label_svc = Label(root, text="service chain")
button_congestion = Button(root, text="Set Congestion")
label_svc.grid (row =0)
button_congestion.grid (row =1)

e_SVC = StringVar()
entry_svc = Entry(root,textvariable=e_SVC)
e_con = StringVar()
entry_congestion = Entry(root,textvariable=e_con)

entry_svc.grid(row=0, column=1)
entry_congestion.grid(row=1, column=1)

label_prefix = Label(root, text="protect network prefix")
label_prefix.grid (row =2)

e_prefix = StringVar()
entry_prefix = Entry(root,textvariable=e_prefix)
entry_prefix.grid(row=2, column=1)


scrollbar = Scrollbar(root)



mylist = Listbox(root, yscrollcommand = scrollbar.set )
'''
for line in range(100):
   mylist.insert(END, "This is line number " + str(line))
'''
mylist.grid(row =3,columnspan=2,sticky = 'news')
scrollbar.grid(row =3,column = 2)
scrollbar.config( command = mylist.yview )

label_show_path = Label(root, text = 'show the current path')
label_show_path.grid(row = 4,column = 0,sticky = 'sw')

var = StringVar()
label_show_path = Label(root, textvariable=var, relief=RAISED)
var.set("Hello Opendaylight")
label_show_path.grid(row = 5,column = 0,columnspan = 2,sticky = 'new')



button_show_topo = Button(root, text='Show Topology',command = topo_get)
button_show_topo.grid(row=4, column=1,sticky ='n')

button_path_optimal = Button(root, text='Set New Path',command = congestion_proc)
button_path_optimal.grid(row=6, column=0,sticky = 'n')

button_path_undo = Button(root, text='Unset New Path',command = call_undo)
button_path_undo.grid(row=6, column=1,sticky = 'n')

current_pic = PhotoImage(file='1.png')
label_pic = Label(image=current_pic)

#label_pic.image = current_pic
label_pic.grid(row=0, column=3, rowspan=7, sticky=W+E+N+S, padx=5, pady=5)


root.mainloop()

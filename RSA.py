#coding=UTF-8

import function as fun
import time
from math import sqrt
from function import Route
import cPickle as pickle
import csv
import sys

#nodes=fun.read_node('data/link_list_node50.xlsx','data/length_node50.xlsx')#从excwl读入节点列表

data_path=sys.argv[1]
nodes=fun.read_node(data_path+'ad_node.xlsx',data_path+'link_length.xlsx',data_path+'node_axis.xlsx',data_path+'ave_delay.xlsx')
num=int(sqrt(len(nodes)))


source=[int(sys.argv[x]) for x in range(2,6)]

d_node=int(sys.argv[6])

def RSA_main(data_path,num,source,d_node,c_para,e_range,speed_path):
    #创建速度文件对象
    file_s = open(speed_path,'rb')

    nodes=fun.read_node(data_path+'ad_node.xlsx',data_path+'link_length.xlsx',data_path+'node_axis.xlsx',data_path+'ave_delay.xlsx')
    
    print('线程开始')
    start_t=time.clock()
    a_node=[]#激活的节点列表
    for i in source:
        nodes[i].status=2
        a_node.append(nodes[i])

    w_node=[] #等待的节点
    time_unit=30 #时间单元为30s
    clock=0

    #读取新一时间单元的速度并赋值给对象
    speed_list = pickle.load(file_s)
    fun.read_speed(speed_list,nodes)

    #循环条件,终点为26
    while nodes[d_node].last_node == 0:
        #为等待中和已经激活的节点添加时间
        for node in w_node:
            node.div_time(time_unit)
        for node in a_node:
            node.div_time(time_unit)

    #判断等待列表中节点是否已经激活
        i=0
        while i < len(w_node):
            if w_node[i].w_time >= w_node[i].delay:
                w_node[i].status=2
                w_node[i].w_time-=w_node[i].delay
                a_node.append(w_node[i])
                w_node.remove(w_node[i]) #节点被激活
            else:
                i+=1
        #存储一次循环中新激活的节点
        a_node_t=[]
        w_node_t=[]
        for node in a_node:
            a_node_1,w_node_1=fun.spread_node(node)
            a_node_t.extend(a_node_1)
            w_node_t.extend(w_node_1)
        a_node.extend(a_node_t)
        w_node.extend(w_node_t)
        #判断激活列表中节点是否死亡
        i=0
        while i < len(a_node):
            if a_node[i].check_dead():
                a_node.remove(a_node[i])
            else:
                i+=1

        fun.update_speed(nodes) #更新道路速度
        clock+=1
        #读取新一时间单元的速度并赋值给对象
        speed_list = pickle.load(file_s)
        fun.read_speed(speed_list,nodes)



    file_s.close()
    route=fun.trace_back(nodes[d_node])
    finish_t=time.clock()

    
    r_time=fun.real_time(nodes,route,d_node,data_path)
    """
    print(c_para,e_range)
    print(route)
    print('预测时间为：'+str(clock*30))
    print('实际时间为：'+str(r_time))
    print('RSA运行时间为'+str(finish_t-start_t))
    """

    """
    #实验数据存储文件
    filename=data_path+'result.txt'
    #写入实验数据
    with open(filename,'a') as file:
        file.write('----------------------')
        file.write('\n')
        file.write('纠正频率：')
        file.write(str(c_para))
        file.write('单步预测误差')
        file.write(str(e_range))
        file.write('\n')
        file.write('RSA最短路径为：')
        file.write(str(route))
        file.write('最短路径长度：'+str(fun.routeLength(nodes,route)))
        file.write('\n')
        file.write('RSA实际时间为：'+str(r_time)+'\n')
        file.write('RSA运行时间为'+str(finish_t-start_t)+'\n')
        file.write('----------------------')
    """
    csv_file=data_path+str(c_para)+'_'+str(e_range)+'result.csv'
    with open(csv_file,'a') as file:
        csv_write=csv.writer(file,dialect='excel')
        csv_write.writerow([str(finish_t-start_t)[0:4],str(r_time)[0:7],fun.routeLength(nodes,route)])

    """
    if e_range==0:
        jpg_path=data_path+str(c_para)+'_'+str(e_range)+'_' 
        fun.draw_net(nodes,num,source,d_node,route,jpg_path)       
    """

def loop(data_path,num,source,d_node):
    RSA_main(data_path,num,source,d_node,0,0,data_path+"speed.dat")
    c_paras=[5,10,15,500]
    e_ranges=[0.05,0.1,0.15,0.2,0.25]
    
    for e_range in e_ranges:
        for c_para in c_paras:
            speed_path=data_path+str(c_para)+'_'+str(e_range)+'_'+"pre_speed.dat"
            RSA_main(data_path,num,source,d_node,c_para,e_range,speed_path)

loop(data_path,num,source,d_node)

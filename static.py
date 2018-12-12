#coding=UTF-8
import Dij
from math import sqrt
from Dij import Route
import time
import cPickle as pickle

import sys
sys.setrecursionlimit(100000)

#从文件读路网
data_path=raw_input('请输入数据文件夹路径（以/结尾）')
nodes=Dij.read_node(data_path+'ad_node.xlsx',data_path+'link_length.xlsx',data_path+'node_axis.xlsx',data_path+'ave_delay.xlsx')
num=int(sqrt(len(nodes)))

#输入多个起点
source=[]
s_node=int(raw_input('请输入起点：'))
while s_node != num**2:
    source.append(s_node)
    s_node=int(raw_input('请添加下一节点，输入节点个数停止添加：'))

d_node=int(raw_input('设置终点：'))

start_t=time.clock()
#从工作簿读第一个时间单元的数据

speedlist = pickle.load(open(data_path+'speed.dat','rb'))
Dij.read_speed(speedlist,nodes)

#对每个起点应用dij算法
r,t=Dij.dijkstra(nodes,source[0],d_node)
new_route=Route(r,t)
best_route=new_route

for i in range(1,len(source)):
    r,t=Dij.dijkstra(nodes,source[i],d_node)
    new_route=Route(r,t)
    if new_route.time < best_route.time:
        best_route=new_route

finish_t=time.clock()

print(best_route.route)
print('最短路径长度'+str(best_route.time))

r_time=Dij.real_time(nodes,best_route.route,d_node,data_path)

print('Dij实际时间为'+str(r_time))
print('Dij运行时间为'+str(finish_t-start_t))

#实验数据存储文件
filename=data_path+'result.txt'
#写入实验数据
with open(filename,'a') as file:
    file.write('\n')
    file.write('Dij最短路径为：')
    file.write(str(best_route.route))
    file.write('路径长度：'+str(best_route.time))
    file.write('\n')
    file.write('Dij实际时间为'+str(r_time)+'\n')
    file.write('Dij运行时间为'+str(finish_t-start_t)+'\n')

Dij.draw_net(nodes,num,source,d_node,best_route.route,data_path)

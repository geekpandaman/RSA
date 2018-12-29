#coding=UTF-8
import GAfun
import time
from math import sqrt
import cPickle as pickle
import sys
import csv

"""
gen=50 #迭代次数
pop_size=80 #种群数量

pc=0.1 #交叉概率
pm=0.1 #变异概率

pe=0.1 #精英法则比例
pk=1 #种群保留比例
"""

#读入节点
data_path=sys.argv[1]
nodes=GAfun.read_node(data_path+'ad_node.xlsx',data_path+'link_length.xlsx',data_path+'node_axis.xlsx',data_path+'ave_delay.xlsx')
num=int(sqrt(len(nodes)))

source=[int(sys.argv[x]) for x in range(2,3)]
d_node=int(sys.argv[3])

#实际路径集
pra_route_list=[]
"""
#显示算法初始状态
print('迭代次数为：'+str(gen))
print('种群数量：'+str(pop_size))
print('交叉概率:'+str(pc))
print('变异概率：'+str(pm))
print('精英法则比例：'+str(pe))
print('种群保留比例：'+str(pk))
"""
start_t=time.clock()




for s_node in source:
    file_s = open(data_path+"speed.dat","rb")
    #实际路径
    pra_route=GAfun.Route([],0)
    pra_route.route.append(s_node)

    #更新当前单元的速度
    time_unit=0
    speed_list=pickle.load(file_s)
    GAfun.read_speed(speed_list,nodes)
    remain_t=30
    #表示当前节点索引
    n=s_node
    #当前节点已经走过的距离
    c_length=0
 
    while n !=d_node:
        #next_n=GAfun.GAmain(nodes,n,d_node,gen,pop_size,pc,pm,pe,pk)
        next_n=GAfun.dijkstra(nodes,n,d_node)
        t_link=GAfun.inquire(nodes[n],nodes[next_n])
        c_length+=remain_t*t_link.speed
        remain_t=0
        if c_length >= t_link.length:
            #到达下一节点
            remain_t=(c_length-t_link.length)/t_link.speed #记录时间余量
            c_length=0
            n=next_n
            pra_route.route.append(n)
            remain_t-=nodes[n].delay

        while remain_t <= 0:
            time_unit+=1
            try:
                speed_list=pickle.load(file_s)
                GAfun.read_speed(speed_list,nodes)
            except:
                n = d_node
                break
            remain_t+=30
    
    pra_route.time=30*(time_unit+1)-remain_t
    pra_route_list.append(pra_route)
    file_s.close()

#快排后取最小路径
GAfun.Qsort(pra_route_list,0,len(pra_route_list)-1)

pra_route=pra_route_list[0]

finish_t=time.clock()

print(pra_route.route)
print('GA实际时间为'+str(pra_route.time))
print('GA运行时间为'+str(finish_t-start_t))
"""
#实验数据存储文件
filename=data_path+'result.txt'
#写入实验数据
with open(filename,'a') as file:
    file.write('\n')
    file.write('DPO最短路径为：')
    file.write(str(pra_route.route))
    file.write('路径长度为'+str(GAfun.routeLength(nodes,pra_route.route)))
    file.write('\n')
    file.write('DPO实际时间为'+str(pra_route.time)+'\n')
    file.write('DPO运行时间为'+str(finish_t-start_t)+'\n')

GAfun.draw_net(nodes,num,source,d_node,pra_route.route,data_path)
"""
csv_file=data_path+'OLRO_result.csv'
with open(csv_file,'a') as file:
    csv_write=csv.writer(file,dialect='excel')
    csv_write.writerow([str(finish_t-start_t)[0:4],str(pra_route.time)[0:7],str(GAfun.routeLength(nodes,pra_route.route)/3.6)[0:5]])
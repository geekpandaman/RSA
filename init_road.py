#coding=UTF-8

import function as fun
import sys
import csv

#生成路网模块

num=int(sys.argv[1])
time_units=int(sys.argv[2])

nodes=fun.init_node(num)
fun.print_node(nodes)#打印节点状态

#创建实验数据文件夹
data_path="data_"+str(num**2)+"/"
fun.mkdir(data_path)
fun.write_nodes(nodes,data_path)

#实验数据存储文件
filename=data_path+'result.txt'
#写入实验数据
with open(filename,'w') as file:
    file.write('矩阵边长为：'+str(num)+'\n')

e_list=[0.05,0.1,0.15,0.2,0.25]

p_list=[5,10,15,500]


csv_file=data_path+'0'+'_'+'0'+'result.csv'
with open(csv_file,'w') as file:
        csv_write=csv.writer(file,dialect='excel')
        csv_write.writerow(['RunTime','RealTime','RouteLength'])

csv_file=data_path+'OLRO_result.csv'
with open(csv_file,'w') as file:
        csv_write=csv.writer(file,dialect='excel')
        csv_write.writerow(['RunTime','RealTime','RouteLength'])

for e in e_list:
    for p in p_list:
        csv_file=data_path+str(p)+'_'+str(e)+'result.csv'
        with open(csv_file,'w') as file:
            csv_write=csv.writer(file,dialect='excel')
            csv_write.writerow(['RunTime','RealTime','RouteLength'])

fun.write_speed(data_path,nodes,time_units)

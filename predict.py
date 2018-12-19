#coding=UTF-8

import function as fun
from math import sqrt
import cPickle as pickle
import sys

#从命令行获取参数
data_path=sys.argv[1]
time_units=int(sys.argv[2])

nodes=fun.read_node(data_path+'ad_node.xlsx',data_path+'link_length.xlsx',data_path+'node_axis.xlsx',data_path+'ave_delay.xlsx')
num=int(sqrt(len(nodes)))



#实验数据存储文件
filename=data_path+'result.txt'
#写入实验数据
#with open(filename,'w') as file:
    #file.write('矩阵边长为：'+str(num)+'\n')

#预测误差列表
e_list=[0.05,0.1,0.15,0.2,0.25]
for e in e_list:
    fun.write_error(data_path,nodes,time_units,e)

p_list=[5,10,15,500]

for e in e_list:
    for p in p_list:
       fun.p_write_speed(data_path,time_units,p,e) 

print('successfully predicting!')

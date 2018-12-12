#coding=UTF-8

import function as fun
from math import sqrt
import cPickle as pickle

data_path=raw_input('请输入数据文件夹路径（以/结尾）')
nodes=fun.read_node(data_path+'ad_node.xlsx',data_path+'link_length.xlsx',data_path+'node_axis.xlsx',data_path+'ave_delay.xlsx')
num=int(sqrt(len(nodes)))



#实验数据存储文件
filename=data_path+'result.txt'
#写入实验数据
with open(filename,'w') as file:
    file.write('矩阵边长为：'+str(num)+'\n')

time_units=int(raw_input('time units:'))

e_range=float(raw_input("新增预测误差："))
e_list=[]
while e_range != 0:
    e_list.append(e_range)
    #fun.write_error(data_path,nodes,time_units,e_range)
    e_range=float(raw_input("新增预测误差："))

pre=int(raw_input("新增预测数据："))
while pre == 1:
    c_para=int(raw_input('纠正频率：'))
    for e_range in e_list:
        fun.p_write_speed(data_path,time_units,c_para,e_range)
    pre=int(raw_input("新增预测数据："))

print('successfully predicting!')
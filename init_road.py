#coding=UTF-8

import function as fun


#生成路网模块

num=int(raw_input('输入矩阵边长：'))
nodes=fun.init_node(num)
fun.print_node(nodes)#打印节点状态

time_units=int(raw_input('生成时间单元的数量：'))


#创建实验数据文件夹
data_path="data_"+str(num**2)+"/"
fun.mkdir(data_path)
fun.write_nodes(nodes,data_path)

#实验数据存储文件
filename=data_path+'result.txt'
#写入实验数据
with open(filename,'w') as file:
    file.write('矩阵边长为：'+str(num)+'\n')


fun.write_speed(data_path,nodes,time_units)

e_range=float(raw_input("新增预测误差："))
e_list=[]
while e_range != 0:
    e_list.append(e_range)
    fun.write_error(data_path,nodes,time_units,e_range)
    e_range=float(raw_input("新增预测误差："))

pre=int(raw_input("新增预测数据："))
while pre == 1:
    c_para=int(raw_input('纠正频率：'))
    for e_range in e_list:
        fun.p_write_speed(data_path,time_units,c_para,e_range)
    pre=int(raw_input("新增预测数据："))

print('successfully predicting!')
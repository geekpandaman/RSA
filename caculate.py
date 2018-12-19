#coding=UTF-8
import function as fun
import cPickle as pickle

def add_speed(path,nodes,time):
    """速度工作簿,并随机出所有时间节点的速度表,c_para表示修正频率，e_range表示预测误差范围"""
    fun.init_speed(nodes)
    path1=path+"speed.dat"
    file = open(path1,'ab')


    for t in range(0,time):
        unitSpeed=[]
        for i in range(0,len(nodes)):
            for j in range(0,len(nodes[i].adjcent_link)):
                unitSpeed.append(nodes[i].adjcent_link[j].speed)
        pickle.dump(unitSpeed,file)
        fun.update_speed(nodes)
    
    file.close()

data_path=raw_input('请输入数据文件夹路径（以/结尾）')
nodes=fun.read_node(data_path+'ad_node.xlsx',data_path+'link_length.xlsx',data_path+'node_axis.xlsx',data_path+'ave_delay.xlsx')
ex_time = int(raw_input('输入增加的时间单元：'))
add_speed(data_path,nodes,ex_time)
print('增加成功！')

#route = [39, 79, 119, 118, 117, 116, 156, 196, 195, 235, 275, 315, 355, 395, 394, 393, 392, 391, 431, 430, 470, 510, 550, 549, 548, 547, 546, 586, 626, 625, 624, 623, 622, 662, 661, 701, 700, 699, 739, 779, 819]

#time=fun.real_time(nodes,route,819,data_path)
#print(time)
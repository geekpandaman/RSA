#coding=UTF-8

class Node():
    """定义道路节点类成员"""

    def __init__(self,node_index,ave_delay,x_value,y_value):

        self.adjcent_link=[]   #邻近连接数组
        self.status=0  #定义路口状态 inactive=0 wating=1 active=2 dead=3
        self.index=node_index #节点在列表中的索引
        self.delay=ave_delay #节点平均延误
        self.last_node=0 
        self.w_time=0 #在该路口已经等待的时间
        self.X=x_value
        self.Y=y_value#设置路口坐标

    def div_time(self,t_unit):
        """为节点增加时间单元"""
        self.w_time+=t_unit
    
    def check_dead(self):
        """若节点死亡，返回True"""
        dead=True
        for link in self.adjcent_link:
            if link.next_node.status == 0:
                dead = False
                break
        return dead

class Link():

    def __init__(self,p_node,length):

        self.length=length
        self.next_node=p_node
        self.ripple_length=0 #链接中波纹的长度
        self.speed=0

class Route():
    """定义路径类，包含路径索引列表以及路径时间"""
    def __init__(self,r,t):
        self.route=r
        self.time=t

import xlrd
import xlwt
from xlutils.copy import copy
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import math
from random import randint
from random import uniform
import os
import cPickle as pickle

def read_node(path1,path2,path3,path4):
    """从excel初始化节点列表,path1为邻接表，path2为路径长度表，path3为节点坐标表，path4为平均延误表"""

    workbook=xlrd.open_workbook(path1)
    sheet1=workbook.sheet_by_index(0)

    workbook3=xlrd.open_workbook(path3)
    sheet3=workbook3.sheet_by_index(0)

    workbook4=xlrd.open_workbook(path4)
    sheet4=workbook4.sheet_by_index(0)

    nodes=[]
    #初始化shee1.nrows个节点
    for i in range(0,sheet1.nrows):
        new_node=Node(i,sheet4.cell(i,0).value,sheet3.cell(i,0).value,sheet3.cell(i,1).value)
        nodes.append(new_node)
    print('初始化节点成功')

    workbook2=xlrd.open_workbook(path2)
    sheet2=workbook2.sheet_by_index(0)

    #为节点添加连接
    for i in range(0,sheet1.nrows):
        for j in range(0,4):
            if sheet1.cell(i,j).value!='':
                new_link=Link(nodes[int(sheet1.cell(i,j).value)],int(sheet2.cell(i,j).value)) #excel中数据默认格式为float,需进行格式转换
                nodes[i].adjcent_link.append(new_link)

    print('初始化链接成功')
    return nodes
    
def mkdir(dir_path):
    """创建数据存储文件夹"""
    folder = os.path.exists(dir_path)
    if not folder:
        os.makedirs(dir_path)    
    else:
        print ("文件夹已经存在！")

def write_nodes(nodes,dir_path):
    """将路网写入工作簿"""
    wb1=xlwt.Workbook()
    ws1=wb1.add_sheet("sheet1")
    wb2=xlwt.Workbook()
    ws2=wb2.add_sheet("sheet1")
    wb3=xlwt.Workbook()
    ws3=wb3.add_sheet("sheet1")
    wb4=xlwt.Workbook()
    ws4=wb4.add_sheet("sheet1")   

    for i in range(0,len(nodes)):
        for j in range(0,len(nodes[i].adjcent_link)):
            ws1.write(i,j,nodes[i].adjcent_link[j].next_node.index)
            ws2.write(i,j,nodes[i].adjcent_link[j].length)
        ws3.write(i,0,nodes[i].X)
        ws3.write(i,1,nodes[i].Y)
        ws4.write(i,0,nodes[i].delay)

    path1=dir_path+"ad_node.xlsx"
    path2=dir_path+"link_length.xlsx"
    path3=dir_path+"node_axis.xlsx"
    path4=dir_path+"ave_delay.xlsx"
    wb1.save(path1)
    wb2.save(path2)
    wb3.save(path3)
    wb4.save(path4)
    "路网写入文件成功"

def add_speed_sheet(path,nodes,time):
    """将速度写入工作簿"""
    path=path+"speed.xlsx"
    rb=xlrd.open_workbook(path)
    wb=copy(rb) #利用xlutils.copy作为管道
    ws=wb.add_sheet(str(time))
    for i in range(0,len(nodes)):
        for j in range(0,len(nodes[i].adjcent_link)):
            ws.write(i,j,nodes[i].adjcent_link[j].speed)
    wb.save(path)

def write_speed(path,nodes,time):
    """速度工作簿,并随机出所有时间节点的速度表,c_para表示修正频率，e_range表示预测误差范围"""
    init_speed(nodes)
    path1=path+"speed.dat"
    file = open(path1,'wb')


    for t in range(0,time):
        unitSpeed=[]
        for i in range(0,len(nodes)):
            for j in range(0,len(nodes[i].adjcent_link)):
                unitSpeed.append(nodes[i].adjcent_link[j].speed)
        pickle.dump(unitSpeed,file)
        update_speed(nodes)
    
    file.close()
    

def write_error(path,nodes,time,e_range):

    path2=path+str(e_range)+"pre_e.dat"
    file = open(path2,'wb')

    for t in range(0,time):
        unitError=[]
        for i in range(0,len(nodes)):
            for j in range(0,len(nodes[i].adjcent_link)):
                value=round(uniform(-e_range,e_range),6)
                unitError.append(value)
        pickle.dump(unitError,file)
    
    file.close()


def p_write_speed(path,time,c_para,e_range):
    """生成不同条件下的速度表,预测矩阵要少一个时间单元"""
    file_S = open(path+'speed.dat','rb')
    file_E = open(path+str(e_range)+"pre_e.dat",'rb')
    file_P = open(path+str(c_para)+'_'+str(e_range)+'_'+"pre_speed.dat",'wb')

    speedList=pickle.load(file_S)
    e_list=pickle.load(file_E)
    #累计误差矩阵
    accum_e=[]
    for n in range(0,len(e_list)):
        accum_e.append(1)
    pre_speed=[]
    for t in range(0,time-1):
        if t%c_para ==0:
            for n in range(0,len(accum_e)):
                accum_e[n]=1
        else:
            for n in range(0,len(accum_e)):
                accum_e[n]+=e_list[n]
                if accum_e[n] < 0:
                    accum_e[n]=0
        pre_unit=[]
        for n in range(0,len(speedList)):
            pre_unit.append(speedList[n]*accum_e[n])
        #向文件添加新的预测矩阵
        pickle.dump(pre_unit,file_P)
    
        #更新当前时间单元的速度矩阵和误差矩阵
        speedList=pickle.load(file_S)
        e_list=pickle.load(file_E)
        
    
    file_E.close()
    file_P.close()
    file_S.close()

def read_speed(speedlist,nodes):
    """读出速度"""
    #应用迭代器
    s = iter(speedlist)
    for i in range(0,len(nodes)):
        for j in range(0,len(nodes[i].adjcent_link)):
            #利用生成器表达式
            nodes[i].adjcent_link[j].speed=s.next()


def init_speed(nodes):
    """利用正态分布初始化速度"""
    rand_speed=np.random.normal(30, 10,200)#均值为28，标准差为5，元素个数为200的列表
    for node in nodes:
        for link in node.adjcent_link:
            speed=round(np.random.choice(rand_speed),2)
            #限定速度取值范围
            while speed <=0 or speed>50:
                speed=round(np.random.choice(rand_speed),2)
            link.speed=speed  #取两位小数


def update_speed(nodes):
    """随机数变化，4.16 m/s"""
    for node in nodes:
        for link in node.adjcent_link:
            delta_s=link.speed+round(uniform(-4,4),2)
            if delta_s <0:
                #delta_s=link.speed+round(uniform(-10,10),2)
                delta_s=0
            elif delta_s>50:
                delta_s=50

            link.speed=delta_s

def print_node(nodes):
    """打印每个节点连接点"""
    for node in nodes:
        print(node.index,node.delay)
        for link in node.adjcent_link:
            print(str(link.next_node.index)+' '+str(link.length))
        print("\n")
    print("节点初始化成功")


def spread_node(node):
    """对于激活节点调用,返回该节点激活的节点"""
    a_node=[]
    w_node=[]
    for link in node.adjcent_link:
        if link.next_node.status == 0:
            link.ripple_length+=link.speed*node.w_time
            if link.ripple_length >= link.length:#波纹到达下一节点
                link.next_node.status=1  #将下一节点设置为等待状态
                link.next_node.last_node=node
                link.next_node.w_time=(link.ripple_length-link.length)/link.speed #该时间单元内节点余量
                link.ripple_length=link.length
                if link.next_node.w_time >=link.next_node.delay:#判断下一节点是否已被激活
                    link.next_node.status=2
                    link.next_node.w_time=link.next_node.w_time-link.next_node.delay
                    a_node_1,w_node_1=spread_node(link.next_node) #递归调用，注意空间复杂度
                    a_node.extend(a_node_1)
                    w_node.extend(w_node_1)
            if link.next_node.status == 1:
                w_node.append(link.next_node)
            elif link.next_node.status == 2:
                a_node.append(link.next_node)
    node.w_time=0 #将时间余量转化为节点中的波纹长度
    #是否要设置节点死亡？
    return (a_node,w_node) #返回列表

def trace_back(r_node):
    """回溯路径"""
    route=[]
    while r_node != 0:
        route.append(r_node.index)
        r_node=r_node.last_node
    route.reverse()#反向排序
    return route

def draw_link(nodes,n1,n2):
    """画出两点之间的连线,size为矩阵的边长"""
    x=[]
    y=[]
    x.append(nodes[n1].X)
    x.append(nodes[n2].X)
    y.append(nodes[n1].Y)
    y.append(nodes[n2].Y)
    plt.plot(x,y,linewidth = '0.4',color = 'cyan')#画出线条并设置宽度



def init_node(size):
    """生成路网"""
    nodes=[]
    for i in range(0,size):
        for j in range(0,size):
            x_value=round(i+uniform(-0.5,0.5),2)
            y_value=round(j+uniform(-0.5,0.5),2)
            new_node=Node(size*i+j,randint(20,40),x_value,y_value)
            #new_node=Node(size*i+j,20,x_value,y_value)
            nodes.append(new_node)
    print('节点生成成功')
    #初始化链接
    for i in range(0,size**2):
        #右方节点
        if i%size != size-1:
            distance=round(math.sqrt((nodes[i].X-nodes[i+1].X)**2+(nodes[i].Y-nodes[i+1].Y)**2),2)*1000 #比例尺为1000
            new_link=Link(nodes[i+1],distance)
            nodes[i].adjcent_link.append(new_link)
            new_link_r=Link(nodes[i],distance)
            nodes[i+1].adjcent_link.append(new_link_r)
        #上方节点
        if i<size*(size-1): 
            distance=round(math.sqrt((nodes[i].X-nodes[i+size].X)**2+(nodes[i].Y-nodes[i+size].Y)**2),2)*1000
            new_link=Link(nodes[i+size],distance)
            nodes[i].adjcent_link.append(new_link)
            new_link_r=Link(nodes[i],distance)
            nodes[i+size].adjcent_link.append(new_link_r)
    print('链接生成成功')
    return nodes

def draw_net(nodes,size,source,d_node,route,data_path):
    """画出路网"""
    print('绘制节点中...')
    #储存坐标值
    x_value=[]
    y_value=[]
    for i in range(0,size**2):
        x_value.append(nodes[i].X)
        y_value.append(nodes[i].Y)
    plt.scatter(x_value,y_value,s=5,color='grey') #画出节点

    #标出起点
    x_value=[]
    y_value=[]
    for i in source:
        x_value.append(nodes[i].X)
        y_value.append(nodes[i].Y)
    plt.scatter(x_value,y_value,color='green') #画出节点

    #标出终点
    plt.scatter(nodes[d_node].X,nodes[d_node].Y,color='red')

    #对于每个节点，只画右方和上方节点的连接线
    print('绘制链接中')
    for i in range(0,size**2):
        #右方节点
        if i%size != size-1:
            draw_link(nodes,i,i+1)
        #上方节点
        if i<size*(size-1): 
            draw_link(nodes,i,i+size)
    
    #绘制最优路径
    x_value=[]
    y_value=[]
    for i in route:
        x_value.append(nodes[i].X) 
        y_value.append(nodes[i].Y)
    plt.plot(x_value,y_value,linewidth = '1',color = 'blue')

    plt.axis([-1,size*1.1,-1,size*1.1])
    plt.rcParams['savefig.dpi'] = 300
    plt.savefig(data_path+"best_route.png")
    #plt.show()

def inquire(n1,n2):
    """查询两节点之间的链接，传入两个节点对象，返回链接对象"""
    i=0
    while n1.adjcent_link[i].next_node != n2:
        i+=1
        if i == len(n1.adjcent_link):
            print('error,查询失败！')
            i-=1
            break
    return n1.adjcent_link[i]

def real_time(nodes,route,destination,data_path):
    """输入路网和路径，计算车辆实际用时,传入终点"""
    time_unit=0
    remain_t=30
    speed_path=data_path+"speed.dat"
    #创建速度文件对象
    file_s = open(speed_path,'rb')
    #读取新一时间单元的速度并赋值给对象
    speed_list = pickle.load(file_s)
    read_speed(speed_list,nodes)
    #标示当前节点索引
    n=0
    #当前链接已经走过的距离
    c_length=0
    while route[n] != destination:
        t_link=inquire(nodes[route[n]],nodes[route[n+1]])
        c_length+=remain_t*t_link.speed
        remain_t=0
        if c_length >= t_link.length:
            #到达下一节点
            remain_t=(c_length-t_link.length)/t_link.speed #记录时间余量
            c_length=0
            n+=1
            remain_t-=nodes[route[n]].delay
            
        while remain_t <= 0:
            time_unit+=1
            #读取新一时间单元的速度并赋值给对象
            speed_list = pickle.load(file_s)
            read_speed(speed_list,nodes)
            remain_t+=30
    file_s.close()
    return 30*(time_unit+1)-remain_t
        
def routeLength(nodes,route):
    """传入路径列表"""
    totalLength=0
    for i in range(0,len(route)-1):
        t_link=inquire(nodes[route[i]],nodes[route[i+1]])
        totalLength+=t_link.length
    return totalLength
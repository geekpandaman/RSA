#coding=UTF-8

class Node():
    """定义道路节点类成员"""

    def __init__(self,node_index,ave_delay,x_value,y_value):

        self.adjcent_link=[]   #邻近连接数组
        self.status=0  #定义路口状态 inactive=0 wating=1 active=2 dead=3
        self.delay=ave_delay
        self.X=x_value
        self.Y=y_value
        self.index=node_index
        self.last_node=0
        self.weight=0
        self.status=False #True表示已经成为过permanent节点
    
    def check_status(self):
        """若节点需要被踢除，返回True"""
        status=True
        for link in self.adjcent_link:
            if link.next_node.status == False:
                status = False
                break
        return status

class Link():

    def __init__(self,p_node,length):

        self.length=length
        self.next_node=p_node
        self.speed=0

class Route():
    """定义路径类，包含路径索引列表以及路径时间"""
    def __init__(self,r,t):
        self.route=r
        self.time=t


import xlrd
import copy
import numpy as np
import matplotlib.pyplot as plt
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

def dijkstra(nodes_copy,s_node,d_node):
    """求一次最短路径问题，返回值为当前路口转向决策,列表为传值，起重点参数为索引。返回值为路径列表和终点权值"""
    nodes=copy.deepcopy(nodes_copy) #利用深复制使函数传值
    permanent=[] #permanent标号的集
    p_node=nodes[s_node] #最新的permanent标号点
    permanent.append(p_node)
    p_node.status=True
    while nodes[d_node].last_node == 0:
        #对新选择的标号节点p_node，检查邻近节点的标号,进行temp标号
        for link in p_node.adjcent_link:
            #weight=p_node.weight+link.length/link.speed+link.next_node.delay
            weight=p_node.weight+link.length
            #比较并更新新节点标号
            if link.next_node.status == False: 
                if link.next_node.weight > (weight+p_node.weight) or link.next_node.weight == 0:
                    link.next_node.last_node=p_node
                    link.next_node.weight=weight
        """
        #随机选择一节点为p_node
        for link in p_node.adjcent_link:
            if link.next_node.status == False:
                min_weight=link.next_node.weight
                t_node=link.next_node
                break
        BUG_Warning!!!!
        """
        
        #随机选取新的p_node节点，后面动态管理列表步骤使得此步不会出错
        for link in permanent[0].adjcent_link:
            if link.next_node.status == False:
                p_node=link.next_node
                break

        #从temp节点中找到权值最小的待标号点，作为p_node
        for node in permanent:
            for link in node.adjcent_link:
                if link.next_node.status==False:
                    if link.next_node.weight < p_node.weight:
                        p_node=link.next_node
        
        permanent.append(p_node)
        p_node.status=True

        #剔除周围不再有temp节点的permanent节点
        i=0
        while i < len(permanent):
            if permanent[i].check_status():
                permanent.remove(permanent[i])
            else:
                i+=1
    
    route=trace_back(nodes[d_node])
    return (route,nodes[d_node].weight)

def trace_back(r_node):
    """回溯路径"""
    route=[]
    while r_node != 0:
        route.append(r_node.index)
        r_node=r_node.last_node
    route.reverse()#反向排序
    return route

def print_node(nodes):
    """打印每个节点连接点"""
    for node in nodes:
        print(node.index,node.X,node.Y)
        for link in node.adjcent_link:
            print(str(link.next_node.index)+' '+str(link.length))
        print("\n")
    print("节点初始化成功")

def draw_link(nodes,n1,n2):
    """画出两点之间的连线,size为矩阵的边长"""
    x=[]
    y=[]
    x.append(nodes[n1].X)
    x.append(nodes[n2].X)
    y.append(nodes[n1].Y)
    y.append(nodes[n2].Y)
    plt.plot(x,y,linewidth = '0.4',color = 'cyan')#画出线条并设置宽度

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
    print('绘制链接中...')
    for i in range(0,size**2):
        #右方节点
        if i%size != size-1:
            draw_link(nodes,i,i+1)
        #上方节点
        if i<size*(size-1):
            draw_link(nodes,i,i+size)
        #print(i)
    
    #绘制最优路径
    x_value=[]
    y_value=[]
    for i in route:
        x_value.append(nodes[i].X) 
        y_value.append(nodes[i].Y)
    plt.plot(x_value,y_value,linewidth = '1',color = 'blue')

    plt.axis([-1,size*1.1,-1,size*1.1])
    plt.rcParams['savefig.dpi'] = 300
    plt.savefig(data_path+"best_route_dij.png")
    plt.show()
    
    
def read_speed(speedlist,nodes,time):
    unit_list=speedlist[time]
    n=0
    for i in range(0,len(nodes)):
        for j in range(0,len(nodes[i].adjcent_link)):
            nodes[i].adjcent_link[j].speed=unit_list[n]


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
    speedlist=pickle.load(open(data_path+'speed.dat','rb'))
    read_speed(speedlist,nodes,time_unit)
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
            read_speed(speedlist,nodes,time_unit)
            remain_t+=30
    
    return 30*(time_unit+1)-remain_t
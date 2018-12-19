#coding=UTF-8

class Node():
    """定义道路节点类成员"""

    def __init__(self,node_index,ave_delay,x_value,y_value):

        self.adjcent_link=[]   #邻近连接数组
        self.index=node_index #节点在列表中的索引
        self.delay=ave_delay
        self.X=x_value
        self.Y=y_value#设置路口坐标
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
        self.fit_value=0

import xlrd
import xlwt
from xlutils.copy import copy
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import math
from random import randint
from random import uniform
from random import choice
import os
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

def init_speed(nodes):
    """利用正态分布初始化速度"""
    rand_speed=np.random.normal(28, 5,200)#均值为28，标准差为5，元素个数为200的列表
    for node in nodes:
        for link in node.adjcent_link:
            speed=round(np.random.choice(rand_speed),2)
            #限定速度取值范围
            while speed <=0 or speed>50:
                speed=round(np.random.choice(rand_speed),2)
            link.speed=speed  #取两位小数

def read_speed(speedlist,nodes):
    """读出速度"""
    #应用迭代器
    s = iter(speedlist)
    for i in range(0,len(nodes)):
        for j in range(0,len(nodes[i].adjcent_link)):
            #利用生成器表达式
            nodes[i].adjcent_link[j].speed=s.next()

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
    print('绘制链接中')
    for i in range(0,size**2):
        #右方节点
        if i%size != size-1:
            draw_link(nodes,i,i+1)
        #上方节点
        if i<size*(size-1): 
            draw_link(nodes,i,i+size)
        print(i)
    
    #绘制最优路径
    x_value=[]
    y_value=[]
    for i in route:
        x_value.append(nodes[i].X) 
        y_value.append(nodes[i].Y)
    plt.plot(x_value,y_value,linewidth = '1',color = 'blue')

    plt.axis([-1,size*1.1,-1,size*1.1])
    plt.rcParams['savefig.dpi'] = 300
    plt.savefig(data_path+"best_route_DPO.png")
    plt.show()
def compare(route,node):
    """判断路径是否进入死胡同，传入节点对象,进入死胡同则返回True"""
    n=0
    for link in node.adjcent_link:
        if link.next_node.index in route:
            n+=1 
    if n == len(node.adjcent_link):
        return True
    else:
        return False


def coding(nodes,s_node,d_node):
    """对基因进行编码,传入节点索引"""
    #定义新路径
    new_r=Route([s_node],0)

    #下一编码节点
    n_node=nodes[s_node]

    while n_node.index != d_node:

        #若走进死路，则重新编码
        if compare(new_r.route,n_node):
            new_r.route=[s_node]
            new_r.time=0
            n_node=nodes[s_node]

        t_link = choice(n_node.adjcent_link)
        #若下一节点重复则重新选择
        while t_link.next_node.index in new_r.route:
            t_link = choice(n_node.adjcent_link)
        if t_link.speed != 0:
            new_r.time+=(round(t_link.length/t_link.speed,2)+t_link.next_node.delay)
        else:
            new_r.time+=10000
        new_r.route.append(t_link.next_node.index)
        n_node=t_link.next_node
    
    if new_r.time <= 0:
        print('error!')
    
    return new_r

def Qsort(routes,low,high):
    """以路径时间为主键，从小到大对路径进行快速排序"""
    if low<high:
        pivotloc = partition(routes,low,high)
        Qsort(routes,low,pivotloc-1)
        Qsort(routes,pivotloc+1,high)

def partition(routes,low,high):
    """一次快速排序"""
    pivot=routes[low]
    pivotkey=pivot.time
    while (low < high):
        while(low < high and routes[high].time >= pivotkey):
            high-=1
        routes[low]=routes[high]
        while(low < high and routes[low].time <= pivotkey):
            low+=1
        routes[high]=routes[low]
    routes[low]=pivot
    return low

def fit_func(routes):
    """计算适应度累计概率,利用转轮盘法产生新一代个体"""
    total=0
    for route in routes:
        total+=1/route.time
    acc_value=0
    for route in routes:
        acc_value+=(1/route.time)/total
        route.fit_value=acc_value
    #新一代种群,转轮盘选择
    new_routes=[]
    for i in range(0,len(routes)):
        posb=uniform(0,1)

        j=0
        while posb > routes[j].fit_value:
            j+=1
        new_routes.append(routes[j])

    return new_routes

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

def recaculate_t(R,nodes):
    """重新计算路径时间"""
    T=0
    for i in range(0,len(R.route)-1):
        no1=nodes[R.route[i]]
        no2=nodes[R.route[i+1]]
        L=inquire(no1,no2)
        if L.speed != 0:
            T+=(round(L.length/L.speed,2)+L.next_node.delay)
        else:
            T+=10000
    R.time=T

def crossover(routes,nodes,pc):
    """染色体交叉"""
    for i in range(0,len(routes)):
        posb=uniform(0,1)
        if posb<pc:
            #交换点在两个列表中的位置
            id1=0
            id2=0
            id1=randint(1,len(routes[i].route)-2) #起点和终点交叉没有意义,是否要设置？
            cpoint=routes[i].route[id1]
            while id2 ==0:
                index_c=randint(0,len(routes)-1) #第二条路径的下标
                route_c=routes[index_c]
                for j in range(0,len(route_c.route)):
                    if route_c.route[j] == cpoint:
                        id2=j
                        break
            #交换染色体
            new_route1=Route([],0)
            new_route2=Route([],0)
            new_route1.route.extend(routes[i].route[:id1])
            new_route1.route.extend(route_c.route[id2:])
            new_route2.route.extend(route_c.route[:id2])
            new_route2.route.extend(routes[i].route[id1:])

            recaculate_t(new_route1,nodes)
            recaculate_t(new_route2,nodes)
            routes[i]=new_route1
            routes[index_c]=new_route2

def mutation(routes,nodes,d_node,pm):
    """染色体变异,d_node传索引"""
    for i in range(0,len(routes)):
        posb=uniform(0,1)
        if posb<pm:
            #变异点
            id1=randint(0,len(routes[i].route)-1) #终点变异没有意义，终点的上一点变异意义大不大？
            new_route=Route([],0)
            new_route.route.extend(routes[i].route[:id1+1])

            #重新编码
            n_node=nodes[new_route.route[-1]]
            while n_node.index != d_node:
                #若走进死路，则重新编码
                if compare(new_route.route,n_node):
                    new_route.route=routes[i].route[:id1+1]
                    n_node=nodes[new_route.route[-1]]
                t_link = choice(n_node.adjcent_link)
                #若下一节点重复则重新选择
                while t_link.next_node.index in new_route.route:
                    t_link = choice(n_node.adjcent_link)
                
                new_route.route.append(t_link.next_node.index)
                n_node=t_link.next_node

            recaculate_t(new_route,nodes)
            routes[i]=new_route



def GAmain(nodes,s_node,d_node,gen,pop_size,pc,pm,pe,pk):
    """一次遗传算法，返回下一路口"""
    #编码
    routes=[]
    for i in range(0,pop_size):
        new_route=coding(nodes,s_node,d_node)
        routes.append(new_route)
    Qsort(routes,0,len(routes)-1)
    if len(routes[0].route) > 4:
        #开始迭代
        for i in range(0,gen):
            #子代种群
            son_routes=[]
            #排序后，精英个体直接进入下一代
            Qsort(routes,0,len(routes)-1)
            son_routes.extend(routes[:int(pe*len(routes))])
            #差的个体不进入轮盘选择
            routes=routes[int(pe*len(routes)):int(pk*len(routes))]
            son_routes.extend(fit_func(routes))
            #染色体交叉,变异
            crossover(son_routes,nodes,pc)
            #mutation(son_routes,nodes,d_node,pm)
            routes=son_routes

    #挑选出最好个体
    Qsort(routes,0,len(routes)-1)
    #此处返回值为下一个节点要走的位置
    return routes[0].route[1]

def routeLength(nodes,route):
    """传入路径列表"""
    totalLength=0
    for i in range(0,len(route)-1):
        t_link=inquire(nodes[route[i]],nodes[route[i+1]])
        totalLength+=t_link.length
    return totalLength

def dijkstra(nodes,s_node,d_node):
    """求一次最短路径问题，返回值为当前路口转向决策,列表为传值，起重点参数为索引。返回值为路径列表和终点权值"""
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
    reset_nodes(nodes)
    return route[1]

def trace_back(r_node):
    """回溯路径"""
    route=[]
    while r_node != 0:
        route.append(r_node.index)
        r_node=r_node.last_node
    route.reverse()#反向排序
    return route

def reset_nodes(nodes):
    """在一次dij后将路网恢复到原始状态，代替深复制传值的解决方案"""
    for i in range(0,len(nodes)):
        node = nodes[i]
        node.weight = 0
        node.last_node = 0
        node.status = False
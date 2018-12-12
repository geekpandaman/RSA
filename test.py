import cPickle as pickle
import os
import time


#speed=pickle.load(open("data_400/speed.dat","rb"))

#501=pickle.load(open("data_400/5_0.1_pre_speed.dat","rb"))

#1001=pickle.load(open('data_400/10_0.1_pre_speed.dat','rb'))

def write_test():
    file = open("test.dat",'wb')
    speed_list = [25 for x in range(0,20000)]
    pickle.dump(speed_list,file)
    for i in range(0,300):
        pickle.dump(speed_list,file)

write_test()

print('OK!')
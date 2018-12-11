import cPickle as pickle
import os
import time


speed=pickle.load(open("data_400/speed.dat","rb"))

501=pickle.load(open("data_400/5_0.1_pre_speed.dat","rb"))

1001=pickle.load(open('data_400/10_0.1_pre_speed.dat','rb'))

print('OK!')
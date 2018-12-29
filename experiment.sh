#!/bin/bash


data_path=data_400/
R_time_unit=120
P_time_unit=80
num=20


python init_road.py $num $R_time_unit
python RSA.py $data_path 0 399
python GA.py $data_path 0 399


for((i=1;i<=10;i++));  
do   
python predict.py $data_path $P_time_unit



cd $data_path
rm -rf *e.dat *pre_speed.dat
cd ..
echo $i
done

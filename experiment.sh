#!/bin/bash


data_path=data_400/
time_unit=60
num=20


python init_road.py $num $time_unit 



for((i=1;i<=10;i++));  
do   
python predict.py $data_path $time_unit

python RSA.py $data_path 0 19 380 399 210

cd $data_path
rm -rf *e.dat *pre_speed.dat
cd ..
echo $i
done
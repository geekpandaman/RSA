#!/bin/bash


data_path=data_3600/
time_unit=180
num=60


python init_road.py $num $time_unit 



for((i=1;i<=1000;i++));  
do   
python predict.py $data_path $time_unit

python RSA.py $data_path 0 59 3540 3599 1830

cd $data_path
rm -rf *e.dat *pre_speed.dat
cd ..
echo $i
done

#! /bin/bash

mkdir raw_data_meteonet

cd raw_data_meteonet

wget https://meteonet.umr-cnrm.fr/dataset/data/SE/ground_stations/SE_ground_stations_2016.tar.gz
tar -xf SE_ground_stations_2016.tar.gz
rm SE_ground_stations_2016.tar.gz

wget https://meteonet.umr-cnrm.fr/dataset/data/SE/ground_stations/SE_ground_stations_2017.tar.gz
tar -xf SE_ground_stations_2017.tar.gz
rm SE_ground_stations_2017.tar.gz

wget https://meteonet.umr-cnrm.fr/dataset/data/SE/ground_stations/SE_ground_stations_2018.tar.gz
tar -xf SE_ground_stations_2018.tar.gz
rm SE_ground_stations_2018.tar.gz

cd ../

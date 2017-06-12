#!/bin/bash
pip3 install virtualenv
rm -rf .venv
virtualenv -p python3 .venv
source .venv/bin/activate
pip3 install awsebcli
pip3 install bs4
pip3 install django
pip3 install jupyter
pip3 install matplotlib
pip3 install nba_py
pip3 install numpy
pip3 install pandas
pip3 install pprint
pip3 install psycopg2
pip3 install pymongo
pip3 install requests
pip3 install seaborn
pip3 install sklearn
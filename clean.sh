#!/bin/sh

#export LC_ALL=en_US.UTF-8
#export LANG=en_US.UTF-8

input_file=$1
output_file=$2

#/opt/python-3.6/bin/virtualenv --system-site-packages venv

#source venv/bin/activate

python3 ./clean.py $input_file $output_file

#deactivate

#rm -rf venv

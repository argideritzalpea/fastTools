#!/bin/sh

train_file=$1
test_file=$2

cat $train_file | sed 's/^\(.*\)\,.*$/\1/' > trainIDfile
cat $test_file | sed 's/^\(.*\)\,.*$/\1/' > testIDfile

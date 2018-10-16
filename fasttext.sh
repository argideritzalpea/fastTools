#!/bin/sh

FTprogram=$1
input_file=$2
output_file=$3
predict_file=$4
test_file=$5
bin='.bin'
model_input=$output_file$bin
echo $model_input

#$FTprogram supervised -input $input_file -output $output_file -epoch 150 -dim 300 -wordNgrams 2 -pretrainedVectors /home2/haberc/tmp/Habes/Env/wiki-news-300d-1M.vec 

$FTprogram supervised -input $input_file -output $output_file -epoch 400 -dim 300 -lr .08 -pretrainedVectors /home2/haberc/tmp/Habes/Env/bahamas_clean_tok.vec

#$FTprogram supervised -input $input_file -output $output_file -epoch 10

$FTprogram predict $model_input $test_file > $predict_file 


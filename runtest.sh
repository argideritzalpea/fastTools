#!/bin/sh

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

/opt/python-3.6/bin/virtualenv --system-site-packages venv

source venv/bin/activate
cat training_data_extra_sort.txt | sed 's/^\(.*\)\,.*$/\1/' > trainIDfile
cat ../carib_test.txt | sed 's/^\(.*\)\,.*$/\1/' > testIDfile
python3 tdidf_svm_classify.py training_data_extra_sort.txt ../carib_test.txt 21 __label__snorkel

#python3 ./ft_cv.py bahamas_rando_CH.txt 5 reeftags /opt/fastText

deactivate

rm -rf venv

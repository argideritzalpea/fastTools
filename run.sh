#!/bin/sh

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

/opt/python-3.6/bin/virtualenv --system-site-packages venv

source venv/bin/activate

#cat training_data_extra_sort.txt | sed 's/^\(.*\)\,.*$/\1/' > trainIDfile
#cat ../caribbean_20180501.txt | sed 's/^\(.*\)\,.*$/\1/' > testIDfile

#python3 tdidf_svm.py leave_return_test_formatted.txt 0 __label__R
#python3 tdidf_svm.py leave_return_test_formatted.txt 0 __label__L

#python3 tdidf_svm_classify.py training_data_extra_sort.txt ../caribbean_20180501.txt 21 __label__no_reef
#python3 tdidf_svm_classify.py training_data_extra_sort.txt ../caribbean_20180501.txt 21 __label__reef_adj
#python3 tdidf_svm_classify.py training_data_extra_sort.txt ../caribbean_20180501.txt 21 __label__on_reef

python3 ./ft_cv.py leave_return_test_formatted.txt 5 LRtags /opt/fastText

deactivate

rm -rf venv

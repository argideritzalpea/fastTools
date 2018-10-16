#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 11:56:12 2018

@author: Chris
"""

# Accepts a training set as input

# Splits it up into K sets, creates folders for each

# follows process for each

# averages at end
import os
import sys
import numpy as np
import subprocess

oldstdout = sys.stdout

train_file = sys.argv[1]
training_data = open(sys.argv[1], 'r').read().split('\n')
K = sys.argv[2]
tagfile = sys.argv[3]
FTfolder = sys.argv[4]

training_data = [x for x in training_data if x != '']

divided_data = np.array_split(training_data, int(K))
divided_data = [list(x) for x in divided_data]

results_dir = train_file + '_results'
try:
    os.stat(results_dir)
except:
    os.mkdir(results_dir)

Kfolds = range(int(K))
for i in Kfolds:
    kdir = str(i+1)
    try:
        os.stat(kdir)
    except:
        os.mkdir(kdir)
    trainname = str(i+1) + '_train.vec'
    testname = str(i+1) + '_test.vec'
    trainloc = kdir + '/' + trainname
    testloc = kdir + '/' + testname
    testloctok = kdir + '/' + testname + '.tok'
    sys.stdout = open(trainloc, 'w')
    for index in Kfolds:
        if index != i:
            for vec in divided_data[index]:
                print(vec)
    sys.stdout = open(testloc, 'w')
    for vectest in divided_data[i]:
        print(vectest)
    sys.stdout.close()
    tagloc = tagfile
    tokfolder = kdir + '/binarized'
    subprocess.check_call(['./tag.py', trainloc, tagloc, trainname, str(i+1), '1'])
    subprocess.check_call(['./tag.py', testloc, tagloc, testname, str(i+1), '0'])
    subprocess.check_call(['./ft_models.py', FTfolder, tokfolder, testloc])
    predictfolder = tokfolder + '/predict'
    resultsloc = kdir + '/results'
    subprocess.check_call(['./evaluate.py', testloctok, predictfolder, resultsloc])

sys.stdout = oldstdout



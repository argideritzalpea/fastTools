#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 14:22:25 2018

@author: Chris Haberland
University of Washington
"""

import sys
import subprocess
import os

FTfolder = sys.argv[1]
tok_folder = sys.argv[2]
test_file = sys.argv[3]

FTprogram = FTfolder + '/fasttext'

for filename in os.listdir(tok_folder):
    modelspath = './' + tok_folder + '/models/'
    predictpath = './' + tok_folder + '/predict/'
    inputpath = tok_folder + '/' + filename
    title = filename.split('.txt')[0]
    modelname = title + '.model'
    predictname = title + '.pred'
    outputpath = modelspath + modelname
    predictoutputpath = predictpath + predictname
    if not os.path.exists(modelspath):
        os.makedirs(modelspath)
    if not os.path.exists(predictpath):
        os.makedirs(predictpath)
    if filename.startswith("__label__") and filename.endswith(".tok"):
        subprocess.check_call(['./fasttext.sh', FTprogram, inputpath, outputpath, predictoutputpath, test_file])
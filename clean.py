#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 14:22:25 2018

@author: Chris Haberland
University of Washington
"""

import sys
import re
import os
import string
from nltk.corpus import stopwords
from collections import OrderedDict
import nltk
import subprocess

inputfile = open(sys.argv[1], 'r').read()

stop_words = set(stopwords.words('english'))  # set of stop words
punctuation = set(string.punctuation)  # set of punctuation

sys.stdout = open(sys.argv[2], 'w')

subexes = ["s/’/'/g", "s/′/'/g", "s/''/ /g", "s/'/ ' /g", 's/“/"/g', 's/”/"/g', 's/"/ /g', "s/\\./ \\. /g", "s/<br \\/>/ /g", "s/, / , /g", "s/(/ ( /g", "s/)/ ) /g", "s/\\!/ \\! /g", "s/\\?/ \\? /g", "s/\\;/ /g", "s/\\:/ /g", "s/-/ - /g", "s/=/ /g", "s/=/ /g", "s/*/ /g", "s/|/ /g", "s/«/ /g"]

def __normalize_text(s):
    for subex in subexes:
        s = subprocess.check_output(['sed', subex], input=s.encode()).decode('utf-8')
    return s

def __spaces(s):
    return ' '.join(s.split('[^\S\n]'))

def __digits(s):
    return ''.join(filter(lambda c: not c.isdigit(), s))

def __stopwords(s):
    return ''.join(filter(lambda c: c not in stop_words, s))

def __punc(s):
    return ''.join(filter(lambda c: c not in punctuation, s))

def preproc(s):
    return __digits(__spaces(__normalize_text(s.lower())))
    #return __digits((__normalize_text(s.lower())))

def no_stop(s):
    return [word for word in s if word not in stop_words]

def no_punc(s):
    return [word for word in s if word not in punctuation]

def del_adj(s):
    postuples = nltk.pos_tag(s)
    return [tup[0] for tup in postuples if tup[1] != 'JJ']


tokenized_vectors = preproc(inputfile).split('\n')

for ind, vector in enumerate(tokenized_vectors[:-1]):
    #if vector != '':
        #vecsplit = vector.split()
        #vector = " ".join(filter(lambda x:x[0:9]!='__label__', vecsplit))
        #for label in docstruct[ind][1]:
        #    print(ont[str(label)], end=" ")
    print(' '.join(no_stop(vector.split())))

sys.stdout.close()

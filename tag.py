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

cwd = os.getcwd()

oldstdout = sys.stdout

inputfile = open(sys.argv[1], 'r')
original_language = open(sys.argv[1], 'r').read().split('\n')
#vectors = open(sys.argv[2], 'r').read().split('\n')
tagfile = open(sys.argv[2], 'r').read().split('\n')

stop_words = set(stopwords.words('english'))  # set of stop words
punctuation = set(string.punctuation)  # set of punctuation

try:
    kdir = sys.argv[4]
except:
    pass

try:
    trainswitch = sys.argv[5]
except:
    pass


categories = OrderedDict()
catlabels = OrderedDict()
revcat = OrderedDict()
subcategories = OrderedDict()
subcatlabels = OrderedDict()
revsub = OrderedDict()
cat2subcat = OrderedDict()
subcat2cat = OrderedDict()
all_labels = set()
currentcat = ''
for modelline in tagfile:
    if modelline != '':
        modelsplit = modelline.split()
        if modelsplit[0] == 'category':
            all_labels.add(modelsplit[2])
            categories[modelsplit[1]] = modelsplit[2]
            currentcat = modelsplit[1]
            revcat[modelsplit[2]] = [modelsplit[1]]
            label = ''
            for labelword in modelsplit[3:]:
                label += labelword + ' '
            catlabels[modelsplit[1]] = label
        else:
            all_labels.add(modelsplit[1])
            subcategories[modelsplit[0]] = modelsplit[1]
            revsub[modelsplit[1]] = [modelsplit[0]]
            cat2subcat.setdefault(currentcat, set())
            cat2subcat[currentcat].add(modelsplit[0])
            subcat2cat[modelsplit[0]] = currentcat
            label = ''
            for labelword in modelsplit[2:]:
                label += labelword + ' '
            subcatlabels[modelsplit[0]] = label
            

print('Begin tagging!')
print('')

def ontPrint():
    for cat in categories:
        print(cat, catlabels[cat])
        subcats = []
        for subcat in cat2subcat[cat]:
            subcats.append(subcat)
        subcats = sorted(subcats)
        for subcat in subcats:
            print('\t', subcat, subcatlabels[subcat])
        print('')

def tagsomething(line, docindex):
    breakindex = 0
    tags = set()
    if splitline[0][0:9] == "__label__":
        for x in splitline:
            if x[0:9] == "__label__":
                try:
                    tags.add(revsub[x][0])
                except:
                    pass
                try:
                    tags.add(revcat[x][0])
                except:
                    pass
    else:
        print('#####################')
        print('')
        print("Please tag document ", docindex, ":", sep='')
        print('')
        raw = input(original_language[docindex].split(',')[1]+'\n\nEnter tag(s): ')
        print('')
        if raw == "quit":
            breakindex = 1
            print("End of tagging session")
        elif raw == "'":
            ontPrint()
            tags, breakindex = tagsomething(line, docindex)
        else:
            rawtags = raw.split()
            if len(rawtags) == 0:
                print("Try again")
                tags, breakindex = tagsomething(line, docindex)
            elif len(rawtags) == 1:
                try:
                    tags.add(rawtags[0])
                    print('')
                except:
                    print("Error")
                    tags, breakindex = tagsomething(line, docindex)
            elif len(rawtags) > 1:
                try:
                    for cat in rawtags:
                        tags.add(cat)
                    print('')
                except:
                    print("input error")
                    tags, breakindex = tagsomething(line, docindex)
            invalids = set()
            for item in rawtags:
                if str(item) not in subcategories:
                    invalids.add(item)
            if len(invalids) > 0:
                print(invalids, " not instantiated in the ontology file")
                tags, breakindex = tagsomething(line, docindex)
    return tags, breakindex

docindex = 0
docstruct = OrderedDict()
continueind = 0
pastid = 0

for line in original_language:
    if line != '':
        if continueind == 0:
            firstsplit = line.split(',', 1)
            docid = firstsplit[0]
            rest = firstsplit[1]
            splitline = rest.split()
            line = " ".join(filter(lambda x:x[0:9]!='__label__', splitline))
            docstruct.setdefault(docindex, [])
            docstruct[docindex].append(line)
            taggedtags, breakindex = tagsomething(line, docindex)
            docstruct[docindex].append(taggedtags)
            docstruct[docindex].append(docid)
            #docstruct[docindex].append(original_language[docindex])
            if breakindex == 1:
                continueind = 1
        else:
            taggedtags = []
            docstruct.setdefault(docindex, [])
            docstruct[docindex].append(line)
            docstruct[docindex].append(taggedtags)
            pastid += 1
            #docstruct[docindex].append(original_language[docindex])
        docindex += 1

sys.stdout = oldstdout

submainpath = cwd + '/' + sys.argv[4] + '/' + sys.argv[3]
sys.stdout = open(submainpath, 'w')

for i in docstruct:
    vector = docstruct[i][0]
    try:
        docid = docstruct[i][2]
    except:
        docid = ''
    quicktags = " ".join([str(x) for x in docstruct[i][1]])
    quicktags = quicktags.split()
    taglabels = set()
    for x in quicktags:
        if x in subcategories:
            taglabels.add(subcategories[x])
            taglabels.add(categories[subcat2cat[x]])
    if "none" in taglabels:
        taglabels.remove("none")
    if docid != '':
        print(docid, end=',')
    for label in taglabels:
        print(label, end=" ")
    print(vector)


import subprocess

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

tokpath = sys.argv[3]+'.tok'
subpath = cwd + '/' + sys.argv[4] + '/' + tokpath
sys.stdout = open(subpath, 'w')

ont = dict(subcategories, **categories)
tokenized_vectors = preproc(inputfile.read()).split('\n')

for ind, vector in enumerate(tokenized_vectors):
    if vector != '':
        #vecsplit = vector.split()
        #vector = " ".join(filter(lambda x:x[0:9]!='__label__', vecsplit))
        #for label in docstruct[ind][1]:
        #    print(ont[str(label)], end=" ")
        print(' '.join(no_stop(vector.split()))[1:])

sys.stdout = oldstdout

if trainswitch == '1':
    binarizedpath = cwd + '/' + kdir + '/binarized/'
    if not os.path.exists(binarizedpath):
        os.makedirs(binarizedpath)
    
    for label in all_labels:
        arg = 's/' + label + '/IGJOJERGJOTYURREU/g'
        revarg = 's/IGJOJERGJOTYURREU/' + label + '/g'
        s = subprocess.check_output(['sed', arg], input=open(subpath, 'r').read(), universal_newlines=True)
        s = subprocess.check_output(['sed', 's/__label__[^ ]*//g'], input=s, universal_newlines=True)
        s = subprocess.check_output(['sed', "s/^[ \t]*//g"], input=s, universal_newlines=True)
        s = subprocess.check_output(['sed', revarg], input=s, universal_newlines=True)
        filepath = binarizedpath + label + '_' + tokpath
        sys.stdout = open(filepath,'w')
        s = s.split('\n')
        matchstring = label
        for line in s:
            if line != '':
                if re.match(matchstring, line):
                    print(line)
                else:
                    print('__label__none '+line)


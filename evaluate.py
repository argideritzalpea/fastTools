#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 15:35:14 2018

@author: Chris
"""
import sys
import os

inputfile = open(sys.argv[1], 'r')
predictfolder = sys.argv[2]
sys.stdout = open(sys.argv[3], 'w')

training_data = inputfile.read().split('\n')


labels = set()

gold_standard = {}
for index, line in enumerate(training_data):
    if line != '':
        gold_standard[index] = set()
        splitline = line.split()
        for token in splitline:
            if token.startswith('__label__'):
                gold_standard[index].add(token)
                labels.add(token)
            else:
                continue

predictions = {}
for filename in os.listdir(predictfolder):
    path = predictfolder + '/' + filename
    predictfile = open(path, 'r')
    prediction_data = predictfile.read().split('\n')
    for index, line in enumerate(prediction_data):
        if line != '':
            predictions.setdefault(index, set())
            if line != '__label__none':
                predictions[index].add(line)

evaluation = {}
for label in labels:
    evaluation.setdefault(label, {})
    positives = 0
    truepositives = 0
    relevant = 0
    index = 0
    retrieveddocs = set()
    relevantdocs = set()
    alldocs = len(gold_standard)
    truepos = 0
    trueneg = 0
    for gold, predict in zip(gold_standard, predictions):
        if label in gold_standard[gold]:
            relevantdocs.add(index)
            if label in predictions[predict]:
                retrieveddocs.add(index)
                truepos += 1
        else:
            if label in predictions[predict]:
                retrieveddocs.add(index)
            else:
                trueneg += 1
        index += 1
        #print(predictions[predict], gold_standard[gold])
    #print(label, relevantdocs, retrieveddocs)
    try:
        precision = (len(relevantdocs.intersection(retrieveddocs))/len(retrieveddocs))
    except:
        precision = 'error'
    try:
        recall = (len(relevantdocs.intersection(retrieveddocs))/len(relevantdocs))
    except:
        recall = 'error'
    try:
        f1 = 2*(precision*recall)/(precision+recall)
    except:
        f1 = 'error'
    try:
        acc = (truepos + trueneg)/alldocs
    except:
        acc = 'error'
    print(label)
    print('acc:', '{0:.3}'.format(acc), 'precision:', '{0:.3}'.format(precision), 'recall:', '{0:.3}'.format(recall), 'F:', '{0:.3}'.format(f1), sep="\t")
    print('')
import subprocess
import os
import sys

inputfile = open(sys.argv[1], 'r')

subexes = ["s/’/'/g", "s/′/'/g", "s/''/ /g", "s/'/ ' /g", 's/“/"/g', 's/”/"/g', 's/"/ /g', "s/\\./ \\. /g", "s/<br \\/>/ /g", "s/, / , /g", "s/(/ ( /g", "s/)/ ) /g", "s/\\!/ \\! /g", "s/\\?/ \\? /g", "s/\\;/ /g", "s/\\:/ /g", "s/-/ - /g", "s/=/ /g", "s/=/ /g", "s/*/ /g", "s/|/ /g", "s/«/ /g"]

def __normalize_text(s):
    for subex in subexes:
        s = subprocess.check_output(['sed', subex], input=s.encode()).decode('utf-8')
    return s

def __spaces(s):
    return ' '.join(s.split('[^\S\n]'))

def __digits(s):
    return ''.join(filter(lambda c: not c.isdigit(), s))

def preproc(s):
    #return __digits(__spaces(__normalize_text(s.lower())))
    return __digits((__normalize_text(s.lower())))



sys.stdout = open(sys.argv[2], 'w')

tokenized_vectors = preproc(inputfile.read()).split('\n')

for ind, vector in enumerate(tokenized_vectors):
    if vector != '':
        #vecsplit = vector.split()
        #vector = " ".join(filter(lambda x:x[0:9]!='__label__', vecsplit))
        #for label in docstruct[ind][1]:
        #    print(ont[str(label)], end=" ")
        print(' '.join(vector.split())[1:])
sys.stdout.close()

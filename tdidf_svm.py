from table_vectors import *
import sys

the_label_in_question = sys.argv[3]

with open(sys.argv[1],'r') as target_file:
    read_file = target_file.read()
    labs_to_index, index_to_labs = getUniqueLabels(read_file)
    data = makeCSVTable(read_file, labs_to_index)
    textdata = getTDIDFVecs(read_file)
    #print(data)

    for index in index_to_labs:
        data.rename(columns={data.columns[int(index)]: index_to_labs[index]}, inplace=True)
    
    #print(len(textdata))
    classifyData(the_label_in_question, data, textdata, int(sys.argv[2]))
    getGrams(the_label_in_question)
#for colname in data.columns:
#    print(colname)

    #print(textdata)

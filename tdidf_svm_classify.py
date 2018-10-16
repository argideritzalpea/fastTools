from table_vectors import *
import sys

the_label_in_question = sys.argv[4]

with open(sys.argv[1],'r') as train_file, open(sys.argv[2]) as test_file:
    read_file_train = train_file.read()
    read_file_test = test_file.read()
    labs_to_index, index_to_labs = getUniqueLabels(read_file_train)
    data = makeCSVTable(read_file_train, labs_to_index)
    traindata = getTDIDFVecs(read_file_train)
    testdata = getTDIDFVecs(read_file_test)

    for index in index_to_labs:
        data.rename(columns={data.columns[int(index)]: index_to_labs[index]}, inplace=True)
    
    preds = testSVM(the_label_in_question, data, traindata, testdata, int(sys.argv[3]))
    setup = {'pred':preds, 'docs':testdata}
    df = pd.DataFrame(data=setup)
    
    import os
    if not os.path.exists('output_pkls'):
        os.makedirs('output_pkls')
    
    df.to_pickle('output_pkls/'+the_label_in_question + '.pkl')
    print(df)

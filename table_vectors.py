import sys
import re
import pandas as pd
import numpy as np
import subprocess
import csv
from multiscorer import MultiScorer
from sklearn.metrics import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score

def getUniqueLabels(a_vector_file):
    raw_text_vectors = a_vector_file
    unique_labels = set(re.findall("__label__\w*", raw_text_vectors))
    label_lookup = {}
    ind_lookup = {}
    for ind, label in enumerate(unique_labels):
        label_lookup[label] = ind
        ind_lookup[ind] = label
    return label_lookup, ind_lookup

def makeCSVTable(read_vectors, lookup):
    text = read_vectors.split('\n')[:-1]
    label_table = np.zeros([len(text),len(lookup)])
    for label in lookup:
        for ind, line in enumerate(text):
            if re.search(label, line):
                label_table[ind, lookup[label]] = 1
            else:
                label_table[ind, lookup[label]] = 0
    panda_table = pd.DataFrame(label_table)
    return panda_table

def getIDs(a_vector_file):
    text = a_vector_file
    # text is a string
    print(text)
    s = subprocess.check_output(['sed', 's/^\(.*\)\,.*$/\1/'], input=text, universal_newlines=True)
    print(s)
    print(type(s))
    with open('the_ids', 'w') as the_file:
        the_file.write(s)
        pandas_vec = pd.DataFrame(s)
    return pandas_vec[0]

def getTDIDFVecs(a_vector_file):
    text = a_vector_file
    ids = []
    for line in text.split('\n'):
        if line != '':
            ID = line.split(',')[0]
            ids.append(int(ID))
    panda_id = pd.DataFrame(ids)[0]
    s = subprocess.check_output(['sed', 's/__label__[^ ]*//g'], input=text, universal_newlines=True)
    x = re.sub('\d*, *', '', s)
    with open('rawvec', 'w') as the_file:
        the_file.write(x)
    subprocess.check_call(['./clean.sh', 'rawvec','tokvec'])
    with open('tokvec') as thefile:
        reread = thefile.read().split('\n')[:-1]
        pandas_vec = pd.DataFrame(reread)
        pandas_vec.index = panda_id
    print(panda_id)
    print(pandas_vec[0])
    return pandas_vec[0]

def classifyData(label, binarydata, textvec, cutoff):
    models = [RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
    LinearSVC(),
    MultinomialNB(),
    LogisticRegression(random_state=0)]
    
    binarydata['category_id'] = binarydata[label].factorize()[0]
    from io import StringIO
    category_id_df = binarydata[[label, 'category_id']].drop_duplicates().sort_values('category_id')
    category_to_id = dict(category_id_df.values)
    id_to_category = dict(category_id_df[['category_id', label]].values)    

    CV = 5
    X_train, X_test, y_train, y_test = train_test_split(textvec, binarydata[label], random_state = 0)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=cutoff, encoding='latin-1', ngram_range=(1, 2))
    features = tfidf.fit_transform(textvec).toarray()

    labels = binarydata['category_id']
    cv_df = pd.DataFrame(index=range(CV * len(models)))
    entries = []
    #print(features, labels)
    for model in models:
        scorer = MultiScorer({'F-measure': (f1_score, {'pos_label':1, 'average':'binary'}),'Accuracy' : (accuracy_score, {}),'Precision' : (precision_score, {'average':'binary'}), 'Recall' : (recall_score, {'average':'binary'})})
        model_name = model.__class__.__name__
        cross_val_score(model, features, labels, scoring=scorer, cv=CV)
        results = scorer.get_results()
        print(model_name)
        for metric_name in results.keys():
            average_score = np.average(results[metric_name])
            print('%s : %f' % (metric_name, average_score))

    '''
    cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
    cv_df.groupby('model_name').accuracy.mean()

    X_train, X_test, y_train, y_test = train_test_split(textvec, binarydata[label], random_state = 0)
    count_vec = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = MultinomialNB().fit(X_train_tfidf, y_train)
    print(cv_df.groupby('model_name').accuracy.mean())
    '''

    model = LinearSVC()

    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, binarydata.index, test_size=0.33, random_state=0)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    from sklearn.feature_selection import chi2

    N = 10
    for Product, category_id in sorted(category_to_id.items()):
        print(Product, category_id)
        indices = np.argsort(model.coef_[int(category_id)])
        feature_names = np.array(tfidf.get_feature_names())[indices]
        unigrams = [v for v in reversed(feature_names) if len(v.split(' ')) == 1][:N]
        bigrams = [v for v in reversed(feature_names) if len(v.split(' ')) == 2][:N]
        print("# '{}':".format(Product))
        print("  . Top unigrams:\n       . {}".format('\n       . '.join(unigrams)))
        print("  . Top bigrams:\n       . {}".format('\n       . '.join(bigrams)))

def testSVM(label, binarydata, train, test, cutoff):
    model = LinearSVC()
    binarydata['category_id'] = binarydata[label].factorize()[0]
    category_id_df = binarydata[[label, 'category_id']].drop_duplicates().sort_values('category_id')
    category_to_id = dict(category_id_df.values)
    id_to_category = dict(category_id_df[['category_id', label]].values)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=cutoff, encoding='latin-1', ngram_range=(1, 2)) 
    features = tfidf.fit_transform(train).toarray()

    labels = binarydata['category_id']
    
    X_test_tfidf = tfidf.transform(test).toarray()

    model.fit(features, labels)
    y_pred = model.predict(X_test_tfidf)

    return y_pred

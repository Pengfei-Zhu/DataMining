#encoding=utf-8

import sys
import os
import warnings
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.datasets import fetch_20newsgroups
from TextPreprocess import TextPreprocess

reload(sys)

warnings.filterwarnings('ignore')

n_samples=2000
n_features=1000
n_top_words=20

#导入语料集
corpus_set=TextPreprocess()
corpus_set.wordbag_path='text_corpus2_wordbag/'
corpus_set.trainset_name='trainset.dat'
corpus_set.stopword_path='extra_dict/hlt_stop_words.txt'

stpwrdlst=corpus_set.getStopword(corpus_set.stopword_path)

corpus_set.load_trainset()
clusters=len(corpus_set.data_set.target_name)
print '共',clusters,'种类别',corpus_set.data_set.target_name

for i in range(0,clusters-1):
    findx=corpus_set.data_set.label.index(i)
    counts=corpus_set.data_set.label.count(i)
    lindx=findx+counts-1
    
    vectorizer=TfidfVectorizer(max_df=0.95,min_df=2,max_features=n_features,stop_words=stpwrdlst)
    tfidf=vectorizer.fit_transform(corpus_set.data_set.contents[findx:lindx])
    nmf=NMF(n_components=1,random_state=1).fit(tfidf)
    
    feature_names=vectorizer.get_feature_names()
    
    print 'topic',corpus_set.data_set.target_name[i]
    print ' '.join([feature_names[i] for i in nmf.components_[0].argsort()[:-n_top_words - 1:-1]])
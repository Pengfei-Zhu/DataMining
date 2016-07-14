#encoding=utf-8

import sys
import os
import numpy as np

from sklearn.datasets.base import Bunch

import pickle

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from TextPreprocess import TextPreprocess

#����svm
from sklearn.svm import LinearSVC

from text_mining import calculate_accurate,calculate_result

reload(sys)

testsamp=TextPreprocess()
testsamp.corpus_path='test_corpus2_small/'
testsamp.pos_path='test_corpus2_pos/'

testsamp.preprocess()

testsamp.segment_path='test_corpus2_segment/'
testsamp.stopword_path='extra_dict/hlt_stop_words.txt'

testsamp.segment()

category=os.listdir(testsamp.segment_path)
random_index=2
actual=[]

test_path=testsamp.segment_path+category[random_index]+'/'
test_data=[]
file_list=os.listdir(test_path)
for file_path in file_list:
    file_name=test_path+file_path
    file_obj=open(file_name,'rb')
    test_data.append(file_obj.read())
    actual.append(random_index)
    file_obj.close()
    
stpwrdlst=testsamp.getStopword(testsamp.stopword_path)


train_set=TextPreprocess()
train_set.wordbag_path='text_corpus2_wordbag/'
train_set.wordbag_name='wordbag.dat'
train_set.load_wordbag()
print train_set.wordbag.tdm.shape


fea_test=testsamp.tfidf_value(test_data, stpwrdlst, train_set.wordbag.vocabulary)
print fea_test.shape

#应用linear_svm算法    输入词袋向量和分类标签

svclf=LinearSVC(penalty='11',dual=False,tol=1e-4)
svclf.fit(train_set.wordbag.tdm,train_set.wordbag.label)

predicted=svclf.predict(fea_test)

for file_name,expct_cate in zip(file_list,predicted):
    print "测试语料文件名:",file_name,": 实际类别:",category[random_index],"<-->预测类别:",train_set.wordbag.target_name[expct_cate]


actual=np.array(actual)

calculate_accurate(actual, predicted)
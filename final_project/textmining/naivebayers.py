# encoding=utf-8

import sys
import os
import numpy as np


from sklearn.datasets.base import Bunch



import pickle
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from TextPreprocess import TextPreprocess

#导入多项式贝叶斯算法
from sklearn.naive_bayes import MultinomialNB
from text_mining import calculate_accurate

reload(sys)

# 测试语料预处理
testsamp=TextPreprocess()

testsamp.corpus_path='test_corpus2_small/' 
testsamp.pos_path='test_corpus2_pos/'  

# 测试语料预处理
testsamp.preprocess()

testsamp.segment_path='test_corpus2_segment/'
testsamp.stopword_path='extra_dict/hlt_stop_words.txt'
# 为测试语料分词
testsamp.segment()

# 随机选择分好类的测试语料
category=os.listdir(testsamp.segment_path)
random_index=2
actual=[]
# 导入测试语料
test_path=testsamp.segment_path+category[random_index]+'/'
test_data=[]
file_list=os.listdir(test_path)

for file_path in file_list:
    file_name=test_path+file_path
    file_obj=open(file_name,'rb')
    test_data.append(file_obj.read())
    actual.append(random_index)
    file_obj.close()
    
#对测试文本进行tf-idf计算

stpwrdlst=testsamp.getStopword(testsamp.stopword_path)

#导入训练词袋模型
train_set=TextPreprocess()
train_set.wordbag_path='text_corpus2_wordbag/'
train_set.wordbag_name='wordbag.dat'
train_set.load_wordbag()
print train_set.wordbag.tdm.shape

#使用tfidfvectorizer初始化测试语料

fea_test=testsamp.tfidf_value(test_data, stpwrdlst, train_set.wordbag.vocabulary)
print fea_test.shape

#应用朴素贝叶斯算法
clf=MultinomialNB(alpha=0.001).fit(train_set.wordbag.tdm,train_set.wordbag.label)

#预测分类结果
predicted=clf.predict(fea_test)
for file_name,expct_cate in zip(file_list,predicted):
    print '测试语料文件名：',file_name,'实际类别：',category[random_index],'预测类别：',train_set.wordbag.target_name[expct_cate]
    
actual=np.array(actual)
calculate_accurate(actual, predicted)
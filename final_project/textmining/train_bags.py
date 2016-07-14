#encoding=utf-8
import sys
import os


from sklearn.datasets.base import Bunch

import pickle
import jieba

from sklearn.feature_extraction.text import HashingVectorizer

reload(sys)


corpus_path='text_corpus_segment'+'/'

wordbag_path='text_corpus1_wordbag'+'/'


data_set=Bunch(target_name=[],label=[],filenames=[],contents=[])


dir_list=os.listdir(corpus_path)
data_set.target_name=dir_list


for mydir in dir_list:
    class_path=corpus_path+'/' 
    file_list=os.listdir(class_path) 
    for file_path in file_list:
        file_name=class_path+file_path
        data_set.filenames.append(file_name)
        data_set.label.append(data_set.target_name.index(mydir))
        file_read=open(file_name,'rb')
        seg_corpus=file_read.read()
        data_set.contents.append(seg_corpus)
        file_read.close()
        

file_obj=open(wordbag_path+'train_set.data','wb')
pickle.dump(data_set,file_obj)
file_obj.close()
file_obj=open(wordbag_path+'train_set.data','rb')
data_set={}


data_set=pickle.load(file_obj)
file_obj.close()


print data_set.target_name

print len(data_set.label)

print len(data_set.contents)
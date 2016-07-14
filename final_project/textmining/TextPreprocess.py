#encoding=utf-8

import sys
import os
import jieba

#引入bunch类
from sklearn.datasets.base import Bunch

#引入持久化类

import pickle

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

reload(sys)

#文本预处理类

class TextPreprocess:
    #定义词袋对象data_set，bunch类提供一种key,value的对象形式
    #target_name所有分类集名称雷彪
    #label:每个文件的分类标签列表
    #filenames：文件名称
    #contents:文件内容
    data_set=Bunch(target_name=[],label=[],filenames=[],contents=[])
    wordbag=Bunch(target_name=[],label=[],filenames=[],tdm=[],vocabulary=[])
    def __init__(self):
        self.corpus_path=''  #原始语料路径
        self.pos_path=''     #预处理后语料路径
        self.segment_path='' #分词后语料路径
        self.wordbag_path='' #词袋模型路径
        self.stopword_path=''#停用词表路径
        self.trainset_name=''#训练集文件名
        self.wordbag_name=''#词包文件名
        
    #对输入语料进行基本预处理，删除语料的换行符，并持久化
    #处理后在pos_path下建立与corpus_path相同的子目录和文件结构
    
    def preprocess(self):
        if(self.corpus_path=='' or self.pos_path==''):
            print 'corpus_path或pos_path不能为空'
            return
        
        dir_list=os.listdir(self.corpus_path)
        
        for mydir in dir_list:
            class_path=self.corpus_path+mydir+'/'
            file_list=os.listdir(class_path)
            for file_path in file_list:
                file_name=class_path+file_path
                file_read=open(file_name,'rb')
                raw_corpus=file_read.read()
                
                #按行切分字符串为一个数组
                corpus_array=raw_corpus.splitlines()
                raw_corpus=''
                for line in corpus_array:
                    line=line.strip()
                    
                    raw_corpus=self.custom_pruneLine(line,raw_corpus)
                    
                #拼出分词后语料分类目录
                
                pos_dir=self.pos_path+mydir+'/'
                if not os.path.exists(pos_dir):
                    os.mkdir(pos_dir)
                    
                file_write=open(pos_dir+file_path,'wb')
                file_write.write(raw_corpus)
                
                file_write.close()
                file_read.close()
                
        print '中文语料修改处理成功'
        
    #对行的简单修建
    def simple_pruneLine(self,line,raw_corpus):
        if line !='':
            raw_corpus+=line
        return raw_corpus
    
    #自定义行处理
    
    def custom_pruneLine(self,line,raw_corpus):
        
        if line.find('【 日  期 】')!=-1:
            line=''
        elif line.find('【 版  号 】')!=-1:
            line=''
        elif line.find('【 作  者 】')!=-1:
            line=''
        elif line.find('【 正  文 】')!=-1:
            line=''
        elif line.find('【 标  题 】')!=-1:
            line=''
        
        if line !='':
            raw_corpus+=line
            
        return raw_corpus
    
    #对预处理后的语料进行分词，并持久化
    #处理后在segment_path下建立与pos_path相同的子目录和文件结构
    
    def segment(self):
        if(self.segment_path=='' or self.pos_path==''):
            print 'segment_path或pos_path不能为空'
            return
        
        dir_list=os.listdir(self.pos_path)
        
        for mydir in dir_list:
            class_path=self.pos_path+mydir+'/'
            file_list=os.listdir(class_path)
            for file_path in file_list:
                file_name=class_path+file_path
                file_read=open(file_name,'rb')
                raw_corpus=file_read.read()
                seg_corpus=jieba.cut(raw_corpus)
                
                seg_dir=self.segment_path+mydir+'/'
                if not os.path.exists(seg_dir):
                    os.makedirs(seg_dir)
                    
                file_write=open(seg_dir+file_path,'wb')
                file_write.write(' '.join(seg_corpus).encode('utf-8'))
                
                file_read.close()
                file_write.close()
                
        print '中文语料分词成功完成'
        
    #打包分词后训练语料
    def train_bag(self):
        if(self.segment_path=='' or self.wordbag_path=='' or self.trainset_name==''):
            print '不能为空'
            return
        
        #获取corpus_path下的所有子分类
        dir_list=os.listdir(self.segment_path)
        self.data_set.target_name=dir_list
        
        for mydir in dir_list:
            class_path=self.segment_path+mydir+'/'
            file_list=os.listdir(class_path)
            for file_path in file_list:
                file_name=class_path+file_path
                self.data_set.filenames.append(file_name)
                self.data_set.label.append(self.data_set.target_name.index(mydir))
                
                file_read=open(file_name,'rb')
                seg_corpus=file_read.read()
                self.data_set.contents.append(seg_corpus)
                file_read.close()
                
        #词袋对象持久化
        file_obj=open(self.wordbag_path+self.trainset_name,'wb')
        pickle.dump(self.data_set,file_obj)
        file_obj.close()
        print '分词语料打包完成'
        
    #计算训练语料的tfidf权值并持久化为词袋
    def tfidf_bag(self):
        if(self.wordbag_path=='' or self.wordbag_name=='' or self.stopword_path==''):
            print '不能为空'
            return
        
        #读取持久化后的训练集对象
        
        file_obj=open(self.wordbag_path+self.trainset_name,'rb')
        self.data_set=pickle.load(file_obj)
        file_obj.close()
        
        #定义词袋数据结构：tdm:tf-idf计算后词袋
        
        self.wordbag.target_name=self.data_set.target_name
        self.wordbag.label=self.data_set.label
        self.wordbag.filenames=self.data_set.filenames
        
        #构建语料
        corpus=self.data_set.contents
        stpwrdlst=self.getStopword(self.stopword_path)
        #使用tfidfvectorizer初始化向量空间模型--创建词袋
        vectorizer=TfidfVectorizer(stop_words=stpwrdlst,sublinear_tf=True,max_df=0.5)
        
        #统计每个词语的tf-idf权值
        transformer=TfidfTransformer()
        
        #文本转为词频矩阵
        self.wordbag.tdm=vectorizer.fit_transform(corpus)
        
        #保存词袋词典文件
        self.wordbag.vocabulary=vectorizer.vocabulary_
        
        #创建词袋的持久化
        file_obj=open(self.wordbag_path+self.wordbag_name,'wb')
        pickle.dump(self.wordbag,file_obj)
        file_obj.close()
        print 'tf-idf词袋创建成功'
        
    #导入获取停用词表
    def getStopword(self,stopword_path):
        stpwrd_dic=open(stopword_path,'rb')
        stpwrd_content=stpwrd_dic.read()
        #将停用词表转换为list
        stpwrdlst=stpwrd_content.splitlines()
        stpwrd_dic.close()
        return stpwrdlst
    
    #验证持久化结果
    def verify_trainset(self):
        file_obj=open(self.wordbag_path+self.trainset_name,'rb')
        
        self.data_set=pickle.load(file_obj)
        file_obj.close()
        
        #输出数据集包含的所有类别
        print self.data_set.target_name
        #输出数据集包含的类别标签数
        print len(self.data_set.label)
        #输出数据集包含的文件内容数
        print len(self.data_set.contents)
        
    def verify_wordbag(self):
        file_obj=open(self.wordbag_path+self.wordbag_name,'rb')
        #读取持久化后的对象
        self.wordbag=pickle.load(file_obj)
        file_obj.close()
        #输出数据集包含的所有类别
        print self.wordbag.target_name
        #输出数据集包含的类别标签数
        print len(self.wordbag.label)
        #输出数据集包含的文件内容数
        print self.wordbag.tdm.shape
        
    #进行tf-idf权值计算，myvocabulary导入的词典
    def tfidf_value(self,test_data,stpwrdlst,myvocabulary):
        vectorizer=TfidfVectorizer(vocabulary=myvocabulary)
        transformer=TfidfTransformer()
        return vectorizer.fit_transform(test_data)
    
    #导出词袋模型
    def load_wordbag(self):
        file_obj=open(self.wordbag_path+self.wordbag_name,'rb')
        self.wordbag=pickle.load(file_obj)
        file_obj.close()
        
    #导出训练语料集
    def load_trainset(self):
        file_obj=open(self.wordbag_path+self.trainset_name,'rb')
        self.data_set=pickle.load(file_obj)
        file_obj.close()
        
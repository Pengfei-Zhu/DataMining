#encoding=utf-8
import sys
import os
import jieba

reload(sys)

corpus_path='text_corpus_small'+'/'

seg_path='text_corpus_segment'+'/'

dir_list=os.listdir(corpus_path)

for mydir in dir_list:
    class_path=corpus_path+mydir+'/'
    file_list=os.listdir(class_path)
    for file_path in file_list:
        file_name=class_path+file_path
        file_read=open(file_name,'rb')
        raw_corpus=file_read.read()
        seg_corpus=jieba.cut(raw_corpus)
        
        seg_dir=seg_path+mydir+'/'
        if not os.path.exists(seg_dir):
            os.makedirs(seg_dir)
        file_write=open(seg_dir+file_path,'wb')
        
        file_write.write(' '.join(seg_corpus).encode('utf-8'))
        file_read.close()
        file_write.close()
print '中文语料分词成功完成'
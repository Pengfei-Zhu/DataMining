#encoding=utf-8

import sys
import os
from TextPreprocess import TextPreprocess

reload(sys)

tp=TextPreprocess()
tp.corpus_path='text_corpus2_small/'
tp.pos_path='text_corpus2_pos/'
tp.segment_path='text_corpus2_segment/'
tp.wordbag_path='text_corpus2_wordbag/'
tp.stopword_path='extra_dict/hlt_stop_words.txt'
tp.trainset_name='trainset.dat'
tp.wordbag_name='wordbag.dat'

tp.preprocess()
tp.segment()
tp.train_bag()
tp.tfidf_bag()
tp.verify_trainset()
tp.verify_wordbag()
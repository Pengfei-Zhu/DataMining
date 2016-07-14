# -*- coding: utf-8 -*-

import sys
import os
import warnings
import numpy as np

from sklearn import metrics

warnings.filterwarnings('ignore')

def calculate_accurate(actual,predict):
    m_precision=metrics.accuracy_score(actual,predict)
    print '结果计算'
    print '精度:{0:.3f}'.format(m_precision) 
#召回，精度，f1测试

def calculate_result(actual,predict):
    m_precision=metrics.precision_score(actual,predict)
    m_recall=metrics.recall_score(actual,predict)
    
    print '结果计算'
    print '精度:{0:.3f}'.format(m_precision)
    print '召回:{0:0.3f}'.format(m_recall)  
    print 'f1-score:{0:.3f}'.format(metrics.f1_score(actual,predict))
                                    

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 16:04:00 2015

@author: Mengxiang Chen
"""
from math import log, sqrt
def tf(text, featureWords):
#后面做了归一化，所以直接用词频计算就行了
    vec = [0.0 for i in range(len(featureWords))]
    for i in text:
        i = i.strip()
        if i in featureWords:
            vec[featureWords[i]]+= 1
            
    return vec
    
def idf(featureWordsCount, totalSamples, featureWords):
    vec = [0.0 for i in range(len(featureWords))]
    for k in featureWordsCount.keys():
        vec[featureWords[k]] = log(totalSamples/(featureWordsCount[k]+1))
    return vec
    
def normalize(vec):
    vec_mode = 0
    for i in range(len(vec)):
        vec_mode += vec[i]**2
        
    vec_mode = sqrt(vec_mode)
    if vec_mode == 0:
        return vec
    for i in range(len(vec)):
        vec[i] /= vec_mode
    
    return vec
def feature_vector_calculate(tfV, idfV):

    vec = [0.0 for i in range(len(tfV))]
    for i in range(len(tfV)):
        vec[i] = tfV[i]*idfV[i]
    
    vec = normalize(vec)
    return vec
    
def global_count(featureWords, inputFile, labelSplitTag, strSplitTag):
    ifile = open(inputFile, 'r', encoding='utf-8')
    featureWordsCount = dict()
        
    totalSamples = 0
    
    for line in ifile:
        totalSamples += 1
        line = line.strip().split(labelSplitTag)
        label = int(line[0])
        line = line[1]
        line = line.strip().split(strSplitTag)
        for word in line:
            if word in featureWords:
                if word in featureWordsCount:
                    featureWordsCount[word] += 1
                else:
                    featureWordsCount[word] = 1
    
    return featureWordsCount, totalSamples
    
    
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 19:56:05 2015

@author: Mengxiang Chen
"""


def build_dict(stopwordsFile, inputFile, labelSplitTag, strSplitTag):
    ifile = open(inputFile, 'r', encoding='utf-8')
    stopwords = set()
    if (len(stopwordsFile)):
        sf = open(stopwordsFile, 'r')
        for l in sf:
            l = l.strip().split('\t')
            for i in l:
                sf.add(i)
    
    wordsClassCount = dict()
    classCount = dict()
    totalSamples = 0
    
    for line in ifile:
        line = line.strip().split(labelSplitTag)
        label = int(line[0])
        totalSamples += 1
        if label in classCount:
            classCount[label] += 1
        else:
            classCount[label] = 1
        line = line[1]
        line = line.strip().split(strSplitTag)
        sample_dict = set() #save all valid words in this sample
        for word in line:
            word = word.strip()
            if word in stopwords:
                continue

            if len(word) < 2:
                continue
            sample_dict.add(word)
        #count all word in this sample
        for word in sample_dict:
            if not word in wordsClassCount:
                wordsClassCount[word] = dict()
            if not label in wordsClassCount[word]:
                wordsClassCount[word][label] = 1
            else:
                wordsClassCount[word][label] += 1
       
    #set other word-label pair to zero
    for word in wordsClassCount.keys():
        for label in classCount.keys():
            if not label in wordsClassCount[word]:
                wordsClassCount[word][label] = 0
    return wordsClassCount, classCount, totalSamples

def chi_select(wordsClassCount, classCount, ratio):
    
    featureWordsCount = dict()
    
    wordsCount = dict()
    for word in wordsClassCount.keys():
        wordsCount[word] = sum(wordsClassCount[word].values())
        
    totalSamples = sum(classCount.values())
    
    for label in classCount.keys():
        #save the chi value of this word for this class
        wordsChiValue = dict()
        for word in wordsClassCount.keys():

            A = float(wordsClassCount[word][label])
            B = float(wordsCount[word] - A)
            C = float(classCount[label] - A)
            D = float(totalSamples - A - B - C);
            if (A+B)*(C+D) == 0:
                wordsChiValue[word] = 0.0
            else:
                wordsChiValue[word] = (A*D-B*C)**2/((A+B)*(C+D))
        
        sortedChi = sorted(wordsChiValue.items(), key = lambda x:x[1], reverse=True)
        #note that after sorted, sortedChi is a list with (k,v) as elements, not a dict
        sortedChi = sortedChi[0:int(len(sortedChi)*ratio)]
        for i in sortedChi:
            featureWordsCount[i[0]] = wordsCount[i[0]]
            
    featureWords = dict()
    i =0
    for k in featureWordsCount.keys():
        featureWords[k] = i
        i += 1
    #save for IDF calculation
    return featureWords
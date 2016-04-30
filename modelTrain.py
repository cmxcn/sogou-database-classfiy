# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 20:42:02 2015

@author: Mengxiang Chen
"""
from featureSelection import *
from weightCalculation import *

def write_feature_vector(outFile, fv, label):
    outFile.write('{0}'.format(label))
    allZero = True
    for i in range(len(fv)):
        if fv[i] == 0:
            continue
        outFile.write('\t{0}:{1}'.format(i+1, fv[i]))
        allZero = False
    
    if allZero:
        outFile.write('\t1:0.0')
    outFile.write('\n')

def write_dict(dictFile, featureWords):
    dFile = open(dictFile, 'w')
    sortedDict = sorted(featureWords.items(), key = lambda x:x[1])
    for i in sortedDict:
        dFile.write('{0}\t{1}\n'.format(i[0], i[1]))

def read_dict(dictFile):
    dictFile = open(dictFile, 'r')
    featureWords = dict()
    for line in dictFile:
        line = line.strip().split('\t')
        featureWords[line[0]] = int(line[1])
    
    return featureWords


def build_feature_dict(inputFile, dictFile, stopwordsFile, labelSplitTag, strSplitTag):
    wordsClassCount, classCount, totalSamples = build_dict(stopwordsFile, inputFile, labelSplitTag, strSplitTag)
    featureWords = chi_select(wordsClassCount, classCount, 0.3)
    write_dict(dictFile, featureWords)
    return featureWords
    


def build_svm_sample(featureWords, inputFile, outputFile, labelSplitTag, strSplitTag):
    
    featureWordsCount, totalSamples = global_count(featureWords, inputFile, labelSplitTag, strSplitTag)
   # print(len(featureWords))
    idfV = idf(featureWordsCount, totalSamples, featureWords)
    
    
   # print(idfV)
    iFile = open(inputFile, 'r', encoding='utf-8')
    oFile = open(outputFile, 'w')


    for l in iFile:
        l = l.strip().split(labelSplitTag)
        label = int(l[0])
        l = l[1]
        l = l.strip().split(strSplitTag)
        tfV = tf(l, featureWords)
        print(len(l))
        fv = feature_vector_calculate(tfV, idfV)
        write_feature_vector(oFile, fv, label)
        
    oFile.close()
    
def build_train_samples(inputFile, outputFile, dictFile, stopwordsFile, labelSplitTag, strSplitTag):
    featureWords = build_feature_dict(inputFile, dictFile, stopwordsFile, labelSplitTag, strSplitTag)
    print('total feature words: {0}'.format(len(featureWords)))
    build_svm_sample(featureWords, inputFile, outputFile, labelSplitTag, strSplitTag)
    print('svm samples finished\n')

def build_test_samples(inputFile, outputFile, dictFile, labelSplitTag, strSplitTag):
    featureWords = read_dict(dictFile)
    build_svm_sample(featureWords, inputFile, outputFile, labelSplitTag, strSplitTag)
    
if __name__=='__main__':
    build_train_samples('binary_seged.train', 'btrain', 'bdict', '', '\t', '^')   
    build_test_samples('binary_seged.test', 'btest', 'bdict', '\t', '^')
    
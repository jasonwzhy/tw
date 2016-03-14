#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: model_base_dict.py
# Author: gaodengke
# mail: gaodengke@brandbigdata.com
# Created Time: 2016-02-25 10:35:40
#########################################################################
import re
import sys
#import json
from langconv import *
import jieba
import os
import sys
BASEDIR = os.path.dirname(__file__)

class TerrorModel(object):
    def __init__(self):
        '''
            初始化。
        '''
        self.filterPattern = re.compile(r'(）|（|》|《|】|【|­|‘|、|、|”|“|…|’|\!|\"|\#|\$|%|\&|\'|\(|\)|\*|\+|-|\.|/|:|;|<|=|>|\?|@|\[|\]|\^|_|\`|\{|\}|~|：)')
        self.sentencePunc = re.compile(r'(。|；|？|！)')
        #加载情感权重词典
        self.keyWord = {}
        fDict = open(BASEDIR+'/MyKeyWeightDict.txt')
        while(True):
            line = fDict.readline().strip()
            if not line:
                break
            element = line.split('\t')
            if not self.keyWord.has_key(element[0]):
                self.keyWord[element[0]] = float(element[1])
        fDict.close()
        #加载程度副词词典
        self.degreeWord = {}
        fDict = open(BASEDIR+'/MyDegreeDict.txt')
        while(True):
            line = fDict.readline().strip()
            if not line:
                break
            element = line.split('\t')
            if not self.degreeWord.has_key(element[0]):
                self.degreeWord[element[0]] = float(element[1])
        fDict.close()
        #加载否定词词典
        self.notWord = {}
        fDict = open(BASEDIR+'/MyNotDict.txt')
        while(True):
            line = fDict.readline().strip()
            if not line:
                break
            element = line.split('\t')
            if not self.notWord.has_key(element[0]):
                self.notWord[element[0]] = ''
        fDict.close()
        #加载自定义切词词典  
        jieba.load_userdict(BASEDIR+"/MyKeyDict.txt")
        #过滤后输出文本
        self.filterText = ''

    def precessData(self,line):
        ''' 
            筛选语料。
        '''
        markLen = len('"text":')
        if not line:
            return ''
        #extract text
        begin = line.find('"text":')
        if begin == -1:
            return ''
        begin += markLen
        end = line.find(',"userid":')
        if end != -1:
            line = line[begin:end]
        else:
            end = line.find('"userid":')
            if end != -1:
                line = line[begin:end]
            else:
                line = line[begin:]

        end = line.find('https://')
        if end != -1:
            line = line[:end]
        else:
            end = line.find('http://')
            if end != -1:
                line = line[:end]

        self.filterText = line.replace('\n','') 
        return line

    def getElementTrendency(self,element):
        '''
            计算单位意群的倾向。
        '''
        #结果
        result = 0.0
        #非中文过滤
        element = self.isUstr(element.decode('utf-8'))
        #空字符及全数字字符过滤
        if (not element) or element.isdigit():
            return result
        #print '<element>=',element
        #转换繁体到简体  
        element = Converter('zh-hans').convert(element)  
        element = element.encode('utf-8')
        #分词
        segList = jieba.cut(element)
        segTemp = "\t".join(segList).encode('utf-8')
        segList = segTemp.split('\t')
        #意群的倾向计算。
        segPos = 0
        lastSegPos = 0
        partTrendency = 1.0
        for w in segList:
            #print w
            if self.keyWord.has_key(w):
                partTrendency = 1.0
                segPos = segList.index(w)
                i=segPos-1
                while i >= lastSegPos:
                    if self.degreeWord.has_key(segList[i]):
                        partTrendency *= self.degreeWord[segList[i]]
                        #print '<partTrendency>=',partTrendency
                        if (i>1) and self.notWord.has_key(segList[i-1]):
                            partTrendency *= 0.5
                            i = i-2
                        else:
                            i = i-1
#                    elif self.notWord.has_key(segList[i]):
#                        partTrendency *= -1.0
#                        i = i-1
                    else:
                        i = i-1
                partTrendency *= self.keyWord[w]
                lastSegPos = segPos-1
                result += partTrendency
        return result

    def isUstr(self,in_str):
        '''
            过滤非中文。
        '''
        out_str=''
        for i in range(len(in_str)):
            if self.isUchar(in_str[i]):
                out_str=out_str+in_str[i]
            else:
                out_str=out_str+''
        return out_str
    
    def isUchar(self,uchar):
        '''
            字符过滤检测。
        '''
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
        """判断一个unicode是否是数字"""
        if uchar >= u'\u0030' and uchar<=u'\u0039':
            return True        
#        """判断一个unicode是否是英文字母"""
#        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
#            return True
#       if uchar in ('-',',','，','。','.','>','?'):
#            return True
        return False
    
    #推文接口
    def getPaperTrendency(self,line):
        '''
            计算每篇文章的倾向。
        '''
        #print line
        #过滤预处理
        line = self.precessData(line)
        line = line.replace(';','；')
        line = line.replace('?','？')
        line = line.replace('!','！')
        line = line.replace(',','，')
        #print '<line>=',line
        #中间变量
        paragraphNum = 0
        sentenceNum = 0
        paragraphTrendency = 0.0
        sentenceTrendency = 0.0
        elementTrendency = 0.0
        #结果
        paperTrendency = 0.0
        #计算
        #print line
        paragraphList = line.split('\n')
        #print '!!',len(paragraphList)
        paragraphFilterList = []
        for paragraph in paragraphList:
            #print paragraph
            paragraph = self.filterPattern.sub('',paragraph).strip()
            #print '<paragraph>=',paragraph
            paragraph = paragraph.replace(' ','')
            paragraph = paragraph.replace('\t','')
            if paragraph:
                paragraphFilterList.append(paragraph)
        paragraphNum = len(paragraphFilterList)
        #print '<paragraphNum>=',paragraphNum
        for paragraph in paragraphFilterList:
            paragraphTrendency = 0.0
            sentenceList = self.sentencePunc.split(paragraph)
            sentenceFilterList = []
            for sentence in sentenceList:
                if (not self.sentencePunc.match(sentence)) and sentence:
                    sentenceFilterList.append(sentence)
            sentenceNum = len(sentenceFilterList)
            for sentence in sentenceFilterList:
                #print '<sentence>=',sentence
                sentenceTrendency = 0.0
                elementList = sentence.split('，')
                for element in elementList:
                    #print '<element>=',element
                    elementTrendency = self.getElementTrendency(element)
                    sentenceTrendency += elementTrendency
                #print '<sentenceTrendency>=',sentenceTrendency/sentenceNum
                paragraphTrendency += sentenceTrendency/sentenceNum
            #print '<sentenceNum>=',sentenceNum
            paperTrendency += paragraphTrendency/paragraphNum
            paperTrendency = min(paperTrendency,1.0)
            paperTrendency = max(0.0,paperTrendency)
        return paperTrendency

    #用户接口
    def getPersonTerrorTendency(self,tendencyList):
        ''' 
            以人为单位计算情感倾向。
        '''
#        total =  len(tendency_list)
#        sum_tendency = 0.0 
#        nzero_tendency = 0 
#        for line in tendencyList:
#            tendency = float(line)
#            if tendency:
#                sum_tendency += tendency
#                nzero_tendency += 1
#        average = sum_tendency/total
#        res_tendency = average*(nzero_tendency**0.5)
#        res_tendency = min(res_tendency,1.0)
        res_tendency = max(tendencyList)
        res_tendency = min(res_tendency,1.0)
        res_tendency = max(0.0,res_tendency)
        return res_tendency

    def main(self):
        '''
            处理总接口。
        '''
        result = 0.0
        for line in sys.stdin:
            if not line:
                break
            result = self.getPaperTrendency(line)
            #print result,":",line.replace('\n','')
            print result,":",self.filterText
                    


if __name__=="__main__":
    reload(sys)
    # sys.setdefaultencoding('utf-8')
    sys.setdefaultencoding('utf8')
    obj = TerrorModel()
    # obj.main()
    print obj.getPersonTerrorTendency([0/10.0,2/10.0,9/10.0,1/10.0,2/10.0])

#!/usr/bin/env python
#-*-coding:utf-8 -*-
# author:shiran time:2018-1-22
import csv
import json
# import pandas as pd
# import sys
# import collections
# import re
def format():#主要用于数据文件的格式化，去掉数据文件中可能存在的回车
    with open('./s_paper.csv', "r+", encoding='utf-8') as raw:
        with open('./s_paper1.csv', "w+", encoding='utf-8') as result:
            line = raw.readline()
            next_line = raw.readline()
            while (next_line != ''):
                line = next_line
                next_line = raw.readline()
                while (re.match(re.compile('^[1-9]'), next_line) == None and next_line != ''):
                    line = line.replace('\n', '') + next_line
                    next_line = raw.readline()
                    print(line)
                    print(next_line)
                result.write(line)

def TransPaper(file1,file2):#论文数据解析
    global authornum
    jsonData = open(file1,'r',encoding='utf-8')
    csvfile = open(file2, 'w+', newline='',encoding='utf-8')
    data = {}
    writer = csv.writer(csvfile)
    keys=['id','title','entities','year','journalName','doi']    # 定义文件的待谢属性
    for dic in jsonData:  # 读取json数据的每一行，将values数据一次一行的写入csv中
        dic = json.loads(dic[0:])
        for key in keys:
            if key in keys:
                if(dic.get(key)):
                   data[key] = str(dic.get(key)).replace("\n"," ")#替换掉结尾的回车符
                else:
                    data[key]="null"
        writer.writerow([data['id'],data['title'],data['entities'],data['year'],data['journalName'],data['doi']])
    jsonData.close()
    csvfile.close()


def TransRelationship(file1,file2):#关系解析
    jsonData = open(file1, 'r', encoding='utf-8')
    csvfile2 = open(file2, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile2)
    #keys=['s_id','e_id','pro']
    #writer.writerow(keys)
    rela={}#定义一个字典，存放每一条数据
    for dic in jsonData:  # 读取json数据的每一行，将values数据一次一行的写入csv中
        dic = json.loads(dic[0:])
        templist_out=dic.get('outCitations')#提取每条数据的outcitation属性
        if(templist_out):
            for cite_id in templist_out:#遍历给键赋上对应的值
                rela['s_id'] = dic.get('id')
                rela['e_id'] = cite_id
                rela['pro'] = "cites"
                # writer.writerow([rela['s_id'], rela['e_id'], rela['pro']])
                sets.add(str(rela))#将每条数据放入集合中，避免出现重复
    for r in (sets):#遍历集合，依次写回
        c_r=eval(r)
        writer.writerow([c_r['s_id'], c_r['e_id'], c_r['pro']])
    jsonData.close()
    csvfile2.close()

def TransAuthor(file1,file2):#作者解析
    global num
    global noidnum

    jsonData = open(file1, 'r', encoding='utf-8')
    csvfile1 = open(file2, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvfile1)
    keys = ['author_id', 'name']
    # writer.writerow(keys)
    for dic in jsonData:  # 读取json数据的每一行，将values数据一次一行的写入csv中
        dic = json.loads(dic[0:])
        templist=dic.get('authors')#获取每条数据的authors属性，存放至列表
        if(templist):
            for a in templist:
                data = {}
                data['name']=a.get('name')
                if len(a.get('ids'))>1:#统计有多个id的作者有多少
                    print(len(a.get('ids')))
                    num+=1
                    data['author_id'] = str(a.get('ids')[0]).replace("\n", " ")
                elif len(a.get('ids'))==1:#有多个或者一个id的都选用第一个id作为该作者的id
                    data['author_id'] = str(a.get('ids')[0]).replace("\n", " ")
                else:#没有id的，计数赋给id
                    noidnum=noidnum+1
                    continue
                writer.writerow([data['author_id'],data['name']])
    jsonData.close()
    csvfile1.close()

def TransAuthorPaperRela(file1,file2):#关系解析
    jsonData = open(file1, 'r', encoding='utf-8')
    csvfile2 = open(file2, 'w+', newline='', encoding='utf-8')
    writer = csv.writer(csvfile2)
    keys=['au_id','paper_id','pro']
    #writer.writerow(keys)
    rela={}
    for dic in jsonData:  # 读取json数据的每一行，将values数据一次一行的写入csv中
        dic = json.loads(dic[0:])
        templist=dic.get('authors')#获取该篇文章所有的作者
        if(templist):
            for au in templist:#将该篇文章与每个作者对应写回文件
                if(len(au.get('ids'))==0):
                    continue
                else:
                    rela['paper_id'] = dic.get('id')
                    rela['au_id'] = str(au.get('ids')[0])
                    rela['pro'] = "writes"
                writer.writerow([rela['au_id'], rela['paper_id'], rela['pro']])
    jsonData.close()
    csvfile2.close()

import os
num=0#有多个id的作者数量
noidnum=0#没有id的作者数量
path = os.path.abspath("/data/corpus_sr/dataset1/")#存放数据文件的路径
#print(path)
for root, dirs, files in os.walk(path):
    #print(path)
    for file in files:
        data_file = path + '/' + file
        csv_file_paper="/data/corpus_sr/dataset_new/papers/"+file+"_paper.csv"
        # print(data_file)
        # print(csv_file_paper)
        TransPaper(data_file,csv_file_paper)
        csv_file_au="/data/corpus_sr/dataset_new/authors/" +file+"_au.csv"
        # print(data_file)
        # print(csv_file_au)
        TransAuthor(data_file,csv_file_au)
        # print(num)
        # print(noidnum)
        csv_file_r = "/data/corpus_sr/dataset_new/AuthorPaper/" + file + "_AuPaper.csv"
        # print(data_file)
        # print(csv_file_r)
        TransAuthorPaperRela(data_file, csv_file_r)




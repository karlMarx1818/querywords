# coding=utf-8
import requests
import csv
import time
class Dictionary:
    def __init__(self):
        self.url_head = 'http://dict.youdao.com/app/baidu/search?q='
        self.flags=('<li><span class=\'title\'>', '</span><p>', '</p></li>')

    #<li><span class="title">Uranus</span><p>乌拉诺斯 | 天神</p></li>
    #网页源代码格式为  <li><span class="title">英文</span><p>中文</p></li>
    #有三个特征元素
    
    def get_requests_context(self, word):#爬取网页源代码
        url = self.url_head + word
        r = requests.get(url)
        return r.text   #string

    def query_word(self, word):#查询单个单词的释义
        text = self.get_requests_context(word)#网页源代码
        head = text.find(self.flags[0])
        if head == -1:  #未找到特征一，非正常网页，未收录单词
            return word, '未收录'
        #str.find(str, beg=0, end=len(string))  return 起始下标 或-1
        head = text.find(self.flags[1], head) + len(self.flags[1])#中文起始位置
        tail = text.find(self.flags[2])#中文结束位置+1
        return word, text[head:tail]#截取字符串的左闭右开区间

    def query_words(self, words):#查询words中的所有单词并将结果存在results中
        results = list()    
        for word in words:
            results.append(self.query_word(word))#查询当前单词并将结果添加至results末尾
        return results
        #string results[N][2]

    def query_from_file(self, file_name):
        words = list()  #待查询单词的列表，从in中逐行读入;string words[N]
        with open(file_name, 'r') as file:
            word = file.readline()
            while word:
                words.append(word.strip('\n'))
                word = file.readline()
        return self.query_words(words)
 #str.strip('chars') :
        #i=0     while( str[i] in chars) del str[i++]
        #i=len-1 while( str[i] in chars) del str[i--]
    def many_query_from_console(self):
        words = list()
        word = input()
        while word!="-1":
            words.append(word.strip('\n'))
            word = input()
        return self.query_words(words)

    def query_from_console(self):
        word=input()
        return self.query_word(word)

if __name__ == "__main__":
    dic = Dictionary()
    print("select mode:\n0:console I/O   1:many console I/O   2:txt I/O   3:csv")
    mode=int(input())
    if(mode==2):
        results = dic.query_from_file('in.txt')
        with open('out.txt', 'w') as file:
            for result in results:
                file.write("{:16}{}\n".format(result[0],result[1]))

    elif(mode==0) :
        with open('cache.txt', 'a+') as file:
            file.write('\n'+chr(9608)+chr(9608)+chr(9608)+chr(9608)+chr(9608))
            file.write(time.strftime('%Y-%m-%d %H:%M:%S\n',time.localtime(time.time()))) 
            while 1:
                result=dic.query_from_console()
                print(result[1])
                file.write("{:16}{}\n".format(result[0],result[1]))
    elif(mode==3):
        results = dic.query_from_file('in.txt')
        with open('out.csv','a',newline='') as file:
            file_csv=csv.writer(file)
            #for result in results:
            file_csv.writerows(results)

    else :
        results = dic.many_query_from_console()
        with open('cache.txt', 'a+') as file:
            file.write('\n'+chr(9608)+chr(9608)+chr(9608)+chr(9608)+chr(9608))
            file.write(time.strftime('%Y-%m-%d %H:%M:%S\n',time.localtime(time.time()))) 
            for result in results:
                print("{:16}{}".format(result[0],result[1]))
                file.write("{:16}{}\n".format(result[0],result[1]))
        mode=input()
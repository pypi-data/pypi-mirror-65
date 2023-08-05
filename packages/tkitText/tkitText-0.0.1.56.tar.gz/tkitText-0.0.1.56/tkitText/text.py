# -*- coding: utf-8 -*-
# 对文件进行预处理
import re
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from readability import Document
import html2text

from harvesttext.resources import get_qh_typed_words,get_baidu_stopwords
from harvesttext import loadHT,saveHT
from harvesttext import HarvestText
from tqdm import tqdm
import  hashlib

from fuzzywuzzy import fuzz
# from fuzzywuzzy import process

import regex as re


import jieba.analyse
import gc
class Text:
    """
    文本处理函数



    """
    def __init__(self,ht_model=None):
        self.ht_model=ht_model
        pass
    def __del__(self):
        # print("释放Text()")
        try:
           del self.ht_model
        except:
            pass
       
    def md5(self,string):
        # 对要加密的字符串进行指定编码
        string = string.encode(encoding ='UTF-8')
        # md5加密
        # print(hashlib.md5(string))
        # 将md5 加密结果转字符串显示
        string = hashlib.md5(string).hexdigest()
        # print(string)
        return string
    def filterPunctuation(self,x):
        """
        中文标点替换为英文标点
        """
        x = re.sub(r'[‘’]', "'", x)
        x = re.sub(r'[“”]', '"', x)
        x = re.sub(r'[…]', '...', x)
        x = re.sub(r'[—]', '-', x)
        x = re.sub(r"&nbsp", "", x)
        return x
    def auto_find(self, stringA, stringB,ftype='start'):
        """
        自动搜索开始或者结尾
        ftype='start'  或者end
        """


        for i in range(0,len(stringB)):
            # print('i',i)
            
            if ftype=='start':
                f_r=1
                if len(stringB)-i==1:
                    # print("取值",0)
                    find_w=stringB[0]
                else:
                    # print("取值",(1*(f_r-1),len(stringB)-i-1)*f_r)
                    find_w=stringB[1*(f_r-1):(len(stringB)-i)*f_r]
                n=stringA.find(find_w)
                # print('find_w',find_w)
            else:
                f_r=-1
 
                # print('stringB[f_r]',stringB[f_r])
                if len(stringB)-i==1:
                    # print("取值",-1)
                    find_w=stringB[-1]
                else:
                    # print("取值",((len(stringB)-i)*f_r,1*(f_r)))
                    find_w=stringB[(len(stringB)-i)*f_r::]
                # print('stringB[f_r]',stringB[f_r])
                # print('find_w',find_w)

            n=stringA.find(find_w)
            # print('n',n)
            
            if n!=-1:
                pass
                # # print(find_w)
                if ftype=='start':
                    # print("开始结束")
                    return n
                else:
                    return n+len(find_w) #预测结尾时候加上词长度
                
            
        

    def find_match(self,a,b):
        """
        搜索一个相似的文本
        从a中搜索b
        """  
        print(b)
        find_b=a.find(b)
        if find_b==-1:
            start=self.auto_find(a,b,'start')
            # exit()
            end=self.auto_find(a,b,'end')
            if start !=None and end !=None:
                c=a[start:end]
                f=fuzz.partial_ratio(b,c)
                # print(f)
                return c,f
        else: 
            c=a[find_b:find_b+len(b)]
            # print(c)
            # print(find_b)
            # print(len(b))
            # f=fuzz.partial_ratio(c,b)
            # print(f)
            # if f==100:
            return c,100


        # # f=fuzz.partial_ratio(a,b)
        # start=a.find(b[1:3])
        # end=a.find(b[-3:-1])
        # c=a[start:end]
        # f=fuzz.partial_ratio(c,b)
        # # print(f)
        # return c,f

    # a="嘉朵能够帮助或带领丹恩·萧完成许多事，如逛商店；牠在完成一天的工作后便待在马厩里"
    # b="帮助或带领丹恩"
    # c=find_match(a,b)
    # print(c)
    def load_ht(self,ht_model=None):
        """
        加载模型

        """
        if ht_model== None:
            pass
        else:
            self.ht_model=ht_model
        if self.ht_model == None:
            self.ht = HarvestText()        
        else:
            self.ht = loadHT(self.ht_model)

    def save_ht(self,ht_model=None):
        """
        保存模型
        >>>  
        """
     
        # self.ht.add_new_words(new_words)

        if ht_model== None:
            pass
            # print("模型保存",self.ht_model)
        else:
            self.ht_model=ht_model
        saveHT(self.ht,self.ht_model)
        print("模型保存",self.ht_model)  
    
    # for span, entity in t.ht.entity_linking(text):
    # 	print(span, entity)
    def release(self):
        """
        释放模型
        """
        del self
        gc.collect()
        pass

    def named_entity_recognition(self,text):
        """
        识别文字中的实体
        """
        self.clear(text)
        entity_type_dict={}
        for word,tag0 in self.ht.posseg(text):
            # 三种前缀代表：人名（nr），地名（ns），机构名（nt）
            # print(x)
            # tag0 = str(x.nature)
            # print(word,tag0)
            if tag0.startswith("nr"):
                entity_type_dict[word] = "人名"
            elif tag0.startswith("ns"):
                entity_type_dict[word] = "地名"
            elif tag0.startswith("nt"):
                entity_type_dict[word] = "机构名"
            elif tag0.startswith("nz"):
                entity_type_dict[word] = "其他专名"
            elif tag0.startswith("动物"):
                entity_type_dict[word] = "动物"
        
        # print(entity_type_dict)
        return entity_type_dict
    def typed_words(self,ht_model=None):
        """
        添加类型词
        >>> add_words(new_words,path)
        """
        # print("进行新词发现")
        # max_len=10000
        typed_words, stopwords = get_qh_typed_words(), get_baidu_stopwords()
        self.ht.add_typed_words(typed_words)
        # self.ht.add_new_words(new_words)
        self.save_ht(ht_model)            
    def add_entity(self,words,ht_model=None):
        """
        添加类型词
        words=[("词语",'类型')]
        """
        for word,type0 in words:
           tt.ht.add_new_entity(word, type0=type0)  # 作为特定类型登录
        self.save_ht(ht_model)
    def add_words(self,new_words=[],ht_model=None):
        """
        添加新词
        >>> add_words(new_words,path)
        """
        # print("进行新词发现")
        # max_len=10000
        # typed_words, stopwords = get_qh_typed_words(), get_baidu_stopwords()
        # self.ht.add_typed_words(typed_words)
        self.ht.add_new_words(new_words)
        self.save_ht(ht_model)
    
    # def add_typed_words(self,new_words=[],ht_model=None):
    #     """
    #     添加新词
    #     >>> add_words(new_words,path)
    #     """
     
    #     # self.ht.add_new_words(new_words)

    #     # if ht_model== None:
    #     #     pass
    #     #     # print("模型保存",self.ht_model)
    #     # else:
    #     #     self.ht_model=ht_model
    #     # saveHT(self.ht,self.ht_model)
    #     # print("模型保存",self.ht_model)   
 
    def find_new_words(self,text):
        """
        新词发现函数


        >>> find_new_words(text,path)
        """
        print("进行新词发现")
        max_len=10000
        typed_words, stopwords = get_qh_typed_words(), get_baidu_stopwords()
        self.ht.add_typed_words(typed_words)
        #返回关于新词质量的一系列信息，允许手工改进筛选(pd.DataFrame型)
        for i in tqdm(range(len(text)//max_len+1)):
                #截取内容
                # one.append(text[i*max_len:(i+1)*max_len]+"")
                b=text[i*max_len:(i+1)*max_len]
                if len(b)>10:
                    new_words_info=self.ht.word_discover(b)
                    new_words=new_words_info.index.tolist()
                    # print(new_words)
                    print("新词数量",len(new_words))
                    words=self.ht.seg(b)
                    for word in new_words:
                        if word in words:
                            new_words.remove(word)
                    print(new_words)
                    print("去重复后数量",len(new_words))    
                    self.ht.add_new_words(new_words)
                    saveHT(self.ht,self.ht_model)
        # # new_words_info = self.ht.word_discover(text)
        # #new_words_info = ht.word_discover(para, threshold_seeds=["武磊"])  
        # new_words = new_words_info.index.tolist()
        # # print(new_words)
        # print("新词数量",len(new_words))
        saveHT(self.ht,self.ht_model)
        print("模型保存",self.ht_model)
    # 遍历目录文件夹
    def sentence_segmentation_v1(self,para):
        """分句函数
        进行精细中文分句（基于正则表达式）

        >>> sentence_segmentation_v1(text)

        """
        para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
        para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
        para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
        para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        para = para.rstrip()  # 段尾如果有多余的\n就去掉它
        # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
        seg=para.split("\n")

        while '' in seg:
            seg.remove('')
        return seg

    def sentence_segmentation(self, text):
        """
        句子分割函数

        包括 (。|！|\!|\.|？|\?)

        >>> sentence_segmentation("这里似乎内.容不给")
        >>> ['法院经审理查明，被告人陈淑惠在担任银川市兴庆区委副书记、区长，灵武市委副书记、代市长、市长期间，利用职务上的便利，在工程款拨付、项目审批等方面为他人谋取利益，先后非法收受他人财物折合人民币546万余元、英镑2万元、美元3万元', '法院认为，被告人陈淑惠身为国家工作人员，利用职务之便，为他人谋取利益，非法收受他人财物数额特别巨大，其行为已构成受贿罪', '陈淑惠到案后，如实交代了监察机关尚未掌握的其他绝大部分受贿犯罪事实', '在案发前，陈淑惠主动向部分行贿人退赃158万元，案发后积极退缴剩余全部赃款', '在检察机关审查起诉及法院审理期间，陈淑惠认罪认罚，确有悔罪表现，应当从轻处罚', '综上，法院以被告人陈淑惠犯受贿罪判处其有期徒刑10年，并处罚金人民币60万元，受贿违法所得财物依法予以没收，上缴国库', '据公开简历，陈淑惠出生于1963年5月，2009年11月至2012年5月，曾任灵武市市长', '2018年10月，陈淑惠被查', '“政事儿”注意到，陈淑惠曾经的搭档市委书记李建军于今年5月被宣布调查', '李建军也是陈淑惠的前任灵武市长', '2009年1月至2009年11月，李建军任职了10个月的灵武市长就升任市委书记，接任灵武市长的正是陈淑惠，此后两人党政班子搭档了两年时间']


        """
        #sentences = re.split('(。|！|\!|\.|？|\?|\：|\:|\?)',string)
        #分句函数
        tr4w = TextRank4Keyword()

        tr4w.analyze(text=text, lower=True, window=2)
        return tr4w.sentences
        # sentences = re.split('(。|！|\!|\.|？|\?)',string)         # 保留分割符

        # new_sents = []
        # for i in range(int(len(sentences)/2)):
        #     sent = sentences[2*i] + sentences[2*i+1]
        #     new_sents.append(sent)

        # return new_sents
    def participle(self, text,dotype='words_no_filter'):
        """
        分词函数
        指出过滤停用词 提取核心关键词
        dotype 可选参数：
            words_no_filter：对sentences中每个句子分词而得到的两级列表。
            words_no_stop_words：去掉words_no_filter中的停止词而得到的二维列表。
            words_all_filters：保留words_no_stop_words中指定词性的单词而得到的二维列表。

        >>> participle(text,dotype='words_no_filter')
        >>> [['李建军', '任职', '了', '10', '个', '月', '的', '灵武', '市长', '就', '升任', '市委书记', '接任', '灵武', '市长', '的', '正是', '陈', '淑惠']]




        """
        tr4w = TextRank4Keyword()
        tr4w.analyze(text=text, lower=True, window=2)
        if dotype=='words_no_stop_words':
            return tr4w.words_no_stop_words
        if dotype=='words_all_filters':
            return tr4w.words_all_filters
        return tr4w.words_no_filter

    def html_text(self,html):
        """从html中提取正文

        >>> html_text(html)


        """
        # response = requests.get(url)
        # logging.info(response.text)
        # html = request.urlopen(url)

        # logging.info(html)

        doc = Document(html)
        # doc = Document(html)
        # logging.info(doc.title())
        try:
          html= doc.summary(True)
        except:
          return ''
        #   logging.info(doc.get_clean_html())
        # t =html2text.html2text(html)
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.bypass_tables = False
        text_maker.ignore_images = True
        text_maker.images_to_alt = True
        # html = function_to_get_some_html()
        text = text_maker.handle(html)
        text=self.remove_HTML_tag('img',text)
        # print(text)
        return text
    def remove_HTML_tag(self,tag, string):
        """删除特定的标签

        # 删除掉图片
        >>> tag ='img'
        >>> string ='''
          萌照镇楼。\n

          <img data-rawwidth="1393" data-rawheight="1104"
          src="https://pic3.zhimg.com/50/63f68657ef2e5c22fef8b982a141cfd0_hd.jpg"
          class="origin_image zh-lightbox-thumb" width="1393" data-
          original="https://pic3.zhimg.com/63f68657ef2e5c22fef8b982a141cfd0_r.jpg"/>

          母犬发情期的主要特征：

          '''

        >>> remove_HTML_tag(tag, string)

        """
        string = re.sub(r"<\b(" + tag + r")\b[^>]*>", r"", string)
        return re.sub(r"<\/\b(" + tag + r")\b[^>]*>", r"", string)
    def filter_tags(self, htmlstr):
        """清理掉html代码

        >>> filter_tags(htmlstr)


        """
        re_doctype = re.compile('<![DOCTYPE|doctype].*>')
        re_nav = re.compile('<nav.+</nav>')
        re_cdata = re.compile('//<!\[CDATA\[.*//\]\]>', re.DOTALL)
        re_script = re.compile(
            '<\s*script[^>]*>.*?<\s*/\s*script\s*>', re.DOTALL | re.I)
        re_style = re.compile(
            '<\s*style[^>]*>.*?<\s*/\s*style\s*>', re.DOTALL | re.I)
        re_textarea = re.compile(
            '<\s*textarea[^>]*>.*?<\s*/\s*textarea\s*>', re.DOTALL | re.I)
        re_br = re.compile('<br\s*?/?>')
        re_h = re.compile('</?\w+.*?>', re.DOTALL)
        re_comment = re.compile('<!--.*?-->', re.DOTALL)
        re_space = re.compile(' +')
        s = re_cdata.sub('', htmlstr)
        s = re_doctype.sub('',s)
        s = re_nav.sub('', s)
        s = re_script.sub('', s)
        s = re_style.sub('', s)
        s = re_textarea.sub('', s)
        s = re_br.sub('', s)
        s = re_h.sub('', s)
        s = re_comment.sub('', s)
        s = re.sub('\\t', '', s)
        s = re_space.sub(' ', s)
        s = self.replaceCharEntity(s)
        return s
    def remove_word_wrap(self,html):
        """删除多余的换行

        """
        nt =  re.sub('[\n]+', '\n', html)
        return nt
    # def clear(self, string):
    #     """清理多余空格

    #     清理多余的换行空格等

    #     >>> clear('这里似乎内\t容不给')

    #     """

    #     # return string.strip()
    #     # for line in string.readlines():
    #     # string = re.sub('[\n]+', '\n', string)
    #     string = string.replace('\n', '').replace(
    #         '\n\n', '\n').replace('\r\n', '\n').replace('   ', '\n')
    #     # string = string.replace('\n\n', ' ').replace('\n', '')
    #     string = re.sub(' +', ' ', string)
    #     return string
    # 清理多余的换行空格等
    def clear(self, string):
        """清理多余空格

        清理多余的换行空格等

        >>> clear('这里似乎内\t容不给')

        """

        # return string.strip()
        # for line in string.readlines():
        # string = re.sub('[\n]+', '\n', string)
        string = string.replace('\n', '').replace(
            '\n\n', '\n').replace('\r\n', '\n').replace('   ', '\n')
        # string = string.replace('\n\n', ' ').replace('\n', '')
        string = re.sub(' +', ' ', string)
        return string
    def summary(self, text,num=10):
        """获取文本的摘要

        >>> summary( text,num=10)
        >>> [{'index': 0, 'sentence': '法院经审理查明，被告人陈淑惠在担任银川市兴庆区委副书记、区长，灵武市委副书记、代市长、市长期间，利用职务上的便利，在工程款拨付、项目审批等方面为他人谋取利益，先后非法收受他人财物折合人民币546万余元、英镑2万元、美元3万元', 'weight': 0.12558810530050332}, {'index': 1, 'sentence': '法院认为，被告人陈淑惠身为国家工作人员，利用职务之便，为他人谋取利益，非法收受他人财物数额特别巨大，其行为已构成受贿罪', 'weight': 0.11183996893770527}, {'index': 10, 'sentence': '2009年1月至2009年11月，李建军任职了10个月的灵武市长就升任市委书记，接任灵武市长的正是陈淑惠，此后两人党政班子搭档了两年时间', 'weight': 0.10833734824662838}]


        """
        tr4s = TextRank4Sentence()
        tr4s.analyze(text=text, lower=True, source = 'all_filters')
        # print(tr4s.get_key_sentences(num=3))
        return tr4s.get_key_sentences(num=num)

        # return data
    def get_keywords(self, text,num=10):
        """获取文本的关键词
        https://github.com/napoler/TextRank4ZH

        >>> get_keywords( text,num=10)
        >>> [{'word': '淑惠', 'weight': 0.03249010309710726}, {'word': '法院', 'weight': 0.02192152416206948}, {'word': '灵武', 'weight': 0.021869542539628625}, {'word': '李建军', 'weight': 0.019213098969148662}, {'word': '人财物', 'weight': 0.01856601133033217}, {'word': '市长', 'weight': 0.017907055156049748}, {'word': '市委书记', 'weight': 0.017755388969961372}, {'word': '被告人', 'weight': 0.016851090405232656}, {'word': '受贿罪', 'weight': 0.016218911983344443}, {'word': '行贿人', 'weight': 0.015739567821084217}]

        """
        tr4w = TextRank4Keyword()

        tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
        return tr4w.get_keywords(num, word_min_len=2)
        # return data
    # jieba分词器通过词频获取关键词
    def jieba_keywords(self,text,num=10):
        # keywords = jieba.analyse.extract_tags(text, topK=10)
        keywords = jieba.analyse.textrank(text, topK=10, allowPOS=('ns', 'n', 'vn', 'v'))
        # print keywords
        return keywords
    def get_keyphrases(self, text,num=10):
        """获取文本的关键短语

        >>> get_keyphrases( text,num=10)
        >>> ['灵武市长', '陈淑惠', '被告人陈', '被告人陈淑惠']


        """
        tr4w = TextRank4Keyword()
        # print( '关键短语：' )
        tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

        return tr4w.get_keyphrases(keywords_num=num, min_occur_num= 2)

        # return data
    def text_processing(self, text):
        """对文本进行更多的处理
        获取到更多的内容
        进行分词，分句等处理

        >>> text_processing(text)

        """

        data = {
            'keyphrases':self.get_keyphrases(text),
            'keywords' : self.get_keywords(text),
            'summary':self.summary(text),
            'sentence':self.sentence_segmentation(text),
            'text':text



        }
        return data

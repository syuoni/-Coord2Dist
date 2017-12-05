# -*- coding: utf-8 -*-
import jieba
from hanziconv import HanziConv as HC
import re

jieba.load_userdict('userdict.txt')

emoji_pt = re.compile('\[{1}\w+?\]{1}')
link_pt = re.compile('https?://[a-z0-9A-Z_./]+')
share_pt1 = re.compile('[\(（].+?\@.+?[\)）]')
share_pt2 = re.compile('@\w+?[\s\u200b]')
blank_pt = re.compile('\s+')
remove_pt = re.compile('[『』【】《》\[\]<>、“”‘’\"\'\u200b]')
# '.*?': 匹配任意内容，但尽可能短
# [！!？?。…；:~～\s]: 标点符号，类似...需要单独处理
split_pt1 = re.compile('.*?[！!？?。…；;~～\s]+')
split_pt2 = re.compile('\.{2,}')


def sent_extract(sent):
    sent = HC.toSimplified(sent)
    
    extracted = []
    for pt in [emoji_pt, link_pt, share_pt1, share_pt2]:
        ex = ';'.join(pt.findall(sent))
        if ex:
            sent = pt.sub('', sent)
        extracted.append(ex)
        
    sent = remove_pt.sub('', sent).strip()
    return sent, extracted

def sent_split(sent):
    if not split_pt1.fullmatch(sent):
        sent = sent + ' '
    
    sub_sent_seq = []
    for sub_sent in split_pt1.findall(sent):
        for sub_sub_sent in split_pt2.split(sub_sent):
            if len(sub_sub_sent) > 4:
                sub_sent_seq.append(sub_sub_sent)
    return sub_sent_seq

def sent_cut(sent):    
    return [w for w in jieba.cut(sent) if not blank_pt.fullmatch(w)]


if __name__ == '__main__':
    sent = '【#我在北京这一年# 第二期】>>本期讲述“帝都人对钱的看法”——靠什么来赚钱？?!.！ 多少钱7.12才够花...听过了再多道理，依旧耗不过这房价…来看看帝都人的白日梦&血泪史！猛戳右[向右]盘点2016：怎么才能成为有钱人？40个神回复 @北京人不知道的北京事儿 @神街坊 @拜托啦学妹 ​'
    
    sent, extracted = sent_extract(sent)
    print(sent)
    print(sent_split(sent))
    print(sent_cut(sent))

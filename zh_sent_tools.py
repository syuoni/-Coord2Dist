# -*- coding: utf-8 -*-
import jieba
from hanziconv import HanziConv as HC
import re

jieba.load_userdict('word-dic.txt')

class Full2Half(object):
    '''translate full-width characters to half-widths
    '''
    _f2h = {fc: hc for fc, hc in zip(range(0xFF01, 0xFF5E), range(0x21, 0x7E))}
    _f2h.update({0x3000: 0x20})
    _h2f = {hc: fc for fc, hc in _f2h.items()}
    
    @staticmethod
    def full2half(text):
        return text.translate(Full2Half._f2h)
    
    @staticmethod
    def half2full(text):
        return text.translate(Full2Half._h2f)

class Sent2WordSeq(object):
    def __init__(self, remove_punc=True, remove_stop=True, remove_pts=None, min_len=2):
        self.punc_pt = re.compile('[！!？?。\.…,，；;:：~～\-—\s（）『』【】《》\(\)\[\]<>、“”‘’\"\']+')
        with open('zh-stopwords.txt', encoding='utf-8') as f:
            self.stop = [w.strip() for w in f if not self.punc_pt.fullmatch(w)]
        self.remove_punc = remove_punc
        self.remove_stop = remove_stop
        self.remove_pts = remove_pts
        self.min_len = min_len
        
    def sent2word_seq(self, sent):
        sent = HC.toSimplified(sent)
        sent = Full2Half.full2half(sent)
        
        word_seq = []
        # TODO: cut or cut_for_search??
        for w in jieba.cut(sent):
            if self.remove_punc and self.punc_pt.fullmatch(w):
                continue
            if self.remove_stop and w in self.stop:
                continue
            if self.remove_pts is not None:
                matched = False
                for pt in self.remove_pts:
                    if pt.fullmatch(w):
                        matched = True
                        break
                if matched:
                    continue
            if len(w) < self.min_len:
                continue
            word_seq.append(w)
            
        return word_seq

if __name__ == '__main__':
    s2w = Sent2WordSeq(remove_pts=[re.compile('\d+'), re.compile('+'), re.compile('[①-⑩]+')])
    print(s2w.sent2word_seq('⑥2006年'))
    
    
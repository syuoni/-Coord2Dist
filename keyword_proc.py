# update: 2017-05-23
import numpy as np

class Leaf(object):
    def __init__(self, word):
        self.word = word
        
    def match_text(self, text, ext_text=None):
        return self.word in text
    
    def to_string(self):
        return self.word

class Node(object):
    def __init__(self, node_list, stop_list, conjunc=True):
        '''conjunc: indicate conjunction or disjunction
        '''
        self.node_list = node_list
        self.stop_list = stop_list
        self.conjunc = conjunc
    
    def match_text(self, text, ext_text=None):
        '''stop-words should be verified in an extended text, to make sure that
        there is no stop-words in surrounding context. 
        '''
        if ext_text is None:
            ext_text = text
            
        if self.conjunc is True:
            node_res = all([node.match_text(text=text, ext_text=ext_text) for node in self.node_list])
        else:
            node_res = any([node.match_text(text=text, ext_text=ext_text) for node in self.node_list])        
        if len(self.stop_list) == 0:
            stop_res = True
        else:
            stop_res = not any([node.match_text(text=ext_text) for node in self.stop_list])
        return (node_res and stop_res)
            
    def to_string(self):
        string = ''
        sep = '&' if self.conjunc else '/'
        for node in self.node_list:
            string = string + sep + node.to_string()        
        for node in self.stop_list:
            string = string + '-' + node.to_string()
        return '[' + string + ']'


def parse2node(text):
    '''text: pattern which could be parsed to a instance of Node
    '''
    # check whether brackedts removing is needed
    if text[0] == '[' and text[-1] == ']':
        remove_bracket = False
        depth = 0
        for letter in text:
            if letter == '[':
                depth += 1
            else:
                depth -= 1
                if depth < 0:
                    remove_bracket = True
                    break
        if remove_bracket:
            text = text[1:-1]
    
    if not any([sep in text for sep in ['&', '/', '-']]):
        return Leaf(text)
    
    index_slice_seq = []
    depth = 0
    last_index = 0
    for index, letter in enumerate(text[1:], 1):
        if letter in ['&', '/', '-'] and depth == 0:
            index_slice_seq.append((last_index, index))
            last_index = index
        if letter == '[':
            depth += 1
        if letter == ']':
            depth -= 1
    index_slice_seq.append((last_index, len(text)))
    assert depth == 0
    
    if text[0] == '/':
        conjunc = False
    elif text[0] == '&':
        conjunc = True
    else:
        raise Exception('Invalid conjunction or disjunction indicator!', text[0])
        
    node_list = []
    stop_list = []
    for k, (x, y) in enumerate(index_slice_seq):
        sub_text = text[x:y]
        if sub_text[0] == '-':
            stop_list.append(parse2node(sub_text[1:]))
        else:
            node_list.append(parse2node(sub_text[1:]))
    return Node(node_list, stop_list, conjunc=conjunc)


def extract_text(node, text, range_size=15, ext_margin=5):
    text_len = len(text)
    if text_len <= range_size:
        return text if node.match_text(text) else None
    else:
        sub_text_seq = [text[k:(k+range_size)] for k in range(text_len-range_size+1)]
        ext_text_seq = [text[max(0, k-ext_margin):min(text_len, k+range_size+ext_margin)] for k in range(text_len-range_size+1)]
        matched_seq = [node.match_text(text=sub_text, ext_text=ext_text) for sub_text, ext_text in zip(sub_text_seq, ext_text_seq)]
        
        # continued matched-index should be aggregated to average-value
        matched_idx_info = []
        last_matched = False
        for idx, matched in enumerate(matched_seq):
            if matched:
                if last_matched is False:
                    matched_idx_info.append([idx])
                    last_matched = True
                else:
                    matched_idx_info[-1].append(idx)
            else:
                last_matched = False
        selected_list = [int(np.round(np.mean(seq))) for seq in matched_idx_info]
        return '\n'.join([sub_text_seq[k] for k in selected_list]) if len(selected_list) > 0 else None


if __name__ == '__main__':
#    text = '&[/环境/周边-远处]&安静'
#    node = parse2node(text)
#    print(node.to_string())
#    print(node.match_text('周边安静'))
#    print(extract_text(node, 'bb周边安静bububububbbbbbbbbbbbb周边安静'))
    
    pattern = '&干-干净'
    node = parse2node(pattern)
    print(node.to_string())
    print(extract_text(node, '周围安静周围安静周围安静周围安静周围安静干净'))
    print(extract_text(node, '周围安静周围安静周围安静周围安静周围安静干净', ext_margin=0))
    
#    text = '&空调&[/噪声/吵/[&声音&大-小]]'
#    node = parse2node(text)
#    long_text = '没有想象中五星酒店的奢华！房屋地毯质量极差，而且全是烟头烫过的痕迹！手龙头、洗浴水龙头质量都不好！空调开关是英文的、而且空调声音有点大没有新风换气功能！早餐想当丰富！酒店总机相当业余，居然不知道，电话请勿查询和请勿打扰功能！'
#    print(extract_text(node, long_text))
    

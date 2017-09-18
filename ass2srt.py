# -*- coding: utf-8 -*-
import glob
import chardet
import asstosrt

for ass_fn in glob.iglob('*.ass'):
    with open(ass_fn, 'rb') as f:
        ass_bytes = f.read()
    
    encoding = chardet.detect(ass_bytes)['encoding']
    with open(ass_fn, 'r', encoding=encoding) as f:
        srt_str = asstosrt.convert(f)
        
    srt_fn = ass_fn[:-4] + '.srt'
    with open(srt_fn, 'w', encoding='utf-8') as f:
        f.write(srt_str)


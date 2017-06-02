
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


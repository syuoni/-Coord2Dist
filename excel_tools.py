import bs4
import quopri
import xlrd, xlsxwriter
from datetime import datetime, timedelta

def xldate_to_datetime(xldate):
    start_date = datetime(1899, 12, 31)
    # Excel treats 1900 as a leap year
    if xldate <= 59:
        delta = timedelta(days=xldate)
    else:
        delta = timedelta(days=xldate-1)
    return start_date + delta


def html2xlsx(htmlfn, xlsxfn, rowcol=None, sheet_name='Sheet1', encoding='utf-8', quopri_decoding=False):
    if rowcol is not None:
        row_tag, col_tag = rowcol
    else:
        row_tag, col_tag = 'tr', 'td'
    
    with open(htmlfn, encoding=encoding) as f:
        html = f.read()
    if quopri_decoding:
        html = quopri.decodestring(html)
    soup = bs4.BeautifulSoup(html, 'lxml')
    
    dst = xlsxwriter.Workbook(xlsxfn)
    dstSht = dst.add_worksheet(sheet_name)
    for i, row in enumerate(soup.findAll(row_tag)):
        for j, cell in enumerate(row.findAll(col_tag)):
            dstSht.write(i, j, cell.text.strip())
    dst.close()
    
        
if __name__ == '__main__':
#    src = xlrd.open_workbook('..\\formula_test.xlsx')
#    srcSht = src.sheet_by_index(0)
#    for j in range(3, 7):
#        xldt = srcSht.cell_value(j, 0)
#        print(xldt, xldate_to_datetime(xldt))

    html2xlsx('现任管理层[600547.SH].xls', '现任管理层[600547.SH].xlsx', rowcol=('tr', 'td'), quopri_decoding=True)
    html2xlsx('离任高管[600547.SH].xls', '离任高管[600547.SH].xlsx', rowcol=('row', 'cell'), quopri_decoding=False)
    
    
    
    
    
        
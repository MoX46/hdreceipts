import os, re
from PyPDF2 import PdfReader


file = 'receipts/eReceipt (2).pdf'

reader = PdfReader(file)
page = reader.pages[0]
text = page.extract_text()

lines = text.split('\n')
clean_liens = []
receipt = {'id':None,'date_time':None,'products':[]}

for line in lines:
    clean_liens.append(' '.join(line.strip().split()))
    
for index, line in enumerate(clean_liens):
    product_line_match = re.search('(^\d{8,})( )(.+)( )(-?\d*(\.\d+)?$)',line)
    multi_product_line_match = re.search('(^\d)(@)(-?\d*(\.\d+)?)( )(-?\d*(\.\d+)?$)',line)
    
    if product_line_match:
        product = {}
        product['barcode'] = product_line_match[1]
        product['description'] = product_line_match[3]
        product['price'] = float(product_line_match[5])
        product['qty'] = 1
        product['unit_price'] = float(product_line_match[5])
        receipt['products'].append(product)
        
    if multi_product_line_match:
        product = {}
        product_line_match = re.search('(^\d{8,})( )(.+$)',clean_liens[index-1])
        product['barcode'] = product_line_match[1]
        product['description'] = product_line_match[3]
        product['price'] = float(multi_product_line_match[6])
        product['qty'] = int(multi_product_line_match[1])
        product['unit_price'] = float(multi_product_line_match[3])
        receipt['products'].append(product)
    
for x in receipt['products']:
    print(x)
    
    
'''
17850 Yonge Street Newmarket, ONT
LARRY TIMBERS STORE MGR (905)898-0090
7030 00030 33586 27/08/22 01:46 PM
CASHIER JANE
* ORIG REC: 7030 002 26043 14/08/22 TA *
885911137652 2" BRAD NAIL -10.24
GST/HST -1.33
* ORIG REC: 7030 009 29711 13/08/22 TA *
697285605756 Valve Stop
2@-16.13 -32.26
061788787019 Pipe Cutter -14.98
038753480039 PLUMER PUTTY -6.65
026508264294 DRAIN -33.59
GST/HST -11.37
SUBTOTAL -97.72
GST/HST -12.70
TOTAL -$110.42
XXXXXXXXXXXX8170 MASTERCARD -110.42
INVOICE 8302100 TA
REFUND-CUSTOMER COPY
13% HST R135772911
13% HST R135772911
DID WE NAIL IT?
Take a short survey for a chance TO WIN
A $3,000 HOME DEPOT GIFT CARD!
www.homedepot.com/survey
User ID: XG0 74491 67491
PASSWORD: 22427 67461
Entries must be completed within 14 days
of purchase. See complete rules on
website. No purchase necessary.
(Sondage offert en français sur le Web.)
Page 1 of
1
'''
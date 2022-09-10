#!/usr/bin/env python3

import os, re, datetime, json
from PyPDF2 import PdfReader

class HDReceipt:
    def __init__(self, file):
        reader = PdfReader(file)
        self.pdf = reader.pages[0]
        self.text = self.pdf.extract_text()
        lines = self.text.split('\n')
        self.line_items = []
        for line in lines:
            self.line_items.append(' '.join(line.strip().split()))

        self.extract()

    def extract(self):
        self.receipt_details = {'id':None, 'date_time':None, 'orig_recipt_details':[], 'products':[]}
        for index, line in enumerate(self.line_items):
            product_line_match = re.search('(^\d{8,})( )(.+)( )(-?\d*(\.\d+)?$)',line)
            multi_product_line_match = re.search('(^\d)(@)(-?\d*(\.\d+)?)( )(-?\d*(\.\d+)?$)',line)
            id_date_time_match = re.search('^(\d{4} \d{5} \d{5}) (\d{2}/\d{2}/\d{2} \d{2}:\d{2} [APM]{2})',line)
            orig_id_date_time_match = re.search('^(\* ORIG REC: )(\d{4} \d{3} \d{5}) (\d{2}/\d{2}/\d{2}) (TA \*)',line)

            if orig_id_date_time_match:
                tmp = {'id':None, 'date':None}
                tmp['id'] = orig_id_date_time_match[2]
                tmp['date'] = orig_id_date_time_match[3]
                self.receipt_details['orig_recipt_details'].append(tmp)

            if id_date_time_match:
                self.receipt_details['id'] = id_date_time_match[1]
                self.receipt_details['date_time'] = id_date_time_match[2]
                
            if product_line_match:
                product = {}
                product['barcode'] = product_line_match[1]
                product['description'] = product_line_match[3].replace('<A>','').strip()
                product['price'] = float(product_line_match[5])
                product['qty'] = 1
                product['unit_price'] = float(product_line_match[5])
                self.receipt_details['products'].append(product)
                
            if multi_product_line_match:
                product = {}
                product_line_match = re.search('(^\d{8,})( )(.+$)',self.line_items[index-1])
                product['barcode'] = product_line_match[1]
                product['description'] = product_line_match[3]
                product['price'] = float(multi_product_line_match[6])
                product['qty'] = int(multi_product_line_match[1])
                product['unit_price'] = float(multi_product_line_match[3])
                self.receipt_details['products'].append(product)

    def get_pdf(self):
        return self.pdf
    
    def get_raw(self):
        return self.receipt_details

    def get_json(self):
        return (json.dumps(self.receipt_details, indent = 4))

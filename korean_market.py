import csv

krx_codes = []
kosdaq_codes = []

with open('corporations_krx.csv', 'r', encoding='utf8') as file_read:
    csv_reader = csv.reader(file_read)
    for row in csv_reader:
        stock_code = row[1]
        if stock_code.isdecimal():
            krx_codes.append(row[1])

with open('corporations_kosdaq.csv', 'r', encoding='utf8') as file_read:
    csv_reader = csv.reader(file_read)
    for row in csv_reader:
        stock_code = row[1]
        if stock_code.isdecimal():
            krx_codes.append(row[1])

all_stock_codes = krx_codes + kosdaq_codes
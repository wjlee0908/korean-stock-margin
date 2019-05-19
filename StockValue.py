from company import *
import korean_market
import csv

# samsung_electronics = Company('005930')

companies = []

for code in korean_market.all_stock_codes:
        companies.append(Company(code))
'''
with open('company_inforamtion.txt', 'w') as f:
        for com in companies:
                f.write(str(com) + '\n')
'''

companies.append(Company('005930'))

with open('corporation_information.csv', 'w', encoding='utf8') as file_write:
    csv_writer = csv.writer(file_write)
    csv_writer.writerow(['종목코드', '회사명', '유동자산', '유동부채', '투자자산', '비유동부채', '영업이익'])

    for com in companies:
            csv_writer.writerow(com.get_information_list())


from company import *
import korean_market

# samsung_electronics = Company('005930')

companies = []

for code in korean_market.all_stock_codes:
        companies.append(Company(code))

with open('company_inforamtion.txt', 'w') as f:
        for com in companies:
                f.write(com + '\n')

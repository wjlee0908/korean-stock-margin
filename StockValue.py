import requests
import sys
from bs4 import BeautifulSoup
import Currency

def generate_dict_from_html_table(table_html, row_headers, column_index):
    """ (bs4.element.Tag, list, int) -> dict
    
    read data from html tag form table and store it in dictionary.
    And returns dictionary.
    
    financial_table = financial_table.find('div', {'name':'yt1'})
    >>> generate_dict_from_html_table(financial_table, ['profit', 'debt'], 4)
    {'profit' : '300,000', 'debt' : '20,000'}
    """

    table_info = dict()

    for tr in table_html.find_all('tr'):
        header_name = tr.find('th')
        # 찾을 행과 헤더가 동일한 행의 값만 읽음
        if header_name.text in row_headers:
            tds = list(tr.find_all('td'))    # 행의 모든 열 정보 list로 저장
            table_info[header_name.text] = tds[column_index].text

    return table_info


# 재무제표 있는 기업정보 사이트(상장온라인)의 주소
company_information_url = "http://media.kisline.com/fininfo/mainFininfo.nice"
# stock_code = '005930'    # 조회할 기업의 종목 코드
stock_code = '005380'
table_page_num = 4    # 재무제표 있는 페이지 번호. nav 파리미터
# 데이터 읽어올 행의 key 리스트
row_to_search = ['유동자산(계)', '유동부채(계)', '장기투자자산', '비유동부채(계)', '영업이익(손실)']
finance_value = {key : 0 for key in row_to_search}
# company_information = {'종목코드' : stock_code}
company_information = dict()    # 종목코드 : 재무정보 매핑한 딕셔너리
response = requests.get(company_information_url, {'paper_stock': stock_code, 'nav':str(table_page_num)})

# 페이지 읽어오기 실패하면 종료
if response.status_code != 200:
    print("페이지가 응답하지 않습니다.")
    sys.exit(1)

soup = BeautifulSoup(response.content, 'html.parser')

financial_table = soup.find('div', {'id': 'Sin1'})
financial_table = financial_table.find('div', {'name':'yt1'})
year_index = 4    # 연도 열의 인덱스
money_unit = 1000000    # 표에서 돈의 기본 단위

financial_dict = generate_dict_from_html_table(financial_table, row_to_search, year_index)
'''
print(type(financial_table))
year_index = 4    # 여러 해의 정보 중 몇 번째 해의 정보 가져올지.
table_unit = 1000000    # 재무재표 표의 기본 단위. 백만원
for tr in financial_table.find_all('tr'):
    header_name = tr.find('th')
    # 찾을 행과 헤더가 동일한 행의 값만 읽음
    if header_name.text in row_to_search:
        tds = list(tr.find_all('td'))    # 행의 모든 열 정보 list로 저장
        finance_value[header_name.text] = Currency.convert_to_int(tds[year_index].text, 1000000)
        '''


profit_table = soup.find('div', {'id':'Pin1'})
profit_table = profit_table.find('div', {'name':'ypt1'})
profit_dict = generate_dict_from_html_table(profit_table, row_to_search, year_index)

'''
for tr in profit_table.find_all('tr'):
    header_name = tr.find('th')
    # 찾을 행과 헤더가 동일한 행의 값만 읽음
    if header_name.text in row_to_search:
        tds = list(tr.find_all('td'))    # 행의 모든 열 정보 list로 저장
        finance_value[header_name.text] = Currency.convert_to_int(tds[year_index].text, 1000000)
'''

finance_value.update(financial_dict)
finance_value.update(profit_dict)

for key, value in finance_value.items():
    finance_value[key] = Currency.convert_to_int(value, money_unit)

company_information[stock_code] = finance_value

print(company_information)

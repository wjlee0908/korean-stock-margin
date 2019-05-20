import requests
from bs4 import BeautifulSoup
import currency

class Company:
    def __init__(self, stock_code, year):
        self.__stock_code = stock_code
        self.__year = year
        self.__name = ''    # 기업명
        self.__asset = 0    # 유동자산
        self.__current_liabilities = 0    # 유동부채
        self.__fixed_liabilities = 0    # 고정부채
        self.__investment_asset = 0    # 투자자산
        self.__profit = 0    # 영업이익
        self.__value = 0    # 기업가치
        
        self.__is_scraping_succeed = self.__set_information_from_table(self.__stock_code)

        if self.__is_scraping_succeed:
            self.__value = self.calculate_value()

    def __str__(self):
        return '기업명: {}  종목코드: {}    유동자산: {}    유동부채: {}    고정부채: {}    투자자산: {}    영업이익: {}    기업가치: {}'\
            .format(self.__name, self.__stock_code, self.__asset, self.__current_liabilities, self.__fixed_liabilities, \
                self.__investment_asset, self.__profit, self.__value)

    def get_information_list(self):
        return [self.__stock_code, self.__name, self.__asset, self.__current_liabilities, \
        self.__fixed_liabilities, self.__investment_asset, self.__profit, self.__value]

    def get_value(self):
        return self.__value
    
    def is_valid(self):
        return self.__is_scraping_succeed

    def calculate_value(self):
        business_value = self.__profit * 13.3
        asset_value = self.__asset - (1.29 * self.__current_liabilities) + self.__investment_asset
        return business_value + asset_value - self.__fixed_liabilities

    def __set_information_from_table(self, stock_code):
        # 재무제표 있는 기업정보 사이트(상장온라인)의 주소
        company_information_url = "http://media.kisline.com/fininfo/mainFininfo.nice"
        table_page_num = 4    # 재무제표 있는 페이지 번호. nav 파리미터

        # 상장온라인 사이트에서 재무정보를 받아 멤버로 설정.
        money_unit = 1000000    # 표에서 돈의 기본 단위

        response = requests.get(company_information_url, {'paper_stock': stock_code, 'nav':str(table_page_num)})

        # 페이지 읽어오기 실패하면 종료
        if response.status_code != 200:
            print("페이지가 응답하지 않습니다.")
            return False

        # html 파일을 beatutifulsoup로 파싱
        soup = BeautifulSoup(response.content, 'html.parser')
        if type(soup) == type(None):
            return False

        # 회사명 탐색
        info_div = soup.find('div', {'class':'cot'})
        if type(info_div) == type(None):
            return False
        name_tag = info_div.find('strong')
        if type(name_tag) == type(None):
            return False
        
        self.__name = name_tag.text

        # 재무정보 테이블 탐색
        row_to_search = ['유동자산(계)', '유동부채(계)', '장기투자자산', '비유동부채(계)']
        financial_table = soup.find('div', {'name':'yt1'})
        year_index = self.__find_year_column_index(financial_table, self.__year)
        if year_index == None:
            return False
        financial_dict = self.__generate_dict_from_html_table(financial_table, row_to_search, year_index)

        # 테이블에서 재무정보가 찾아야 하는 행의 갯수와 다르면 종료.
        if len(financial_dict) != len(row_to_search):
            return False
            
        for key, value in financial_dict.items():
            # 상장온라인 표에서 0을 '-'으로 표기해서 변환해줌
            if financial_dict[key] == '-':
                financial_dict[key] = '0'
            financial_dict[key] = currency.convert_to_int(financial_dict[key], money_unit)

        self.__asset = financial_dict['유동자산(계)']
        self.__current_liabilities = financial_dict['유동부채(계)']
        self.__investment_asset = financial_dict['장기투자자산']
        self.__fixed_liabilities = financial_dict['비유동부채(계)']

        # 포괄손익계산서 테이블 탐색
        row_to_search = ['영업이익(손실)']
        profit_table = soup.find('div', {'name':'ypt1'})
        year_index = self.__find_year_column_index(financial_table, self.__year)
        if year_index == None:
            return False
        profit_dict = self.__generate_dict_from_html_table(profit_table, row_to_search, year_index)

        for key, value in profit_dict.items():
            # 상장온라인 표에서 0을 '-'으로 표기해서 변환해줌
            if profit_dict[key] == '-':
                profit_dict[key] = '0'
            profit_dict[key] = currency.convert_to_int(profit_dict[key], money_unit)
        
        self.__profit = profit_dict['영업이익(손실)']

        return True

    def __generate_dict_from_html_table(self, table_html, row_headers, column_index):
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

            # 찾을 행 있을 때만 진행
            if type(header_name) == type(None):
                continue

            # 찾을 행과 헤더가 동일한 행의 값만 읽음
            if header_name.text in row_headers:
                tds = list(tr.find_all('td'))    # 행의 모든 열 정보 list로 저장
                table_info[header_name.text] = tds[column_index].text

        return table_info

    def __find_year_column_index(self, table_tag, year):
       head_row = table_tag.find('tr')    # 테이블에서 첫 번째 row
       headers = head_row.find_all('th')

       for idx, th in enumerate(headers):
           header_name = th.text
           if str(year) + '.' in header_name:
               return idx - 1    # data 첫 열은 th라서 data index는 -1

       return None
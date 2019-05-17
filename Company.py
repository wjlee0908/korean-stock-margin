import requests
from bs4 import BeautifulSoup
import Currency

class Company:
    def __init__(self, stock_code):
        self.__stock_code = stock_code

        self.__asset = 0    # 유동자산
        self.__current_liabilities = 0    # 유동부채
        self.__fixed_liabilities = 0    # 고정부채
        self.__investment_asset = 0    # 투자자산
        self.__profit = 0    # 영업이익
        
        self.__set_information_from_table(self.__stock_code)

    def __set_information_from_table(self, stock_code):
        # 재무제표 있는 기업정보 사이트(상장온라인)의 주소
        company_information_url = "http://media.kisline.com/fininfo/mainFininfo.nice"
        table_page_num = 4    # 재무제표 있는 페이지 번호. nav 파리미터

        # 상장온라인 사이트에서 재무정보를 받아 멤버로 설정.
        year_index = 4    # 연도 열의 인덱스
        money_unit = 1000000    # 표에서 돈의 기본 단위

        response = requests.get(company_information_url, {'paper_stock': stock_code, 'nav':str(table_page_num)})

        # 페이지 읽어오기 실패하면 종료
        if response.status_code != 200:
            print("페이지가 응답하지 않습니다.")
            return

        # html 파일을 beatutifulsoup로 파싱
        soup = BeautifulSoup(response.content, 'html.parser')

        # 재무정보 테이블 탐색
        row_to_search = ['유동자산(계)', '유동부채(계)', '장기투자자산', '비유동부채(계)']
        financial_table = soup.find('div', {'name':'yt1'})
        financial_dict = self.__generate_dict_from_html_table(financial_table, row_to_search, year_index)

        for key, value in financial_dict.items():
            financial_dict[key] = Currency.convert_to_int(value, money_unit)

        self.__asset = financial_dict['유동자산(계)']
        self.__current_liabilities = financial_dict['유동부채(계)']
        self.__investment_asset = financial_dict['장기투자자산']
        self.__fixed_liabilities = financial_dict['비유동부채(계)']

        # 포괄손익계산서 테이블 탐색
        row_to_search = ['영업이익(손실)']
        profit_table = soup.find('div', {'name':'ypt1'})
        profit_dict = self.__generate_dict_from_html_table(profit_table, row_to_search, year_index)

        for key, value in profit_dict.items():
            profit_dict[key] = Currency.convert_to_int(value, money_unit)
        
        self.__profit = profit_dict['영업이익(손실)']

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
            # 찾을 행과 헤더가 동일한 행의 값만 읽음
            if header_name.text in row_headers:
                tds = list(tr.find_all('td'))    # 행의 모든 열 정보 list로 저장
                table_info[header_name.text] = tds[column_index].text

        return table_info
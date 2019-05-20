from multiprocessing import Process, Manager
import random

from company import *
import korean_market
import csv

def add_new_company(company_list, codes):
        for code in codes:
            company_list.append(Company(code))


if __name__ == "__main__":

    with Manager() as manager:
        companies = manager.list()
        processes = []
        num_processes = 4
        # stock_codes = korean_market.all_stock_codes
        stock_codes = random.sample(korean_market.all_stock_codes, k=100)    # [TEST] 테스트용 샘플 100개 추출
        len_single_list = len(stock_codes) // num_processes

        # 리스트 하나를 process 개수만큼 나눠서 병렬 처리
        for i in range(num_processes):
            idx_start = i * len_single_list
            if i == num_processes - 1:
                idx_end = len(stock_codes)
            else:    
                idx_end = len_single_list * (i+1)
            codes = stock_codes[idx_start:idx_end]

            # 모든 상장 기업 정보 크롤링하는 과정 멀티프로세싱
            p = Process(target=add_new_company, args=(companies, codes))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()

        with open('corporation_information_test.csv', 'w', encoding='utf8') as file_write:
                csv_writer = csv.writer(file_write)
                csv_writer.writerow(['종목코드', '회사명', '유동자산', '유동부채', '투자자산', '비유동부채', '영업이익'])

                for com in companies:
                        csv_writer.writerow(com.get_information_list())

    '''
    for code in korean_market.all_stock_codes:
        companies.append(Company(code))
    
    with open('corporation_information.csv', 'w', encoding='utf8') as file_write:
        csv_writer = csv.writer(file_write)
        csv_writer.writerow(['종목코드', '회사명', '유동자산', '유동부채', '투자자산', '비유동부채', '영업이익'])

        for com in companies:
                csv_writer.writerow(com.get_information_list())
    '''




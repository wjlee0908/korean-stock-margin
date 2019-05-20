import pandas as pd                
import matplotlib as mpl          
import matplotlib.pyplot as plt    

# csv 파일을 읽어서 DataFrame 객체로 만듦. 인덱스 컬럼은 point로 설정
df = pd.read_csv('corporation_information.csv', index_col='회사명', encoding='utf-8')


# Windows 한글 폰트 설정
font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
mpl.rc('font', family=font_name)
 
df[["기업가치"]]
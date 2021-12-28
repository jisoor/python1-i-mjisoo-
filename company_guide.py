import pandas as pd
import requests
from selenium import webdriver
driver = webdriver.Chrome('./chromedriver', options=options)

# [코드 3.19] 데이터프레임 형태 바꾸기 코드 함수화 (CH3. 데이터 수집하기.ipynb)
def change_df(firm_code, dataframe):
    for num, col in enumerate(dataframe.columns):
        temp_df = pd.DataFrame({firm_code: dataframe[col]})
        temp_df = temp_df.T
        temp_df.columns = [[col] * len(dataframe), temp_df.columns]
        if num == 0:
            total_df = temp_df
        else:
            total_df = pd.merge(total_df, temp_df, how='outer', left_index=True, right_index=True)

    return total_df

# [코드 3.21] 재무 비율 데이터프레임을 만드는 함수 (CH3. 데이터 수집하기.ipynb)

# [코드 3.23] 투자지표 데이터프레임을 만드는 함수 (CH3. 데이터 수집하기.ipynb)
def make_invest_dataframe(firm_code):
    invest_url = 'https://comp.fnguide.com/SVO2/asp/SVD_Invest.asp?pGB=1&cID=&MenuYn=Y&ReportGB=D&NewMenuID=105&stkGb=701&gicode=' + firm_code
    driver.get(invest_url)
    cols = []
   # invest_tables = pd.read_html(invest_page.text)
    temp_df = invest_tables[1]

    temp_df = temp_df.set_index(temp_df.columns[0])
    temp_df = temp_df.loc[['PER수정주가(보통주) / 수정EPS PER계산에 참여한 계정 펼치기',
                            'PCR수정주가(보통주) / 수정CFPS PCR계산에 참여한 계정 펼치기',
                            'PSR수정주가(보통주) / 수정SPS PSR계산에 참여한 계정 펼치기',
                            'PBR수정주가(보통주) / 수정BPS PBR계산에 참여한 계정 펼치기',
                            '세후영업이익 + 유무형자산상각비 총현금흐름']]
    temp_df.index = ['PER', 'PCR', 'PSR', 'PBR', '총현금흐름']
    # temp_df = temp_df.loc[['PER 계산에 참여한 계정 펼치기',
    #                        'PCR 계산에 참여한 계정 펼치기',
    #                        'PSR 계산에 참여한 계정 펼치기',
    #                        'PBR 계산에 참여한 계정 펼치기',
    #                        '총현금흐름세후영업이익 + 유무형자산상각비 총현금흐름']]
    # temp_df.index = ['PER', 'PCR', 'PSR', 'PBR', '총현금흐름']
    # invest_df = temp_df
    # return invest_df
    return temp_df


# [코드 3.24] 5개 회사의 투자지표 데이터 가져와서 합쳐보기 (CH3. 데이터 수집하기.ipynb)
firmcode_list = ['A005930', 'A005380', 'A035420', 'A003550', 'A034730']

for num, code in enumerate(firmcode_list):
    invest_df = make_invest_dataframe(code)
    invest_df_changed = change_df(code, invest_df)
    if num == 0 :
        total_invest = invest_df_changed
    else:
        total_invest = pd.concat([total_invest, invest_df_changed])
print("실험",total_invest)
# 각각 유형별로 콘캣 후 - > 16개 전부 콘캣

# 각각 유형에서 콘캣
import pandas as pd
import glob
mbti_type = ['enfp','estp', 'esfp', 'entp', 'estj', 'esfj', 'enfj', 'entj', 'istj', 'isfj', 'infj', 'intj', 'istp', 'isfp', 'infp', 'intp']


for i in mbti_type:
    each_type_paths = glob.glob('./crawling/{}/*').format(i) #첨에 enfp 타입의 모든 크로링 데이터 가져옴
    df = pd.DataFrame()
    for each_type_path in each_type_paths: #만약 enfp하나에, 10개 데이터 있다 치면 10개 하나씩 가져와서
        df_temp = pd.read_csv(each_type_path, index_col=False)  #각각 csv로 변환 후
        df = pd.concat([df, df_temp]) #데이터프레임으로 콘캣
    df.dropna(inplace=True) # 난값 제거
    df.drop(['title'], inplace=True, axis=1)    # 'title'열 삭제
    df['type'] = '{}'.format(i)          # mbti 타입 열을 추가
    df.reset_index(drop=True, inplace=True) # 리셋 인덱스?
    df.to_csv('./crawling/final_crawling/{}_all_data.csv'.format(i), index=False) # mbti 하나 저장.

# 위에거 다 하고 난 후 주석 처리하고 밑에거 실행
data_paths = glob.glob('./crawling/final_crawling/*')
df = pd.DataFrame()
for data_path in data_paths:
    df_temp = pd.read_csv(data_path, index_col=0)
    df = pd.concat([df, df_temp])
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_csv('./crawling/final_mbti_crawling.csv', index=False)
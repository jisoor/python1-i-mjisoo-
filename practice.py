import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt #자연어 : 사람이 쓰는 언어  ko =한국ㅇ더 pip install konlpy /pip install tweepy==3.10.0
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./crawling/team_crawling/naver_headline_news.csv')
print(df.head())
print(df.info())

X = df['title']
Y = df['category']

###  라벨 인코더
encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)  # 정치 경제 등 숫자로, array타입으로
print(labeled_Y[:5])        # [3 3 3 3 3]

##### 라벨 이름
label= encoder.classes_
print(label)                #['Culture' 'Economic' 'IT' 'Politics' 'Social' 'World']

# with open('./models/encoder_1.pickle', 'wb') as f:
#     pickle.dump(encoder, f) #encoder을 f에다가 저장
onehot_Y =  to_categorical(labeled_Y)  # 1과 0으로 이루어진 행렬로 만들어줌
print(onehot_Y)

okt = Okt() # 형태소 분리 #
 # 한문장 예시로 형태소 분리해 보기
print(type(X))
okt_morph_X = okt.morphs(X[10], stem=True)
print(X[10])
print(okt_morph_X)

 # title열의 모든 문장 형태소 분리
for i in range(len(X)):
    X[i] = okt.morphs(X[i])
print(X)

# 불용어 제거
stopwords = pd.read_csv('./crawling/stopwords.csv', index_col=0)

for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)  #리스트를 한 문장으로 만들기
print(X)

# 형태소 분리된 단어들을 토크나이징(모든 단어가
token = Tokenizer()
token.fit_on_texts(X)   # 모든 유니크한 단어를 1:'지수', 2:'오늘' 이ㅣ런식으로 딕셔너리화함
tokened_X = token.texts_to_sequences(X)
print(tokened_X[:5])
<<<<<<< HEAD
=======

##### 패딩 작업 ######
# 서로 다른 개수의 단어로 이루어진 문장을 같은 길이로 만들어주기 위해 패딩사용, 0을 붙여서 길이를 맞춰 array형태로 변환한다.

#최대 길이를 가진 문장 구하기
max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

X_pad = pad_sequences(tokened_X, max)
print(X_pad[:10])

# 참고자료 padded = pad_sequences(sequences, maxlen=6)  maxlen 파라미터는 시퀀스의 최대 길이를 제한합니다. 최대 길이를 6으로 지정하면 길이를 넘는 시퀀스는 잘라냅니다.

X_train, X_test, Y_train, Y_test = train_test_split(X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('./crawling/news_data_max_{}_wordsize_{}'.format(max, wordsize), xy)
>>>>>>> d8a7526 (doing nltk ...)

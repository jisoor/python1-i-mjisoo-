import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
from tensorflow.keras.utils import to_categorical
from konlpy.tag import Okt # 가 아니라 영문 nltk


pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./crawling/all_mbti.csv')
print(df.head())
print(df.info())

X = df['comment']
Y = df['type']

# y값 전처리
encoder = LabelEncoder()
labeled_Y = encoder.fit_transfrom(Y) # enfp, estj 등의 타입을 숫자로 0~15까지로 만들어서 array타입에 저장

label = encoder.classes_
print(labeled_Y[:5])
print(label)  # encoder라벨정보가 리스트로 나옴
with open('./models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)
onehot_Y = to_categorical(labeled_Y) # 행렬로 만듬


########## 형태소 분리
okt = Okt()








import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
from tensorflow.keras.utils import to_categorical
from konlpy.tag import Okt # 가 아니라 영문 nltk
import nltk
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

print(list(stop_words))

# Create a CSV file to store a set of stopwords

import csv # Import the csv module to work with csv files
with open('./stopwords(Eng).csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(stop_words)

pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./recompiled_all_mbti.csv')
print(df.head())
print(df.info())

X = df['comment']
Y = df['type']

# y값 전처리
# encoder = LabelEncoder()
# labeled_Y = encoder.fit_transform(Y) # enfp, estj 등의 타입을 숫자로 0~15까지로 만들어서 array타입에 저장
#
# label = encoder.classes_
# print(labeled_Y[:5])
# print(label)  # encoder라벨정보가 리스트로 나옴
# with open('./models/encoder.pickle', 'wb') as f:
#     pickle.dump(encoder, f)
# onehot_Y = to_categorical(labeled_Y) # 행렬로 만듬
# print(onehot_Y)

########## 형태소 분리
# okt = Okt()
print(type(X))

# 단어로 토크나이징 하기
# 처음 사용하는 경우라면 먼저 nltk.download('punkt') 를 실행하여 Punket Tokenizer Models (13MB) 를 다운로드 해줍니다.
# nltk.word_tokenize() 함수를 사용해서 괄호 안에 텍스트 문자열 객체를 넣어주면 Token으로 쪼개줍니다.

nltk.download('punkt')
sentence = "NLTK is a leading platform for building Python programs to work with human language data."
tokens = nltk.word_tokenize(sentence)
print(tokens)

# pos 태깅
nltk.download('averaged_perceptron_tagger')
tagged = nltk.pos_tag(tokens)
print(tagged)

#stemmizing은 동사일경우만 VB VBD VBG VBN VBP VBZ
verbs_list = [t[0] for t in tagged if (t[1] == "VB") | (t[1] =="VBD") | (t[1] =="VBG")| (t[1] =="VBN")| (t[1] =="VBP")| (t[1] =="VBZ") ]
print(verbs_list)


from nltk.stem import LancasterStemmer

Lcs = LancasterStemmer()

verbs_list_new = []
for i in verbs_list:
    i = Lcs.stem(i)
    verbs_list_new.append(i)
print(verbs_list_new)
# 또는 한줄로걍
# print("Lancaster Stemmer:", [Lcs.stem(i) for i in verbs_list])


#lemmatizing 동사원형으로 복귀
from nltk.stem import WordNetLemmatizer

lm = WordNetLemmatizer()

[lm.lemmatize(i, pos="v") for i in verbs_list]

# 품사가 동사인거 제외하고 전부가져오기








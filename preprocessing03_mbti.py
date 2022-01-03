import pandas as pd
<<<<<<< HEAD
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

# y값전처리, x값 nltk랑 불용어 제거, x값 전처리 encoder, token, modeling npy 만들기

pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./crawling/recompiled_all_mbti.csv')
=======
from sklearn.preprocessing import LabelEncoder
import pickle
from tensorflow.keras.utils import to_categorical
from konlpy.tag import Okt # 가 아니라 영문 nltk


pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./crawling/final_all_mbti.csv')
>>>>>>> origin/main
print(df.head())
print(df.info())

X = df['comment']
Y = df['type']

# y값 전처리
encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y) # enfp, estj 등의 타입을 숫자로 0~15까지로 만들어서 array타입에 저장

label = encoder.classes_
print(labeled_Y[:5])
print(label)  # encoder라벨정보가 리스트로 나옴
<<<<<<< HEAD
# with open('./models/encoder.pickle', 'wb') as f:
#     pickle.dump(encoder, f)
onehot_Y = to_categorical(labeled_Y) # 행렬로 만듬
print(onehot_Y)

########## nltk 형태소 분리 ##############

import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from nltk.tag import untag
# nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

# ############# tokenizing
for i in range(len(X)):
    X[i] = nltk.word_tokenize(X[i])
print(X)
############# pos 태깅 ( word_tokenize 먼저 해야함)
for i in range(len(X)):
    X[i] = nltk.pos_tag(X[i])
print(X)

## lemmatzing  품사가 VB VBD VBG VBN VBP VBZ 애네만 골라서 동사 원형(lemmatizing)만들기
lm = WordNetLemmatizer()

for i in range(len(X)):
    for j in range(len(X[i])):
        X[i][j] = list(X[i][j])  #투플이니까 리스트로 바꼬야지!!
        if (X[i][j][1] == "VB") | (X[i][j][1] == "VBD") | (X[i][j][1] == "VBG")| (X[i][j][1] == "VBN")| (X[i][j][1] == "VBP")| (X[i][j][1] == "VBZ"):
            X[i][j][0] = lm.lemmatize(X[i][j][0], pos='v')
print(X[i])

# 모두 untag 해서 리스트 만들기
for i in range(len(X)):
    for j in range(len(X[i])):
        #l = []
        X[i][j] = X[i][j][0]
        #l.append(X[i][j])
   # X[i] = l
print('untagged\lists: ', X[0],X[1] )

# 한글자인 단어 빼기, stopwords에 관형사 빼기
# 그 다음 tokenizing 시작

stopwords = pd.read_csv('./stopwords(Eng).csv')
stopwords = stopwords.T
stopwords.reset_index(inplace=True)
print(stopwords.info())
print(stopwords.columns)

# exit()
=======
with open('./models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)
onehot_Y = to_categorical(labeled_Y) # 행렬로 만듬
print(onehot_Y)

########## 형태소 분리
okt = Okt()
print(type(X))
okt_morph_X = okt.morphs(X[10], stem=True)
print(X[10])
print(okt_morph_X)


for i in range(len(X)):
    X[i] = okt.morphs(X[i])
# print(X)

stopwords = pd.read_csv('./crawling/stopwords.csv', index_col=0)

>>>>>>> origin/main
for j in range(len(X)):
    words=[]
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
<<<<<<< HEAD
            if X[j][i] not in list(stopwords['index']):
                words.append(X[j][i])
    X[j] = ' '.join(words)
print('불용어 까지 제거한 X', X)

# cleaned_df = pd.DataFrame(X, columns=['comment'])
# cleaned_df.to_csv('./cleaned_nltk_mbti.csv', index=False)
# print(cleaned_df.head())

########### 토크나이징
=======
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)
print(X)

>>>>>>> origin/main
token = Tokenizer()
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
print(tokened_X[:5])

<<<<<<< HEAD
# with open('./models/mbti_token.pickle', 'wb') as f:
#     pickle.dump(token, f)
=======
with open('./models/news_token.pickle', 'wb') as f:
    pickle.dump(token, f)
>>>>>>> origin/main

wordsize = len(token.word_index) + 1
print(wordsize)
print(token.index_word)

max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

X_pad = pad_sequences(tokened_X, max)
print(X_pad[:10])

<<<<<<< HEAD
# X_train, X_test, Y_train, Y_test = train_test_split(X_pad, onehot_Y, test_size=0.1)
# print(X_train.shape, Y_train.shape)
# print(X_test.shape, Y_test.shape)
#
# xy = X_train, X_test, Y_train, Y_test
# np.save('./crawling/mbti_data_max_{}_wordsize_{}'.format(max, wordsize), xy)
=======
X_train, X_test, Y_train, Y_test = train_test_split(X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('./crawling/news_data_max_{}_wordsize_{}'.format(max, wordsize), xy)
>>>>>>> origin/main

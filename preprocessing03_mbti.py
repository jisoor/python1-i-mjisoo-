import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
from tensorflow.keras.utils import to_categorical
from konlpy.tag import Okt # 가 아니라 영문 nltk


pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./crawling/final_all_mbti.csv')
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

for j in range(len(X)):
    words=[]
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)
print(X)

token = Tokenizer()
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
print(tokened_X[:5])

with open('./models/news_token.pickle', 'wb') as f:
    pickle.dump(token, f)

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

X_train, X_test, Y_train, Y_test = train_test_split(X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('./crawling/news_data_max_{}_wordsize_{}'.format(max, wordsize), xy)
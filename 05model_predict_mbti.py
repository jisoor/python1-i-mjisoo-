import pandas as pd
import numpy as np

from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model

pd.set_option('display.unicode.east_asian_width', True)
# data load
df = pd.read_csv('./crawling/naver_headline_news20211116.csv')
print(df.head())
print(df.info())

X = df['title']
Y = df['category']

#target labeling
with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
labeled_Y = encoder.transform(Y)
print(encoder.classes_)
label = encoder.classes_
print(labeled_Y[:5])
print(label)

onehot_Y = to_categorical(labeled_Y)
print(onehot_Y)
# 형태소 분리, 한 글자/불용어 제거
okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)

stopwords = pd.read_csv(
    './crawling/stopwords.csv',
    index_col=0)

for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)
print(X)


# titles tokenizing

with open('./models/news_token.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_X = token.texts_to_sequences(X)
print(tokened_X[:5])


for i in range(len(tokened_X)):
    if 23 < len(tokened_X[i]):
        tokened_X[i] = tokened_X[i][:23]
# padding
X_pad = pad_sequences(tokened_X, 23)
print(X_pad[:10])

# model.load
# model.predict(X_pad)
# predict과 onehot_Y와 비교


model = load_model('./models/news_category_classfication_model_0.7447780966758728.h5')
preds = model.predict(X_pad)
predicts = []
for pred in preds:
    predicts.append(label[np.argmax(pred)])

print(predicts)
df['predict'] = predicts
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 20)


df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] == df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 'O'
    else :
        df.loc[i, 'OX'] = 'X'
print(df.head(30))
print(df['OX'].value_counts()/len(df))

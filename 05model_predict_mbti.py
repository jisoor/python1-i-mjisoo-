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


X = 'jisoo is so kind and generous , passionate about her life'
Y = ['enfp','estp', 'esfp', 'entp', 'estj', 'esfj', 'enfj', 'entj', 'istj', 'isfj', 'infj', 'intj', 'istp', 'isfp', 'infp', 'intp']

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
import nltk
from nltk.tag import untag
from nltk.stem import WordNetLemmatizer

# ############# tokenizing
tokened_X = nltk.word_tokenize(X)
print(tokened_X)

############# pos 태깅 ( word_tokenize 먼저 해야함)
possed_X = nltk.pos_tag(tokened_X)
print(possed_X)

## lemmatzing  품사가 VB VBD VBG VBN VBP VBZ 애네만 골라서 동사 원형(lemmatizing)만들기
lm = WordNetLemmatizer()
for i in range(len(possed_X)):
    possed_X[i] = list(possed_X[i])
    if (possed_X[i][1] == "VB") | (possed_X[i][1] == "VBD") | (possed_X[i][1] == "VBG")| (possed_X[i][1] == "VBN")| (possed_X[i][1] == "VBP")| (possed_X[i][1] == "VBZ"):
        possed_X[i][0] = lm.lemmatize(possed_X[i], pos = 'v')

print(possed_X)

# 모두 untag 해서 리스트 만들기
for i in range(len(possed_X)):
    possed_X[i] = possed_X[i][0]

print('untagged\lists: ', possed_X )

# 한글자인 단어 빼기, stopwords에 관형사 빼기
# 그 다음 tokenizing 시작


#  불용어, 한글자제거
stopwords = pd.read_csv('./stopwords(Eng).csv')
stopwords = stopwords.T
stopwords.reset_index(inplace=True)
print(stopwords.info())
print(stopwords.columns)

# for j in range(len(X)):
#     words=[]
#     for i in range(len(X[j])):
#         if len(X[j][i]) > 1:
#             if X[j][i] not in list(stopwords['index']):
#                 words.append(X[j][i])
#     X[j] = ' '.join(words)

for i in range(len(possed_X)):
    words = []
    if len(possed_X[i]) > 1:
        if possed_X[i] not in list(stopwords['index']):
            words.append(possed_X[i])
X = ' '.join(words)
print('불용어 까지 제거한 X', X)



# titles tokenizing

with open('./models/mbti_token.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_X = token.texts_to_sequences(X)
print(tokened_X[:5])


for i in range(len(tokened_X)):
    if 1250 < len(tokened_X[i]):
        tokened_X[i] = tokened_X[i][:1250]
# padding
X_pad = pad_sequences(tokened_X, 1250)
print(X_pad[:10])

# model.load
# model.predict(X_pad)
# predict과 onehot_Y와 비교

############### d여기까지함 ##########################

model = load_model('./models/mbti_classification_model_0.2888889014720917.h5')
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

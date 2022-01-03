from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import pickle

# recompile... nltk로 ^^

pd.set_option('display.max_columns', 30)
df = pd.read_csv('./crawling/final_all_mbti.csv', index_col=False)
print(df.info())
print(df.columns)
# print(type(df))
# print(df.iloc[0, 1])


for i in range(6300):
    str_comment = df.iloc[i, 0]
    comment = re.compile('[^a-z|A-Z]').sub(' ', str_comment)
    df.iloc[i, 0] = comment


df.to_csv('./recompiled_all_mbti.csv', index=False)

print(df.head())

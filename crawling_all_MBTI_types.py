
mbti_type = ['enfp','estp', 'esfp', 'entp', 'estj', 'esfj', 'enfj', 'entj', 'istj', 'isfj', 'infj', 'intj', 'istp', 'isfp', 'infp', 'intp']

for m in mbti_type:
    url = 'https://www.personality-database.com/search?keyword={}'.format(m)

# 완성된 코드를 위의 코드로 씌우기.

# 저장할 때
df_mbti = pd.DataFrame(titles, columns=['title'])
df_mbti['comment'] = comments
df_mbti.to_csv('./crawling/{}/{}_{}번째프로필.csv'.format(m, m, i), index=False)



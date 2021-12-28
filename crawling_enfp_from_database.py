from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time

options = webdriver.ChromeOptions()
# options.add_argument('lang=ko_KR')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=options)

############## start ################
url = 'https://www.personality-database.com/search?keyword=enfp'
# 어떠카지? enfp로 검색한 총 몇개의 프로필이 있는지 모름(계속 밑으로 스크롤링 되고 숫자가 안나옴)
titles = []
comments = []
driver.get(url)
time.sleep(2)
next_button_xpath = '//*[@id="root"]/div/section/main/div[1]/div[2]/div[1]/div/div[1]/div[5]/div[1]/span[1]'
review_number_xpath = '//*[@id="root"]/div/section/main/div[1]/div[2]/div[1]/div/div[1]/div[5]/h2'

#  #리뷰갯수   형태는 Typology Comments 5437
for i in range(1,1001):  # enfp로 검색한 페이지의 총 article수가 몇개인지 모르므로 1000으로 설정. 30개씩
    try:
        time.sleep(1)
        title_xpath ='//*[@id="root"]/div/section/main/div[1]/div[2]/div[1]/div/div[1]/div[3]/a[{}]/div/div[2]/h2'.format(i)
        title = driver.find_element_by_xpath(title_xpath).text
        print(title)
        driver.find_element_by_xpath(title_xpath).click()
        time.sleep(5)
        driver.find_element_by_xpath(next_button_xpath).click()
        time.sleep(4)
        titles.append(title)
        review_number = driver.find_element_by_xpath(review_number_xpath).text
        review_number = int(review_number[18:])
        print(review_number)
        for j in range(1, review_number+1):  # 리뷰의 갯수, 10개씩
            try:
                comment_xpath = '//*[@id="root"]/div/section/main/div[1]/div[2]/div[1]/div/div[1]/div[5]/div[2]/div[{}]/div/div[2]/div[1]/div[1]'.format(j)
                comment = driver.find_element_by_xpath(comment_xpath).text
                comments.append(comment)
            except NoSuchElementException:
                comment_xpath_1 = '//*[@id="root"]/div/section/main/div[1]/div[2]/div[1]/div/div[1]/div[5]/div[2]/div[{}]/div/div[2]/div[1]/div'.format(j)
                try:
                    comment_1 = driver.find_element_by_xpath(comment_xpath_1).text
                    comments.append(comment_1)
                except:
                    print('not exist')
            except:
                continue
        driver.get(url)
        time.sleep(2)
        df_enfp = pd.DataFrame(titles, columns=['title'])
        df_enfp['comment'] = comments
        df_enfp.to_csv('./crawling/enfp_{},{}번째프로필.csv'.format(i, j), index=False)
    except:
        print('empty title')
        continue
    #스크롤 내리는 코드
 # 스크롤 내리는 코드  j는 10번 i는 30번


titles = []
comments =[]

print(len(titles))
driver.close()


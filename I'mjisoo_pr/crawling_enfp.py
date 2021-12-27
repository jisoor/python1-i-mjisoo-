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
df_titles = pd.DataFrame()
pages = [131, 131, 131, 101, 131, 77]
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
for l in [4,5]:
    titles = []
    for k in range(1,pages[l]): #406
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(l, k)
        driver.get(url)
        #time.sleep(0.01)
        for j in range(1,5):
            for i in range(1,6):
                try:
                    try:
                        title = driver.find_element_by_xpath(
                            '//*[@id="section_body"]/ul[{1}]/li[{0}]/dl/dt[2]/a'.format(i, j)).text
                        title = re.compile('[^가-힣|a-z|A-Z ]').sub(' ', title)
                        print(title)
                        titles.append(title)
                    except NoSuchElementException:
                        title = driver.find_element_by_xpath(
                            '//*[@id="section_body"]/ul[{1}]/li[{0}]/dl/dt/a'.format(i, j)).text
                        title = re.compile('[^가-힣|a-z|A-Z ]').sub(' ', title)
                        print(title)
                        titles.append(title)
                except StaleElementReferenceException:
                    driver.get(url)
                    print('StaleElementReferenceException')
                    time.sleep(1)
                    crawl_title()
                except:
                    print('error')
        if k % 50 == 0:
            df_section_titles = pd.DataFrame(titles, columns=['title'])
            df_section_titles['category'] = category[l]
            df_section_titles.to_csv('./crawling/news_{}_{}-{}.csv'.format(category[l], k-49, k), index=False)
            titles = []
    df_section_titles = pd.DataFrame(titles, columns=['title'])
    df_section_titles['category'] = category[l]
    df_section_titles.to_csv('./crawling/news_{}_remain.csv'.format(category[l]), index=False)


############## start ################
url = 'https://www.personality-database.com/search?keyword=enfp'
# 어떠카지? enfp로 검색한 총 몇개의 프로필이 있는지 모름(계속 밑으로 스크롤링 되고 숫자가 안나옴)
titles = []
driver.get(url)
next_button_xpath = '//*[@id="root"]/div/section/main/div[1]/div[2]/div[1]/div/div[1]/div[5]/div[1]/span[1]'
review_number = driver.find_element_by_xpath('//*[@id="root"]/div/section/main/div[1]/div[2]/div[1]/div/div[1]/div[5]/h2').text
review_number = int(review_number[19:])
 #리뷰갯수   형태는 Typology Comments 5437
for i in range(1,1001):  # enfp로 검색한 페이지의 총 article수가 몇개인지 모르므로 1000으로 설정.
    try:
        title = driver.find_element_by_xpath(
        '//*[@id="root"]/div/section/main/div[1]/div[2]/div[1]/div/div[1]/div[3]/a[{}]/div/div[2]/h2'.format(i).text)
        print(title)
        titles.append(title)
        driver.find_element_by_xpath(title).click()
        next_button_xpath.click()
        for j in range(1, review_number+1 ):  # 리뷰의 갯수
            try:
                if
                comment = driver.find_element_by_xpath(
                    ('//*[@id="root"]/div/section/main/div[1]/div[2]/div[1]/div/div[1]/div[5]/div[2]/div[1]/div/div[2]/div[1]/div'))
            except NoSuchElementException:




    except:
        print('empty title')
        continue











df_titles.to_csv('./crawling/naver_news.csv')
print(len(titles))
driver.close()


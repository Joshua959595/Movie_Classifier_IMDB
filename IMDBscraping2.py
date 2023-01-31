# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 21:06:15 2019

@author: kds @eddited : Joshua J Seo
"""
# wd: C:\Users\82104\AppData\Local\Programs\Python\Python39

from selenium import webdriver
from bs4 import BeautifulSoup
import time, random
import pandas as pd
import openpyxl

# IMDB 리뷰 수집 함수

def imdb_get_review(serching_movie_title_id):
    # 크롬 브라우저 헤더 정보를 옵션으로 추가
    options = webdriver.ChromeOptions()
    # 다음 'options.add_argument'의 주석처리를 해제하면, 브라우저가 활성화 되지 않은 상태에서 웹 크롤링 수행
    # options.add_argument('headless')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36")
    
    # 크롬 브라우저의 드라이버 경로 설정 및 옵션 적용
    driver = webdriver.Chrome(r'C:\Users\82104\AppData\Local\Programs\Python\Python39\chromedriver.exe', options=options)

    # serching_movie_title_id : 리뷰를 확인할 영화의 IMDB 코드 값
    imdb_review_page_url = "http://www.imdb.com/title/tt"+str(serching_movie_title_id)+"/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc"

    # 크롬 브라우저를 실행하여 웹 페이지 접속
    driver.get(imdb_review_page_url)
    # 브라우저 로딩 완료까지 10초 대기
    driver.implicitly_wait(10)

    # 리뷰 데이터 전체 확인
    for i in range(15): #1p:roughly 25comments
        try:
            driver.find_element_by_xpath("//*[@id='load-more-trigger']").click()


        except:
            # 마지막 리뷰의 스크린 샷 이미지 저장
            driver.save_screenshot(str(serching_movie_title_id)+'_screen.png')
            # 리뷰의 전체 로딩이 완료되어 더 이상 클릭할 속성이 없는 경우, break 종료"""
            break


    # 웹페이지 파싱
    imdb_review_virtual_page = driver.page_source
    imdb_review_pages = BeautifulSoup(imdb_review_virtual_page, 'html.parser')


    # 드라이브 종료, 크롬 브라우저는 로컬 컴퓨터의 메모리를 많이 사용하기 때문에, 페이지 파싱까지 완료되면 바로 종료
    driver.quit()


    # 리뷰별 타이틀, 날짜, 리뷰내용 저장을 위한 리스트 생성
    imdb_review_titles = []
    imdb_review_dates = []
    imdb_review_contents = []


    # 파싱 된 웹 페이지에서 데이터 선택, 각각 해당하는 리스트 변수에 저장하기
    for review_page in imdb_review_pages.find_all("div", {"class":"lister-item-content"}):
        title_tamp = review_page.find("a", {"class":"title"}).get_text()
        imdb_review_titles.append(title_tamp)

        date_tamp = review_page.find("span", {"class":"review-date"}).get_text()
        imdb_review_dates.append(date_tamp)

        content_tamp = review_page.find("div", {"class":"content"}).get_text()
        imdb_review_contents.append(content_tamp)

    return imdb_review_titles, imdb_review_dates, imdb_review_contents


    

if __name__ == "__main__":
    # Avengers: Infinity War (2018) - 4154756
    # Gisaengchung = 6751668
    # D-war = 0372873 (0으로시작할때는 문자열로)
    reviews = imdb_get_review(6751668)
    
    df = pd.DataFrame(reviews)#columns = ["titles", "dates", "contents"]
    df = df.transpose()
    df.to_excel('parasite.xlsx')
    print('끝!')

# 영화코드 입력
# 데이터 개수 확정
# 엑셀 파일 이름 

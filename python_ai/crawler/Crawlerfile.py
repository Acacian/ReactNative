from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import time
import random
import re

# URL 설정
url = "https://booktoki347.com/novel?book=%EC%84%B1%EC%9D%B8%EC%86%8C%EC%84%A4"

# 사용자 데이터 디렉토리
user_data_dir = r"C:\chromeCookie_new"

# Chrome 실행 및 URL 접속
print(f"Chrome 브라우저를 실행하고 {url}로 이동합니다. Cloudflare 검증을 수동으로 완료해주세요.")
subprocess.Popen(f'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="{user_data_dir}" {url}')

# 스크립트 시작 전 대기 시간 (초)
INITIAL_WAIT_TIME = 20
print(f"{INITIAL_WAIT_TIME}초 동안 Cloudflare 검증을 완료해주세요. 그 후 크롤링을 시작합니다.")
time.sleep(INITIAL_WAIT_TIME)

# 옵션 설정
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# WebDriver 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=option)
driver.maximize_window()

# 추가 헤더 설정
driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {"headers": {"Accept-Language": "en-US,en;q=0.9"}})

def random_sleep(min_time=3, max_time=7):
    time.sleep(random.uniform(min_time, max_time))

# 여기서부터 크롤링 로직을 시작합니다.
print("크롤링을 시작합니다...")

def crawl_novel(novel_url, novel_title):
    driver.get(novel_url)
    random_sleep()
    
    while True:
        try:
            chapters = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.item-subject"))
            )
            
            for chapter in chapters:
                chapter_title = chapter.text
                if not re.search(r'\d+화', chapter_title):
                    continue
                
                print(f"크롤링 중: {novel_title} - {chapter_title}")
                chapter.click()
                random_sleep()
                
                content = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.x229f860fec"))
                )
                
                # 여기서 content.text를 저장하거나 처리합니다
                with open(f"{novel_title} - {chapter_title}.txt", "w", encoding="utf-8") as f:
                    f.write(content.text)
                
                driver.back()
                random_sleep()
            
            next_page = driver.find_elements(By.CSS_SELECTOR, "a.next")
            if not next_page:
                break
            next_page[0].click()
            random_sleep()
        except Exception as e:
            print(f"에러 발생: {e}")
            break

print("페이지로 이동합니다...")
driver.get(url)
random_sleep()

try:
    novels = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.in-lable a"))
    )
    
    for novel in novels:
        novel_title = novel.find_element(By.CSS_SELECTOR, "span.title.white").text
        novel_url = novel.get_attribute("href")
        print(f"소설 크롤링 시작: {novel_title}")
        crawl_novel(novel_url, novel_title)
        driver.get(url)  # 소설 목록 페이지로 돌아가기
        random_sleep()
        
except Exception as e:
    print(f"에러 발생: {e}")
    print("현재 페이지 소스:")
    print(driver.page_source[:1000])  # 처음 1000자만 출력

print("작업이 완료되었습니다. 브라우저를 닫으려면 Enter 키를 누르세요...")
input()

driver.quit()
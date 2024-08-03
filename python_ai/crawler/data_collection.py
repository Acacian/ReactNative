import time
import random
import json
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NovelCrawler:
    BASE_URL = "https://booktoki347.com"
    CRAWLED_NOVELS_FILE = "/app/downloads/crawled_novels.json"
    COMBINED_DATA_FILE = "/app/downloads/combined_data.txt"

    def __init__(self):
        self.driver = None

    def setup(self):
        logger.info("Setting up Chrome driver...")
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--start-maximized')
        options.add_argument('--headless')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--user-data-dir=/tmp/chrome-user-data')
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        logger.info("Chrome driver setup complete.")

    def initial_site_access(self):
        logger.info(f"Accessing base URL: {self.BASE_URL}")
        self.driver.get(self.BASE_URL)
        time.sleep(10)  # Cloudflare 우회를 위한 대기

        # "로봇이 아닙니다" 체크박스 클릭 (있는 경우)
        try:
            checkbox = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="checkbox"]'))
            )
            if checkbox:
                checkbox.click()
                time.sleep(2)
        except:
            logger.info("No checkbox found or already verified.")

        time.sleep(5)  # 추가 대기

    def navigate_to_novel_list(self):
        novel_list_url = f"{self.BASE_URL}/novel?book=%EC%84%B1%EC%9D%B8%EC%86%8C%EC%84%A4&page=1"
        self.driver.get(novel_list_url)
        time.sleep(5)

        # 소설 목록이 로드되었는지 확인
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.img-item"))
            )
            logger.info("Novel list page loaded successfully.")
        except:
            logger.error("Failed to load novel list page.")
            raise

    def get_novel_links(self):
        self.navigate_to_novel_list()
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        novel_elements = soup.select("div.img-item a[href^='/novel/']")
        links = [(element.img['alt'], self.BASE_URL + element['href']) for element in novel_elements if element.img]
        logger.info(f"Found {len(links)} novel links")
        if len(links) == 0:
            logger.warning("No links found. Check if the website structure has changed.")
        return links

    def get_chapter_links(self, novel_url):
        logger.info(f"Accessing novel URL: {novel_url}")
        self.driver.get(novel_url)
        time.sleep(5)
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        chapter_elements = soup.select("select[name='wr_id'] option")
        chapter_links = [(option.text, f"{novel_url}/{option['value']}") for option in chapter_elements]
        logger.info(f"Found {len(chapter_links)} chapters")
        return chapter_links

    def get_chapter_content(self, chapter_url):
        logger.info(f"Accessing chapter URL: {chapter_url}")
        self.driver.get(chapter_url)
        time.sleep(5)
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        content_element = soup.select_one("#novel_content")
        if content_element:
            paragraphs = content_element.find_all('p')
            content = "\n".join([p.text for p in paragraphs])
            logger.info(f"Successfully retrieved content. Length: {len(content)} characters")
            return content
        else:
            logger.error("Could not find content element")
            return ""

    def load_crawled_novels(self):
        logger.info("Loading previously crawled novels")
        try:
            with open(self.CRAWLED_NOVELS_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.info("No existing crawled novels file found. Starting fresh.")
            return {}

    def save_crawled_novels(self, crawled_novels):
        logger.info(f"Saving crawled novels information to {self.CRAWLED_NOVELS_FILE}")
        with open(self.CRAWLED_NOVELS_FILE, 'w') as f:
            json.dump(crawled_novels, f)
        logger.info("Crawled novels information saved successfully")

    def crawl_novels(self):
        self.initial_site_access()
        crawled_novels = self.load_crawled_novels()
        all_content = []
        
        try:
            novel_links = self.get_novel_links()
            
            for novel_title, novel_url in novel_links:
                if novel_title in crawled_novels:
                    logger.info(f"Skipping already crawled novel: {novel_title}")
                    continue
                
                logger.info(f"Crawling novel: {novel_title}")
                chapter_links = self.get_chapter_links(novel_url)
                novel_content = []
                
                for chapter_title, chapter_url in chapter_links[:5]:  # 테스트를 위해 처음 5개 챕터만 크롤링
                    chapter_content = self.get_chapter_content(chapter_url)
                    novel_content.append((chapter_title, chapter_content))
                    all_content.append(f"{novel_title} - {chapter_title}\n\n{chapter_content}\n\n{'='*50}\n\n")
                    logger.info(f"Crawled chapter: {chapter_title}")
                    time.sleep(random.uniform(1, 3))
                
                novel_file_path = f"/app/downloads/{novel_title}.txt"
                logger.info(f"Saving novel content to: {novel_file_path}")
                with open(novel_file_path, 'w', encoding='utf-8') as f:
                    for chapter_title, chapter_content in novel_content:
                        f.write(f"{chapter_title}\n\n{chapter_content}\n\n{'='*50}\n\n")
                logger.info(f"Novel content saved successfully: {novel_title}")
                
                crawled_novels[novel_title] = len(chapter_links)
                self.save_crawled_novels(crawled_novels)
                
                logger.info(f"Completed crawling novel: {novel_title}")
                time.sleep(random.uniform(3, 5))
            
            # 모든 내용을 하나의 파일에 저장
            logger.info(f"Saving all crawled content to: {self.COMBINED_DATA_FILE}")
            with open(self.COMBINED_DATA_FILE, 'w', encoding='utf-8') as f:
                f.writelines(all_content)
            logger.info("All crawled content saved successfully")
            
        except Exception as e:
            logger.error(f"Error in crawl_novels: {str(e)}", exc_info=True)
            raise

    def cleanup(self):
        if self.driver:
            self.driver.quit()
        logger.info("Crawling process completed")

def main():
    crawler = NovelCrawler()
    try:
        crawler.setup()
        crawler.crawl_novels()
    except Exception as e:
        logger.error(f"An error occurred during the crawling process: {e}")
    finally:
        crawler.cleanup()

if __name__ == "__main__":
    main()
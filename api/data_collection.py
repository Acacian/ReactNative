import os
import time
import logging
import zipfile
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_all_zips(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(root)
                logger.info(f"Extracted: {file_path}")

def read_text_files(directory):
    texts = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                    texts.append(text)
                    logger.info(f"Read file: {os.path.join(root, file)}, Length: {len(text)} characters")
    return texts

def fetch_novel_content(novel_id, max_pages=5, timeout=300):
    content = []
    base_url = f"https://booktoki346.com/novel/{novel_id}"
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    logger.info(f"Setting up Chrome driver for novel ID: {novel_id}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        for page in range(1, max_pages + 1):
            url = f"{base_url}?book=%EC%84%B1%EC%9D%B8%EC%86%8C%EC%84%A4&spage={page}"
            logger.info(f"Navigating to URL: {url}")
            driver.get(url)
            
            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "novel-detail-body")))
                logger.info(f"Page {page} loaded successfully")
            except TimeoutException:
                logger.warning(f"Timeout waiting for page {page} to load. Skipping this novel.")
                return content

            soup = BeautifulSoup(driver.page_source, "html.parser")
            novel_content = soup.find("div", class_="novel-detail-body")

            if novel_content:
                text = novel_content.get_text().strip()
                content.append(text)
                logger.info(f"Collected content from page {page}, Length: {len(text)} characters")
            else:
                logger.warning(f"No content found on page {page}")
                break

            time.sleep(2)

    except Exception as e:
        logger.exception(f"Error fetching content for novel ID {novel_id}: {e}")
    finally:
        driver.quit()

    return content

def get_random_novel_ids(start_id, end_id, count):
    return random.sample(range(start_id, end_id + 1), count)

if __name__ == "__main__":
    extract_all_zips('/app/Korean_SNS_DATA')
    existing_data = read_text_files('/app/Korean_SNS_DATA')
    logger.info(f"Read {len(existing_data)} existing text files")

    start_id = 13510000
    end_id = 13520000
    num_novels = 50
    novel_ids = get_random_novel_ids(start_id, end_id, num_novels)

    crawled_data = []
    total_chars = sum(len(text) for text in existing_data)
    logger.info(f"Initial total characters: {total_chars}")

    while total_chars < 1000000:  # 최소 100만 글자를 목표로 설정
        for novel_id in novel_ids:
            novel_content = fetch_novel_content(novel_id)
            if novel_content:
                crawled_data.extend(novel_content)
                total_chars += sum(len(text) for text in novel_content)
                logger.info(f"Crawled novel ID {novel_id}: {len(novel_content)} pages, Total characters: {total_chars}")
            else:
                logger.warning(f"Skipped novel ID {novel_id}: No content found")
            
            if total_chars >= 1000000:
                logger.info("Sufficient data collected. Stopping crawling.")
                break
        
        if total_chars < 1000000:
            logger.info("Not enough data collected. Getting new novel IDs.")
            novel_ids = get_random_novel_ids(start_id, end_id, num_novels)
    
    logger.info(f"Crawled {len(crawled_data)} new content pieces")

    all_data = existing_data + crawled_data

    with open("/app/combined_data.txt", "w", encoding="utf-8") as f:
        for item in all_data:
            f.write(f"{item}\n\n---\n\n")
    
    logger.info(f"Total {len(all_data)} items saved to combined_data.txt")

    data_size = os.path.getsize("/app/combined_data.txt") / (1024 * 1024)
    logger.info(f"Total data size: {data_size:.2f} MB")

    # 파일 내용 샘플 로깅
    with open("/app/combined_data.txt", "r", encoding="utf-8") as f:
        sample = f.read(1000)  # 처음 1000자만 읽기
        logger.info(f"Sample of combined_data.txt:\n{sample}")

    logger.info("Data collection completed")
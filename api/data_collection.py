import os
import time
import logging
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_all_zips(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(root)
                logging.info(f"Extracted: {file_path}")

def read_text_files(directory):
    texts = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    texts.append(f.read())
    return texts

def fetch_novel_content(novel_id, max_pages=5, timeout=300):
    content = []
    base_url = f"https://booktoki346.com/novel/{novel_id}"
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    logging.info(f"Setting up Chrome driver for novel ID: {novel_id}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        for page in range(1, max_pages + 1):
            url = f"{base_url}?book=%EC%84%B1%EC%9D%B8%EC%86%8C%EC%84%A4&spage={page}"
            logging.info(f"Navigating to URL: {url}")
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "novel-detail-body")))
            logging.info(f"Page {page} loaded successfully")

            soup = BeautifulSoup(driver.page_source, "html.parser")
            novel_content = soup.find("div", class_="novel-detail-body")

            if novel_content:
                text = novel_content.get_text().strip()
                content.append(text)
                logging.info(f"Collected content from page {page}")
            else:
                logging.warning(f"No content found on page {page}")

            time.sleep(2)  # 서버에 부담을 주지 않기 위한 딜레이

    except Exception as e:
        logging.exception(f"Error fetching content for novel ID {novel_id}: {e}")
    finally:
        driver.quit()

    return content

if __name__ == "__main__":
    # ZIP 파일 압축 해제
    extract_all_zips('/app/Korean_SNS_DATA')

    # 기존 데이터 읽기
    existing_data = read_text_files('/app/Korean_SNS_DATA')
    logging.info(f"Read {len(existing_data)} existing text files")

    # 새로운 데이터 크롤링
    novel_ids = [13510249, 13510250, 13510251]  # 예시 ID들, 필요에 따라 수정
    crawled_data = []
    for novel_id in novel_ids:
        novel_content = fetch_novel_content(novel_id)
        crawled_data.extend(novel_content)
    
    logging.info(f"Crawled {len(crawled_data)} new content pieces")

    # 모든 데이터 결합
    all_data = existing_data + crawled_data

    # 결합된 데이터 저장
    with open("/app/combined_data.txt", "w", encoding="utf-8") as f:
        for item in all_data:
            f.write(f"{item}\n\n---\n\n")
    
    logging.info(f"Total {len(all_data)} items saved to combined_data.txt")
    logging.info("Data collection completed")
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

def bypass_captcha(driver):
    try:
        captcha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captcha-element"))
        )
        driver.execute_script("arguments[0].remove();", captcha)
        logger.info("Captcha bypassed")
    except:
        logger.info("No captcha found or unable to bypass")

def navigate_to_random_novel(driver):
    try:
        driver.get("https://booktoki347.com")
        bypass_captcha(driver)
        
        adult_novel_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/novel?book=%EC%84%B1%EC%9D%B8%EC%86%8C%EC%84%A4')]"))
        )
        adult_novel_link.click()
        
        novels = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list-item"))
        )
        if novels:
            random.choice(novels).click()
        else:
            logger.warning("No novels found")
            return False
        
        return True
    except Exception as e:
        logger.exception(f"Error navigating to novel: {e}")
        return False

def fetch_novel_content(max_chapters=50, timeout=300):
    content = []
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    logger.info("Setting up Chrome driver")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        if not navigate_to_random_novel(driver):
            return content

        for chapter in range(1, max_chapters + 1):
            try:
                chapter_links = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), '화')]"))
                )
                if chapter_links:
                    random.choice(chapter_links).click()
                else:
                    logger.warning("No chapter links found")
                    break

                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "novel_content")))
                logger.info(f"Chapter {chapter} loaded successfully")

                soup = BeautifulSoup(driver.page_source, "html.parser")
                novel_content = soup.find("div", id="novel_content")

                if novel_content:
                    paragraphs = novel_content.find_all("p")
                    chapter_text = "\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                    content.append(chapter_text)
                    logger.info(f"Collected content from chapter {chapter}, Length: {len(chapter_text)} characters")
                else:
                    logger.warning(f"No content found in chapter {chapter}")
                    break

                time.sleep(2)

            except Exception as e:
                logger.exception(f"Error fetching chapter {chapter}: {e}")
                break

    except Exception as e:
        logger.exception(f"Error fetching content: {e}")
    finally:
        driver.quit()

    return content

if __name__ == "__main__":
    extract_all_zips('/app/Korean_SNS_DATA')
    existing_data = read_text_files('/app/Korean_SNS_DATA')
    logger.info(f"Read {len(existing_data)} existing text files")

    crawled_data = []
    total_chars = sum(len(text) for text in existing_data)
    logger.info(f"Initial total characters: {total_chars}")

    while total_chars < 1000000:  # 최소 100만 글자를 목표로 설정
        novel_content = fetch_novel_content()
        if novel_content:
            crawled_data.extend(novel_content)
            total_chars += sum(len(text) for text in novel_content)
            logger.info(f"Crawled new content: {len(novel_content)} chapters, Total characters: {total_chars}")
        else:
            logger.warning("No content found in this attempt")
        
        if total_chars >= 1000000:
            logger.info("Sufficient data collected. Stopping crawling.")
            break

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
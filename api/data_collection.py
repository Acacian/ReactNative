import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_tweets(query, max_tweets=100, timeout=300):  # 5분 타임아웃
    tweet_texts = []
    url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    logging.info(f"Setting up Chrome driver for query: {query}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        logging.info(f"Navigating to URL: {url}")
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logging.info("Page loaded successfully")

        start_time = time.time()
        while len(tweet_texts) < max_tweets:
            if time.time() - start_time > timeout:
                logging.warning(f"Timeout reached for query: {query}")
                break

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            tweets = soup.find_all("div", {"data-testid": "tweet"})

            for tweet in tweets:
                tweet_text = tweet.find("div", {"lang": "ko"})
                if tweet_text:
                    tweet_texts.append(tweet_text.get_text())
                if len(tweet_texts) >= max_tweets:
                    break

            logging.info(f"Collected {len(tweet_texts)} tweets for query '{query}'")

    except Exception as e:
        logging.exception(f"Error fetching tweets for query '{query}': {e}")
    finally:
        driver.quit()

    return tweet_texts

if __name__ == "__main__":
    queries = ["감정", "기쁨", "슬픔", "화남", "행복", "분노", "불안", "걱정", "희망", "사랑"]
    with open("/app/collected_data.txt", "w", encoding="utf-8") as file:
        for query in queries:
            logging.info(f"Starting collection for query: {query}")
            tweets = fetch_tweets(query)
            for tweet in tweets:
                file.write(f"{query}: {tweet}\n")
            logging.info(f"Finished collecting tweets for '{query}'")
    
    logging.info("Data collection completed")
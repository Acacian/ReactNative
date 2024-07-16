import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

def fetch_tweets(query, max_tweets=100):
    tweet_texts = []
    url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"
    
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-logging")
    options.add_argument("--single-process")
    options.add_argument("--data-path=/tmp/data-path")
    options.add_argument("--homedir=/tmp")
    options.add_argument("--disk-cache-dir=/tmp/cache-dir")
    
    driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        scroll_pause_time = 2
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while len(tweet_texts) < max_tweets:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            tweets = soup.find_all("div", {"data-testid": "tweet"})

            for tweet in tweets:
                tweet_text = tweet.find("div", {"lang": "ko"})
                if tweet_text:
                    tweet_texts.append(tweet_text.get_text())
                if len(tweet_texts) >= max_tweets:
                    break
        
        logging.info(f"Fetched {len(tweet_texts)} tweets for query '{query}'")

    except Exception as e:
        logging.error(f"Error fetching tweets for query '{query}': {e}")
    finally:
        driver.quit()

    return tweet_texts

if __name__ == "__main__":
    with open("/app/collected_data.txt", "w", encoding="utf-8") as file:
        for query in ["감정", "기쁨", "슬픔", "화남"]:
            tweets = fetch_tweets(query)
            for tweet in tweets:
                file.write(f"{tweet}\n")

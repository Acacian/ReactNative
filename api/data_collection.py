import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def fetch_tweets(query, max_tweets=100):
    tweet_texts = []
    url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    wait = WebDriverWait(driver, 20)

    tweet_xpath = "//div[@data-testid='tweet']"
    try:
        tweets = wait.until(EC.presence_of_all_elements_located((By.XPATH, tweet_xpath)))
        for tweet in tweets[:max_tweets]:
            tweet_text = tweet.find_element_by_xpath(".//div[@class='css-901oao r-1nao33i r-1q142lx r-1cwl3u0 r-1d4mawv r-1udh08x r-15d164r r-6koalj r-16dba41 r-1wbh5a2 r-1guathk r-1ny4l3l']").text
            tweet_texts.append(tweet_text)
    except TimeoutException:
        print(f"Timeout while fetching tweets for query '{query}'. Collected tweets so far: {len(tweet_texts)}")
    finally:
        driver.quit()

    return tweet_texts

if __name__ == "__main__":
    queries = ["감정", "기쁨", "슬픔", "화남"]
    with open("/app/collected_data.txt", "w", encoding="utf-8") as file:
        for query in queries:
            tweets = fetch_tweets(query)
            for tweet in tweets:
                file.write(f"{tweet}\n")

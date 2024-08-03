import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import BaseCase
import random
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CloudflareBypass(BaseCase):
    def setUp(self):
        options = uc.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = uc.Chrome(options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        super().setUp()

    def simulate_human_behavior(self):
        # 마우스 움직임 시뮬레이션
        self.driver.execute_script("""
            var event = new MouseEvent('mousemove', {
                'view': window,
                'bubbles': true,
                'cancelable': true,
                'clientX': Math.floor(Math.random() * window.innerWidth),
                'clientY': Math.floor(Math.random() * window.innerHeight)
            });
            document.dispatchEvent(event);
        """)
        time.sleep(random.uniform(0.5, 2))

    def get_novel_links(self, url):
        self.driver.get(url)
        self.simulate_human_behavior()
        
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            selectors = [
                "div.img-item a[href^='/novel/']",
                "a[href*='novel']",
                "//a[contains(@href, 'novel')]"
            ]
            
            novel_elements = []
            for selector in selectors:
                try:
                    if selector.startswith("//"):
                        novel_elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        novel_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if novel_elements:
                        break
                except Exception as e:
                    logger.warning(f"Selector {selector} failed: {str(e)}")
            
            if not novel_elements:
                raise Exception("No novel links found with any selector")
            
            links = [(element.find_element(By.TAG_NAME, 'img').get_attribute('alt'), element.get_attribute('href')) 
                     for element in novel_elements]
            logger.info(f"Found {len(links)} novel links")
            return links
        except Exception as e:
            logger.error(f"Error finding novel links: {str(e)}")
            logger.debug(f"Page source: {self.driver.page_source}")
            raise

    def crawl_novels(self, base_url):
        try:
            novel_links = self.get_novel_links(base_url)
            for title, url in novel_links[:5]:  # 처음 5개 소설만 크롤링
                logger.info(f"Crawling novel: {title}")
                self.driver.get(url)
                self.simulate_human_behavior()
                # 여기에 각 소설 페이지에서 데이터를 추출하는 로직 추가
                time.sleep(random.uniform(3, 7))
        except Exception as e:
            logger.error(f"Error in crawl_novels: {str(e)}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    bypass = CloudflareBypass()
    bypass.setUp()
    bypass.crawl_novels("https://booktoki347.com/novel?book=%EC%84%B1%EC%9D%B8%EC%86%8C%EC%84%A4&page=1")
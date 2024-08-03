import asyncio
from data_collection import NovelCrawler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting the novel crawling process")
    crawler = NovelCrawler()
    
    try:
        await crawler.setup()
        await crawler.crawl_novels()
        logger.info("Novel crawling process completed successfully")
    except Exception as e:
        logger.error(f"An error occurred during the crawling process: {e}")
    finally:
        await crawler.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
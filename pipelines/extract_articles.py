from typing import List, Dict, Any
import json
from zenml import step, pipeline
from scrapper.webscraper import WebScraperFactoryImpl
from loguru import logger

@step
def get_data(urls: List[str]) -> List[Dict[str, Any]]:
    logger.info("Started Scraping data....")
    articles = []
    scraperFactory = WebScraperFactoryImpl()
    
    for url in urls:
        try:
            scraper = scraperFactory.get_scraper(url)
            data = scraper.scrape(url)
            logger.info(f"scraped data from url : {url}")
            articles.append(data)
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")

    print(f"Scraped {len(articles)} articles.")
    return articles


@step
def save_to_json(data: List[Dict[str, Any]], filename: str = 'article_data.json') -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {str(e)}")


@pipeline(enable_cache=False)
def extract_articles(urls: List[str]) -> None:
    logger.info("Going to Extract the Urls Data ....")
    articles = get_data(urls)
    save_to_json(articles)
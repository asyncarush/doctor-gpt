from typing import List, Dict, Any

import json
from zenml import step, pipeline
from model.articles import Articles
from scrapper.webscraper import WebScraperFactoryImpl
from loguru import logger


from database.database import db

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

@step
def save_to_data_warehouse(articles: List[Articles]):
    collection = db['articles']
    try:
        
        # get all existing urls

        existing_blogs = [ doc['url'] for doc in collection.find({}, {'url' : 1}) ]
        
        
        new_articles = [ article for article in articles if article.url not in existing_blogs ]

        if not new_articles:
            logger.info("No new articles to save")
            return

        # Convert each Articles object to a dictionary
        articles_dicts = [article.dict() for article in new_articles]
        collection.insert_many(articles_dicts)
        logger.info(f"Successfully saved {len(articles_dicts)} articles to MongoDB")
    except Exception as e:
        logger.error(f"Error saving to data warehouse: {str(e)}")
        raise  # Re-raise the exception to fail the pipeline

@pipeline(enable_cache=False)
def extract_articles(urls: List[str]) -> None:
    logger.info("Going to Extract the Urls Data ....")
    articles = get_data(urls)
    logger.info("Saving Data to warehouse")
    save_to_data_warehouse(articles)


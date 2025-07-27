from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from zenml import logger
from zenml.steps import step
from loguru import logger

class WebScraper(ABC):
    @abstractmethod
    def scrape(self, url: str) -> str:
        pass

class WebScraperFactory(ABC):
    @abstractmethod
    def get_scraper(self, url: str) -> WebScraper:
        pass


class WebScraperFactoryImpl(WebScraperFactory):
    def get_scraper(self, url: str) -> WebScraper:
        if "health.harvard.edu" in url:
            logger.info(f"Retured Harved Scraper for {url}")
            return HarvardScraper()
        else:
            raise ValueError(f"No scraper found for URL: {url}")

class HarvardScraper(WebScraper):
    def scrape(self, url: str) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
        }
        articles = []

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
           
            soup = BeautifulSoup(response.content, 'html.parser')

            title_tag = soup.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else 'No title found'
           
            time_tag = soup.find("time")
            time_content = datetime.strptime(time_tag.get_text(strip=True), '%B %d, %Y').isoformat() if time_tag else ''
           
            div_content_tag = soup.find("div", class_="content-repository-content")
            content = div_content_tag.get_text(strip=True) if div_content_tag else ''
           
            article = {
                'title': title,
                'url': url,
                'publication_date': time_content,
                'content': content,
                'extracted_at': datetime.now().isoformat()
            }
            
            logger.info(f"Scrapping data for {url} is done ✅")
            
            return article

        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")   
    
        return articles
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from zenml import step, pipeline

@step
def extract_articles(urls: List[str]) -> List[Dict[str, Any]]:
    """Extract article content from a list of URLs."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
    }
    articles = []
    for url in urls:
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
            articles.append({
                'title': title,
                'url': url,
                'publication_date': time_content,
                'content': content,
                'extracted_at': datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
    return articles

@step
def process_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [article for article in articles if article is not None]

@step
def save_articles(articles: List[Dict[str, Any]]) -> None:
    import json
    from datetime import datetime
    if not articles:
        print("No articles to save.")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"articles_{timestamp}.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved {len(articles)} articles to {filename}")
    except Exception as e:
        print(f"Error saving articles: {str(e)}")


@pipeline
def web_scraping_pipeline(urls: List[str]) -> None:
    articles = extract_articles(urls)
    processed_articles = process_articles(articles)
    save_articles(processed_articles)

if __name__ == "__main__":
    urls = [
        "https://www.health.harvard.edu/blog/want-to-cool-down-14-ideas-to-try-202408073065",
        "https://www.health.harvard.edu/blog/wildfires-how-to-cope-when-smoke-affects-air-quality-and-health-202306232947"
    ]
    web_scraping_pipeline(urls)
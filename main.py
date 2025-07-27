from pipelines.extract_articles import extract_articles

if __name__ == "__main__":
    urls = [
        "https://www.health.harvard.edu/blog/want-to-cool-down-14-ideas-to-try-202408073065",
        "https://www.health.harvard.edu/blog/wildfires-how-to-cope-when-smoke-affects-air-quality-and-health-202306232947",
        "https://www.health.harvard.edu/blog/what-is-a-psa-test-and-how-is-it-used-202507143101"
    ]
extract_articles(urls=urls)


    
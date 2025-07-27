from pymongo import MongoClient
from loguru import logger

try:
    client = MongoClient("mongodb://llm_engineering:llm_engineering@127.0.0.1:27017")
    db = client['doctor-gpt']
except Exception as e:
    logger.info(f"Error connecting Mongodb database : {e}")



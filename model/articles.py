from pydantic import BaseModel
from datetime import datetime

#Schema for Articles
class Articles(BaseModel):
    title : str
    url : str
    publication_date : str
    content : str
    extracted_at : datetime

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)
db = client['webscraping']
collection_scrapes = db['scrapes']

def obtener_ultimo_scraping():
    """Obtiene el último scraping guardado."""
    return collection_scrapes.find_one({}, sort=[('scraped_at', -1)])

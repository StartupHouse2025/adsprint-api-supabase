import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['webscraping']

# Colecciones
collection_scrapes = db['scrapes']
collection_titulos_copies = db['titulos_copies']
collection_scripts = db['scripts']

def obtener_datos_para_script():
    """Busca los datos necesarios para configurar el guión"""

    scraping = collection_scrapes.find_one({}, sort=[('scraped_at', -1)])
    titulos_copies = collection_titulos_copies.find_one({}, sort=[('generated_at', -1)])

    if not scraping or not titulos_copies:
        return None

    return {
        'url': scraping.get('url'),
        'titulos': titulos_copies.get('titulos', []),
        'copies': titulos_copies.get('copies', []),
        'publicos_objetivos': titulos_copies.get('publicos_objetivos', [])
    }

def guardar_script_mongo(script_text):
    """Guarda el guión generado en MongoDB"""
    doc = {
        'script': script_text,
        'saved_at': db.client.SERVER_INFO.get('localTime')
    }
    collection_scripts.insert_one(doc)

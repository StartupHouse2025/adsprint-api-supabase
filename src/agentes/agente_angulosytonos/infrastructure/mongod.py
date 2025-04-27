import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['webscraping']
scripts_collection = db['scripts']

def guardar_script_mongo(titulo, descripcion, publico_objetivo, script):
    scripts_collection.insert_one({
        'titulo': titulo,
        'descripcion': descripcion,
        'publico_objetivo': publico_objetivo,
        'guion': script,
        'created_at': datetime.utcnow()
    })

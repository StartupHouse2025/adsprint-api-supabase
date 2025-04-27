from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['webscraping']
collection_tituloscopies = db['titulos_copies']

def guardar_tituloscopies_mongo(titulos, copies, publicos_objetivos, url):
    doc = {
        'titulos': titulos,
        'copies': copies,
        'publicos': publicos_objetivos,
        'url': url
    }
    collection_tituloscopies.insert_one(doc)

def obtener_ultimo_tituloscopies():
    doc = collection_tituloscopies.find_one({}, sort=[('_id', -1)])
    return doc

from flask import Blueprint, request, jsonify
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import requests
from PIL import Image
from io import BytesIO
from pymongo import MongoClient
from datetime import datetime
import os

# Blueprint
agente_scraping_bp = Blueprint('agente_scraping', __name__)

# Mongo
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['webscraping']
collection_scrapes = db['scrapes']
collection_selecciones = db['selecciones']

# Variable temporal para almacenar último scraping
ultimo_scraping_resultado = {}

def extraer_info(url):
    """Extrae títulos, descripciones, imágenes y gifs de la URL"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    titles = []
    descriptions = []
    image_urls = []
    gif_urls = []

    blacklist_keywords = [
        'logo', 'favicon', 'icon', 'paypal', 'visa', 'mastercard', 'secure', 'checkout', 'cart'
    ]

    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        titles.append(heading.get_text(strip=True))

    for paragraph in soup.find_all('p'):
        text = paragraph.get_text(strip=True)
        if len(text) > 30:
            descriptions.append(text)

    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src') or img.get('data-image')
        if src:
            full_url = urljoin(url, src)
            full_url_lower = full_url.lower()
            if any(keyword in full_url_lower for keyword in blacklist_keywords):
                continue
            if "gif" in full_url_lower:
                gif_urls.append(full_url)
            else:
                image_urls.append(full_url)

    # Quitar duplicados
    image_urls = list(set(image_urls))
    gif_urls = list(set(gif_urls))

    # Filtrar imágenes pequeñas
    filtered_images = []
    for img_url in image_urls:
        try:
            response = requests.get(img_url, stream=True, timeout=5)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                width, height = img.size
                if width > 100 and height > 100:
                    filtered_images.append(img_url)
        except Exception:
            continue

    return titles, descriptions, filtered_images, gif_urls

@agente_scraping_bp.route('/scraping/scrape', methods=['GET'])
def scrape():
    """
    Scrapear títulos, descripciones, imágenes y gifs de una URL (no guarda en Mongo).
    ---
    tags:
      - WebScraping
    parameters:
      - in: query
        name: url
        type: string
        required: true
        description: URL de la página a scrapear
    responses:
      200:
        description: Datos extraídos exitosamente
    """
    global ultimo_scraping_resultado

    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Parámetro url es requerido'}), 400

    titles, descriptions, images, gifs = extraer_info(url)

    # Guardar resultado temporal en memoria (no en Mongo todavía)
    ultimo_scraping_resultado = {
        'url': url,
        'titles': titles,
        'descriptions': descriptions,
        'images': images,
        'gifs': gifs,
        'scraped_at': datetime.utcnow()
    }

    return jsonify({
        'titles': titles,
        'descriptions': descriptions,
        'images': images,
        'gifs': gifs
    })

@agente_scraping_bp.route('/scraping/select', methods=['POST'])
def select():
    """
    Guardar selección de imágenes y gifs en MongoDB
    ---
    tags:
      - WebScraping
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            images:
              type: array
              items:
                type: string
            gifs:
              type: array
              items:
                type: string
    responses:
      200:
        description: Selección guardada correctamente
      400:
        description: Error en la validación
    """
    global ultimo_scraping_resultado

    if not ultimo_scraping_resultado:
        return jsonify({'error': 'Primero debes hacer un scraping.'}), 400

    data = request.get_json() or {}
    images = data.get('images', [])
    gifs = data.get('gifs', [])

    if len(images) > 3 or len(gifs) > 3:
        return jsonify({'error': 'Máximo puedes enviar hasta 3 imágenes y 3 gifs'}), 400

    # Guardar selección en MongoDB
    doc = {
        'url': ultimo_scraping_resultado.get('url'),
        'titles': ultimo_scraping_resultado.get('titles'),
        'descriptions': ultimo_scraping_resultado.get('descriptions'),
        'images': images,
        'gifs': gifs,
        'selected_at': datetime.utcnow()
    }
    collection_scrapes.insert_one(doc)

    return jsonify({'message': 'Selección guardada correctamente'})

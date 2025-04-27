from flask import Blueprint, request, jsonify
from src.agentes.agente_titulosycopy.application.response import AgenteTitulosYCopies
from src.agentes.webscrapping.infrastructure.mongod import obtener_ultimo_scraping
from src.agentes.agente_titulosycopy.infrastructure.mongod import guardar_tituloscopies_mongo

agente_ai_bp = Blueprint('agente_ai', __name__)

@agente_ai_bp.route('/generate', methods=['POST'])
def generate_from_scraping():
    """
    Genera títulos y copies basados en el último scraping realizado.
    ---
    tags:
      - Titulos y Copies
    responses:
      200:
        description: Contenido generado exitosamente
      404:
        description: No se encontró scraping previo
      500:
        description: Error interno
    """
    doc = obtener_ultimo_scraping()
    if not doc:
        return jsonify({'error': 'No se encontró scraping previo.'}), 404

    titles = doc.get('titles', [])
    descriptions = doc.get('descriptions', [])
    url = doc.get('url', '')

    agente = AgenteTitulosYCopies()
    try:
        titulos, copies, audiencias = agente.generate_results(titles, descriptions)
        guardar_tituloscopies_mongo(titulos, copies, audiencias, url)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'titles': titulos,
        'copies': copies,
        'audiences': audiencias,
        'source_url': url
    })

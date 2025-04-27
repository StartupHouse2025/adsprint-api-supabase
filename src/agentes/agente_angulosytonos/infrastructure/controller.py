from flask import request, jsonify
from src.agentes.agente_scripts.application.response import AgenteGuiones
from src.agentes.webscrapping.infrastructure.mongod import obtener_ultimo_scraping
from src.agentes.agente_titulosycopy.infrastructure.mongod import obtener_ultimo_tituloscopies
from src.agentes.agente_scripts.infrastructure.mongod import guardar_script_mongo

def generate_script_controller():
    """
    Genera un guión publicitario a partir del scraping y títulos/copies previos.
    ---
    tags:
      - Scripts
    responses:
      200:
        description: Guión generado y guardado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
            script:
              type: string
      404:
        description: No se encontró scraping o títulos/copies previos
      500:
        description: Error interno
    """
    scraping_data = obtener_ultimo_scraping()
    tituloscopies_data = obtener_ultimo_tituloscopies()

    if not scraping_data or not tituloscopies_data:
        return jsonify({'error': 'No hay scraping o títulos/copies guardados. Primero genera esos datos.'}), 500

    titulo = tituloscopies_data.get('titulos', [''])[0] if tituloscopies_data.get('titulos') else 'Producto'
    descripcion = ' '.join(scraping_data.get('descriptions', [])) or 'Descripción no disponible'
    publico_objetivo = tituloscopies_data.get('publicos_objetivos', ['Público general'])[0]

    # Datos fijos por ahora
    pais = "Colombia"
    angulo_de_venta = "Beneficio de producto"
    tono = "Amigable y confiable"
    tipo_de_video = "anuncio corto de video"
    duracion = 30  # segundos

    agente = AgenteGuiones()

    try:
        guion = agente.generate_script(
            titulo,
            descripcion,
            pais,
            publico_objetivo,
            angulo_de_venta,
            tono,
            tipo_de_video,
            duracion
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Guardar en MongoDB
    guardar_script_mongo(titulo, descripcion, publico_objetivo, guion)

    return jsonify({
        'message': 'Guión generado y guardado correctamente.',
        'script': guion
    })

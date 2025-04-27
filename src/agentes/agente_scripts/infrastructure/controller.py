from flask import request, jsonify
from src.agentes.agente_scripts.infrastructure.mongod import obtener_datos_para_script, guardar_script_mongo
from src.agentes.agente_scripts.application.response import AgenteGuiones

# Variable global para guardar la selección previa
seleccion_usuario = {}

def configure_script_controller():
    """
    Configura la selección previa de datos para generar el guión.
    ---
    tags:
      - Scripts
    responses:
      200:
        description: Configuración disponible
    """
    datos = obtener_datos_para_script()
    if not datos:
        return jsonify({"error": "No se encontró información previa."}), 404

    return jsonify({
        "titulos_disponibles": datos["titulos"],
        "copies_disponibles": datos["copies"],
        "publicos_objetivos_disponibles": datos["publicos_objetivos"],
        "instrucciones": {
            "mensaje": "En el POST de generación debes enviar título, copy, público objetivo, país, ángulo de venta, tono, tipo de video y duración."
        }
    })

def generate_script_controller():
    """
    Genera un guión publicitario basado en las selecciones configuradas.
    ---
    tags:
      - Scripts
    consumes:
      - application/json
    responses:
      200:
        description: Guión generado correctamente
      404:
        description: No se encontró información previa
    """
    datos = obtener_datos_para_script()
    if not datos:
        return jsonify({"error": "No se encontró información previa."}), 404

    body = request.get_json()

    try:
        titulo = body["titulo"]
        copy = body["copy"]
        pais = body["pais"]
        publico_objetivo = body["publico_objetivo"]
        angulo_de_venta = body["angulo_de_venta"]
        tono = body["tono"]
        tipo_de_video = body["tipo_de_video"]
        duracion = body["duracion"]
    except KeyError as e:
        return jsonify({"error": f"Falta el campo obligatorio: {e}"}), 400

    agente = AgenteGuiones()
    guion = agente.generate_script(
        titulo,
        copy,
        pais,
        publico_objetivo,
        angulo_de_venta,
        tono,
        tipo_de_video,
        duracion
    )

    guardar_script_mongo(guion)

    return jsonify({
        "message": "Guión generado y guardado correctamente.",
        "script": guion
    })

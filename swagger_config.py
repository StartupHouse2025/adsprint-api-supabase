from flask_swagger_ui import get_swaggerui_blueprint

def configure_swagger(app):
    SWAGGER_URL = '/api/docs'
    API_URL = '/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "AdSprintAI API"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/swagger.json')
    def swagger_spec():
        """
        Especificación manual del Swagger
        """
        return {
            "swagger": "2.0",
            "info": {
                "title": "AdSprintAI API",
                "version": "1.0",
                "description": "Documentación de la API de scraping, generación de contenido y scripts."
            },
            "basePath": "/",
            "schemes": ["http"],
            "paths": {
                "/scraping/scrape": {
                    "get": {
                        "tags": ["WebScraping"],
                        "summary": "Scrapea títulos, descripciones, imágenes y gifs de una URL",
                        "parameters": [
                            {
                                "name": "url",
                                "in": "query",
                                "required": True,
                                "type": "string",
                                "description": "URL de la página para scrapear"
                            }
                        ],
                        "responses": {
                            "200": {"description": "Datos extraídos exitosamente"},
                            "400": {"description": "Parámetro URL faltante"}
                        }
                    }
                },
                "/scraping/select": {
                    "post": {
                        "tags": ["WebScraping"],
                        "summary": "Guarda hasta 3 imágenes y 3 gifs seleccionados del scraping",
                        "parameters": [
                            {
                                "in": "body",
                                "name": "body",
                                "required": True,
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "images": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "gifs": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        ],
                        "responses": {
                            "200": {"description": "Selección guardada correctamente"},
                            "400": {"description": "Error en la validación"}
                        }
                    }
                },
                "/ai/generate": {
                    "post": {
                        "tags": ["Titulos y Copies"],
                        "summary": "Genera títulos y copies basados en el último scraping realizado",
                        "responses": {
                            "200": {"description": "Contenido generado exitosamente"},
                            "404": {"description": "No se encontró scraping previo"}
                        }
                    }
                },
                "/script/generate_script": {
                    "post": {
                        "tags": ["Scripts"],
                        "summary": "Genera un guión publicitario a partir del scraping y títulos/copies previos",
                        "responses": {
                            "200": {"description": "Guión generado y guardado correctamente"},
                            "404": {"description": "No se encontró información previa"}
                        }
                    }
                }
            }
        }

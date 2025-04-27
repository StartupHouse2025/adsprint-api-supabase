from flask import Flask
from flask_cors import CORS
from routes.agentes.webscrapping import agente_scraping_bp
from routes.agentes.agente_titulosycopy import agente_ai_bp
from routes.agentes.agente_script_bp import agente_script_bp
from swagger_config import configure_swagger
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Registrar Blueprints
app.register_blueprint(agente_scraping_bp, url_prefix='/scraping')
app.register_blueprint(agente_ai_bp, url_prefix='/ai')
app.register_blueprint(agente_script_bp, url_prefix='/script')

# Swagger
configure_swagger(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

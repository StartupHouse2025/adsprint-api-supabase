from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_cors import CORS
from routes.credential.credential_route import credential_bp
from routes.credential.register_route import register_bp
from routes.credential.put_route import put_credential_bp
from routes.credential.delete_route import delete_bp  # Importar el nuevo Blueprint
from routes.credential.password_reset_route import password_reset_bp  # Importar el nuevo Blueprint
from swagger_config import configure_swagger  # Importar la configuración de Swagger

app = Flask(__name__)
CORS(app)

app.register_blueprint(credential_bp, url_prefix='/get_credential')
app.register_blueprint(register_bp, url_prefix='/set_register')
app.register_blueprint(put_credential_bp, url_prefix='/put_credential')
app.register_blueprint(delete_bp, url_prefix='/delete_credential')  # Registrar el nuevo Blueprint
app.register_blueprint(password_reset_bp, url_prefix='/password')  # Registrar el nuevo Blueprint

# Configurar Swagger
configure_swagger(app)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
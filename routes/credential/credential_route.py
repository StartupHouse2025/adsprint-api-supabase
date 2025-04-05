from flask import Blueprint, request, jsonify
from src.credential.get_credential.infrastructure.controller import CredentialController
from include.validators import checkArgs, parsedRespond
from src.supabase.connect import SupabaseConnection  # Update import for Supabase connection

# Crear un blueprint para el manejo de rutas de usuario
credential_bp = Blueprint('credential', __name__)

# Instanciar el controlador de usuario
credential_controller = CredentialController()

# Función de consulta
def consulta(credential, pasw):
    credential_info = credential_controller.authenticate_credential(credential, pasw)  # Pasar credencial y contraseña
    return parsedRespond(credential_info)

@credential_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Autenticación de usuario por credenciales.
    ---
    tags:
      - Consulta Credenciales
    parameters:
      - name: credential
        in: query
        type: string
        required: true
        description: Credencial del usuario (correo o número de teléfono).
      - name: pass
        in: query
        type: string
        required: true
        description: Contraseña del usuario.
    responses:
      200:
        description: Autenticación exitosa.
        schema:
          type: object
          properties:
            status:
              type: boolean
              example: true
            message:
              type: string
              example: "ok"
            data:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjdkMzg1MTI4Y2Q0NzQ1NjJkMmU5NjEzIiwiZW1haWwiOiJleGFtcGxlQGV4YW1wbGUuY29tIiwiY2VsX251bWJlciI6MTIzNDU2Nzg5MCwidXNlcl9uYW1lIjoiRXhhbXBsZSBVc2VyIiwicm9sZSI6IkV4YW1wbGUgU3VwZXIiLCJpYXQiOjE2MzIwNzQwNzIsImV4cCI6MTYzMjA3NzY3Mn0.1J9Z2J9J9Z2J9"
      400:
        description: Error de autenticación.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
              example: "Usuario o contraseña incorrectos"
    """
    if request.method == 'GET':
        # Si los parámetros vienen en la URL
        checkArgs(['credential', 'pass'], request.args)
        credential = request.args['credential']
        pasw = request.args['pass']
    elif request.method == 'POST':
        # Si los parámetros vienen en un formulario POST
        credential = request.form.get('credential')
        pasw = request.form.get('password')

    try:
        # Llamar al método de autenticación del controlador
        return jsonify(consulta(credential, pasw)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400



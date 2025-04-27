from flask import Blueprint
from src.agentes.agente_scripts.infrastructure.controller import (
    configure_script_controller,
    generate_script_controller
)

agente_script_bp = Blueprint('agente_script', __name__)

agente_script_bp.route('/script/configure', methods=['GET'])(configure_script_controller)
agente_script_bp.route('/script/generate_script', methods=['POST'])(generate_script_controller)

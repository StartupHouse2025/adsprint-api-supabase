from src.agentes.agente_titulosycopy.infrastructure.agente_ai import AgenteTitulosYCopies
from ..application.response import GenerarContenidoResponse  # Importa la clase de respuesta

class AgenteTitulosYCopiesController:
    def __init__(self):
        self.agente_ai = AgenteTitulosYCopies()  # Correcto: tu clase que genera contenido
        # No necesitas instanciar la respuesta aquí

    def generar_contenido(self, titulo, descripciones):
        resultados = self.agente_ai.generate_results(titulo, descripciones)
        
        response = GenerarContenidoResponse(
            titulos=resultados[0],
            copies=resultados[1],
            publicos_objetivos=resultados[2]
        ).serialize()

        return response

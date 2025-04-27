import os
import re
import json
import requests
from dotenv import load_dotenv

class AgenteTitulosYCopies:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.generated_file = "contenido_generado.json"
        if not self.api_key:
            raise ValueError("No se encontró la API Key de DeepSeek en el archivo .env")

    def _clean_text(self, text_data):
        """Limpia texto eliminando emojis y caracteres no deseados"""
        if isinstance(text_data, list):
            text_data = " ".join(str(item) for item in text_data if item)
        text_data = re.sub(r'[^\w\s.,;!?¿¡áéíóúÁÉÍÓÚñÑ-]', '', str(text_data))
        return re.sub(r'\s+', ' ', text_data).strip()

    def _call_ai(self, prompt):
        """Interacción con la API"""
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un redactor profesional de contenido comercial, que crea títulos y copies llamativos de venta. No uses emojis ni caracteres especiales."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7
            }
        )
        if response.status_code != 200:
            raise Exception(f"Error de API: {response.status_code} - {response.text}")
        return response.json()["choices"][0]["message"]["content"]

    def generate_results(self, titulo, descripciones):
        """Genera contenido de títulos, copies y públicos objetivos"""
        # Limpieza de datos
        clean_title = self._clean_text(next((t for t in titulo if t and len(t) > 10), ""))
        clean_desc = self._clean_text(" ".join(d for d in descripciones if d and len(d) > 30))

        if not clean_title or not clean_desc:
            raise ValueError("No se pudo obtener información válida del producto.")

        # Generar TITULOS y COPIES
        content_prompt = f"""
Genera 2 títulos publicitarios y 2 copies profesionales, ganadores, llamativos, super redactados como un HUMANO experto en el tema para redes sociales basados en:

PRODUCTO: {clean_title}
DESCRIPCIÓN: {clean_desc}

REQUISITOS:
- Sin emojis ni caracteres especiales
- Títulos máximo 50 caracteres
- Copies de 2-3 frases persuasivas, mínimo 100 caracteres y máximo 248 caracteres cada uno
- No usar palabras como "compra", "adquiere", "obtén" o similares   
- Lenguaje profesional y orientado a beneficios reales
- No inventar marcas o nombres comerciales
- Incluir beneficios clave, ingredientes del producto y facilidad de pago

FORMATO EXACTO:
TITULO 1: [texto]
TITULO 2: [texto]
COPY 1: [texto]
COPY 2: [texto]
"""
        generated_content = self._call_ai(content_prompt)

        titles = []
        copies = []
        for line in generated_content.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('TITULO'):
                titles.append(line.split(': ', 1)[1])
            elif line.startswith('COPY'):
                copies.append(line.split(': ', 1)[1])

        # Generar PÚBLICOS OBJETIVOS
        audiences_prompt = f"""
Genera 5 públicos objetivos numerados (1-5) para este producto:

PRODUCTO: {clean_title}
CARACTERÍSTICAS: {clean_desc}

REQUISITOS:
- Sin emojis ni caracteres especiales
- Cada público en una sola línea numerada
- Público general (no ultra específico), máximo 20 caracteres si es posible
- Basado en datos demográficos y preocupaciones reales
- Incluir necesidades como piel sensible, estrés, envejecimiento, etc.
- No hablar de métodos de pago o procesos de compra.

FORMATO:
1. Público objetivo 1
2. Público objetivo 2
3. Público objetivo 3
4. Público objetivo 4
5. Público objetivo 5
"""
        audiences_response = self._call_ai(audiences_prompt)
        audiences = [
            re.sub(r'^\d+\.\s*', '', line.strip())
            for line in audiences_response.split('\n')
            if re.match(r'^\d+\.', line.strip())
        ]

        # Guardar resultados en archivo
        with open(self.generated_file, 'w', encoding='utf-8') as f:
            json.dump({
                "titulos": titles,
                "copies": copies,
                "publicos_objetivos": audiences
            }, f, ensure_ascii=False, indent=2)

        return titles, copies, audiences

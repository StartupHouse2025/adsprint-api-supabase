import os
import requests
from dotenv import load_dotenv

class AgenteGuiones:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("No se encontró la API Key de DeepSeek en el archivo .env")

    def generate_script(self, titulo, descripcion, pais, publico_objetivo, angulo_de_venta, tono, tipo_de_video, duracion):
        prompt = f"""Crea un guión para un {tipo_de_video} de {duracion} segundos que promocione el siguiente producto:
Título del producto: {titulo}
Descripción del producto: {descripcion}
Que será para el país: {pais}
Con un público objetivo de: {publico_objetivo}
Ángulo de venta: {angulo_de_venta}
Tono del video: {tono}

Devuélveme el guión con la siguiente estructura e instrucciones:
1. No incluyas tiempos ni escenas, solo texto hablado.
2. “Solo diálogo hablado para video publicitario”.
3. Solo dame el guión, sin encabezado de título ni secciones.
4. No incluyas emojis ni caracteres especiales.
5. No incluyas información adicional, solo el guión.

(Solo como ejemplo, no lo uses en el guion final):
¿Tu mirada delata el cansancio y el paso del tiempo?
Descubre los parches que revierten el tiempo en tu mirada.
Con ingredientes suaves y libres de alcohol, ideales para pieles sensibles.
Reducen bolsas, ojeras y arrugas desde la primera aplicación.
Dale a tu piel el cuidado natural y efectivo que merece.
Y lo mejor: paga solo cuando lo tengas en tus manos, sin riesgos.
Fácil de usar, resultados visibles.
Aumenta tu belleza natural sin esfuerzo.
¡Pídelos ya y devuélvele la frescura a tu mirada!
Disponible en todo Colombia.
"""
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Eres un guionista experto en videos publicitarios cortos."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
        )

        if response.status_code != 200:
            raise Exception(f"Error al llamar a la API de DeepSeek: {response.text}")

        contenido = response.json()["choices"][0]["message"]["content"].strip()
        return contenido

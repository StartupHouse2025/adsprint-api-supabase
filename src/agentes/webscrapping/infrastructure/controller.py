from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.application.response import extraer_info
from agents.infrastructure.mongod import guardar_seleccion

app = FastAPI()

class Selection(BaseModel):
    images: list[str]
    gifs: list[str]

@app.get('/scrape/')
def scrape(url: str):
    """Endpoint GET que devuelve JSON con imágenes y gifs."""
    images, gifs = extraer_info(url)
    return {'images': images, 'gifs': gifs}

@app.post('/select/')
def select(selection: Selection):
    """Endpoint POST que guarda en MongoDB la selección de 3 imágenes y 3 gifs."""
    if len(selection.images) != 3 or len(selection.gifs) != 3:
        raise HTTPException(status_code=400, detail='Debe seleccionar exactamente 3 imágenes y 3 gifs')
    guardar_seleccion(selection.images, selection.gifs)
    return {'message': 'Selección guardada correctamente'}
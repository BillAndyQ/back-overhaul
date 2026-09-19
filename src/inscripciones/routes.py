from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.connection_db import get_db
from .repository import InscripcionRepository
from .schemas import InscripcionRequest

route = APIRouter()

@route.get("")
def listar_inscripciones(db: Session = Depends(get_db)):
    return InscripcionRepository(db).get_all()

@route.get("/{id}")
def obtener_inscripcion(id: str, db: Session = Depends(get_db)):
    inscripcion = InscripcionRepository(db).get_by_id(id)
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return inscripcion

@route.post("", status_code=201)
def crear_inscripcion(datos: InscripcionRequest, db: Session = Depends(get_db)):
    return InscripcionRepository(db).crear(datos)

@route.delete("/{id}")
def eliminar_inscripcion(id: str, db: Session = Depends(get_db)):
    if not InscripcionRepository(db).eliminar(id):
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return {"message": "Inscripción eliminada"}

@route.put("/{id}")
def actualizar_inscripcion(id: str, datos: InscripcionRequest, db: Session = Depends(get_db)):
    inscripcion = InscripcionRepository(db).actualizar(id, datos)
    
    if not inscripcion:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontró una inscripción con el ID {id}"
        )
        
    return {"message": "Inscripción actualizada con éxito", "data": inscripcion}
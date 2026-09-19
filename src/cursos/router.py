from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.connection_db import get_db
from .repository import CursoRepository

router = APIRouter()

@router.get("")
def listar_cursos(db: Session = Depends(get_db)):
    return CursoRepository(db).get_all()

@router.get("/{curso_id}")
def obtener_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = CursoRepository(db).get_by_id(curso_id)
    if not curso: raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.post("")
def crear_curso(datos: dict, db: Session = Depends(get_db)):
    return CursoRepository(db).crear(datos)

@router.put("/{curso_id}")
def actualizar_curso(curso_id: int, datos: dict, db: Session = Depends(get_db)):
    curso = CursoRepository(db).actualizar(curso_id, datos)
    if not curso: raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.delete("/{curso_id}")
def eliminar_curso(curso_id: int, db: Session = Depends(get_db)):
    if not CursoRepository(db).eliminar(curso_id):
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"message": "Curso eliminado"}
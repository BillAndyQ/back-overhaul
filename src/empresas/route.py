from fastapi import APIRouter, Depends, HTTPException
from src.connection_db import get_db
from src.empresas.repository import EmpresaRepository
from src.repository import EquipoRepository
from sqlalchemy.orm import Session

router= APIRouter()

@router.get("/")
def listar_empresas(db: Session = Depends(get_db)):
    return EmpresaRepository(db).get_all()

@router.get("/{empresa_id}")
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = EmpresaRepository(db).get_by_id(empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa

@router.post("/")
def crear_empresa(datos: dict, db: Session = Depends(get_db)):
    return EmpresaRepository(db).crear(datos)

@router.put("/{empresa_id}")
def actualizar_empresa(empresa_id: int, datos: dict, db: Session = Depends(get_db)):
    empresa = EmpresaRepository(db).actualizar(empresa_id, datos)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa

@router.delete("/{empresa_id}")
def eliminar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    if not EmpresaRepository(db).eliminar(empresa_id):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return {"message": "Empresa eliminada"}
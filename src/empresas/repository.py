from sqlalchemy.orm import Session
from .models import Empresa

class EmpresaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Empresa).all()

    def get_by_id(self, empresa_id: int):
        return self.db.query(Empresa).filter(Empresa.id == empresa_id).first()

    def crear(self, datos: dict):
        nueva_empresa = Empresa(**datos)
        self.db.add(nueva_empresa)
        self.db.commit()
        self.db.refresh(nueva_empresa)
        return nueva_empresa

    def actualizar(self, empresa_id: int, datos: dict):
        empresa = self.get_by_id(empresa_id)
        if not empresa:
            return None
        for key, value in datos.items():
            setattr(empresa, key, value)
        self.db.commit()
        self.db.refresh(empresa)
        return empresa

    def eliminar(self, empresa_id: int) -> bool:
        empresa = self.get_by_id(empresa_id)
        if not empresa:
            return False
        self.db.delete(empresa)
        self.db.commit()
        return True
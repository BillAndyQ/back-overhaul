from sqlalchemy.orm import Session
from .models import Inscripcion
from .schemas import InscripcionRequest

class InscripcionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Inscripcion).all()

    def get_by_id(self, id: str):
        return self.db.query(Inscripcion).filter(Inscripcion.id == id).first()

    def crear(self, datos: InscripcionRequest):
        nueva_inscripcion = Inscripcion(**datos.model_dump())
        self.db.add(nueva_inscripcion)
        self.db.commit()
        self.db.refresh(nueva_inscripcion)
        return nueva_inscripcion

    def eliminar(self, id: str) -> bool:
        obj = self.get_by_id(id)
        if not obj: return False
        self.db.delete(obj)
        self.db.commit()
        return True
    
    def actualizar(self, id: str, datos: InscripcionRequest):
        inscripcion = self.get_by_id(id)
        if not inscripcion:
            return None
        
        # Actualizamos los campos recibidos
        for key, value in datos.model_dump().items():
            setattr(inscripcion, key, value)
            
        self.db.commit()
        self.db.refresh(inscripcion)
        return inscripcion
from sqlalchemy.orm import Session
from src.cursos.models import Curso

class CursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Curso).all()

    def get_by_id(self, curso_id: int):
        return self.db.query(Curso).filter(Curso.id == curso_id).first()

    def crear(self, datos: dict):
        nuevo_curso = Curso(**datos)
        self.db.add(nuevo_curso)
        self.db.commit()
        self.db.refresh(nuevo_curso)
        return nuevo_curso

    def actualizar(self, curso_id: int, datos: dict):
        curso = self.get_by_id(curso_id)
        if not curso: return None
        for key, value in datos.items():
            setattr(curso, key, value)
        self.db.commit()
        self.db.refresh(curso)
        return curso

    def eliminar(self, curso_id: int) -> bool:
        curso = self.get_by_id(curso_id)
        if not curso: return False
        self.db.delete(curso)
        self.db.commit()
        return True
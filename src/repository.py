from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.models import EquipoModel, OTEquipoModel, OtPersona
from src.schema import PersonaRequest

class EquipoRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- Métodos de Configuración / OT ---
    def crear_persona(self, datos: PersonaRequest):
        try:
            nueva_persona = OtPersona(**datos.model_dump())
            self.db.add(nueva_persona)
            self.db.commit()
            self.db.refresh(nueva_persona)
            return nueva_persona
        
        except Exception as e:
            self.db.rollback()
            print(f"Error al crear persona: {e}")
            return None
    
    def eliminar_personas_por_ot(self, n_ot: str) -> bool:
        try:
            # Filtramos y eliminamos los registros que coinciden con el n_ot
            deleted_count = self.db.query(OtPersona).filter(OtPersona.n_ot == n_ot).delete(synchronize_session=False)
            self.db.commit()
            
            # Retorna True si se eliminó al menos uno
            return deleted_count > 0
        
        except Exception as e:
            self.db.rollback()
            print(f"Error al eliminar personas de la OT {n_ot}: {e}")
            return False

    def actualizar_persona(self, n_ot: int, datos: PersonaRequest):
        try:
            persona = self.db.query(OtPersona).filter(OtPersona.n_ot == n_ot).first()
            if not persona:
                return None
            
            for key, value in datos.model_dump().items():
                if hasattr(persona, key):
                    setattr(persona, key, value)
            
            self.db.commit()
            self.db.refresh(persona)
            
            return persona
        
        except Exception as e:
            self.db.rollback()
            
            print(f"Error al actualizar persona: {e}")
            return None
    
    def get_last_id(self) -> int | None:
        try:
            query = text("SELECT last_id FROM public.ot_config LIMIT 1")
            return self.db.execute(query).scalar()
        
        except Exception:
            return None
        
    def get_id_of_ot(self, n_ot: str) -> int | None:
        try:
            query = text("SELECT id FROM public.ot_equipos WHERE n_ot=:n_ot LIMIT 1")
            return self.db.execute(query, {"n_ot": n_ot}).scalar()
        
        except Exception:
            return None
    
    from sqlalchemy import text
    
    def get_all_ot_equipos(self) -> list[dict] | None:
            try:
                query = text("SELECT * FROM public.ot_equipos")
                result = self.db.execute(query).mappings().all()
                return [dict(row) for row in result]
            except Exception:
                return None
            
    def get_all_ot_personas(self) -> list[dict] | None:
        try:
            query = text("SELECT * FROM public.ot_personas")
            result = self.db.execute(query).mappings().all()
            return [dict(row) for row in result]
        except Exception:
            return None
            
    def get_ot_persona_by_n_ot(self, n_ot: str) -> dict | None:
        try:
            query = text("SELECT * FROM public.ot_personas WHERE n_ot = :n_ot LIMIT 1")
            result = self.db.execute(query, {"n_ot": n_ot}).mappings().first()
            return dict(result) if result else None
        except Exception:
            return None
            
    def get_all_ot_equipos_join(self) -> list[dict] | None:
        try:
            query = text("""
                         SELECT * FROM public.ot_equipos as ot_eq
                        left join public.equipos as eq
                        on ot_eq.id = eq.id_ot_equipo
                         """)
            result = self.db.execute(query).mappings().all()
            print("cargando...")
            return [dict(row) for row in result]

        except Exception as e:
            print(f"DEBUG ERROR: {e}")
            return None
            
    def get_all_empresas(self) -> list[dict] | None:
                try:
                    query = text("SELECT * FROM public.empresas")
                    result = self.db.execute(query).mappings().all()
                    return [dict(row) for row in result]
                except Exception:
                    return None

    def get_equipos_of_ot(self, id_ot_equipo: int) -> list[dict]:
        try:
            # 1. Definimos la consulta (sin LIMIT 1 si esperas varios equipos)
            query = text("SELECT * FROM public.equipos WHERE id_ot_equipo = :id_ot_equipo")
            
            # 2. Ejecutamos y usamos .mappings() para obtener diccionarios
            result = self.db.execute(query, {"id_ot_equipo": id_ot_equipo}).mappings().all()
            
            # 3. Convertimos cada fila a un diccionario estándar
            return [dict(row) for row in result]
            
        except Exception as e:
            # Es muy recomendable imprimir el error para depurar
            print(f"Error al obtener equipos: {e}")
            return [] # Retornamos lista vacía en lugar de None para evitar errores en el frontend

    def create_ot_init(self, n_ot) -> bool:
        try:
            insert_query = text("INSERT INTO ot_equipos (n_ot) VALUES (:n_ot)")
            self.db.execute(insert_query, {"n_ot": n_ot})
            
            update_query = text("UPDATE public.ot_config SET last_id = last_id + 1")
            self.db.execute(update_query)
            
            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Error al crear OT {n_ot}: {e}")
            return False

    def create_ot_init_persona(self, n_ot) -> bool:
        try:
            insert_query = text("INSERT INTO ot_personas (n_ot) VALUES (:n_ot)")
            self.db.execute(insert_query, {"n_ot": n_ot})
            
            update_query = text("UPDATE public.ot_config SET last_id = last_id + 1")
            self.db.execute(update_query)
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error al crear OT de persona {n_ot}: {e}")
            return False

    # --- Métodos ORM para 'equipos' ---
    
    def actualizar_ot_equipo(self, datos: dict, n_ot: str):
        # 1. Buscamos el registro único por n_ot
        equipo_db = self.db.query(OTEquipoModel).filter(OTEquipoModel.n_ot == n_ot).first()
        
        if not equipo_db:
            # Aquí puedes lanzar una excepción de FastAPI o retornar None
            raise Exception(f"No se encontró la OT con el número: {n_ot}")

        # 2. Actualizamos solo los campos que vienen en 'datos'
        for key, value in datos.items():
            # Verificamos que el atributo exista en el modelo para evitar errores
            if hasattr(equipo_db, key):
                setattr(equipo_db, key, value)
        
        # 3. Guardamos cambios
        self.db.commit()
        self.db.refresh(equipo_db)
        
        return equipo_db
    
    def obtener_ot_equipo(self, n_ot: str):
        """
        Busca y retorna un registro específico de OT por su número.
        """
        equipo_db = self.db.query(OTEquipoModel).filter(OTEquipoModel.n_ot == n_ot).first()
        
        if not equipo_db:
            return None
            
        return equipo_db

    def crear_equipo(self, datos: dict):
        nuevo_equipo = EquipoModel(**datos)
        self.db.add(nuevo_equipo)
        self.db.commit()
        self.db.refresh(nuevo_equipo)
        return nuevo_equipo

    def actualizar_equipo(self, equipo_id: int, datos: dict):
        equipo = self.db.query(EquipoModel).filter(EquipoModel.id == equipo_id).first()
        if not equipo:
            return None
        for key, value in datos.items():
            if hasattr(equipo, key) and value is not None:
                setattr(equipo, key, value)
        self.db.commit()
        self.db.refresh(equipo)
        return equipo
    
    def delete_equipo(self, equipo_id: int):
        # 1. Buscar el equipo
        equipo = self.db.query(EquipoModel).filter(EquipoModel.id == equipo_id).first()
        
        # 2. Si no existe, retornamos False para que el endpoint sepa que no hubo nada que borrar
        if not equipo:
            return False
            
        # 3. Eliminar y persistir
        self.db.delete(equipo)
        self.db.commit()
        return True
    
    # Eliminación lógica, no permanente de orden de trabajo
    def delete_ot_equipo(self, equipo_id: int):
        # 1. Buscar el equipo
        equipo = self.db.query(OTEquipoModel).filter(OTEquipoModel.id == equipo_id).first()
        
        # 2. Si no existe, retornamos False
        if not equipo:
            return False
            
        # 3. Actualización lógica: cambiamos el flag en lugar de borrar
        equipo.deleted = True
        
        # 4. Guardar cambios
        self.db.commit()
        self.db.refresh(equipo)
        
        return True
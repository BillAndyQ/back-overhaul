from datetime import datetime
from sqlalchemy.orm import Session

# Suponiendo que el repositorio está en .repository
from .repository import EquipoRepository 

def service_create_ot(db: Session) -> str:
    repo = EquipoRepository(db)
    
    # 1. Obtener el último ID desde la DB
    last_id = repo.get_last_id() or 0
    
    # 2. Generar el nuevo código
    codigo_ot = generar_codigo_formateado(last_id)
    
    # 3. Guardar el nuevo registro y actualizar el contador
    exito = repo.create_ot_init(codigo_ot)
    
    if not exito:
        raise Exception("Error al persistir la nueva OT en la base de datos")
        
    return codigo_ot

def service_create_ot_init(db: Session) -> str:
    repo = EquipoRepository(db)
    
    # 1. Obtener el último ID desde la DB
    last_id = repo.get_last_id() or 0
    codigo_ot = generar_codigo_formateado(last_id)
    exito = repo.create_ot_init_persona(codigo_ot)
    
    if not exito:
        raise Exception("Error al persistir la nueva OT en la base de datos")
    
    return codigo_ot

def generar_codigo_formateado(ultimo_id: int) -> str:
    """
    Formatea un ID según el patrón OM-MM-YYYY-000000
    """
    # Incrementamos el ID para la nueva OT
    nuevo_id = ultimo_id + 1
    ahora = datetime.now()
    
    # Formatear el ID con 6 dígitos y construir la cadena
    return f"OM-{ahora.strftime('%m')}-{ahora.strftime('%Y')}-{nuevo_id:03d}"
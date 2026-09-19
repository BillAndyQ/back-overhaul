# tests/export_xlsx.py
from src.connection_db import SessionLocal # Importa la clase de sesión, no la función Depends
from src.repository import EquipoRepository

# ... resto de tu código (test_export) ...

def test_export():
    # 1. Crear una sesión manual (sin FastAPI)
    db = SessionLocal() 
    try:
        # 2. Instanciar el repositorio
        repo = EquipoRepository(db)
        
        # 3. Obtener los datos
        data = repo.get_all_ot_equipos()
        print(data)
        exportar_a_excel(data)
    finally:
        # 4. IMPORTANTE: Cerrar la sesión manualmente
        db.close()

if __name__ == "__main__":
    test_export()
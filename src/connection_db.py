import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://root:password@localhost:5432/postgres")

# 1. El engine gestiona la conexión a la base de datos
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 2. SessionLocal es una fábrica de objetos de sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. La función que usará FastAPI como dependencia
def get_db():
    db = SessionLocal() # Crea la sesión
    try:
        yield db        # Entrega la sesión al endpoint
    finally:
        db.close()      # Cierra la sesión cuando el request termina
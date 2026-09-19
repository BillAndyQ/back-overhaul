import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# 1. Cambia el prefijo de la URL: si es postgres, usa postgresql+asyncpg://
# Asegúrate de que el driver (asyncpg) esté instalado
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://root:password@localhost:5432/postgres")

# 2. Usa create_async_engine
engine = create_async_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# 3. Usa async_sessionmaker y especifica la clase AsyncSession
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 4. Actualiza la dependencia para que sea asíncrona
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
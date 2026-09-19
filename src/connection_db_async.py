from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.db_url import get_async_database_url

# 1. Siempre driver asyncpg, aunque DATABASE_URL sea postgresql://
DATABASE_URL = get_async_database_url()

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
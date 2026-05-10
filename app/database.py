from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/order_db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL,
                             echo=True,
                             future=True)
SessionLocal = sessionmaker(bind=engine,
                            class_=AsyncSession,
                            expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as session:
        yield session

import asyncio

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///example.db"

# Async engine and session
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal: sessionmaker = sessionmaker(
    engine,  # type:ignore
    expire_on_commit=False,
    class_=AsyncSession,
)


class BaseModel(DeclarativeBase):
    pass


# Define the model
class UserModel(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


async def bulk_insert(session: AsyncSession, users: list):
    """Bulk Insert Users"""
    session.add_all(users)
    await session.commit()


async def bulk_update(session: AsyncSession, user_updates: dict):
    """Bulk Update Users (Example: Update emails by ID)"""
    stmt = select(UserModel).where(UserModel.id.in_(user_updates.keys()))
    result = await session.execute(stmt)
    users = result.scalars().all()

    for user in users:
        user.email = user_updates[user.id]  # Update email

    await session.commit()


async def bulk_delete(session: AsyncSession, user_ids: list):
    """Bulk Delete Users"""
    stmt = select(UserModel).where(UserModel.id.in_(user_ids))
    result = await session.execute(stmt)
    users = result.scalars().all()

    for user in users:
        await session.delete(user)

    await session.commit()


async def fetch_users(session: AsyncSession):
    """Select Users"""
    result = await session.execute(select(UserModel))
    return result.scalars().all()


async def main():
    await create_tables()  # Ensure tables exist

    async with AsyncSessionLocal() as session:
        # Bulk Insert
        users = [
            UserModel(name="Alice", email="alice@example.com"),
            UserModel(name="Bob", email="bob@example.com"),
            UserModel(name="Charlie", email="charlie@example.com"),
        ]
        await bulk_insert(session, users)

        # Bulk Update
        await bulk_update(session, {
            1: "new_alice@example.com",
            2: "new_bob@example.com"
        })

        # Fetch and Print
        users = await fetch_users(session)
        print([f"{user.id}: {user.name} - {user.email}" for user in users])

        # Bulk Delete
        await bulk_delete(session, [1, 3])

        # Fetch and Print After Deletion
        users = await fetch_users(session)
        print([f"{user.id}: {user.name} - {user.email}" for user in users])


if __name__ == "__main__":
    asyncio.run(main())

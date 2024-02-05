# pip install aiomysql
# pip install sqlalchemy[asyncio]  # (>= 2.x)

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from sqlalchemy import func, select, BIGINT, VARCHAR
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped


async_engine = create_async_engine("mysql+aiomysql://root:1234@localhost:3306/test",
                                   pool_recycle=3600, pool_pre_ping=True, echo=True)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)


@asynccontextmanager
async def db_session_scope():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e  # raise again after rollback session.
        finally:
            await session.close()


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)


async def add_user(user: User) -> User:
    async with db_session_scope() as session:
        async with session.begin():
            session.add_all([user])
    return user


async def get_user_by_id(idx: int) -> User | None:
    async with db_session_scope() as session:
        query = select(User).filter(User.id == idx)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def update_user_name_by_id(idx: int, name: str) -> User:
    async with db_session_scope() as session:
        query = select(User).filter(User.id == idx)
        result = await session.execute(query)
        obj = result.scalar_one_or_none()
        obj.name = name
        return obj


async def main():
    usr = User(name="user1")
    usr1 = await add_user(usr)
    assert "user1" == (await get_user_by_id(usr1.id)).name
    assert "user11" == (await update_user_name_by_id(usr1.id, "user11")).name


if __name__ == "__main__":
    asyncio.run(main())

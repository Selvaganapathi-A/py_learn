from sqlalchemy import Column, Integer, String, Table, create_engine
from sqlalchemy.exc import (DatabaseError, DataError, IntegrityError,
                            PendingRollbackError, ProgrammingError,
                            TimeoutError)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__: str = 'User'
    pk: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        'user_name',
        String,
        unique=True,
    )
    age: Mapped[int] = mapped_column(
        'user_age',
        Integer,
    )

    def __repr__(self) -> str:
        return f'User : {self.name}, Age : {self.age}'


def main():
    # Database Setup
    # dataase on disk
    # engine = create_engine('sqlite:///pandora.db', echo=False)
    # dataase on memory (RAM) ## Much Faster for read and arite of very large number of records
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # Add User
    try:
        new_user = User(name='Jenzy', age=17)
        session.add(new_user)
        session.commit()
    except IntegrityError as seie:
        print('Database Error', seie)
        session.rollback()
    # Read Users
    users = session.query(User).all()
    print(users)
    users = session.query(User).where(User.name == 'Jenzy').first()
    print('Jenzy == ', users)
    users = session.query(
        session.query(User).where(User.name == 'James').exists()).scalar()
    print('James == ', users)
    # Dispose Database
    engine.dispose(True)


if __name__ == '__main__':
    main()

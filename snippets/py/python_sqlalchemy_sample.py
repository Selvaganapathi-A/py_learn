from sqlalchemy import Column, create_engine, Integer, String, Table
from sqlalchemy.exc import DatabaseError, DataError, IntegrityError
from sqlalchemy.exc import PendingRollbackError, ProgrammingError
from sqlalchemy.exc import TimeoutError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker


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
    engine = create_engine('sqlite:///pandora.db', echo=False)
    Base.metadata.create_all(bind=engine)
    #
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
    #
    users = session.query(User).where(User.name == 'Jenzy').first()
    print('Jenzy == ', users)
    #
    users = session.query(
        session.query(User).where(User.name == 'James').exists()).scalar()
    print('James == ', users)

    # Dispose Database
    engine.dispose(True)
    pass


if __name__ == "__main__":
    main()
    pass

from sqlalchemy import (
    Boolean,
    Integer,
    String,
    and_,
    case,
    create_engine,
    insert,
    or_,
    select,
    update,
)
from sqlalchemy.orm import Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeBase


class BaseModel(DeclarativeBase): ...


class User(BaseModel):
    __tablename__: str = 'user'
    pk: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=True, default=None)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=True, default=None)
    sex: Mapped[str] = mapped_column(String, nullable=True, default=None)
    canVote: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)
    canMarry: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)

    def __str__(self) -> str:
        return f'<{self.name} {self.surname}>'

    def __repr__(self) -> str:
        return f'<{self.name} {self.surname}, {self.age}>'


def main(session: Session):
    # * bulk insert
    session.execute(
        statement=insert(User),
        params=[
            {'surname': 'hanson', 'name': 'elena', 'age': 14, 'sex': 'F'},
            {'surname': 'carr', 'name': 'tony', 'age': 17, 'sex': 'M'},
            {'surname': 'ellis', 'name': 'rosemary', 'age': 16, 'sex': 'F'},
            {'surname': 'mcbride', 'name': 'spphia', 'age': 39, 'sex': 'F'},
            {'surname': 'garrett', 'name': 'karen', 'age': 28, 'sex': 'F'},
            {'surname': 'moran', 'name': 'john', 'age': 41, 'sex': 'M'},
            {'surname': 'cooper', 'name': 'mike', 'age': 18, 'sex': 'M'},
        ],
    )
    #
    # * Before Update
    for user in session.execute(select(User)).scalars().fetchall():
        print(
            (
                user.sex,
                user.age,
                user.name,
                'I can Vote' if user.canVote else "can't Vote",
                '💖' if user.canMarry else '-',
            )
        )
    # * 2 boolean fields
    cache = []
    for user in session.execute(select(User)).scalars().fetchall():
        cache.append(
            {
                'pk': user.pk,
                'canVote': user.age >= 18,
                'canMarry': (user.sex == 'M' and user.age > 19)
                or (user.sex == 'F' and user.age > 16),
            }
        )
    # * bulk update
    session.execute(update(User), cache)
    # #
    # # * Update the same via sqlquery
    # #
    session.execute(
        update(User).values(
            canMarry=or_(
                and_(
                    User.sex == 'M',
                    User.age > 19,
                ),
                and_(
                    User.sex == 'F',
                    User.age > 16,
                ),
            ),
        )
    )
    # #
    # #
    # #
    # * After Update
    for user in session.execute(select(User)).scalars().fetchall():
        print(
            (
                user,
                user.sex,
                user.age,
                user.name,
                '🤚' if user.canVote else '0',
                '💖' if user.canMarry else '-',
            )
        )
    #
    session.commit()


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo=True)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    BaseModel.metadata.create_all(bind=engine)
    main(session)
    engine.dispose()

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.decl_api import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class Parent(Base):
    #
    __tablename__ = 'Parent'
    #
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    #
    name: Mapped[str] = mapped_column(String, nullable=False)
    #
    child_pk: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            'Child.pk',
            ondelete='SET NULL',
            onupdate='SET NULL',
        ),
        nullable=True,
        unique=True,
    )
    #
    child = relationship('Child', back_populates='parent')


class Child(Base):
    __tablename__ = 'Child'
    #
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    #
    parent: Mapped[Parent] = relationship('Parent', back_populates='child')

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.decl_api import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()
"""
Many to Many Relationship
via
Association Object.
"""


class Association(Base):
    __tablename__: str = 'ChildParentRelationship'
    __table_args__ = (UniqueConstraint('child_pk',
                                       'parent_pk',
                                       name='uniqueRelationship'),)

    child_pk: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('child.pk', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        primary_key=True,
    )
    parent_pk: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            'parent.pk',
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        nullable=False,
        primary_key=True,
    )
    parent: Mapped['Parent'] = relationship(back_populates='children')
    child: Mapped['Child'] = relationship(back_populates='parents')


class Parent(Base):
    __tablename__ = 'parent'
    __table_args__ = (UniqueConstraint('first_name', 'last_name'),)
    #
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    #
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    children: Mapped[set['Association']] = relationship(
        # secondary=Association,
        back_populates='parent',)


class Child(Base):
    __tablename__ = 'child'
    __table_args__ = (UniqueConstraint('first_name', 'last_name'),)
    #
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    #
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    parents: Mapped[set['Association']] = relationship(
        # secondary=Association,
        back_populates='child',)

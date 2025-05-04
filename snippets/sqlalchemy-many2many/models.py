from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Table,
                        UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.decl_api import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()
"""
Many to Many Relationship
via
Association Table.
"""

associationTable = Table(
    'childParentRelationship',
    Base.metadata,
    Column(
        'parent_pk',
        ForeignKey(
            'parent.pk',
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        primary_key=True,
    ),
    Column(
        'child_pk',
        ForeignKey(
            'child.pk',
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        primary_key=True,
    ),
    Column(
        'created',
        DateTime(timezone=True),
        default=func.now(),
    ),
    UniqueConstraint('child_pk', 'parent_pk', name='unixrelationship'),
)

# class Association(Base):
#     __tablename__: str = 'association'
#     child_pk: Mapped[int] = mapped_column(
#         ForeignKey('parent.pk', ondelete='CASCADE', onupdate='CASCADE'),
#         primary_key=True,
#     )
#     parent_pk: Mapped[int] = mapped_column(
#         ForeignKey('parent.pk', ondelete='CASCADE', onupdate='CASCADE'),
#         primary_key=True,
#     )
#     child: Mapped['Child'] = relationship('Child', back_populates='child')
#     parent: Mapped['Parent'] = relationship('Parent', back_populates='parent')


class Parent(Base):
    __tablename__ = 'parent'
    __table_args__ = (UniqueConstraint('first_name', 'last_name'),)
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    children: Mapped[set['Child']] = relationship(
        secondary='childParentRelationship',
        back_populates='parents',
    )


class Child(Base):
    __tablename__ = 'child'

    __table_args__ = (UniqueConstraint('first_name', 'last_name'),)
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    parents: Mapped[set['Parent']] = relationship(
        secondary='childParentRelationship',
        back_populates='children',
    )

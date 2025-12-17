from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.decl_api import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class Vehicle(Base):
    __tablename__ = 'Vehicle'
    pk: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    vehicle_number: Mapped[str] = mapped_column(String, nullable=False)
    registration_number: Mapped[str] = mapped_column(String, nullable=False)
    driver_pk: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            'Driver.pk',
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        nullable=False,
        # unique=True,
    )
    driver = relationship(
        'Driver',
        back_populates='vehicles',
    )


class Driver(Base):
    __tablename__ = 'Driver'
    pk: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    vehicles: Mapped[set[Vehicle]] = relationship(
        'Vehicle',
        back_populates='driver',
    )

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

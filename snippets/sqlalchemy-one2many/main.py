from models import Base, Driver, Vehicle
from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm.session import Session, sessionmaker


def workarea(session: Session):
    driver_adam = Driver(first_name='Adam', last_name='Chris')
    driver_jerry = Driver(first_name='Jerry', last_name='Chris')
    driver_tom = Driver(first_name='Tom', last_name='Chris')
    #
    bmw = Vehicle(vehicle_number='bmw-i10', registration_number='11')
    honda = Vehicle(vehicle_number='honda activa', registration_number='12')
    toyoto = Vehicle(vehicle_number='toyoto sedan', registration_number='13')
    nano = Vehicle(vehicle_number='nano tata', registration_number='14')
    #
    driver_adam.vehicles.add(bmw)
    driver_adam.vehicles.add(honda)
    #
    driver_jerry.vehicles.add(nano)
    #
    driver_tom.vehicles.add(toyoto)
    #
    session.add(driver_adam)
    session.add(driver_jerry)
    session.add(driver_tom)
    session.commit()
    #
    for driver in session.execute(select(Driver)).scalars().all():
        print(driver.name)
        for vehicle in driver.vehicles:
            print('-->', vehicle.vehicle_number, vehicle.registration_number)
    #
    for vehicle in (
        session.execute(
            select(Vehicle)
            .join(Driver, Driver.pk == Vehicle.driver_pk)
            .order_by(
                Driver.last_name,
                Driver.first_name,
            )
        )
        .scalars()
        .all()
    ):
        print(
            vehicle.vehicle_number,
            vehicle.registration_number,
            'owned by',
            vehicle.driver.name,
        )


def main():
    session: Session
    engine: Engine = create_engine('sqlite:///:memory:', echo=False)
    #
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #
    sessionLocal = sessionmaker(bind=engine)
    session = sessionLocal()
    #
    workarea(session=session)
    #
    session.commit()
    #
    engine.dispose()


if __name__ == '__main__':
    main()
